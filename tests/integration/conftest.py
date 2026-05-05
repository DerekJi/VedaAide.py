"""
Pytest configuration and fixtures for integration tests.

Provides:
- Isolated collection names for testing
- Automatic cleanup between tests
- Qdrant service management
"""

import uuid
from pathlib import Path

import pytest

from tests.common._check_dependencies import DependencyError, check_qdrant_availability


@pytest.fixture
def test_data_dir() -> Path:
    """Get path to test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def isolated_collection_name() -> str:
    """
    Generate an isolated collection name for testing.

    Uses format: test_vedaaide_{uuid}
    This ensures:
    - Isolation from production collections (different prefix)
    - Isolation between test runs (unique UUID)
    - Easy identification as test data (test_ prefix)

    Returns:
        Unique collection name starting with test_vedaaide_
    """
    unique_id = str(uuid.uuid4())[:8]  # Use first 8 chars of UUID
    return f"test_vedaaide_{unique_id}"


@pytest.fixture
def qdrant_client():
    """
    Provide Qdrant client for integration tests.

    Skips test if Qdrant is not available.
    """
    try:
        check_qdrant_availability()
        from qdrant_client import QdrantClient

        client = QdrantClient(url="http://localhost:6333")
        return client
    except DependencyError as e:
        pytest.skip(f"Qdrant not available: {e}")


@pytest.fixture
def isolated_indexer(isolated_collection_name):
    """
    Provide an isolated DocumentIndexer instance.

    Features:
    - Uses isolated collection name
    - Automatically cleans up after test
    - Skips if Qdrant not available
    """
    try:
        check_qdrant_availability()
    except DependencyError as e:
        pytest.skip(f"Qdrant not available: {e}")

    from src.core.retrieval.document_indexer import DocumentIndexer

    indexer = DocumentIndexer(
        collection_name=isolated_collection_name,
        qdrant_url="http://localhost:6333",
    )

    # Cleanup before test starts
    try:
        if indexer.collection_exists():
            indexer._delete_collection()
    except Exception:
        pass

    yield indexer

    # Cleanup after test finishes
    try:
        if indexer.collection_exists():
            indexer._delete_collection()
    except Exception:
        pass


@pytest.fixture
def integration_test_marker():
    """
    Mark a test as an integration test requiring external services.

    This marker can be used to:
    - Run only integration tests: pytest -m integration
    - Skip integration tests: pytest -m "not integration"
    """
    pytest.mark.integration


# Configure pytest markers
def pytest_configure(config):
    """Register custom pytest markers and generate test PDF files."""
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests requiring external services",
    )
    config.addinivalue_line(
        "markers", "requires_qdrant: marks tests that require Qdrant service to be running"
    )
    config.addinivalue_line(
        "markers", "requires_ollama: marks tests that require Ollama service to be running"
    )

    # Generate test PDF files
    test_data_dir = Path(__file__).parent / "test_data"
    _generate_test_pdfs(test_data_dir)


def _generate_test_pdfs(test_data_dir: Path) -> None:
    """Generate PDF test files for DocumentLoader testing."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas as canvas_module
    except ImportError:
        return

    # Ensure test_data_dir exists
    test_data_dir.mkdir(parents=True, exist_ok=True)

    # Generate resume PDF if not exists
    resume_pdf = test_data_dir / "resume_sample.pdf"
    if not resume_pdf.exists():
        try:
            c = canvas_module.Canvas(str(resume_pdf), pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(50, 750, "Senior Software Engineer Resume")
            c.drawString(50, 730, "Alice Johnson")
            c.drawString(50, 710, "Email: alice.johnson@example.com")
            c.setFont("Helvetica", 10)
            c.drawString(50, 680, "Skills: Python, Java, AWS, Kubernetes, Docker")
            c.drawString(50, 660, "Experience: 8+ years in full-stack development")
            c.save()
        except Exception as e:
            print(f"Warning: Failed to generate resume PDF: {e}")

    # Generate job posting PDF if not exists
    job_pdf = test_data_dir / "job_posting_sample.pdf"
    if not job_pdf.exists():
        try:
            c = canvas_module.Canvas(str(job_pdf), pagesize=letter)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, 750, "Python Developer - Job Posting")
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, 720, "TechVentures Inc.")
            c.setFont("Helvetica", 10)
            c.drawString(70, 700, "Position: Senior Python Developer")
            c.drawString(70, 685, "Location: New York, NY (Remote)")
            c.drawString(70, 670, "Salary: $120,000 - $150,000")
            c.drawString(50, 650, "Looking for Python developer with 3+ years experience")
            c.save()
        except Exception as e:
            print(f"Warning: Failed to generate job posting PDF: {e}")
