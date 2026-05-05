"""Integration tests for the data import pipeline (import_deidentified_data.py)."""


class TestImportPipeline:
    def test_load_and_deidentify_returns_records(self) -> None:
        """load_and_deidentify produces DocumentRecords from sample data."""
        from scripts.data.import_deidentified_data import load_and_deidentify

        records = load_and_deidentify(data_dir="data/public_samples")
        assert len(records) >= 20, "Must produce >= 20 documents"

    def test_public_samples_have_minimum_resume_and_job_counts(self) -> None:
        """Task 1.4 requires at least 10 resumes and 10 job postings."""
        from scripts.data.import_deidentified_data import load_and_deidentify

        records = load_and_deidentify(data_dir="data/public_samples")
        resume_count = sum(1 for rec in records if rec.doc_type == "resume")
        job_count = sum(1 for rec in records if rec.doc_type == "job_posting")

        assert resume_count >= 10, "Must include >= 10 resume records"
        assert job_count >= 10, "Must include >= 10 job posting records"

    def test_all_records_have_content(self) -> None:
        """Every DocumentRecord must have non-empty content."""
        from scripts.data.import_deidentified_data import load_and_deidentify

        records = load_and_deidentify(data_dir="data/public_samples")
        for rec in records:
            assert rec.content.strip(), f"Empty content for {rec.doc_id}"

    def test_record_types_are_valid(self) -> None:
        """All records must have a known doc_type."""
        from scripts.data.import_deidentified_data import load_and_deidentify

        valid_types = {"resume", "job_posting", "qa"}
        records = load_and_deidentify(data_dir="data/public_samples")
        for rec in records:
            assert rec.doc_type in valid_types, f"Unknown type '{rec.doc_type}' for {rec.doc_id}"

    def test_verify_deidentification_passes(self) -> None:
        """Deidentification verification passes on sample data (no synthetic PII)."""
        from scripts.data.import_deidentified_data import (
            load_and_deidentify,
            verify_deidentification,
        )

        records = load_and_deidentify(data_dir="data/public_samples")
        result = verify_deidentification(records)
        assert result is True
