---
applyTo: '**/*.py'
---
## Development Environment

The project uses Docker Compose for local infrastructure (Qdrant required, LangFuse optional). Kubernetes/Skaffold/Kind is not part of the current workflow.

## Development Workflow Requirements

When developing or fixing issues, you MUST:

1. **Ensure compilation passes** - No compilation errors
2. **Ensure startup without errors** - Services/applications run normally
3. **Continuous iteration until complete**:
   - If any issues arise: Fix → Verify → Monitor → Iterate
   - Do not abandon mid-way
   - Continue until all above conditions are met

## Python Code Quality Standards (Strict Enforcement)

### File Organization
- Modularize code by functionality: UI logic, business logic, database operations, and configuration must be separated
- Single file should not exceed 200 lines (unless necessary)
- **Strictly prohibited**: Writing all logic in `main.py` or a single function

### Function Design (Single Responsibility Principle)
- One function should do only one thing
- Functions exceeding 30-50 lines must be split into sub-functions
- Function names must be clear and self-documenting (e.g., `get_user_by_id` instead of `handle_data`)

### Object-Oriented Design
- Complex logic must be abstracted into classes
- Leverage inheritance and polymorphism for extensibility
- Pursue loose coupling design patterns

### Type Hints (Mandatory)
- All functions and methods must declare input/output types

### Documentation & Comments
- Important functions/classes must include Google-style docstrings
- Explain purpose, parameters, and return values

### Code Style
- Strict PEP 8 compliance (4-space indentation)
- Compatible with ruff/pylint

### Development Process
- **Before writing code**: Think about module structure
- Actively split code into multiple files with single responsibilities
- Never implement everything in one file or function

## Language Requirements

All documentation and code comments in `.github/instructions/` and `.github/ISSUE_TEMPLATE/` must be in **English only**.

> **Note**: `.github/prompts/` contains developer-facing prompt guides that may be written in Chinese for clarity. They are not subject to the English-only rule.
>
> **Deduplication**: `.github/python-code-quality.instructions.md` (applies to `**/*.py`) and `.github/instructions/coding-standards.instructions.md` (applies to `src/**/*.py, tests/**/*.py`) cover the same rules. The `coding-standards.instructions.md` version is authoritative for scoped Python files; this file applies as a broader fallback.
