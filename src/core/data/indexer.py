"""Document indexer for VedaAide using LlamaIndex and Qdrant.

Builds a multi-dimensional data model from deidentified documents and
indexes them into a Qdrant vector store for semantic retrieval.

Usage:
    >>> from src.core.data.indexer import DocumentIndexer
    >>> indexer = DocumentIndexer()
    >>> stats = indexer.index_documents(documents)
    >>> print(stats)  # {"indexed": 10, "collection": "vedaaide_docs", ...}
"""

import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Lazy imports — only resolved at call time to avoid hard runtime dependency.
# They are imported at module level as None so tests can patch them.
try:
    from llama_index.core import Document, Settings, VectorStoreIndex
    from llama_index.vector_stores.qdrant import QdrantVectorStore
except ImportError:  # pragma: no cover
    Document = None  # type: ignore[misc,assignment]
    Settings = None  # type: ignore[misc,assignment]
    VectorStoreIndex = None  # type: ignore[misc,assignment]
    QdrantVectorStore = None  # type: ignore[misc,assignment]

# Default Qdrant settings
DEFAULT_QDRANT_URL = "http://localhost:6333"
DEFAULT_COLLECTION_NAME = "vedaaide_docs"
DEFAULT_EMBED_MODEL = "BAAI/bge-small-en-v1.5"
EMBED_DIM = 384  # bge-small-en-v1.5 output dimension


@dataclass
class DocumentRecord:
    """A normalized document ready for indexing."""

    doc_id: str
    doc_type: str  # "resume" | "job_posting" | "qa"
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: str = ""
    indexed_at: str = ""

    def __post_init__(self) -> None:
        if not self.version:
            self.version = self._compute_hash()
        if not self.indexed_at:
            self.indexed_at = datetime.now(timezone.utc).isoformat()

    def _compute_hash(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()[:12]


@dataclass
class IndexStats:
    """Statistics from an indexing run."""

    collection: str
    indexed: int
    skipped: int
    errors: int
    total_vectors: int
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DocumentIndexer:
    """Index deidentified documents into Qdrant via LlamaIndex.

    Uses HuggingFace BGE-small embeddings (local, no API key required) and
    stores documents in a Qdrant collection with full metadata.

    Args:
        qdrant_url: URL of the Qdrant server.
        collection_name: Name of the Qdrant collection.
        embed_model_name: HuggingFace model name for embeddings.
    """

    def __init__(
        self,
        qdrant_url: str = DEFAULT_QDRANT_URL,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        embed_model_name: str = DEFAULT_EMBED_MODEL,
    ) -> None:
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.embed_model_name = embed_model_name
        self._qdrant_client: Optional[Any] = None
        self._embed_model: Optional[Any] = None
        self._vector_store: Optional[Any] = None

    def _get_qdrant_client(self) -> Any:
        if self._qdrant_client is None:
            from qdrant_client import QdrantClient  # pylint: disable=import-outside-toplevel

            self._qdrant_client = QdrantClient(url=self.qdrant_url)
            logger.info("Connected to Qdrant at %s", self.qdrant_url)
        return self._qdrant_client

    def _get_embed_model(self) -> Any:
        if self._embed_model is None:
            # pylint: disable-next=import-outside-toplevel
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding

            self._embed_model = HuggingFaceEmbedding(model_name=self.embed_model_name)
            logger.info("Loaded embedding model: %s", self.embed_model_name)
        return self._embed_model

    def _ensure_collection(self) -> None:
        from qdrant_client.models import (  # pylint: disable=import-outside-toplevel
            Distance,
            VectorParams,
        )

        client = self._get_qdrant_client()
        existing = {c.name for c in client.get_collections().collections}
        if self.collection_name not in existing:
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
            )
            logger.info("Created Qdrant collection: %s", self.collection_name)

    def _build_llama_documents(self, records: List[DocumentRecord]) -> List[Any]:
        docs = []
        for rec in records:
            meta = {
                "doc_id": rec.doc_id,
                "doc_type": rec.doc_type,
                "version": rec.version,
                "indexed_at": rec.indexed_at,
                **rec.metadata,
            }
            docs.append(Document(text=rec.content, metadata=meta, id_=rec.doc_id))
        return docs

    def index_documents(self, records: List[DocumentRecord]) -> IndexStats:
        """Index a list of DocumentRecords into Qdrant.

        Args:
            records: List of deidentified document records.

        Returns:
            IndexStats with counts and collection info.
        """
        self._ensure_collection()
        client = self._get_qdrant_client()
        embed_model = self._get_embed_model()

        Settings.embed_model = embed_model
        Settings.llm = None  # no LLM needed for indexing

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=self.collection_name,
        )

        llama_docs = self._build_llama_documents(records)
        indexed = 0
        errors = 0

        for doc in llama_docs:
            try:
                VectorStoreIndex.from_documents(
                    [doc],
                    vector_store=vector_store,
                    show_progress=False,
                )
                indexed += 1
                logger.debug("Indexed doc: %s", doc.id_)
            except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-exception-caught
                errors += 1
                logger.error("Failed to index %s: %s", doc.id_, exc)

        total = client.get_collection(self.collection_name).vectors_count or 0

        stats = IndexStats(
            collection=self.collection_name,
            indexed=indexed,
            skipped=len(records) - indexed - errors,
            errors=errors,
            total_vectors=total,
        )
        logger.info(
            "Indexing complete: %d indexed, %d errors, %d total vectors",
            indexed,
            errors,
            total,
        )
        return stats

    def get_collection_stats(self) -> Dict[str, Any]:
        """Return current collection statistics from Qdrant."""
        client = self._get_qdrant_client()
        info = client.get_collection(self.collection_name)
        return {
            "collection": self.collection_name,
            "vectors_count": info.vectors_count,
            "indexed_vectors_count": info.indexed_vectors_count,
            "status": str(info.status),
        }

    def collection_exists(self) -> bool:
        """Return True if the collection already exists in Qdrant."""
        client = self._get_qdrant_client()
        existing = {c.name for c in client.get_collections().collections}
        return self.collection_name in existing

    def save_manifest(
        self, stats: IndexStats, records: List[DocumentRecord], output_path: str
    ) -> None:
        """Write an index manifest JSON file for version tracking.

        Args:
            stats: IndexStats from the indexing run.
            records: List of indexed records.
            output_path: File path to write the manifest.
        """
        manifest = {
            "version": "1.0",
            "generated_at": stats.timestamp,
            "collection": stats.collection,
            "summary": asdict(stats),
            "documents": [
                {
                    "doc_id": r.doc_id,
                    "doc_type": r.doc_type,
                    "version": r.version,
                    "indexed_at": r.indexed_at,
                }
                for r in records
            ],
        }
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        logger.info("Manifest saved to %s", output_path)
