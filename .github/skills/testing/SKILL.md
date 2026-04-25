---
name: testing
description: Comprehensive testing framework for VedaAide, including unit tests, integration tests, E2E tests with pytest, mocking patterns, and RAGAS evaluation integration
applyTo: "tests/**"
keywords:
  - test
  - unit
  - integration
  - e2e
  - benchmark
  - ragas
  - pytest
  - mock
  - coverage
  - 测试
  - 单元测试
  - 集成测试
  - E2E
  - 基准测试
  - 测试覆盖率
  - 测试金字塔
whenToUse: |
  When writing:
  - Unit tests for core business logic
  - Integration tests for multi-component interactions
  - End-to-end tests for complete workflows
  - Mock setups for external dependencies
  - Parameterized and fixture-based tests
---

# VedaAide Testing Strategy

## Test Pyramid

```
           🎯 E2E Tests (End-to-End)
              ▲ 5-10%
             ╱ ╲
            ╱   ╲ - Complete business flow
           ╱     ╲ - Depends on real services
          ╱       ╲ - Slow but accurate
         ╱─────────╲
        ╱ Integration Tests ╲
       ▲       ▲ 20-30%
      ╱ ╲     ╱ ╲
     ╱   ╲   ╱   ╲ - Multiple module interactions
    ╱     ╲ ╱     ╲ - Mock external services
   ╱       ╱       ╲ - Medium speed
  ╱       ╱ Unit Tests ╲
 ▲▲▲▲▲▲▲▲▲ 60-80%
  - Single function/class
  - Mock all dependencies
  - Fast feedback
```

## Unit Tests

### Coverage Range

- **✅ Must**: Business logic, calculation functions, algorithms
- **✅ Important**: Data transformation, validation rules
- **⚠️ Optional**: Database drivers, API clients (use Mock)

### AAA Pattern

```python
def test_deidentifier_masks_ssn():
    """SSN should be correctly masked."""
    # Arrange
    deidentifier = Deidentifier()
    text = "John Doe, SSN 123-45-6789"

    # Act
    result = deidentifier.deidentify(text, rules=["ssn"])

    # Assert
    assert "[REDACTED]" in result
    assert "123-45-6789" not in result
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

def test_agent_calls_llm_with_correct_context():
    """Agent should call LLM with correct context."""
    # Mock LLM
    mock_llm = Mock()
    mock_llm.generate.return_value = "I have 5 years of Kubernetes experience"

    # Mock Retriever
    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = [
        Document(text="Kubernetes deployment experience", score=0.95)
    ]

    # Create Agent
    agent = Agent(llm=mock_llm, retriever=mock_retriever)

    # Execute
    response = agent.query("Tell me about your experience")

    # Verify
    mock_llm.generate.assert_called_once()
    call_args = mock_llm.generate.call_args
    assert "Kubernetes" in str(call_args)
```

### Using Fixtures

```python
import pytest

@pytest.fixture
def sample_documents():
    """Return sample documents."""
    return [
        Document(text="Python experience", metadata={"tech": "Python"}),
        Document(text="Kubernetes deployment", metadata={"tech": "Kubernetes"}),
    ]

@pytest.fixture
def mock_embedding_model():
    """Return Mock Embedding model."""
    mock = Mock()
    mock.embed.return_value = np.random.random(1536)
    return mock

def test_retriever_with_sample_docs(sample_documents, mock_embedding_model):
    """Test retriever with sample documents."""
    retriever = Retriever(embedding_model=mock_embedding_model)
    results = retriever.retrieve("Python", docs=sample_documents)
    assert len(results) > 0
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input_text,expected_masked", [
    ("SSN 123-45-6789", "[REDACTED]"),
    ("Email john@example.com", "[REDACTED]"),
    ("Phone +1-555-1234", "[REDACTED]"),
])
def test_deidentifier_various_types(input_text, expected_masked):
    """Test masking of various types of sensitive information."""
    deidentifier = Deidentifier()
    result = deidentifier.deidentify(input_text)
    assert expected_masked in result
```

## Integration Tests

### Testing RAG Pipeline

```python
def test_rag_pipeline_end_to_end(qdrant_client, cosmosdb_client):
    """Complete RAG pipeline test (Mock LLM)."""
    # Prepare
    documents = [
        Document(text="Kubernetes experience with 5 years"),
        Document(text="Docker containerization expertise"),
    ]

    # Index documents to Qdrant
    indexer = Indexer(qdrant_client)
    indexer.index_documents(documents)

    # Create Retriever
    retriever = Retriever(qdrant_client)

    # Mock LLM
    mock_llm = Mock()
    mock_llm.generate.return_value = "5 years of Kubernetes"

    # Create RAG Pipeline
    pipeline = RAGPipeline(retriever=retriever, llm=mock_llm)

    # Execute query
    response = pipeline.query("How much Kubernetes experience do you have?")

    # Verify
    assert "Kubernetes" in response or "5 years" in response

    # Verify data persisted to CosmosDB
    persistence = cosmosdb_client.query_by_query_text("Kubernetes")
    assert len(persistence) > 0
```

### Testing Data Persistence

```python
def test_retrieval_persistence_to_cosmosdb(cosmosdb_client):
    """Retrieved data should be persisted to CosmosDB."""
    # Execute retrieval
    query = "experience with databases"
    retriever = Retriever(...)
    contexts = retriever.retrieve(query)

    # Save to CosmosDB
    persistence_handler = PersistenceHandler(cosmosdb_client)
    persistence_handler.save_retrieval(
        query=query,
        contexts=contexts,
        scores=[0.95, 0.87]
    )

    # Verify saved
    saved = cosmosdb_client.query_by_id(...)
    assert saved["query"] == query
    assert len(saved["contexts"]) == len(contexts)
```

## End-to-End Tests (E2E)

### Complete Interview Flow

```python
@pytest.mark.e2e
def test_complete_interview_flow():
    """Complete interview flow (using real services)."""
    # Initialize all services
    qdrant_client = QdrantClient(url="http://localhost:6333")
    cosmosdb_client = CosmosDBClient(...)
    llm = AzureOpenAI(...)  # real LLM

    # Create Agent
    agent = Agent(
```
