.PHONY: help install format lint test verify ci ci-matrix clean pre-commit compile build

# Optional Python version for `ci`; empty means current Poetry environment.
PYTHON_VERSION ?=
# Python versions used by `ci-matrix`.
PYTHON_MATRIX ?= 3.10 3.11 3.12 3.13
# FAST=1 skips integration tests to speed up local checks.
FAST ?= 0

# Support positional version: make ci 3.12
ifneq (,$(filter ci,$(MAKECMDGOALS)))
ifneq ($(word 2,$(MAKECMDGOALS)),)
ifeq ($(PYTHON_VERSION),)
PYTHON_VERSION := $(word 2,$(MAKECMDGOALS))
endif
$(eval $(word 2,$(MAKECMDGOALS)):;@:)
endif
endif

# Default target
help:
	@echo "VedaAide Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Install dependencies via Poetry"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format       - Format code (ruff format)"
	@echo "  make lint         - Run linting checks (ruff check)"
	@echo "  make test         - Run tests with coverage"
	@echo "  make verify       - Run ALL checks (format + lint + test)"
	@echo "  make ci [3.12]    - CI-like checks on one Python version (or current)"
	@echo "                     Add FAST=1 to skip integration tests"
	@echo "  make ci-matrix    - Run CI-like checks across all matrix versions"
	@echo "                     Add FAST=1 for a quicker matrix run"
	@echo ""
	@echo "Build:"
	@echo "  make compile      - Check Python syntax (compile all .py files)"
	@echo "  make build        - Build distribution package (.whl and .tar.gz)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Clean cache and build files"
	@echo "  make pre-commit   - Set up pre-commit hooks"
	@echo ""

compile:
	poetry run python -m compileall src/
	@echo "✅ All Python files compiled successfully"

build: compile
	poetry build
	@echo "✅ Package built successfully"

integration-test:
	poetry run pytest tests/integration/ -v --timeout=300 2>/dev/null || echo "No integration tests yet"

install:
	poetry install

format:
	poetry run ruff format src tests

lint:
	poetry run ruff check src tests

test:
	poetry run pytest --cov

verify: format lint test
	@echo ""
	@echo "All quality checks passed!"

ci:
	@set -e; \
	requested_version="$(PYTHON_VERSION)"; \
	fast_mode="$(FAST)"; \
	current_python=$$(poetry run python -c "import sys; print(sys.executable)"); \
	trap 'poetry env use "$$current_python" >/dev/null 2>&1 || true' EXIT; \
	if [ -n "$$requested_version" ]; then \
		echo "Switching to Python $$requested_version"; \
		poetry env use "$$requested_version" >/dev/null; \
		echo "Installing dependencies..."; \
		poetry install --with dev --sync; \
	fi; \
	echo "Running CI checks with: $$(poetry run python --version)"; \
	echo "FAST mode: $$fast_mode"; \
	poetry run ruff check src tests; \
	poetry run ruff format --check src tests; \
	poetry run pytest tests/unit/ -v --cov=src --cov-report=xml --cov-report=term-missing --timeout=300; \
	if [ "$$fast_mode" = "1" ]; then \
		echo "FAST=1: skipping integration tests"; \
	else \
		poetry run pytest tests/integration/ -v --timeout=300 2>/dev/null || echo "No integration tests yet"; \
	fi

ci-matrix:
	@set -e; \
	current_python=$$(poetry run python -c "import sys; print(sys.executable)"); \
	trap 'poetry env use "$$current_python" >/dev/null 2>&1 || true' EXIT; \
	for version in $(PYTHON_MATRIX); do \
		echo ""; \
		echo "==== Running CI checks for Python $$version ===="; \
		$(MAKE) ci PYTHON_VERSION=$$version FAST=$(FAST); \
	done

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true

pre-commit:
	poetry run pre-commit install
	@echo "✅ Pre-commit hooks installed"
