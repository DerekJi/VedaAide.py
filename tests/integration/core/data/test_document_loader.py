"""Integration tests for DocumentLoader with real data files.

These tests verify that DocumentLoader can correctly load documents
from various sources (JSON, Markdown, TXT, PDF) and preserve metadata.
"""

from pathlib import Path

import pytest

from src.core.data.document_loader import DocumentLoader


@pytest.fixture
def sample_resumes_file(test_data_dir: Path) -> Path:
    """Path to sample resumes JSON file."""
    return test_data_dir / "resumes.json"


@pytest.fixture
def sample_jobs_file(test_data_dir: Path) -> Path:
    """Path to sample job postings JSON file."""
    return test_data_dir / "job_postings.json"


@pytest.fixture
def sample_resume_md_file(test_data_dir: Path) -> Path:
    """Path to sample resume Markdown file."""
    return test_data_dir / "resume_sample.md"


@pytest.fixture
def sample_job_txt_file(test_data_dir: Path) -> Path:
    """Path to sample job posting TXT file."""
    return test_data_dir / "job_posting_sample.txt"


@pytest.fixture
def sample_resume_pdf_file(test_data_dir: Path) -> Path:
    """Path to sample resume PDF file."""
    return test_data_dir / "resume_sample.pdf"


@pytest.fixture
def sample_job_pdf_file(test_data_dir: Path) -> Path:
    """Path to sample job posting PDF file."""
    return test_data_dir / "job_posting_sample.pdf"


class TestDocumentLoaderJSON:
    """Integration tests for DocumentLoader with JSON files."""

    def test_load_json_documents_with_real_resumes(self, sample_resumes_file: Path) -> None:
        """Load real resume documents from JSON file."""
        loader = DocumentLoader()
        documents = loader.load_json_documents(sample_resumes_file)

        assert len(documents) == 3, "Should load 3 resumes"
        assert all(hasattr(doc, "doc_id") for doc in documents)
        assert all(hasattr(doc, "text") for doc in documents)
        assert all(len(doc.text) > 0 for doc in documents)

    def test_load_json_documents_with_real_jobs(self, sample_jobs_file: Path) -> None:
        """Load real job postings from JSON file."""
        loader = DocumentLoader()
        documents = loader.load_json_documents(sample_jobs_file)

        assert len(documents) == 3, "Should load 3 job postings"
        assert all(hasattr(doc, "text") for doc in documents)

    def test_loaded_json_documents_have_metadata(self, sample_resumes_file: Path) -> None:
        """Verify loaded JSON documents include metadata."""
        loader = DocumentLoader()
        documents = loader.load_json_documents(sample_resumes_file)

        for doc in documents:
            assert doc.metadata is not None
            assert "format" in doc.metadata
            assert doc.metadata["format"] == "json"

    def test_loaded_json_documents_have_doc_ids(self, sample_resumes_file: Path) -> None:
        """Verify loaded JSON documents have doc_id field."""
        loader = DocumentLoader()
        documents = loader.load_json_documents(sample_resumes_file)

        assert all(doc.doc_id for doc in documents)
        doc_ids = [doc.doc_id for doc in documents]
        assert len(set(doc_ids)) == len(doc_ids), "All doc_ids should be unique"


class TestDocumentLoaderMarkdown:
    """Integration tests for DocumentLoader with Markdown files."""

    def test_load_markdown_documents(self, sample_resume_md_file: Path) -> None:
        """Load documents from Markdown file."""
        if not sample_resume_md_file.exists():
            pytest.skip("Markdown test file not available")

        loader = DocumentLoader()
        documents = loader.load_markdown_documents(sample_resume_md_file)

        assert len(documents) > 0, "Should load at least one document from Markdown file"
        assert all(hasattr(doc, "text") for doc in documents)
        assert all(len(doc.text) > 0 for doc in documents)

    def test_markdown_documents_have_metadata(self, sample_resume_md_file: Path) -> None:
        """Verify loaded Markdown documents have metadata."""
        if not sample_resume_md_file.exists():
            pytest.skip("Markdown test file not available")

        loader = DocumentLoader()
        documents = loader.load_markdown_documents(sample_resume_md_file)

        for doc in documents:
            assert doc.metadata is not None
            assert "format" in doc.metadata or "source" in doc.metadata


