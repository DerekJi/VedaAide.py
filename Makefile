.PHONY: help install format lint type-check test audit verify clean pre-commit

# Default target
help:
	@echo "VedaAide Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Install dependencies via Poetry"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format       - Format code (black + isort)"
	@echo "  make lint         - Run linting checks (pylint)"
	@echo "  make type-check   - Run type checking (mypy)"
	@echo "  make test         - Run tests with coverage"
	@echo "  make audit        - Run code standards audit (comprehensive review)"
	@echo "  make verify       - Run ALL checks (format + lint + type-check + test + audit)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Clean cache and build files"
	@echo "  make pre-commit   - Set up pre-commit hooks"
	@echo ""

install:
	poetry install

format:
	poetry run black src tests scripts dev-tools
	poetry run isort src tests scripts dev-tools

lint:
	poetry run pylint src tests
	poetry run flake8 src tests dev-tools

type-check:
	poetry run mypy src dev-tools

test:
	poetry run pytest --cov

audit:
	poetry run python dev-tools/code_standards_checker.py

verify: format lint type-check test audit
	@echo ""
	@echo "✅ All quality checks passed!"

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
