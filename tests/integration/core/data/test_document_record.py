"""Integration tests for DocumentRecord (core.data.document_record)."""

from src.core.data.document_record import DocumentRecord


class TestDocumentRecord:
    """Integration tests for DocumentRecord data model."""

    def test_auto_version_hash(self) -> None:
        """Verify DocumentRecord auto-generates version hash."""
        rec = DocumentRecord(doc_id="r1", doc_type="resume", content="hello world")
        assert len(rec.version) == 12, "Version hash should be 12 chars"

    def test_auto_indexed_at(self) -> None:
        """Verify DocumentRecord auto-generates indexed_at timestamp."""
        rec = DocumentRecord(doc_id="r1", doc_type="resume", content="test")
        assert rec.indexed_at.endswith("+00:00") or "T" in rec.indexed_at

    def test_same_content_same_version(self) -> None:
        """Same content should produce same version hash."""
        r1 = DocumentRecord(doc_id="a", doc_type="resume", content="same")
        r2 = DocumentRecord(doc_id="b", doc_type="resume", content="same")
        assert r1.version == r2.version, "Same content should have same version"

    def test_different_content_different_version(self) -> None:
        """Different content should produce different version hashes."""
        r1 = DocumentRecord(doc_id="a", doc_type="resume", content="aaa")
        r2 = DocumentRecord(doc_id="b", doc_type="resume", content="bbb")
        assert r1.version != r2.version, "Different content should have different versions"
