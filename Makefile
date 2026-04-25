.PHONY: help install format lint test verify clean pre-commit

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
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Clean cache and build files"
	@echo "  make pre-commit   - Set up pre-commit hooks"
	@echo ""

install:
	poetry install

format:
	poetry run ruff format src tests scripts dev-tools

lint:
	poetry run ruff check src tests scripts dev-tools

test:
	poetry run pytest --cov

verify: format lint test
	@echo ""
	@echo "All quality checks passed!"

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
