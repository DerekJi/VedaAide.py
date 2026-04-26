# VedaAide Coding Standards

## Python Style Guide

### PEP 8 Compliance
- **Line length limit: 100 characters** (not 79)
  - PEP 8's 79-character limit is legacy (Python 2.7 era for old terminal widths)
  - Modern standard: 88-120 characters (we use: 100 via Ruff)
  - Configured in: `pyproject.toml` (Ruff)
- Indentation: 4 spaces
- Naming:
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: `_leading_underscore`

### Type Hints (Mandatory)
```python
# ✅ Correct
def retrieve_documents(query: str, top_k: int = 5) -> List[Document]:
    """Retrieve relevant documents.

    Args:
        query: Search query string
        top_k: Number of results to return

    Returns:
        List of relevant documents
    """
    pass

# ❌ Incorrect
def retrieve_documents(query, top_k=5):
    pass
```

### Docstring Format (Google Style)
```python
def process_query(query: str, deidentify: bool = True) -> Dict[str, Any]:
    """Process user query.

    This function validates and processes user queries, optionally
    applying deidentification rules.

    Args:
        query: The user's input query string
        deidentify: Whether to apply deidentification rules

    Returns:
        A dictionary containing processed query and metadata:
        - 'cleaned_query': str
        - 'entities': List[str]
        - 'intent': str

    Raises:
        ValueError: If query is empty or too long
        DeidentificationError: If deidentification fails

    Example:
        >>> result = process_query("What is Kafka?")
        >>> print(result['intent'])
        'technical_question'
    """
    pass
```

## Module Organization

### Import Sorting
```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Third-party libraries
import numpy as np
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

# Local imports
from src.core.agent import AgentStateManager
from src.infrastructure.db import CosmosDBClient
from src.utils.config import ConfigManager
```

### Module Size
- **Target**: < 300 lines (max 500 lines)
- **Large file refactoring**: Split into multiple modules

### Class Organization
```python
class MyClass:
    """Class description."""

    # Class constants
    DEFAULT_VALUE = 100

    def __init__(self, param: str):
        """Initialize."""
        self._param = param

    # Public methods (grouped by logic)
    def public_method1(self) -> str:
        """Public method 1."""
        return self._private_helper()

    # Private methods
    def _private_helper(self) -> str:
        """Private helper method."""
        pass
```

## Error Handling

### Use Custom Exceptions
```python
# ✅ Correct
class RetrievalError(Exception):
    """Raised when retrieval fails."""
    pass

try:
    documents = retriever.retrieve(query)
except QdrantException as e:
    logger.error(f"Qdrant retrieval failed: {e}")
    raise RetrievalError(f"Failed to retrieve: {str(e)}") from e

# ❌ Avoid
except Exception as e:
    pass  # Too broad
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

# ✅ Correct
logger.info(f"Starting evaluation with {num_samples} samples")
logger.error(f"Retrieval failed for query: {query}", exc_info=True)
logger.debug(f"Retrieved {len(docs)} documents, scores: {scores}")

# ❌ Avoid
print("Starting evaluation...")  # Use logger instead
logger.error("Error!")  # Insufficient information
```

## Testing Standards

### Test Naming
```python
# Test files
test_retriever.py  # ✅
retriever_test.py  # ⚠️ OK, but not recommended

# Test classes
class TestRetriever:  # ✅
    pass

# Test functions
def test_retrieve_with_empty_query():  # ✅
    pass

def test_retrieve_returns_top_k_results():  # ✅
    pass
```

### AAA Pattern
```python
def test_retrieve_returns_top_k_results():
    """Test that retriever returns exactly top_k results."""
    # Arrange - Prepare test data
    query = "What is RAG?"
    top_k = 5
    retriever = create_test_retriever()

    # Act - Execute the operation being tested
    results = retriever.retrieve(query, top_k=top_k)

    # Assert - Verify results
    assert len(results) == top_k
    assert all(doc.score > 0 for doc in results)
```

