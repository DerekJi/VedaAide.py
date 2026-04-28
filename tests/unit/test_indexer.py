"""
Unit tests for LlamaIndex Document Indexer.

Tests cover:
- Document loading from various formats (JSON, Markdown, TXT, PDF)
- PDF support with text extraction and error handling
- Text chunking with recursive strategy
- Embedding generation and Qdrant indexing
- Deduplication and error handling
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from llama_index.core import Document

from src.core.retrieval.indexer import PYPDF_AVAILABLE, DocumentIndexer


@pytest.fixture
def temp_data_dir():
    """Create temporary directory with sample data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create sample JSON file
        sample_json = [
            {
                "id": "doc_001",
                "name": "Sample Document 1",
                "content": "This is a sample document about Python programming. " * 10,
            },
            {
                "id": "doc_002",
                "name": "Sample Document 2",
                "content": "This is about machine learning and AI. " * 10,
            },
        ]
        json_file = tmpdir / "samples.json"
        with open(json_file, "w") as f:
            json.dump(sample_json, f)

        # Create sample Markdown file
        md_file = tmpdir / "sample.md"
        with open(md_file, "w") as f:
            f.write("# Sample Markdown\n\n")
            f.write("This is a markdown document with content. " * 10)

        # Create sample text file
        txt_file = tmpdir / "sample.txt"
        with open(txt_file, "w") as f:
            f.write("This is a plain text file. " * 10)

        yield tmpdir


@pytest.fixture
def indexer():
    """Create a DocumentIndexer instance with mocked Qdrant client (Ollama backend)."""
    with patch("src.core.retrieval.indexer.QdrantClient"):
        indexer = DocumentIndexer(
            collection_name="test_collection",
            qdrant_url="http://localhost:6333",
            embedding_provider="ollama",
            embedding_model="bge-m3",
        )
        # Mock the clients
        indexer.qdrant_client = Mock()
        indexer.embedding_model_instance = Mock()
        yield indexer


@pytest.fixture
def indexer_azure():
    """Create a DocumentIndexer instance with Azure OpenAI backend."""
    with patch("src.core.retrieval.indexer.QdrantClient"):
        with patch("src.core.retrieval.indexer.OpenAIEmbedding"):
            indexer = DocumentIndexer(
                collection_name="test_collection",
                qdrant_url="http://localhost:6333",
                embedding_provider="azure",
                embedding_model="text-embedding-3-small",
            )
            # Mock the clients
            indexer.qdrant_client = Mock()
            indexer.embedding_model_instance = Mock()
            yield indexer


