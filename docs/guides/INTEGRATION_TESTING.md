# Integration Testing Architecture for VedaAide

## Overview

VedaAide implements a comprehensive integration testing strategy that clearly separates **unit tests** (mocked dependencies) from **integration tests** (real services/data).

### Why Separate Unit and Integration Tests?

| Aspect | Unit Tests | Integration Tests |
|--------|-----------|-------------------|
| **Purpose** | Verify logic in isolation | Verify system components work together |
| **Dependencies** | All mocked | Real services/data |
| **Execution Time** | Fast (~100ms per test) | Slower (~1-5s per test) |
| **CI/CD** | Always run | Conditional on service availability |
| **Value** | High (catches bugs early) | Critical (ensures real-world functionality) |

**Anti-pattern to avoid**: Fully mocked integration tests lose all integration value while adding test maintenance burden.

## Directory Structure

```
tests/
├── unit/                                    # Mocked unit tests
│   ├── test_indexer.py                     # DocumentIndexer unit tests
│   ├── test_deidentification.py            # Deidentification unit tests
│   └── ...
├── integration/                            # Real service integration tests
│   ├── conftest.py                         # Fixtures and pytest config
│   ├── test_data/                          # Real test data
│   │   ├── resumes.json                    # Sample resumes
│   │   └── job_postings.json               # Sample job postings
│   ├── core/
│   │   └── retrieval/
│   │       └── test_document_loader_and_indexer.py  # 19 integration tests
│   └── ...
└── common/
    └── check_dependencies.py               # Reusable dependency checking
```

## Unit Tests: With Mocks

Located in `tests/unit/`, these tests mock all external dependencies:

```python
# tests/unit/test_indexer.py
@patch("src.core.retrieval.document_indexer.QdrantClient")
@patch("src.core.retrieval.document_indexer.embed_and_index")
def test_indexing_with_mocks(mock_embed, mock_qdrant):
    """Unit test: verify indexing logic in isolation"""

    indexer = DocumentIndexer(collection_name="test_vedaaide_unit")

    # All external calls are mocked
    indexer.embed_and_index(documents=[...])

    # Verify mocks were called correctly
    mock_embed.assert_called_once()
```

**Benefits**:
- ✅ Fast execution (~50ms)
- ✅ No external service dependencies
- ✅ Deterministic results
- ✅ Good for CI/CD

**Limitations**:
- ❌ Doesn't test real Qdrant integration
- ❌ Doesn't catch real embedding failures
- ❌ May miss data type mismatches

## Integration Tests: With Real Services

Located in `tests/integration/`, these tests use real services:

```python
# tests/integration/core/retrieval/test_document_loader_and_indexer.py
@pytest.mark.integration
@pytest.mark.requires_qdrant
def test_full_indexing_pipeline(isolated_indexer, test_data_dir):
    """Integration test: verify end-to-end indexing works"""

    # Load REAL data
    documents = DocumentLoader().load_from_directory(
        directory=test_data_dir / "resumes.json"
    )

    # Index into REAL Qdrant
    indexed_docs = isolated_indexer.index_documents(documents)

    # Verify real results
    assert len(indexed_docs) == 3
    collection_stats = isolated_indexer.get_collection_stats()
    assert collection_stats.vector_count > 0
```

**Benefits**:
- ✅ Tests real embedding quality
- ✅ Tests real Qdrant operations
- ✅ Catches data type mismatches
- ✅ Ensures end-to-end workflows

**Tradeoffs**:
- ⏱️ Slower execution (~2-5s per test)
- 🔗 Requires Qdrant service running
- 🔄 May have intermittent failures

## Collection Isolation Pattern

### Problem: Preventing Test Interference

Multiple concurrent tests could:
1. Use the same Collection name → data corruption
2. Leave behind stale Collections → cleanup overhead
3. Interfere with production data → disaster

### Solution: Unique, Isolated Collections

#### 1. Generate Unique Collection Names

