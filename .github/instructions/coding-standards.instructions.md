---
applyTo: "src/**/*.py,tests/**/*.py"
---

# Python Coding Standards (Mandatory)

## Formatting

- Line length limit: **100 characters**
- Indentation: 4 spaces
- Formatter: `black`; import sorting: `isort`

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

## Module Size

- Target: < 300 lines; limit: 500 lines
- Must split modules if exceeding limit

## Pre-PR Checklist

Before submitting, confirm:
- [ ] All functions have type hints
- [ ] All public methods have Docstrings
- [ ] No `print()` statements (use logger)
- [ ] No hardcoded keys or configs
- [ ] `black src/ && isort src/ && pylint src/ && mypy src/` all pass
- [ ] Unit test coverage ≥ 80%