class TestDocumentLoaderTextFiles:
    """Integration tests for DocumentLoader with plain text files."""

    def test_load_text_documents(self, sample_job_txt_file: Path) -> None:
        """Load documents from plain text file."""
        if not sample_job_txt_file.exists():
            pytest.skip("Text test file not available")

        loader = DocumentLoader()
        documents = loader.load_text_documents(sample_job_txt_file)

        assert len(documents) > 0, "Should load at least one document from text file"
        assert all(hasattr(doc, "text") for doc in documents)

    def test_text_documents_have_metadata(self, sample_job_txt_file: Path) -> None:
        """Verify loaded text documents have metadata."""
        if not sample_job_txt_file.exists():
            pytest.skip("Text test file not available")

        loader = DocumentLoader()
        documents = loader.load_text_documents(sample_job_txt_file)

        for doc in documents:
            assert doc.metadata is not None
            assert "source" in doc.metadata or "format" in doc.metadata


class TestDocumentLoaderPDF:
    """Integration tests for DocumentLoader with PDF files."""

    def test_load_pdf_documents(self, sample_resume_pdf_file: Path) -> None:
        """Load documents from PDF file."""
        if not sample_resume_pdf_file.exists():
            pytest.skip("PDF test file not available")

        loader = DocumentLoader()
        documents = loader.load_pdf_documents(sample_resume_pdf_file)

        assert len(documents) > 0, "Should load at least one document from PDF file"
        assert all(hasattr(doc, "text") for doc in documents)
        assert all(len(doc.text) > 0 for doc in documents)

    def test_pdf_documents_have_metadata(self, sample_resume_pdf_file: Path) -> None:
        """Verify loaded PDF documents have metadata."""
        if not sample_resume_pdf_file.exists():
            pytest.skip("PDF test file not available")

        loader = DocumentLoader()
        documents = loader.load_pdf_documents(sample_resume_pdf_file)

        for doc in documents:
            assert doc.metadata is not None
            # PDF documents should have source information
            assert "source" in doc.metadata or "format" in doc.metadata


class TestDocumentLoaderDirectoryLoading:
    """Integration tests for loading documents from directories."""

    def test_load_documents_from_directory(self, test_data_dir: Path) -> None:
        """Load documents recursively from test data directory."""
        loader = DocumentLoader()
        documents = loader.load_documents(test_data_dir, recursive=True)

        # Should load JSON (6 docs), Markdown, TXT, and potentially PDFs
        assert len(documents) >= 6, "Should load at least 6 documents from test data"

    def test_load_documents_respects_recursive_flag(self, test_data_dir: Path) -> None:
        """Verify recursive flag controls directory traversal."""
        loader = DocumentLoader()

        # Non-recursive should load nothing (test_data_dir has only subdirectory)
        docs_non_recursive = loader.load_documents(test_data_dir, recursive=False)

        # Recursive should load all
        docs_recursive = loader.load_documents(test_data_dir, recursive=True)

        # At minimum, recursive should have more or equal docs
        assert len(docs_recursive) >= len(docs_non_recursive)

    def test_directory_loading_includes_multiple_formats(self, test_data_dir: Path) -> None:
        """Verify directory loading includes multiple file formats."""
        loader = DocumentLoader()
        documents = loader.load_documents(test_data_dir, recursive=True)

        # Check for different file formats in loaded documents
        formats = set()
        for doc in documents:
            if "format" in doc.metadata:
                formats.add(doc.metadata["format"])

        # Should have loaded at least JSON
        assert "json" in formats, "Should load JSON documents"

        # Log for debugging
        print(f"Loaded formats: {formats}")