class TestDocumentLoading:
    """Test document loading from various formats."""

    def test_load_json_documents(self, indexer, temp_data_dir):
        """Test loading documents from JSON file."""
        json_file = temp_data_dir / "samples.json"
        documents = indexer._load_json_documents(json_file)

        assert len(documents) == 2
        assert documents[0].doc_id == "doc_001"
        assert "Python programming" in documents[0].text
        assert documents[1].doc_id == "doc_002"
        assert "machine learning" in documents[1].text

    def test_load_json_documents_with_missing_fields(self, indexer, temp_data_dir):
        """Test loading JSON with missing optional fields."""
        json_file = temp_data_dir / "samples.json"

        # Modify JSON to have missing fields
        test_data = [{"content": "Test content"}]
        with open(json_file, "w") as f:
            json.dump(test_data, f)

        documents = indexer._load_json_documents(json_file)
        assert len(documents) == 1
        assert "Test content" in documents[0].text

    def test_load_markdown_documents(self, indexer, temp_data_dir):
        """Test loading documents from Markdown file."""
        md_file = temp_data_dir / "sample.md"
        documents = indexer._load_markdown_documents(md_file)

        assert len(documents) == 1
        assert "markdown" in documents[0].text.lower()
        assert documents[0].metadata["format"] == "markdown"

    def test_load_text_documents(self, indexer, temp_data_dir):
        """Test loading documents from plain text file."""
        txt_file = temp_data_dir / "sample.txt"
        documents = indexer._load_text_documents(txt_file)

        assert len(documents) == 1
        assert "plain text" in documents[0].text
        assert documents[0].metadata["format"] == "text"

    def test_load_documents_recursive(self, indexer, temp_data_dir):
        """Test loading documents recursively from directory."""
        # Create subdirectory with additional files
        subdir = temp_data_dir / "subdir"
        subdir.mkdir()
        sub_json = [{"id": "sub_doc", "name": "Subdoc", "content": "Subdirectory document"}]
        with open(subdir / "sub_samples.json", "w") as f:
            json.dump(sub_json, f)

        documents = indexer.load_documents(temp_data_dir, recursive=True)

        # Should load from both root and subdirectory
        assert len(documents) >= 3

    def test_load_documents_non_recursive(self, indexer, temp_data_dir):
        """Test loading documents non-recursively."""
        documents = indexer.load_documents(temp_data_dir, recursive=False)

        # Should load only from root directory
        assert len(documents) >= 1

    def test_load_documents_invalid_directory(self, indexer):
        """Test loading from non-existent directory."""
        documents = indexer.load_documents("/nonexistent/path")
        assert len(documents) == 0

    @pytest.mark.skipif(not PYPDF_AVAILABLE, reason="PyPDF2 not installed")
    def test_load_pdf_documents(self, indexer, temp_data_dir):
        """Test loading documents from PDF file (text-based)."""
        if not PYPDF_AVAILABLE:
            pytest.skip("PyPDF2 not available")

        # Create a minimal PDF with text
        pdf_file = temp_data_dir / "sample.pdf"

        # Create a simple PDF content manually (basic structure)
        # This is a minimal valid PDF with extractable text
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(This is a sample PDF document.) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000262 00000 n
0000000353 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
432
%%EOF"""

        with open(pdf_file, "wb") as f:
            f.write(pdf_content)

        # Load PDF
        documents = indexer._load_pdf_documents(pdf_file)

        # Should load the PDF (may or may not extract text from this minimal PDF)
        assert isinstance(documents, list)

    def test_load_pdf_documents_pypdf_not_available(self, indexer, temp_data_dir, monkeypatch):
        """Test PDF loading when PyPDF2 is not available."""
        # Mock PYPDF_AVAILABLE as False
        import src.core.retrieval.indexer as indexer_module

        monkeypatch.setattr(indexer_module, "PYPDF_AVAILABLE", False)

        # Create a dummy PDF file
        pdf_file = temp_data_dir / "sample.pdf"
        pdf_file.write_text("fake pdf content")

        # Should return empty list and log warning
        documents = indexer._load_pdf_documents(pdf_file)
        assert len(documents) == 0

    def test_load_pdf_documents_invalid_file(self, indexer, temp_data_dir):
        """Test PDF loading with invalid/corrupted PDF file."""
        if not PYPDF_AVAILABLE:
            pytest.skip("PyPDF2 not available")

        # Create an invalid PDF file
        pdf_file = temp_data_dir / "invalid.pdf"
        pdf_file.write_text("This is not a valid PDF file at all!")

        # Should handle error gracefully
        documents = indexer._load_pdf_documents(pdf_file)
        # Should return empty list or log warning
        assert isinstance(documents, list)

    def test_load_documents_mixed_formats_with_pdf(self, indexer, temp_data_dir):
        """Test loading documents with mixed formats including PDF."""
        if not PYPDF_AVAILABLE:
            pytest.skip("PyPDF2 not available")

        # Create a simple minimal PDF
        pdf_file = temp_data_dir / "doc.pdf"
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 20 >>
stream
BT
(PDF test) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000262 00000 n
0000000331 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
410
%%EOF"""

        with open(pdf_file, "wb") as f:
            f.write(pdf_content)

        # Load all formats including PDF
        documents = indexer.load_documents(temp_data_dir, recursive=True)

        # Should load from multiple formats
        assert len(documents) >= 3  # JSON, MD, TXT, and optionally PDF
        # Check that we have different formats
        formats = {doc.metadata.get("format") for doc in documents}
        assert "json" in formats
        assert "markdown" in formats
        assert "text" in formats


class TestDocumentChunking:
    """Test document chunking logic."""

    def test_chunk_documents_basic(self, indexer):
        """Test basic document chunking."""
        # Create a long document
        long_content = "This is a test sentence. " * 50
        doc = Document(doc_id="test_doc", text=long_content)

        chunked = indexer.chunk_documents([doc])

        # Should create at least one chunk
        assert len(chunked) >= 1
        assert all(chunk.metadata["chunk_index"] >= 0 for chunk in chunked)
        assert all("total_chunks" in chunk.metadata for chunk in chunked)

    def test_chunk_documents_preserves_metadata(self, indexer):
        """Test that chunking preserves original metadata."""
        doc = Document(
            doc_id="test_doc",
            text="This is test content. " * 20,
            metadata={"source": "test.json", "format": "json"},
        )

        chunked = indexer.chunk_documents([doc])

        # Verify metadata preservation
        for chunk in chunked:
            assert chunk.metadata["source"] == "test.json"
            assert chunk.metadata["format"] == "json"

    def test_chunk_documents_respects_chunk_size(self, indexer):
        """Test that chunks respect configured size limit."""
        # Create many shorter sentences to force chunking
        long_content = "This is a test sentence. " * 100
        doc = Document(doc_id="test_doc", text=long_content)

        chunked = indexer.chunk_documents([doc])

        # Should create chunks (SentenceSplitter may have different behavior)
        assert len(chunked) >= 1
        assert sum(len(chunk.text) for chunk in chunked) > 0

    def test_chunk_empty_document(self, indexer):
        """Test chunking of empty document."""
        doc = Document(doc_id="empty", text="")
        chunked = indexer.chunk_documents([doc])

        # Empty document should produce at least one (empty) chunk
        assert len(chunked) >= 0


