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
        llm=llm,
        retriever=Retriever(qdrant_client),
        persistence=PersistenceHandler(cosmosdb_client)
    )
    
    # Simulate interview conversation
    questions = [
        "Tell me about your Kubernetes experience",
        "What challenges did you face?",
        "How did you solve them?"
    ]
    
    responses = []
    for question in questions:
        response = agent.query(question)
        responses.append(response)
        assert len(response) > 10  # ensure meaningful response
    
    # Verify conversation coherence
    assert len(responses) == len(questions)
```

### Evaluation Flow

```python
@pytest.mark.e2e
def test_complete_evaluation_flow():
    """Complete evaluation flow (including RAGAS)."""
    # Prepare test set
    test_queries = [
        "What is your Kubernetes experience?",
        "Tell me about a cloud project",
    ]
    ground_truth_contexts = [
        ["Kubernetes document 1", "Kubernetes document 2"],
        ["Cloud project documentation"],
    ]
    
    # Run Agent to generate responses
    agent = create_test_agent()
    predictions = [
        agent.query(q) for q in test_queries
    ]
    
    # Run RAGAS evaluation
    results = evaluate(
        predictions=predictions,
        ground_truths=ground_truth_contexts,
        metrics=[Faithfulness(), Relevance(), Recall()]
    )
    
    # Verify evaluation scores
    assert results['faithfulness'] > 0.75
    assert results['relevance'] > 0.75
    assert results['recall'] > 0.70
```

## Performance Testing (Benchmarks)

### Retrieval Performance Benchmark

```python
import time

def bench_retrieval_latency(retriever, queries, num_iterations=10):
    """Retrieval latency benchmark test."""
    latencies = []
    
    for _ in range(num_iterations):
        for query in queries:
            start = time.time()
            results = retriever.retrieve(query)
            latencies.append(time.time() - start)
    
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    
    print(f"Average latency: {avg_latency*1000:.2f}ms")
    print(f"Max latency: {max_latency*1000:.2f}ms")
    
    assert avg_latency < 1.0, "Retrieval latency should be < 1 second"
```

### Evaluation Performance Benchmark

```python
def bench_evaluation_throughput():
    """Evaluation throughput benchmark test."""
    evaluator = RAGASEvaluator()
    predictions = ["answer 1"] * 100
    ground_truths = [["doc 1"]] * 100
    
    start = time.time()
    results = evaluator.evaluate_batch(predictions, ground_truths)
    elapsed = time.time() - start
    
    throughput = len(predictions) / elapsed
    print(f"Evaluation throughput: {throughput:.2f} samples/sec")
    
    assert throughput > 5, "Evaluation throughput should be > 5 samples/sec"
```

## Test Coverage

### Target Coverage

```
core/agent/         85%+
core/retrieval/     90%+  ← critical modules
core/rag/          80%+
core/evaluation/   75%+
infrastructure/    60%+  ← depends on external services
utils/            80%+
```

### Generate Coverage Report

```bash
# Run tests and generate coverage report
poetry run pytest tests/ \
  --cov=src/ \
  --cov-report=html \
  --cov-report=term-missing

# View report
open htmlcov/index.html
```

## Test Execution Speed Optimization

### Fast Feedback Loop

```bash
# Run only unit tests (fast)
poetry run pytest tests/unit/ -v

# Run specific test
poetry run pytest tests/unit/test_retriever.py::test_retrieve_basic -v

# Skip slow tests
poetry run pytest -m "not slow" tests/

# Run tests in parallel
poetry run pytest -n auto tests/
```

### Mark Slow Tests

```python
import pytest

@pytest.mark.slow
def test_evaluation_with_large_dataset():
    """Slow test requiring 10+ seconds."""
    pass

# Skip during run: pytest -m "not slow" tests/
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Fast check (2-3 minutes)
      - name: Unit tests
        run: poetry run pytest tests/unit/ --cov=src/
      
      # Integration tests (5-10 minutes)
      - name: Integration tests
        run: poetry run pytest tests/integration/
      
      # Upload coverage report
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Testing Best Practices

### ✅ Recommended

- Unit test every public function
- Use meaningful test names
- Each test should test one thing
- Mock external dependencies
- Use fixtures to share test data
- Run full test suite regularly

### ❌ Avoid

- Test interdependencies (tests should not depend on each other)
- Business logic in tests
- Using real external services (e.g., production databases)
- Ignoring edge cases
- Over-mocking (tests lose value)

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [RAGAS Documentation](https://ragas.io/)
- [Testing Pyramid Principle](https://martinfowler.com/articles/testPyramid.html)
