# Development Setup Guide

This guide walks you through setting up your development environment for VedaAide.

## Prerequisites

- Python 3.9 or higher
- Poetry (dependency management)
- Git
- Make (optional but recommended)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd VedaAide.py
```

### 2. Install Poetry

If you don't have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or for Windows PowerShell:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Verify installation:
```bash
poetry --version
```

### 3. Install Project Dependencies

```bash
poetry install
```

This will:
- Create a virtual environment
- Install all dependencies listed in `pyproject.toml`
- Install development tools (black, pylint, mypy, pytest, etc.)

### 4. (Optional) Set up Pre-commit Hooks

To automatically check code quality before committing:

```bash
make pre-commit
# or manually:
poetry run pre-commit install
```

## Development Workflow

### Running Code Quality Checks

```bash
# Run all checks (format + lint + type-check + test)
make verify

# Or run individually:
make format       # Auto-format code (black + isort)
make lint         # Check code style (pylint)
make type-check   # Check types (mypy)
make test         # Run tests with coverage
```

### Writing Code

1. **Create a new branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Write your code** following [Python Coding Standards](.github/instructions/coding-standards.instructions.md)

3. **Format your code**:
   ```bash
   make format
   ```

4. **Check code quality before committing**:
   ```bash
   make verify
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add my feature"
   ```

6. **Push and create a Pull Request**:
   ```bash
   git push origin feature/my-feature
   ```

## Project Structure

```
VedaAide.py/
├── src/                          # Source code
│   └── core/
│       ├── data/                 # Data loading modules
│       └── retrieval/            # Retrieval and deidentification
├── scripts/                      # Utility scripts
│   └── data/                     # Data generation scripts
├── tests/                        # Test suite
│   └── unit/
├── docs/                         # Documentation
│   ├── guides/
│   ├── planning/
│   └── architecture/
├── infra/                        # Infrastructure configs
├── .github/                      # GitHub configuration
│   ├── instructions/             # Development instructions
│   ├── skills/                   # Reusable skills
│   └── workflows/                # CI/CD workflows
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
└── README.md                    # Project README
```

## Common Tasks

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/unit/test_deidentification.py

# Run with coverage report
poetry run pytest --cov=src

# Run tests in watch mode (requires pytest-watch)
poetry run ptw
```

### Type Checking

```bash
# Check type hints for src/
poetry run mypy src

# Check specific file
poetry run mypy src/core/retrieval/deidentifier.py
```

### Code Formatting

```bash
# Format all Python files
make format

# Format specific files
poetry run black src/core/data/
poetry run isort src/core/data/
```

### Running Data Generation Scripts

```bash
# Run demo generation (basic example)
poetry run python scripts/data/demo_generation.py

# Run with advanced configurations
poetry run python -m scripts.data.advanced_generator --help
```

## Coding Standards

### Type Hints (Mandatory)

All functions must have complete type hints:

```python
# ✅ Good
def retrieve_documents(query: str, top_k: int = 5) -> List[Document]:
    """Retrieve top-k documents matching query."""
    ...

# ❌ Bad
def retrieve_documents(query, top_k=5):
    ...
```

### Docstrings (Google Style, Mandatory)

All public functions and classes must have docstrings:

```python
def process_resume(resume_data: Dict[str, Any]) -> Resume:
    """Process and validate resume data.
    
    Args:
        resume_data: Raw resume data dictionary.
    
    Returns:
        Processed Resume object.
    
    Raises:
        ValueError: If resume data is invalid.
    """
    ...
```

### File Size

- Target: **< 200 lines per file**
- Maximum: **300 lines per file**
- Must split if exceeding 300 lines

See [Coding Standards](../.github/instructions/coding-standards.instructions.md) for complete guidelines.

## Troubleshooting

### Python Not Found in Bash (Windows)

If you get "Python was not found" error in Git Bash:

```bash
# Use Poetry to run Python
poetry run python --version

# Or use full path
/c/Program\ Files/Python311/python --version
```

See [Windows Dev Setup](.github/instructions/windows-dev-setup.instructions.md) for details.

### Virtual Environment Issues

```bash
# Recreate virtual environment
poetry env remove python3.11
poetry install

# Show current environment
poetry env info
```

### Poetry Lock Issues

```bash
# Update lock file
poetry lock --no-update

# Rebuild lock file from scratch
poetry lock --no-cache
```

## Editor Configuration

### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort
- autoDocstring

Create `.vscode/settings.json`:
```json
{
    "python.linting.pylintEnabled": true,
    "python.linting.pylintPath": "${workspaceFolder}/.venv/bin/pylint",
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [100],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

### PyCharm

1. Settings → Project → Python Interpreter
2. Select Poetry interpreter
3. Settings → Editor → Code Style → Python
   - Line length: 100
   - Tab size: 4

## Getting Help

- Check [Coding Standards](.github/instructions/coding-standards.instructions.md)
- Review existing tests in `tests/` for examples
- Check project documentation in `docs/`
- Ask in project discussions or issues

## Next Steps

After setup, consider:

1. Read [Project Context](.github/instructions/project-context.instructions.md)
2. Review [Coding Standards](.github/instructions/coding-standards.instructions.md)
3. Explore existing code in `src/`
4. Run the demo script: `poetry run python scripts/data/demo_generation.py`
5. Run tests: `make test`
