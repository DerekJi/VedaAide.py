"""
LlamaIndex Document Indexing Pipeline for VedaAide RAG System.

This module provides document loading, chunking, and vector indexing
capabilities using LlamaIndex and Qdrant vector database.

Supports multiple document formats:
- JSON (structured documents with id, name, content)
- Markdown (*.md files)
- Plain text (*.txt files)
- PDF (*.pdf files - text-based only, requires PyPDF)

Note on PDF Support:
    PDF files with extractable text are supported. However, scanned PDFs or PDFs
    containing embedded images without text layers may not be processed correctly.
    Images within PDFs may be silently ignored. For OCR support of scanned PDFs,
    consider implementing Azure Computer Vision OCR separately.

Usage:
    indexer = DocumentIndexer(collection_name="vedaaide")
    indexer.index_documents("data/public_samples/", recursive=True)
    print(f"Indexed {indexer.document_count} documents")
"""

import logging
from hashlib import md5
from pathlib import Path
from typing import Any, Literal

from llama_index.core import Document
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.core.data.document_loader import DocumentLoader
from src.core.data.document_loader_interface import IDocumentLoader

logger = logging.getLogger(__name__)


class DocumentIndexer:
    """
    Document indexing pipeline for VedaAide RAG system.

    Handles document loading from multiple formats, intelligent chunking,
    embedding generation, and vector storage in Qdrant.

    Supports multiple embedding backends:
    - "azure": Azure OpenAI Embedding API (production)
    - "ollama": Local Ollama server with bge-m3 model (development)

    Attributes:
        collection_name: Qdrant collection name for storing vectors
        qdrant_client: Qdrant client instance
        embedding_model: Embedding model name/identifier
        embedding_provider: Embedding provider ("azure" or "ollama")
        chunk_size: Size of text chunks for splitting (chars)
        chunk_overlap: Overlap between chunks (chars)
    """

    def __init__(
        self,
        collection_name: str = "vedaaide",
        qdrant_url: str = "http://localhost:6333",
        embedding_provider: Literal["azure", "ollama"] = "ollama",
        embedding_model: str = "bge-m3",
        ollama_base_url: str = "http://localhost:11434",
        chunk_size: int = 512,
        chunk_overlap: int = 64,
        document_loader: IDocumentLoader | None = None,
    ):
        """
        Initialize the document indexer with dependency injection.

        Args:
            collection_name: Name of Qdrant collection
            qdrant_url: URL of Qdrant server (default: localhost:6333)
            embedding_provider: Embedding backend ("azure" or "ollama")
                - "azure": Uses Azure OpenAI API (requires AZURE_OPENAI_KEY env var)
                - "ollama": Uses local Ollama server (default for dev)
            embedding_model:
                - For "azure": model name (e.g., "text-embedding-3-small")
                - For "ollama": model name (e.g., "bge-m3")
            ollama_base_url: Base URL for Ollama server (only used if provider="ollama")
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
            document_loader: IDocumentLoader implementation for loading documents
                If not provided, creates a default DocumentLoader instance
                Can be any class implementing IDocumentLoader interface
        """
        self.collection_name = collection_name
        self.qdrant_url = qdrant_url
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model
        self.ollama_base_url = ollama_base_url
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Dependency injection: use provided DocumentLoader or create default
        self.document_loader = document_loader or DocumentLoader()

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url)

        # Initialize embedding model based on provider
        self.embedding_model_instance = self._create_embedding_model()

        # Initialize text splitter with recursive strategy
        self.text_splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=" ",
        )

        self.document_count = 0
        self._processed_hashes: set = set()

    def _create_embedding_model(self):
        """
        Create embedding model instance based on configured provider.

        Returns:
            Embedding model instance

        Raises:
            ValueError: If provider is not supported or configuration is invalid
        """
        if self.embedding_provider == "azure":
            logger.info(f"Creating Azure OpenAI embedding model: {self.embedding_model}")
            return OpenAIEmbedding(
                model=self.embedding_model,
                embed_batch_size=10,
            )

        elif self.embedding_provider == "ollama":
            logger.info(
                f"Creating Ollama embedding model: {self.embedding_model} at {self.ollama_base_url}"
            )
            try:
                import ollama
            except ImportError:
                raise ImportError("ollama package not installed. Install with: pip install ollama")

            # Create a wrapper class for Ollama that matches the embedding interface
            class OllamaEmbeddingWrapper:
                def __init__(self, model_name: str, base_url: str):
                    self.model_name = model_name
                    self.base_url = base_url
                    self.client = ollama.Client(host=base_url)

                def get_text_embedding(self, text: str) -> list:
                    """Get embedding for a single text."""
                    try:
                        response = self.client.embeddings(
                            model=self.model_name,
                            prompt=text,
                        )
                        return response.get("embedding", [])
                    except Exception as e:
                        logger.error(f"Error generating Ollama embedding: {e}")
                        return []

            return OllamaEmbeddingWrapper(
                model_name=self.embedding_model,
                base_url=self.ollama_base_url,
            )

        else:
            raise ValueError(
                f"Unsupported embedding provider: {self.embedding_provider}. "
                f"Must be 'azure' or 'ollama'"
            )

    def _get_embedding_dimension(self) -> int:
        """
        Get the dimension size of embeddings from the provider.

        Returns:
            Embedding dimension size
        """
        if self.embedding_provider == "azure":
            # Azure OpenAI embedding dimensions by model
            dimensions = {
                "text-embedding-3-small": 1536,
                "text-embedding-3-large": 3072,
                "text-embedding-ada-002": 1536,
            }
            return dimensions.get(self.embedding_model, 1536)

        elif self.embedding_provider == "ollama":
            # Common Ollama model dimensions
            dimensions = {
                "bge-m3": 1024,
                "bge-large-en-v1.5": 1024,
                "nomic-embed-text": 768,
                "all-minilm": 384,
            }
            dim = dimensions.get(self.embedding_model, 1024)
            logger.info(f"Using dimension {dim} for Ollama model {self.embedding_model}")
            return dim

        return 1536  # Default fallback

    def _get_document_hash(self, doc_id: str, content: str) -> str:
        """
        Generate a hash for document deduplication.

        Args:
            doc_id: Document identifier
            content: Document content

        Returns:
            MD5 hash string
        """
        combined = f"{doc_id}:{content[:200]}"
        return md5(combined.encode()).hexdigest()

    def _ensure_collection_exists(self) -> None:
        """
        Ensure Qdrant collection exists with proper schema.

        Automatically determines vector size based on the configured embedding provider.
        """
        try:
            # Try to get collection info
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception:
            # Collection doesn't exist, create it
            vector_size = self._get_embedding_dimension()
            logger.info(
                f"Creating collection '{self.collection_name}' with vector size {vector_size}..."
            )
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")

    def chunk_document(self, document: Document) -> list[Document]:
        """
        Split a single document into chunks using recursive text splitting.

        This implements a hierarchical chunking approach:
        1. First split by paragraph boundaries (\n\n)
        2. Then by sentence boundaries (\n)
        3. Then by word boundaries (space)
        4. Finally by character if needed

        Args:
            document: Document to chunk

        Returns:
            List of chunked documents (nodes)
        """
        # Get existing metadata
        base_metadata = document.metadata or {}

        # Split document text
        text_chunks = self.text_splitter.split_text(document.text)

        # Create individual documents for each chunk
        chunked_docs = []
        for chunk_idx, chunk_text in enumerate(text_chunks):
            chunk_metadata = base_metadata.copy()
            chunk_metadata["chunk_index"] = chunk_idx
            chunk_metadata["total_chunks"] = len(text_chunks)

            chunk_doc = Document(
                doc_id=f"{document.doc_id}_chunk_{chunk_idx}",
                text=chunk_text,
                metadata=chunk_metadata,
            )
            chunked_docs.append(chunk_doc)

        return chunked_docs

    def chunk_documents(self, documents: list[Document]) -> list[Document]:
        """
        Split multiple documents into chunks using recursive text splitting.

        Delegates to chunk_document for each document.

        Args:
            documents: List of documents to chunk

        Returns:
            List of chunked documents (nodes)
        """
        chunked_docs = []
        for doc in documents:
            chunks = self.chunk_document(doc)
            chunked_docs.extend(chunks)

        logger.info(f"Chunked {len(documents)} documents into {len(chunked_docs)} chunks")
        return chunked_docs

    def embed_document(self, document: Document) -> tuple[str, list[float]]:
        """
        Generate embedding for a single document.

        Args:
            document: Document to embed

        Returns:
            Tuple of (doc_id, embedding_vector)
        """
        try:
            embedding = self.embedding_model_instance.get_text_embedding(document.text)
            if not embedding:
                logger.warning(f"Failed to generate embedding for {document.doc_id}")
                return document.doc_id, []
            return document.doc_id, embedding
        except Exception as e:
            logger.error(f"Error embedding document {document.doc_id}: {e}")
            return document.doc_id, []

    def embed_documents(self, documents: list[Document]) -> dict[str, list[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            documents: List of documents to embed

        Returns:
            Dictionary mapping doc_id to embedding_vector
        """
        embeddings_map = {}
        for doc in documents:
            doc_id, embedding = self.embed_document(doc)
            if embedding:
                embeddings_map[doc_id] = embedding

        logger.info(f"Generated embeddings for {len(embeddings_map)} of {len(documents)} documents")
        return embeddings_map

    def index_document(
        self,
        doc_id: str,
        embedding: list[float],
        metadata: dict[str, Any],
    ) -> bool:
        """
        Index a single document with its embedding in Qdrant.

        Handles deduplication and metadata serialization.

        Args:
            doc_id: Document ID
            embedding: Embedding vector
            metadata: Document metadata (will include 'text' and 'doc_id')

        Returns:
            True if successfully indexed, False otherwise
        """
        try:
            # Skip if document already processed
            doc_hash = self._get_document_hash(
                doc_id,
                metadata.get("text", ""),
            )
            if doc_hash in self._processed_hashes:
                logger.debug(f"Skipping duplicate document: {doc_id}")
                return False

            self._processed_hashes.add(doc_hash)

            # Prepare payload for Qdrant
            payload = metadata.copy() if metadata else {}
            payload["doc_id"] = doc_id

            # Convert metadata values to JSON-serializable types
            for key, value in payload.items():
                if value is not None and not isinstance(value, str | int | float | bool):
                    payload[key] = str(value)

            # Create point for Qdrant
            # Use hash of doc_id to ensure consistent IDs
            point_id = int(md5(doc_id.encode()).hexdigest(), 16) % (2**31)

            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload,
            )

            # Upsert to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point],
            )

            return True

        except Exception as e:
            logger.error(f"Failed to index document {doc_id}: {e}")
            return False

    def _embed_and_index_batch(self, documents: list[Document]) -> int:
        """
        Batch process: embed and index multiple documents.

        Internal method that orchestrates embedding and indexing of documents.

        Args:
            documents: List of documents to embed and index

        Returns:
            Number of successfully indexed documents
        """
        if not documents:
            logger.warning("No documents to process")
            return 0

        # Ensure collection exists
        self._ensure_collection_exists()

        indexed_count = 0

        for doc in documents:
            # Step 1: Generate embedding
            doc_id, embedding = self.embed_document(doc)

            if not embedding:
                logger.warning(f"Skipping document due to failed embedding: {doc_id}")
                continue

            # Step 2: Prepare metadata
            metadata = doc.metadata.copy() if doc.metadata else {}
            metadata["text"] = doc.text

            # Step 3: Index document
            if self.index_document(doc_id, embedding, metadata):
                indexed_count += 1

                if indexed_count % 10 == 0:
                    logger.info(f"Indexed {indexed_count} documents...")

        logger.info(f"Successfully indexed {indexed_count} documents")
        return indexed_count

    def index_documents(
        self,
        directory: str,
        recursive: bool = True,
    ) -> int:
        """
        Complete indexing pipeline: load -> chunk -> embed -> index.

        Args:
            directory: Directory containing documents
            recursive: Whether to scan subdirectories

        Returns:
            Number of successfully indexed documents
        """
        logger.info(f"Starting document indexing from {directory}")

        # Load documents using injected document loader
        documents = self.document_loader.load_documents(
            Path(directory),
            recursive=recursive,
        )
        if not documents:
            logger.warning("No documents found to index")
            return 0

        # Chunk documents
        chunked_documents = self.chunk_documents(documents)

        # Embed and index
        indexed_count = self._embed_and_index_batch(chunked_documents)

        self.document_count = indexed_count
        logger.info(f"Indexing complete. Total documents indexed: {indexed_count}")

        return indexed_count

    def collection_exists(self) -> bool:
        """
        Check if the collection exists in Qdrant.

        Returns:
            True if collection exists, False otherwise
        """
        try:
            collections = self.qdrant_client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            return self.collection_name in collection_names
        except Exception as e:
            logger.error(f"Failed to check collection existence: {e}")
            return False

    def get_collection_stats(self) -> dict[str, Any]:
        """
        Get statistics about the current collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)

            return {
                "collection": self.collection_name,
                "vectors_count": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "status": collection_info.status.value,
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}

    def _delete_collection(self) -> None:
        """
        Delete the collection from Qdrant.

        This is useful for cleanup during testing or resetting the index.
        """
        try:
            self.qdrant_client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise
