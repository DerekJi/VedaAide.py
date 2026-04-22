---
applyTo: "tests/**"
---

# Testing Standards (Mandatory)

## Test Pyramid Proportions

| Level | Proportion | Characteristics |
|------|------|------|
| Unit Tests | 60–80% | Individual functions/classes, mock all external dependencies |
| Integration Tests | 20–30% | Multi-module interactions, mock external services (LLM, DB) |
| E2E Tests | 5–10% | Complete business flow, real services |

## Coverage Goals (Mandatory)

```
src/core/agent/         ≥ 85%
src/core/retrieval/     ≥ 90%  ← Critical module, highest requirement
src/core/rag/           ≥ 80%
src/core/evaluation/    ≥ 75%
src/infrastructure/     ≥ 60%  ← Depends on external services, lower requirement
src/utils/              ≥ 80%
```

## AAA Pattern (Mandatory)

All test functions must follow the Arrange / Act / Assert three-section structure, with clear annotations:

```python
def test_deidentifier_masks_ssn():
    # Arrange
    deidentifier = Deidentifier()
    text = "SSN 123-45-6789"

    # Act
    result = deidentifier.deidentify(text, rules=["ssn"])

    # Assert
    assert "[REDACTED]" in result
    assert "123-45-6789" not in result
```

## Mocking Standards

- Unit Tests: **must** mock all external dependencies (LLM, Qdrant, CosmosDB)
- Integration Tests: can mock LLM, databases can use local instances
- E2E Tests: use real services, mark with `@pytest.mark.e2e`

```python
# ✅ Correct — inject mock via constructor
mock_llm = Mock()
mock_llm.generate.return_value = "mock response"
agent = Agent(llm=mock_llm, retriever=mock_retriever)
```

## Naming Convention

- Files: `test_<module>.py`
- Classes: `class TestXxx:`
- Functions: `def test_<action>_<scenario>():` — clearly describe tested behavior and scenario

## Marking Slow Tests

```python
@pytest.mark.slow
@pytest.mark.e2e
def test_complete_interview_flow(): ...
```

In CI: run `pytest -m "not slow"` to skip slow tests.

## Fixture Reuse

Put shared fixtures in `tests/conftest.py`; do not redefine identical fixtures in multiple test files.

## Command Reference

```bash
# Run only unit tests (daily development)
poetry run pytest tests/unit/ -v

# With coverage report
poetry run pytest tests/ --cov=src/ --cov-report=term-missing

# Parallel execution for speed
poetry run pytest -n auto tests/
```
