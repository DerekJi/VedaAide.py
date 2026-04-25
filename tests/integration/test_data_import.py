"""Integration tests for data import and Qdrant indexing pipeline (Task 1.6).

These tests mock Qdrant and LlamaIndex to verify the pipeline logic
without requiring a running Qdrant server or embedding model.
"""

import json
from typing import Any, List
from unittest.mock import MagicMock, patch

import pytest

from src.core.data.indexer import DocumentIndexer, DocumentRecord, IndexStats

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_records() -> List[DocumentRecord]:
    """Provide 12 minimal DocumentRecord objects (> MIN_DOCUMENTS = 10)."""
    records = []
    for i in range(1, 13):
        records.append(
            DocumentRecord(
                doc_id=f"doc_{i:03d}",
                doc_type="resume" if i % 2 == 0 else "job_posting",
                content=f"Sample content for document {i}. No PII here.",
                metadata={"source": "test"},
            )
        )
    return records


@pytest.fixture
def mock_qdrant_client() -> MagicMock:
    """Mock QdrantClient."""
    client = MagicMock()
    collection_mock = MagicMock()
    collection_mock.vectors_count = 12
    collection_mock.indexed_vectors_count = 12
    collection_mock.status = "green"
    client.get_collection.return_value = collection_mock
    client.get_collections.return_value = MagicMock(collections=[])
    return client


# ---------------------------------------------------------------------------
# DocumentRecord tests
# ---------------------------------------------------------------------------


class TestDocumentRecord:
    def test_auto_version_hash(self) -> None:
        rec = DocumentRecord(doc_id="r1", doc_type="resume", content="hello world")
        assert len(rec.version) == 12, "Version hash should be 12 chars"

    def test_auto_indexed_at(self) -> None:
        rec = DocumentRecord(doc_id="r1", doc_type="resume", content="test")
        assert rec.indexed_at.endswith("+00:00") or "T" in rec.indexed_at

    def test_same_content_same_version(self) -> None:
        r1 = DocumentRecord(doc_id="a", doc_type="resume", content="same")
        r2 = DocumentRecord(doc_id="b", doc_type="resume", content="same")
        assert r1.version == r2.version

    def test_different_content_different_version(self) -> None:
        r1 = DocumentRecord(doc_id="a", doc_type="resume", content="aaa")
        r2 = DocumentRecord(doc_id="b", doc_type="resume", content="bbb")
        assert r1.version != r2.version


# ---------------------------------------------------------------------------
# DocumentIndexer tests
# ---------------------------------------------------------------------------


# pylint: disable=redefined-outer-name
class TestDocumentIndexer:
    # pylint: disable-next=redefined-outer-name
    def test_collection_exists_false(self, mock_qdrant_client: MagicMock) -> None:
        """Returns False when collection is not in Qdrant."""
        indexer = DocumentIndexer()
        with patch.object(indexer, "_get_qdrant_client", return_value=mock_qdrant_client):
            assert indexer.collection_exists() is False

    # pylint: disable-next=redefined-outer-name
    def test_collection_exists_true(self, mock_qdrant_client: MagicMock) -> None:
        """Returns True when collection is already present."""
        existing = MagicMock()
        existing.name = "vedaaide_docs"
        mock_qdrant_client.get_collections.return_value = MagicMock(collections=[existing])
        indexer = DocumentIndexer()
        with patch.object(indexer, "_get_qdrant_client", return_value=mock_qdrant_client):
            assert indexer.collection_exists() is True

    # pylint: disable-next=redefined-outer-name
    def test_get_collection_stats(self, mock_qdrant_client: MagicMock) -> None:
        """get_collection_stats returns expected keys."""
        indexer = DocumentIndexer()
        with patch.object(indexer, "_get_qdrant_client", return_value=mock_qdrant_client):
            stats = indexer.get_collection_stats()
        assert "collection" in stats
        assert "vectors_count" in stats
        assert "status" in stats

    def test_index_documents_success(
        self,
        sample_records: List[DocumentRecord],
        mock_qdrant_client: MagicMock,
    ) -> None:
        """index_documents returns correct stats after successful run."""
        indexer = DocumentIndexer()
        mock_embed = MagicMock()
        mock_settings = MagicMock()
        mock_vsi = MagicMock()
        mock_vsi.from_documents.return_value = MagicMock()
        mock_qvs = MagicMock()

        with (
            patch.object(indexer, "_get_qdrant_client", return_value=mock_qdrant_client),
            patch.object(indexer, "_get_embed_model", return_value=mock_embed),
            patch.object(indexer, "_ensure_collection"),
            patch("src.core.data.indexer.Settings", mock_settings),
            patch("src.core.data.indexer.VectorStoreIndex", mock_vsi),
            patch("src.core.data.indexer.QdrantVectorStore", mock_qvs),
        ):
            stats = indexer.index_documents(sample_records)

        assert stats.indexed == len(sample_records)
        assert stats.errors == 0
        assert stats.collection == "vedaaide_docs"

    def test_save_manifest(
        self,
        tmp_path: Any,
        sample_records: List[DocumentRecord],
    ) -> None:
        """save_manifest writes a valid JSON file with expected fields."""
        manifest_path = str(tmp_path / "manifest.json")
        stats = IndexStats(
            collection="vedaaide_docs",
            indexed=12,
            skipped=0,
            errors=0,
            total_vectors=12,
        )
        indexer = DocumentIndexer()
        indexer.save_manifest(stats, sample_records, manifest_path)

        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)

        assert data["version"] == "1.0"
        assert data["collection"] == "vedaaide_docs"
        assert len(data["documents"]) == len(sample_records)
        assert data["documents"][0]["doc_id"] == sample_records[0].doc_id


# ---------------------------------------------------------------------------
# Pipeline integration (load_and_deidentify)
# ---------------------------------------------------------------------------


class TestImportPipeline:
    def test_load_and_deidentify_returns_records(self) -> None:
        """load_and_deidentify produces DocumentRecords from sample data."""
        # pylint: disable-next=import-outside-toplevel
        from scripts.data.import_deidentified_data import load_and_deidentify

        records = load_and_deidentify(data_dir="data/public_samples")
        assert len(records) >= 10, "Must produce >= 10 documents"

    def test_all_records_have_content(self) -> None:
        """Every DocumentRecord must have non-empty content."""
        # pylint: disable-next=import-outside-toplevel
        from scripts.data.import_deidentified_data import load_and_deidentify

        records = load_and_deidentify(data_dir="data/public_samples")
        for rec in records:
            assert rec.content.strip(), f"Empty content for {rec.doc_id}"

    def test_record_types_are_valid(self) -> None:
        """All records must have a known doc_type."""
        # pylint: disable-next=import-outside-toplevel
        from scripts.data.import_deidentified_data import load_and_deidentify

        valid_types = {"resume", "job_posting", "qa"}
        records = load_and_deidentify(data_dir="data/public_samples")
        for rec in records:
            assert rec.doc_type in valid_types, f"Unknown type '{rec.doc_type}' for {rec.doc_id}"

    def test_verify_deidentification_passes(self) -> None:
        """Deidentification verification passes on sample data (no synthetic PII)."""
        # pylint: disable-next=import-outside-toplevel
        from scripts.data.import_deidentified_data import (
            load_and_deidentify,
            verify_deidentification,
        )

        records = load_and_deidentify(data_dir="data/public_samples")
        result = verify_deidentification(records)
        assert result is True