```python
# tests/integration/conftest.py
@pytest.fixture
def isolated_collection_name() -> str:
    """Generate isolated collection: test_vedaaide_{uuid}"""
    unique_id = str(uuid.uuid4())[:8]
    return f"test_vedaaide_{unique_id}"
```

**Format**: `test_vedaaide_a1b2c3d4`

| Part | Example | Purpose |
|------|---------|---------|
| Prefix | `test_vedaaide_` | Identify as automated test collection |
| UUID | `a1b2c3d4` | Ensure uniqueness for each test run |

#### 2. Automatic Cleanup

```python
@pytest.fixture
def isolated_indexer(isolated_collection_name):
    """Provide isolated indexer with auto cleanup"""
    indexer = DocumentIndexer(collection_name=isolated_collection_name)

    # Cleanup BEFORE test
    try:
        indexer._delete_collection()
    except:
        pass  # Collection may not exist yet

    yield indexer  # Test runs here

    # Cleanup AFTER test
    try:
        indexer._delete_collection()
    except:
        pass  # May fail if service down, that's ok
```

**Cleanup Timing**:
- **Before**: Ensure clean slate
- **After**: Prevent test data pollution

### Naming Convention Examples

```
Production:
  vedaaide_docs              ← Real production collection

Development:
  vedaaide_dev              ← Manual testing collection

Automated Tests:
  test_vedaaide_a1b2c3d4    ← Test run 1
  test_vedaaide_e5f6g7h8    ← Test run 2
  test_vedaaide_i9j0k1l2    ← Test run 3 (concurrent)
```

## Dependency Checking

### Problem: Gracefully Handle Missing Services

Tests should skip if required services aren't available, rather than fail:

```python
# ❌ Bad: Hard failure
def test_indexing():
    client = QdrantClient(url="http://localhost:6333")
    # → ConnectionError if Qdrant not running

# ✅ Good: Graceful skip
@pytest.mark.requires_qdrant
def test_indexing(isolated_indexer):
    # → Automatically skipped if Qdrant not available
```

### Implementation

```python
# tests/common/check_dependencies.py
class DependencyError(Exception):
    """Raised when a service is unavailable"""
    pass

def check_qdrant_availability(url: str = "http://localhost:6333",
                             timeout: int = 2) -> bool:
    """Check if Qdrant is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except:
        return False
```

### pytest Configuration

```python
# tests/integration/conftest.py
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "requires_qdrant: mark test as requiring Qdrant service"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
```

### Usage

```bash
# Skip if Qdrant not available
poetry run pytest tests/integration/ -m requires_qdrant

# Run only integration tests
poetry run pytest tests/ -m integration

# Show skipped tests
poetry run pytest tests/ -v | grep SKIPPED
```

## Test Data Organization

```
tests/integration/test_data/
├── resumes.json                    # 3 realistic sample resumes
├── job_postings.json               # 3 realistic sample jobs
└── README.md                       # Data source documentation
```

### Sample Data Format

**resumes.json**:
```json
{
  "id": "resume_001",
  "name": "John Doe",
  "content": "...",
  "metadata": {
    "source": "test_data",
    "format": "json"
  }
}
```

**job_postings.json**:
```json
{
  "id": "job_001",
  "title": "Software Engineer",
  "content": "...",
  "metadata": {
    "source": "test_data",
    "format": "json"
  }
}
```

## Pytest Markers

```python
@pytest.mark.integration           # Integration test (real services)
@pytest.mark.requires_qdrant       # Requires Qdrant service
@pytest.mark.requires_ollama       # Requires Ollama service
@pytest.mark.requires_azure_openai # Requires Azure OpenAI credentials
```

### Running Tests by Marker

```bash
# All integration tests
poetry run pytest -m integration

# Only Qdrant integration tests
poetry run pytest -m "integration and requires_qdrant"

# Exclude integration tests
poetry run pytest -m "not integration"

# Show available markers
poetry run pytest --markers
```