### Mocking
```python
from unittest.mock import Mock, patch

def test_agent_calls_llm():
    """Test that agent calls LLM with correct prompt."""
    # Mock external dependencies
    mock_llm = Mock()
    mock_llm.generate.return_value = "mock response"

    # Create agent (inject mock)
    agent = Agent(llm=mock_llm)

    # Execute
    response = agent.query("test query")

    # Verify LLM was called correctly
    mock_llm.generate.assert_called_once()
    args, kwargs = mock_llm.generate.call_args
    assert "test query" in str(args)
```

## Dependency Injection

### Avoid Hardcoding
```python
# ❌ Bad - Hardcoded dependencies
class Agent:
    def __init__(self):
        self.llm = AzureOpenAI(api_key="...")  # Hardcoded
        self.retriever = QdrantRetriever(...)  # Hardcoded

# ✅ Good - Injected dependencies
class Agent:
    def __init__(self, llm: LLMProvider, retriever: Retriever):
        self.llm = llm
        self.retriever = retriever

# Usage
llm = AzureOpenAI.from_config()
retriever = QdrantRetriever.from_config()
agent = Agent(llm=llm, retriever=retriever)
```

## Configuration Management

### Use ConfigManager
```python
# ❌ Bad
api_key = os.getenv("AZURE_OPENAI_API_KEY")
base_url = os.getenv("AZURE_OPENAI_BASE_URL")

# ✅ Good
config = ConfigManager()
api_key = config.get("azure_openai.api_key")
base_url = config.get("azure_openai.base_url")
```

## Async Programming

### Use async/await
```python
# ✅ Recommended - Async I/O
async def retrieve_async(query: str) -> List[Document]:
    documents = await self.retriever.retrieve(query)
    return documents

# 使用
import asyncio
results = asyncio.run(retrieve_async("query"))

# ❌ 避免
def retrieve_blocking(query: str) -> List[Document]:
    # 阻塞 I/O
    pass
```

## Performance and Caching

### Use Caching to Avoid Repeated Computation
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_embedding(text: str) -> np.ndarray:
    """Cache embedding computation results."""
    return embedder.embed(text)

# Can also use Redis caching
from src.infrastructure.cache import redis_cache

@redis_cache(ttl=3600)
async def get_cached_results(query: str):
    return await expensive_operation(query)
```

## Code Review Checklist

Before submitting a PR, self-check:

- [ ] All functions have type hints
- [ ] All public methods have Docstrings
- [ ] Unit test coverage ≥ 80%
- [ ] Code formatted and linted with Ruff (`ruff check` and `ruff format`)
- [ ] Type hints validated with mypy
- [ ] No print statements (use logger)
- [ ] No hardcoded keys or configs
- [ ] Error handling is complete (try-except-finally)
- [ ] No TODO comments (or tracked by GitHub issue)
- [ ] Code logic is clear, comments where necessary

## Toolchain

### Code Quality with Ruff
```bash
# Check code for linting issues
poetry run ruff check src/ tests/

# Auto-fix linting issues
poetry run ruff check --fix src/ tests/

# Format code
poetry run ruff format src/ tests/

# Check formatting without modifying
poetry run ruff format --check src/ tests/

# Combined: lint + format check
poetry run ruff check src/ tests/ && poetry run ruff format --check src/ tests/
```

### Type Checking
```bash
# MyPy - Type checking
poetry run mypy src/
```

### Testing
```bash
# Run all tests
poetry run pytest tests/

# Generate coverage report
poetry run pytest tests/ --cov=src/ --cov-report=html

# Run specific test
poetry run pytest tests/unit/test_retriever.py -v
```

## Common Errors

| Error | Cause | Fix |
|------|------|------|
| `NameError: name 'X' is not defined` | Missing import or variable name error | Check import, use IDE autocomplete |
| `TypeError: X() takes N args` | Function argument count error | Check function signature and call |
| `KeyError: 'X'` | Dictionary key doesn't exist | Use `.get()` or check with `in` first |
| `AttributeError: 'X' has no attribute 'Y'` | Attribute doesn't exist | Check object type, use type hints |
| Circular import | A imports B, B imports A | Refactor module structure or use lazy import |

## Reference Resources

- [PEP 8 - Python Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