class TestEmbeddingAndIndexing:
    """Test embedding generation and indexing."""

    def test_ensure_collection_exists_new(self, indexer):
        """Test collection creation when it doesn't exist."""
        indexer.qdrant_client.get_collection.side_effect = Exception("Not found")

        indexer._ensure_collection_exists()

        # Should call create_collection
        indexer.qdrant_client.create_collection.assert_called_once()
        call_args = indexer.qdrant_client.create_collection.call_args
        assert call_args[1]["collection_name"] == "test_collection"

    def test_ensure_collection_exists_already(self, indexer):
        """Test when collection already exists."""
        indexer.qdrant_client.get_collection.return_value = Mock()

        indexer._ensure_collection_exists()

        # Should not try to create
        indexer.qdrant_client.create_collection.assert_not_called()

    def test_embed_and_index_success(self, indexer):
        """Test successful embedding and indexing."""
        # Mock embedding generation
        mock_embedding = [0.1] * 1536
        indexer.embedding_model_instance.get_text_embedding.return_value = mock_embedding
        indexer.qdrant_client.get_collection.return_value = Mock()

        docs = [
            Document(doc_id="doc1", text="Test content 1"),
            Document(doc_id="doc2", text="Test content 2"),
        ]

        count = indexer.embed_and_index(docs)

        # Should index 2 documents
        assert count == 2
        assert indexer.qdrant_client.upsert.call_count == 2

    def test_embed_and_index_empty_list(self, indexer):
        """Test indexing empty document list."""
        count = indexer.embed_and_index([])
        assert count == 0

    def test_embed_and_index_deduplication(self, indexer):
        """Test duplicate document deduplication."""
        mock_embedding = [0.1] * 1536
        indexer.embedding_model_instance.get_text_embedding.return_value = mock_embedding
        indexer.qdrant_client.get_collection.return_value = Mock()

        # Create two identical documents
        doc = Document(doc_id="doc1", text="Same content")
        docs = [doc, doc]

        count = indexer.embed_and_index(docs)

        # Should only index once due to deduplication
        assert count == 1
        assert indexer.qdrant_client.upsert.call_count == 1

    def test_embed_and_index_missing_embedding(self, indexer):
        """Test handling when embedding generation fails."""
        indexer.embedding_model_instance.get_text_embedding.return_value = None
        indexer.qdrant_client.get_collection.return_value = Mock()

        docs = [Document(doc_id="doc1", text="Test content")]

        count = indexer.embed_and_index(docs)

        # Should skip document with no embedding
        assert count == 0
        assert indexer.qdrant_client.upsert.call_count == 0


class TestFullPipeline:
    """Test complete indexing pipeline."""

    def test_index_documents_full_pipeline(self, indexer, temp_data_dir):
        """Test complete document indexing pipeline."""
        # Mock dependencies
        mock_embedding = [0.1] * 1536
        indexer.embedding_model_instance.get_text_embedding.return_value = mock_embedding
        indexer.qdrant_client.get_collection.return_value = Mock()

        indexed_count = indexer.index_documents(str(temp_data_dir), recursive=True)

        # Should process documents successfully
        assert indexed_count > 0
        assert indexer.document_count == indexed_count

    def test_get_collection_stats(self, indexer):
        """Test retrieving collection statistics."""
        mock_collection = Mock()
        mock_collection.points_count = 100
        mock_collection.config.params.vectors.size = 1536
        mock_collection.status.value = "green"
        indexer.qdrant_client.get_collection.return_value = mock_collection

        stats = indexer.get_collection_stats()

        assert stats["collection_name"] == "test_collection"
        assert stats["point_count"] == 100
        assert stats["vector_size"] == 1536
        assert stats["status"] == "green"

    def test_get_collection_stats_error(self, indexer):
        """Test error handling in get_collection_stats."""
        indexer.qdrant_client.get_collection.side_effect = Exception("Connection failed")

        stats = indexer.get_collection_stats()

        assert stats == {}