## Current Test Suite Status

### Test Counts

| Category | Count | Status |
|----------|-------|--------|
| Unit Tests | 81 | ✅ 81 passing |
| Integration Tests | 19 | ✅ 19 passing |
| Total | 100 | ✅ All passing |
| Skipped | 4 | ⏭️ Missing services |

### Code Coverage

```
src/core/
├── data/
│   ├── deidentifier.py          87%  ✅ Good
│   ├── document_loader.py       64%  ✅ Acceptable
│   └── document_record.py       45%  ⚠️ Needs more tests
└── retrieval/
    └── document_indexer.py      84%  ✅ Good

Overall: 58% code coverage
```

## Best Practices

### ✅ DO

1. **Use `isolated_indexer` fixture** for Qdrant operations:
   ```python
   def test_indexing(isolated_indexer):  # ✅ Correct
       collection_name = isolated_indexer.collection_name
   ```

2. **Load real data** in integration tests:
   ```python
   @pytest.mark.requires_qdrant
   def test_document_loading(test_data_dir):
       loader = DocumentLoader()
       docs = loader.load_from_directory(test_data_dir)  # ✅ Real files
   ```

3. **Mark tests appropriately**:
   ```python
   @pytest.mark.integration
   @pytest.mark.requires_qdrant
   def test_indexing():  # ✅ Clear intent
       pass
   ```

4. **Check results against real expectations**:
   ```python
   stats = indexer.get_collection_stats()
   assert stats.vector_count > 0  # ✅ Verify real output
   ```

### ❌ DON'T

1. **Mix unit and integration tests**:
   ```python
   # ❌ Wrong: Mocks in integration test
   @pytest.mark.integration
   @patch("QdrantClient")
   def test_indexing(mock_client):
       pass
   ```

2. **Use hardcoded Collection names**:
   ```python
   # ❌ Wrong: Test collision
   def test_first(isolated_indexer):
       indexer = DocumentIndexer(collection_name="test_vedaaide_fixed")

   def test_second(isolated_indexer):
       indexer = DocumentIndexer(collection_name="test_vedaaide_fixed")
       # Same collection name → interference
   ```

3. **Skip cleanup**:
   ```python
   # ❌ Wrong: Collection pollution
   @pytest.fixture
   def my_indexer():
       indexer = DocumentIndexer(collection_name="test")
       yield indexer
       # No cleanup → leftovers
   ```

4. **Load fake/mock data**:
   ```python
   # ❌ Wrong: Loses integration value
   @pytest.mark.integration
   @patch("DocumentLoader")
   def test_indexing(mock_loader):
       mock_loader.return_value = [MagicMock()]  # Fake data
   ```

## Troubleshooting

### Issue: "Qdrant is not available"

```bash
# Start Qdrant via Docker Compose
docker-compose up -d qdrant

# Verify it's running
curl http://localhost:6333/health

# Re-run tests
poetry run pytest tests/integration/
```

### Issue: "Collection already exists"

**Symptom**: `QdrantException: status code 400, ...collection_name...already exists`

**Cause**: Previous test didn't clean up properly

**Solution**:
```bash
# Delete orphaned collections manually
curl -X DELETE http://localhost:6333/collections/test_vedaaide_old

# Or run cleanup and retry
poetry run pytest tests/integration/ --cleanup-orphans
```

### Issue: Tests fail with timeout

**Cause**: Embedding service slow or unavailable

**Solution**:
```bash
# Use local Ollama instead of Azure OpenAI
export EMBEDDING_PROVIDER=ollama
poetry run pytest tests/integration/

# Or increase timeout
poetry run pytest tests/integration/ --timeout=30
```

## Next Steps

- 📊 Increase DocumentRecord coverage from 45% to 70%+
- 🧪 Add more real-world test scenarios (large datasets, PDF parsing)
- 🔄 Implement CI/CD with conditional integration test runs
- 📈 Add performance benchmarks for indexing operations
