---
applyTo: "src/**/*.py,tests/**/*.py"
---

# Python Coding Standards (Mandatory)

## Formatting

- Line length limit: **100 characters**
- Indentation: 4 spaces
- Formatter and import sorting: `ruff format` + `ruff check`

## Naming Convention

| Context | Standard |
|------|------|
| Classes | `PascalCase` |
| Functions, variables | `snake_case` |
| Constants | `UPPER_SNAKE_CASE` |
| Private members | `_leading_underscore` |
| Test files | `test_*.py` |
| Test classes | `class TestXxx:` |
| Test functions | `def test_<action>_<scenario>():` |

## Type Hints (Mandatory)

All functions and methods must have complete parameter type hints and return value type hints. Code without type hints is not allowed to merge.

```python
# ✅ Correct
def retrieve_documents(query: str, top_k: int = 5) -> List[Document]: ...

# ❌ Prohibited
def retrieve_documents(query, top_k=5): ...
```

## Docstring (Google Style, Mandatory)

All public functions and classes must have Docstrings with `Args`, `Returns`, `Raises` (if applicable) sections.

## Import Order

```python
# 1. Standard library
import os
from pathlib import Path
from typing import Dict, List, Optional

# 2. Third-party libraries
import numpy as np
from langchain.chat_models import ChatOpenAI

# 3. Local modules
from src.core.agent import AgentStateManager
```

## Error Handling

- **Prohibit** naked `except Exception as e: pass`
- Use custom exceptions (inherit from project base class), catch specific exceptions then wrap and re-raise
- **Prohibit** using `print()`, uniformly use `logger = logging.getLogger(__name__)`

## Dependency Injection

Prohibit hardcoding instantiation of external services inside classes:

```python
# ❌ Prohibited
class Agent:
    def __init__(self):
        self.llm = AzureOpenAI(api_key="...")  # Hardcoded

# ✅ Correct
class Agent:
    def __init__(self, llm: LLMProvider, retriever: Retriever):
        self.llm = llm
        self.retriever = retriever
```

## Configuration Management

Prohibit directly reading environment variables; uniformly use `ConfigManager`:

```python
# ❌ Prohibited
api_key = os.getenv("AZURE_OPENAI_API_KEY")

# ✅ Correct
config = ConfigManager()
api_key = config.get("azure_openai.api_key")
```

## Async Programming

All I/O operations must use `async/await`; prohibit blocking calls in async context.

## Module Size and Organization

### File Size Guidelines

**Following SRP (Single Responsibility Principle)** — similar to enterprise patterns in .NET:

| Metric | Target | Maximum |
|--------|--------|---------|
| Lines per file | < 200 | 300 lines |
| Lines per class | < 150 | 250 lines |
| Lines per function | < 30 | 50 lines |

**Mandatory split if exceeding**: 300 lines per file

### Refactoring Strategy

When splitting modules, follow this pattern:

```
module/
├── __init__.py          # Package exports
├── base.py              # Abstract base classes, interfaces
├── models.py            # Data classes, domain models (~100 lines)
├── core.py              # Main logic/algorithms (~150 lines)
├── utils.py             # Helper functions (~80 lines)
├── exporter.py          # Output/serialization logic (~100 lines)
└── __main__.py          # CLI entry point (if applicable)
```

### Real-world Example: Data Generator Refactoring

**Before (single file, 480 lines):**
```
data_generator.py
  ├── DataRepository (static data)
  ├── ResumeRecord (model)
  ├── JobPostingRecord (model)
  ├── ResumeGenerator (logic)
  ├── JobPostingGenerator (logic)
  ├── DataExporter (output)
  └── main() (script)
```

**After (modular structure):**
```
generator/
├── __init__.py
├── models.py            # ResumeRecord, JobPostingRecord (~50 lines)
├── repository.py        # DataRepository (~100 lines)
├── resume.py            # ResumeGenerator (~150 lines)
├── job_posting.py       # JobPostingGenerator (~150 lines)
├── exporter.py          # DataExporter (~80 lines)
└── __main__.py          # main() script (~30 lines)
```

**Benefits:**
- ✅ Each file has single, clear responsibility
- ✅ Easy to test individual components
- ✅ Easier to reuse (e.g., import just `ResumeGenerator`)
- ✅ Easier to maintain and extend
- ✅ Follows Python package conventions

### Naming Conventions for Modules

```python
# ✅ Good module organization
src/
├── core/
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py              # LLMProvider (abstract)
│   │   ├── openai.py            # OpenAIProvider
│   │   └── azure.py             # AzureOpenAIProvider
│   └── retrieval/
│       ├── __init__.py
│       ├── models.py            # Document, SearchResult classes
│       ├── hybrid_search.py      # HybridSearchEngine
│       └── ranker.py            # ResultRanker
```

### Import Structure

```python
# src/core/llm/__init__.py
from .base import LLMProvider
from .openai import OpenAIProvider
from .azure import AzureOpenAIProvider

__all__ = ["LLMProvider", "OpenAIProvider", "AzureOpenAIProvider"]
```

This allows clean imports:
```python
from src.core.llm import OpenAIProvider  # ✅ Good
# Instead of:
from src.core.llm.openai import OpenAIProvider  # ❌ Couples to impl
```

## Code Quality Tools

### Automated Formatting and Linting

All code must pass these checks **before submission**:

```bash
make verify  # Runs all checks

# Or individually:
make format      # ruff format
make lint        # ruff check
make test        # pytest with coverage
```

### Development Workflow

1. **Before committing**: `make format` (auto-fixes issues)
2. **Before pushing**: `make verify` (catches all issues)
3. **Pre-commit hooks** automatically run on commit:
   ```bash
   pre-commit install  # Setup once
   ```

## Pre-PR Checklist

Before submitting pull request, confirm:

- [ ] All functions have complete type hints
- [ ] All public methods/classes have Google-style Docstrings
- [ ] No `print()` statements (use `logging` module)
- [ ] No hardcoded API keys or configs
- [ ] No `sys.path.insert()` (use proper package imports)
- [ ] File size: < 300 lines (split if needed)
- [ ] Class size: < 250 lines
- [ ] All checks pass: `make verify`
- [ ] Unit test coverage: ≥ 80%

### Running the Full Check Suite

```bash
# Automatic format + linting + type checking + tests
make verify

# Expected output:
# ✅ All quality checks passed!
```