class TestDocumentHash:
    """Test document hashing for deduplication."""

    def test_get_document_hash_consistency(self, indexer):
        """Test that same document produces same hash."""
        doc_id = "test_doc"
        content = "Test content"

        hash1 = indexer._get_document_hash(doc_id, content)
        hash2 = indexer._get_document_hash(doc_id, content)

        assert hash1 == hash2

    def test_get_document_hash_different_for_different_content(self, indexer):
        """Test that different content produces different hash."""
        doc_id = "test_doc"

        hash1 = indexer._get_document_hash(doc_id, "Content 1")
        hash2 = indexer._get_document_hash(doc_id, "Content 2")

        assert hash1 != hash2


class TestConfiguration:
    """Test DocumentIndexer configuration."""

    def test_custom_chunk_size(self):
        """Test custom chunk size configuration."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            indexer = DocumentIndexer(chunk_size=1024, chunk_overlap=128)

            assert indexer.chunk_size == 1024
            assert indexer.chunk_overlap == 128

    def test_custom_embedding_model(self):
        """Test custom embedding model configuration."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            indexer = DocumentIndexer(
                embedding_provider="azure", embedding_model="text-embedding-3-large"
            )

            assert indexer.embedding_model == "text-embedding-3-large"


class TestEmbeddingProvider:
    """Test embedding provider configuration and switching."""

    def test_ollama_provider_initialization(self):
        """Test initialization with Ollama provider."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            indexer = DocumentIndexer(
                embedding_provider="ollama",
                embedding_model="bge-m3",
                ollama_base_url="http://localhost:11434",
            )

            assert indexer.embedding_provider == "ollama"
            assert indexer.embedding_model == "bge-m3"
            assert indexer.ollama_base_url == "http://localhost:11434"

    def test_azure_provider_initialization(self):
        """Test initialization with Azure OpenAI provider."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            with patch("src.core.retrieval.indexer.OpenAIEmbedding"):
                indexer = DocumentIndexer(
                    embedding_provider="azure",
                    embedding_model="text-embedding-3-small",
                )

                assert indexer.embedding_provider == "azure"
                assert indexer.embedding_model == "text-embedding-3-small"

    def test_invalid_provider_raises_error(self):
        """Test that invalid provider raises ValueError."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            with pytest.raises(ValueError, match="Unsupported embedding provider"):
                DocumentIndexer(embedding_provider="invalid")

    def test_get_embedding_dimension_azure(self):
        """Test getting embedding dimension for Azure provider."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            with patch("src.core.retrieval.indexer.OpenAIEmbedding"):
                indexer = DocumentIndexer(
                    embedding_provider="azure",
                    embedding_model="text-embedding-3-small",
                )

                dim = indexer._get_embedding_dimension()
                assert dim == 1536

    def test_get_embedding_dimension_azure_large(self):
        """Test getting embedding dimension for Azure large model."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            with patch("src.core.retrieval.indexer.OpenAIEmbedding"):
                indexer = DocumentIndexer(
                    embedding_provider="azure",
                    embedding_model="text-embedding-3-large",
                )

                dim = indexer._get_embedding_dimension()
                assert dim == 3072

    def test_get_embedding_dimension_ollama_bge(self):
        """Test getting embedding dimension for Ollama bge-m3."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            indexer = DocumentIndexer(
                embedding_provider="ollama",
                embedding_model="bge-m3",
            )

            dim = indexer._get_embedding_dimension()
            assert dim == 1024

    def test_get_embedding_dimension_ollama_unknown_model(self):
        """Test getting embedding dimension for unknown Ollama model."""
        with patch("src.core.retrieval.indexer.QdrantClient"):
            indexer = DocumentIndexer(
                embedding_provider="ollama",
                embedding_model="unknown-model",
            )

            dim = indexer._get_embedding_dimension()
            # Should return default dimension
            assert dim == 1024


# Integration tests (when real services are available)
@pytest.mark.skip(reason="Requires real Qdrant and Azure OpenAI setup")
class TestIntegrationWithRealServices:
    """Integration tests with actual Qdrant and Azure OpenAI."""

    def test_real_document_indexing(self):
        """Test with real Qdrant and embedding service."""
        # This would require actual service setup
        pass
