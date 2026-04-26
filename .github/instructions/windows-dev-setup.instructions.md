---
applyTo: "**"
---

# Windows Development Environment Setup

## Problem: Python Not Found in Bash

### Symptom
When running Python in Windows bash (Git Bash/MSYS2), you get this error:
```
Python was not found; run without arguments to install from the Microsoft Store,
or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

### Root Causes
1. **Windows App Aliases**: Windows 10/11 intercepts Python shortcuts by default
2. **PATH mismatch**: Bash PATH differs from Windows CMD PATH
3. **Installation location**: Python on Windows is in `C:\Program Files\PythonXXX\`, not Unix standard locations

## Solution: Use Full Python Path

### Quick Fix (Recommended for CI/CD and Scripts)

```bash
# Find installed Python
which python || which python3 || ls /c/Program\ Files/Python*/python.exe 2>/dev/null | head -1

# Use full path for Python scripts
/c/Program\ Files/Python313/python << 'EOPY'
print("Hello from Python")
EOPY

# Use full path for Python files
/c/Program\ Files/Python313/python script.py
```

### Python Version Mapping

| Version | Path |
|---------|------|
| Python 3.13 | `/c/Program Files/Python313/python` |
| Python 3.12 | `/c/Program Files/Python312/python` |
| Python 3.11 | `/c/Program Files/Python311/python` |
| Python 3.10 | `/c/Program Files/Python310/python` |

**Note**: Replace `313` with your installed version number.

## Permanent Solutions

### Option 1: Disable Windows App Aliases (Administrator)

1. Open Settings → Apps → App execution aliases
2. Find `python.exe` and `python3.exe`
3. Toggle OFF both switches
4. Restart bash environment

### Option 2: Add Python to PATH

1. Windows Settings → Environment Variables
2. Click "Edit system environment variables"
3. Add `C:\Program Files\Python313` to PATH
4. Restart all terminals

### Option 3: Configure Git Bash Profile

Add to `~/.bash_profile` or `~/.bashrc`:

```bash
export PATH="/c/Program Files/Python313:$PATH"
```

## Best Practice: Use Poetry (Recommended)

Since this project uses Poetry for dependency management, use these commands:

```bash
# ✅ Recommended: Use Poetry runner
poetry run python script.py
poetry run pytest tests/

# ✅ Alternative: Enter virtual environment
poetry shell
python script.py
pytest tests/
```

Poetry automatically handles Python path resolution within the project's virtual environment.

## Verification Checklist

```bash
# Check Python version directly
/c/Program\ Files/Python313/python --version

# Check via Poetry
poetry show

# Check PATH
echo $PATH | grep -i python || echo "Python not in PATH"
```

## Temporary Alias (Current Session Only)

```bash
alias python='/c/Program\ Files/Python313/python'
alias python3='/c/Program\ Files/Python313/python'
```

To make permanent, add to `~/.bashrc` or `~/.bash_profile`.

## For VedaAide Development

**Recommended workflow:**

```bash
# Clone and setup
git clone <repo>
cd VedaAide.py
poetry install

# Run development tasks
poetry run python -m pytest tests/
poetry run python scripts/some_script.py
poetry run ruff check src/

# Or activate environment
poetry shell
python -m pytest tests/
```

This ensures you always use the correct Python version defined in `pyproject.toml`.
