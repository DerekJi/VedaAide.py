# CI/CD Pipeline Documentation

## Overview

This document describes the GitHub Actions CI/CD pipeline for the VedaAide project. The pipeline automatically runs tests and code quality checks on every push to `main`/`develop` branches and on all pull requests.

## Workflow Configuration

### File Location
- `.github/workflows/ci.yml`

### Trigger Events

The pipeline is triggered on:
1. **Push to main/develop branches** - Automatically runs CI on every commit
2. **Pull Requests to main/develop** - Validates changes before merging

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

## Jobs Overview

### 1. Unit Tests (`test`)

**Purpose**: Run comprehensive unit tests across multiple Python versions

**Configuration**:
- **Matrix Testing**: Tests on Python 3.10, 3.11, 3.12
- **Coverage Reporting**: Generates coverage reports and uploads to Codecov
- **Timeout**: 300 seconds per test session

**Steps**:
1. Check out code
2. Set up Python environment
3. Install dependencies (pytest, pytest-cov, pytest-timeout)
4. Run tests: `pytest tests/unit/ -v --cov=src --cov-report=xml`
5. Upload coverage metrics

**Success Criteria**:
- All unit tests must pass
- Coverage metrics are recorded

**Expected Output**:
```
pytest tests/unit/ -v --cov=src
Name                 Stmts   Miss  Cover
src/core/retrieval   360     12    96%
======== 39 passed in 2.45s ========
```

### 2. Code Quality (`code-quality`)

**Purpose**: Ensure code follows style and quality standards

**Tools Used**:
- **Ruff**: Unified linting and formatting
- **mypy**: Type checking

**Steps**:
1. Check out code
2. Set up Python 3.11 environment
3. Install Ruff and mypy
4. Run Ruff checks (linting)
5. Run Ruff format checks (formatting)
6. Run mypy (type checking)

### 3. Integration Tests (`integration-tests`)

**Purpose**: Run integration tests (placeholder for future)

**Configuration**:
- Runs in `tests/integration/` directory
- Currently non-blocking as integration tests may not exist yet
- Will be enhanced as more integration tests are added

### 4. Test Summary (`test-summary`)

**Purpose**: Aggregate test results and provide clear pass/fail status

**Behavior**:
- ✅ Shows summary of all test runs
- ✅ **Blocks PR if unit tests fail** (required)
- ⚠️ Shows code quality warnings (non-blocking)
- Ensures visibility of overall status

## Usage

### For Developers

1. **Before pushing**: Run tests locally
   ```bash
   pytest tests/unit/ -v
   ```

2. **On push/PR creation**: Pipeline automatically runs

3. **View results**:
   - Check "Checks" tab in PR
   - Look for green ✅ or red ❌ status

### For Repository Maintainers

1. **Check PR status**: All PRs show pipeline results
2. **Merge requirements**: Unit tests must pass (code quality is informational)
3. **Monitor main branch**: All pushes are tested

## Current Test Suite

### Unit Tests
- **Location**: `tests/unit/`
- **Coverage**:
  - `test_deidentification.py`: 39 tests for deidentifier module
    - SSN detection (4 tests)
    - Phone detection (7 tests)
    - Email detection (4 tests)
    - Credit card detection (2 tests)
    - DOB detection (3 tests)
    - Batch processing (2 tests)
    - Verification (3 tests)
    - Edge cases (8 tests)
    - Performance (2 tests)

### Integration Tests
- **Location**: `tests/integration/`
- **Status**: Placeholder - no tests yet

## Dependencies

The pipeline automatically installs:
- `pytest`: Test framework
- `pytest-cov`: Coverage plugin
- `pytest-timeout`: Timeout plugin
- `ruff`: Linting and formatting
- `mypy`: Type checking

To add more dependencies, update the `Install dependencies` step in `.github/workflows/ci.yml`.

## Monitoring and Troubleshooting

### Viewing Pipeline Results

1. **In GitHub UI**:
   - Go to PR → "Checks" tab
   - Click on individual job names for detailed logs
   - Scroll down for step-by-step output

2. **Command Line** (with GitHub CLI):
   ```bash
   gh pr checks <pr-number>
   ```

### Common Issues

#### Tests Fail Locally but Pass in CI
- Check Python version: `python --version`
- Ensure all dependencies: `pip install -r requirements.txt`
- Check platform-specific issues (Windows vs Linux)

#### Tests Pass Locally but Fail in CI
- May be environment-specific (Ubuntu vs Windows)
- Check for hardcoded paths or system assumptions
- Add verbosity: `pytest -vv` for more details

#### Code Quality Warnings
- Run formatters and checks locally:
  ```bash
  poetry run ruff check src/ tests/
  poetry run ruff format src/ tests/
  ```

## Future Enhancements

Planned additions to CI/CD pipeline:
- [ ] Docker build testing
- [ ] Integration tests with services (Qdrant, LangFuse, CosmosDB)
- [ ] Performance benchmarking
- [ ] Documentation build verification
- [ ] Security scanning (SAST)
- [ ] Dependency checking (Dependabot)

## Configuration Files

### GitHub Actions Secrets
Currently no secrets are required. If needed in the future, add them via:
- Repository Settings → Secrets and variables → Actions

### Protected Branch Rules
Recommended settings for `main` branch:
- ✓ Require status checks to pass before merging
- ✓ Require code reviews
- ✓ Dismiss stale PR approvals
- ✓ Include administrators

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.com/)
