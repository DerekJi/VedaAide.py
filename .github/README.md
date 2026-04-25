# VedaAide Development Standards

This directory contains development guidelines, templates, and AI-assisted development configurations for VedaAide.

## 📋 Contents

### Configuration Files (Active)

- **`python-code-quality.instructions.md`** ⭐
  - **Purpose**: Core development standards for the project
  - **Audience**: For recruiters and team members
  - **Content**:
    - Development environment requirements (Podman + Kind)
    - Development workflow enforcement (compile → test → deploy)
    - Python code quality standards (modularization, functions, OOP, type hints, docs, style)
  - **Status**: ✅ English, active, auto-loaded by Copilot Chat

- **`documentation-bilingual.instructions.md`**
  - **Purpose**: Documentation update requirements for bilingual content
  - **Status**: Mixed language (by design for bilingual tracking)
  - **Note**: Defines naming conventions for `*.cn.md` and `*.en.md` files

### Prompt Files (Reference & Guidelines)

Located in `prompts/` subdirectory:

| File | Language | Status | Notes |
|------|----------|--------|-------|
| `coding-standards.md` | English | ⚠️ Needs review | Code style, type hints, docstrings, tests |
| `rag-development.md` | English | ⚠️ Needs review | RAG patterns, hybrid search, Qdrant, DSPy |
| `testing-strategy.md` | Chinese | ⏳ Pending translation | Test pyramid, AAA pattern, mocking |
| `evaluation-strategy.md` | Chinese | ⏳ Pending translation | RAGAS metrics, DSPy compilation |
| `cloud-native-dev.md` | Chinese | ⏳ Pending translation | Skaffold, Podman, Kind setup |
| `project-context.md` | Chinese | ⏳ Pending translation | Project goals, tech stack overview |
| `.prompts.json` | JSON | ✅ Active | Copilot Chat skill definitions |

### Issue Templates

- **`ISSUE_TEMPLATE/task.md`** ⭐
  - **Status**: ✅ English
  - **Purpose**: Standard task/feature request template with DoD (Definition of Done)
  - **Content**: Problem description, objectives, acceptance criteria, code quality checks, documentation requirements

## 🎯 Key Development Standards

### Code Quality (Python)

All Python development must follow:
- **Modularization**: Separate UI, business logic, DB, config; single file ≤ 200 lines
- **Functions**: Single responsibility; split if > 30-50 lines; clear naming
- **OOP**: Abstract complex logic into classes; use inheritance/polymorphism; loose coupling
- **Type Hints**: Mandatory on all functions and methods
- **Docstrings**: Google-style for important functions/classes
- **Style**: PEP 8 (4-space indent), ruff/pylint compatible
- **Architecture**: Think through module structure BEFORE coding

### Development Workflow

Before ending any development task:
1. ✅ **Compilation passes** - No compile errors
2. ✅ **Startup without errors** - Services/applications run normally
3. ✅ **Continuous iteration** - If issues arise: Fix → Verify → Monitor → Iterate
   - Do not abandon mid-way
   - Continue until all conditions met

### Environment

- **Container Runtime**: Podman Desktop (no Docker)
- **K8s Cluster**: Kind Extension (cluster: `k8s-new`)
- **Development Tool**: Skaffold for hot reload and debugging
- **Namespace**: `vedaaide-dev`

## 🔧 For Recruiters

These files document:

1. **Engineering Practices**: How we ensure high-quality, maintainable code
2. **Development Process**: Continuous iteration and quality verification
3. **Tech Stack**: Python 3.10+, RAG architecture, Kubernetes-native
4. **Team Standards**: Code review checklist, naming conventions, architectural patterns

This demonstrates:
- ✅ High-level engineering mentality (not just "working code")
- ✅ Production-ready practices (modularization, testing, observability)
- ✅ Team collaboration (clear standards, templates, documentation)

## 📚 Related Documentation

- **Project Structure**: [docs/planning/PROJECT_STRUCTURE.en.md](../../docs/planning/PROJECT_STRUCTURE.en.md)
- **Project Vision**: [docs/planning/index.md](../../docs/planning/index.md)
- **Main README**: [README.md](../../README.md)

## 🚀 Quick Start

1. Read `python-code-quality.instructions.md` for development standards
2. Use `ISSUE_TEMPLATE/task.md` when creating tasks
3. Reference `prompts/coding-standards.md` for code review checklist
4. Follow development workflow: code → compile → test → deploy

## 📝 Translation Status

| Language | Completion | Priority |
|----------|-----------|----------|
| English | 60% (3/5 main files) | HIGH - Complete for recruiter review |
| Chinese | 100% | For internal team reference |

**Translation Work**: `testing-strategy.md`, `evaluation-strategy.md`, `cloud-native-dev.md`, `project-context.md` require English translation for consistency.

---

**Last Updated**: April 22, 2026
**Maintainers**: VedaAide Development Team
