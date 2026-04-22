# VedaAide Project Structure & Naming Conventions

## Overview

This document defines the directory organization, naming conventions, code layering, and development workflow for the VedaAide project to support efficient collaboration, testing, evaluation, and cloud-native deployment.

---

## 1. Top-Level Directory Structure

```
VedaAide/
├── src/                          # Source code root (planned)
├── tests/                        # Test code (planned)
├── docs/                         # Documentation (planning, API, guides)
├── data/                         # Data storage (resumes, datasets, results)
├── config/                       # Configuration files (planned)
├── scripts/                      # Utility scripts
│   └── k8s/                      # K8s deployment scripts
├── infra/                        # Infrastructure code
│   ├── docker/                   # Dockerfile templates
│   └── k8s/                      # Kubernetes deployment manifests
├── .github/                      # GitHub configuration
│   ├── instructions/             # Copilot instruction files
│   ├── prompts/                  # Copilot Chat prompts
│   └── ISSUE_TEMPLATE/           # GitHub Issue templates
├── docker-compose.yml            # Local dev container orchestration (Qdrant, LangFuse, etc.)
├── skaffold.yaml                 # Cloud Native dev configuration
├── pyproject.toml                # Python project config (to be initialized)
├── .gitignore
└── README.md / README.cn.md
```

---

## 2. Source Code Directory (src/)

### 2.1 Core Layered Architecture

```
src/
├── __init__.py
├── core/                         # Core business logic layer
│   ├── __init__.py
│   ├── agent/                    # Agent-related modules
│   │   ├── __init__.py
│   │   ├── state.py              # Agent state definitions (Pydantic models)
│   │   ├── graph.py              # LangGraph construction and state machine
│   │   ├── tools.py              # Agent tool definitions
│   │   └── strategies.py         # Interview strategies (HR/Tech)
│   │
│   ├── retrieval/                # Retrieval layer
│   │   ├── __init__.py
│   │   ├── indexer.py            # Index management (Qdrant integration)
│   │   ├── retriever.py          # Retrieval logic (vector/hybrid search)
│   │   ├── ranker.py             # Result reranking
│   │   └── deidentifier.py       # Data deidentification utilities
│   │
│   ├── rag/                      # RAG pipeline
│   │   ├── __init__.py
│   │   ├── pipeline.py           # RAG flow orchestration
│   │   ├── prompt_manager.py     # Prompt management and versioning
│   │   └── dspy_compiler.py      # DSPy compilation optimization
│   │
│   └── evaluation/               # Evaluation framework
│       ├── __init__.py
│       ├── ragas_evaluator.py    # RAGAS quantitative evaluation
│       ├── metrics.py            # Custom evaluation metrics
│       └── feedback.py           # User feedback handling
│
├── infrastructure/               # Infrastructure layer
│   ├── __init__.py
│   ├── db/                       # Database management
│   │   ├── __init__.py
│   │   ├── cosmosdb.py           # Azure CosmosDB driver
│   │   ├── qdrant.py             # Qdrant driver and connection pool
│   │   └── models.py             # ORM/data model definitions
│   │
│   ├── llm/                      # LLM interface layer
│   │   ├── __init__.py
│   │   ├── azure_openai.py       # Azure OpenAI integration
│   │   ├── ollama.py             # Ollama local inference
│   │   ├── embeddings.py         # Embedding management
│   │   └── base.py               # LLM base classes and protocols
│   │
│   ├── observability/            # Observability
│   │   ├── __init__.py
│   │   ├── tracing.py            # LangFuse integration
│   │   ├── metrics.py            # Metrics collection (tokens, costs)
│   │   ├── logger.py             # Custom logging
│   │   └── decorators.py         # Observability decorators
│   │
│   └── cache/                    # Cache layer
│       ├── __init__.py
│       └── redis_cache.py        # Optional: Redis caching
│
├── api/                          # API layer (optional: REST/WebSocket)
│   ├── __init__.py
│   ├── routes.py                 # FastAPI routes
│   ├── schemas.py                # Request/response data models
│   └── middleware.py             # Middleware (auth, rate limiting)
│
├── utils/                        # Utility functions
│   ├── __init__.py
│   ├── config.py                 # Configuration loading (from KeyVault)
│   ├── secrets.py                # Secret management
│   ├── validators.py             # Data validation
│   ├── converters.py             # Data conversion
│   └── constants.py              # Constant definitions
│
├── cli/                          # Command-line tools
│   ├── __init__.py
│   ├── __main__.py               # CLI entry point
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── init.py               # Project initialization
│   │   ├── ingest.py             # Data ingestion
│   │   ├── evaluate.py           # Run evaluation
│   │   ├── serve.py              # Start service
│   │   └── demo.py               # Demo command
│   └── args.py                   # Argument definitions
│
└── main.py                       # Application entry point
```

### 2.2 Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| **Module file** | snake_case, descriptive | `agent_state.py`, `cosmosdb_driver.py` |
| **Class name** | PascalCase, with suffix | `AgentStateManager`, `CosmosDBConnector` |
| **Function name** | snake_case, verb-first | `retrieve_contexts()`, `calculate_similarity()` |
| **Constant** | UPPER_SNAKE_CASE | `MAX_RETRIEVAL_K`, `DEFAULT_MODEL_TEMPERATURE` |
| **Private function/attribute** | Single underscore prefix | `_validate_query()`, `_cache_key` |
| **Protected function/attribute** | Double underscore prefix | `__init_embeddings__()` |
| **Type hints** | Full annotation with `typing` | `def retrieve(...) -> List[Document]:` |

---

## 3. Test Directory (tests/)

### 3.1 Test Structure

```
tests/
├── __init__.py
├── conftest.py                   # pytest configuration and fixtures
├── fixtures/                     # Test data and mocks
│   ├── __init__.py
│   ├── sample_data.py            # Sample docs, JDs, resumes
│   ├── mocks.py                  # Mock objects (LLM, DB)
│   └── deidentified_data.py      # Deidentified test data
│
├── unit/                         # Unit tests
│   ├── __init__.py
│   ├── test_deidentifier.py      # Data deidentification tests
│   ├── test_retriever.py         # Retrieval module tests
│   ├── test_ranker.py            # Reranking tests
│   ├── test_agent_tools.py       # Agent tool tests
│   ├── test_dspy_compiler.py     # DSPy optimization tests
│   ├── test_evaluation.py        # Evaluation logic tests
│   └── test_utils.py             # Utility function tests
│
├── integration/                  # Integration tests
│   ├── __init__.py
│   ├── test_rag_pipeline.py      # RAG end-to-end flow
│   ├── test_agent_workflow.py    # Agent complete workflow
│   ├── test_cosmosdb_persistence.py  # CosmosDB data persistence
│   ├── test_llm_integration.py   # LLM integration (mocked)
│   └── test_observability.py     # LangFuse/logging integration
│
├── e2e/                          # End-to-end tests
│   ├── __init__.py
│   ├── test_interview_flow.py    # Complete interview flow
│   ├── test_evaluation_pipeline.py  # Complete evaluation flow
│   └── test_cost_tracking.py     # Cost tracking tests
│
└── benchmarks/                   # Performance tests
    ├── __init__.py
    ├── bench_retrieval.py        # Retrieval performance benchmarks
    ├── bench_inference.py        # Inference performance benchmarks
    └── bench_evaluation.py       # Evaluation performance benchmarks
```

### 3.2 Test Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| **Test file** | test_*.py or *_test.py | `test_retriever.py` |
| **Test function** | test_* | `test_retrieve_with_empty_query()` |
| **Test class** | Test* | `TestRetriever` |
| **Fixture** | snake_case | `@pytest.fixture def sample_resume():` |
| **Parametrized test** | descriptive | `@pytest.mark.parametrize("model,expected", ...)` |

### 3.3 Test Coverage Targets

- **Unit tests**: ≥ 80% line coverage
- **Integration tests**: 100% for critical paths
- **E2E tests**: 100% for core business flows
- **Overall coverage**: ≥ 75%

---

## 4. Documentation Directory (docs/)

### 4.1 Documentation Structure

```
docs/
├── README.md                     # Documentation main entry
├── INDEX.md                      # Documentation index and quick nav
│
├── planning/                     # Project planning documents
│   ├── index.md                  # Project vision (existing)
│   ├── index.en.md               # English version
│   ├── PROJECT_STRUCTURE.md      # This document
│   ├── PROJECT_STRUCTURE.en.md   # English version
│   ├── 00.basics.md              # Basic considerations (existing)
│   ├── AgentScenarios.cn.md      # Agent scenario design
│   ├── AgentScenarios.en.md      # English version
│   └── ROADMAP.md                # Complete implementation roadmap
│
├── guides/                       # Development guides
│   ├── SETUP.md                  # Dev environment setup
│   ├── SETUP.en.md               # English version
│   ├── DEVELOPMENT.md            # Development workflow
│   ├── TESTING.md                # Testing guide
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── CLOUD_NATIVE.md           # Cloud Native dev guide
│   └── TROUBLESHOOTING.md        # Troubleshooting guide
│
├── architecture/                 # Architecture documents
│   ├── OVERVIEW.md               # System architecture overview
│   ├── DATA_FLOW.md              # Data flow design
│   ├── AGENT_STATE_MACHINE.md    # Agent state machine design
│   ├── RAG_PIPELINE.md           # RAG pipeline design
│   ├── OBSERVABILITY.md          # Observability architecture
│   └── SECURITY.md               # Security design
│
├── api/                          # API documentation
│   ├── REST_API.md               # REST API specification
│   ├── SCHEMAS.md                # Data model specification
│   └── EXAMPLES.md               # Usage examples
│
├── evaluation/                   # Evaluation-related documents
│   ├── RAGAS_METRICS.md          # RAGAS metrics explanation
│   ├── EVALUATION_FRAMEWORK.md   # Evaluation framework design
│   ├── FEEDBACK_MECHANISM.md     # Feedback mechanism
│   └── BENCHMARK_REPORTS.md      # Benchmark test reports
│
├── JD/                           # Requirements documents
│   ├── JD-001.md                 # Original job description (existing)
│   └── REQUIREMENTS.md           # Project requirements analysis
│
└── reports/                      # Regular output reports
    ├── evaluation_results/       # Evaluation result reports
    ├── cost_analysis/            # Cost analysis
    └── performance_metrics/      # Performance metrics
```

### 4.2 Documentation Naming Conventions

| Document Type | Convention | Example |
|--------------|-----------|---------|
| **Guide doc** | UPPER_SNAKE_CASE.md | `DEVELOPMENT.md`, `CLOUD_NATIVE.md` |
| **Planning doc** | lowercase or index.md | `00.basics.md`, `index.md` |
| **Architecture doc** | UPPER_SNAKE_CASE.md | `DATA_FLOW.md`, `AGENT_STATE_MACHINE.md` |
| **Chinese version** | filename.cn.md | `SETUP.cn.md` |
| **English version** | filename.en.md or filename.md | `SETUP.en.md` |
| **Report** | format_date.md | `evaluation_results_2026-04-22.md` |

---

## 5. Data Directory (data/)

### 5.1 Data Organization

```
data/
├── raw/                          # Raw data
│   ├── resumes/                  # Personal resumes
│   ├── projects/                 # Project descriptions
│   ├── blogs/                    # Technical blogs
│   └── job_descriptions/         # Job descriptions
│
├── processed/                    # Processed data
│   ├── deidentified/             # Deidentified datasets
│   │   ├── resumes_v1/
│   │   ├── projects_v1/
│   │   └── metadata.json         # Deidentification mapping
│   └── embeddings/               # Pre-computed embeddings
│
├── test/                         # Test data
│   ├── synthetic_qa/             # Synthetic Q&A pairs
│   ├── benchmark_queries/        # Benchmark queries
│   └── edge_cases/               # Edge case test data
│
├── evaluation/                   # Evaluation-related data
│   ├── test_sets/                # Evaluation test sets
│   ├── ragas_results/            # RAGAS evaluation results
│   ├── user_feedback/            # User feedback data
│   └── metrics/                  # Metric data
│
└── snapshots/                    # Data snapshots (version control)
    ├── 2026-04-20/
    ├── 2026-04-21/
    └── 2026-04-22/
```

### 5.2 Data Naming Conventions

| Data Type | Convention | Example |
|-----------|-----------|---------|
| **Data file** | snake_case_v<version>.json | `resumes_v1.json`, `embeddings_v2.pkl` |
| **Test set** | type_size_seed.json | `qa_pairs_100_seed42.json` |
| **Evaluation result** | ragas_<model>_<date>.json | `ragas_gpt4o_2026-04-22.json` |
| **Snapshot directory** | YYYY-MM-DD | `2026-04-22/` |

---

## 6. Configuration Directory (config/)

### 6.1 Configuration Structure

```
config/
├── default.yaml                  # Default configuration
├── development.yaml              # Development environment config
├── staging.yaml                  # Staging environment config
├── production.yaml               # Production environment config
│
├── models/                       # Model configuration
│   ├── llm_config.yaml          # LLM parameters (temp, max_tokens)
│   ├── embedding_config.yaml    # Embedding configuration
│   └── dspy_config.yaml         # DSPy compilation config
│
├── databases/                    # Database configuration
│   ├── qdrant.yaml              # Qdrant connection params
│   ├── cosmosdb.yaml            # CosmosDB connection params
│   └── redis.yaml               # Redis cache config (optional)
│
├── prompts/                      # Prompt templates
│   ├── system_prompts.yaml      # System prompts
│   ├── interview_prompts.yaml   # Interview-related prompts
│   ├── evaluation_prompts.yaml  # Evaluation prompts
│   └── reflection_prompts.yaml  # Reflection prompts
│
├── observability/               # Observability configuration
│   ├── langfuse.yaml            # LangFuse configuration
│   ├── logging.yaml             # Logging configuration
│   └── metrics.yaml             # Metrics collection config
│
└── security/                    # Security configuration
    ├── deidentification.yaml    # Deidentification rules
    └── rate_limits.yaml         # Rate limiting
```

### 6.2 Configuration Management

- **Environment variables first**: `CONFIG_ENV=production`
- **Secret storage**: Azure KeyVault, loaded via `config.py`
- **Local development**: `.env.local` (not committed to Git)
- **Version control**: All `.yaml` committed, `.env` ignored

---

## 7. Scripts Directory (scripts/)

### 7.1 Script Organization

```
scripts/
├── data/                         # Data processing scripts
│   ├── ingest_data.py           # Data ingestion script
│   ├── deidentify_data.py       # Data deidentification script
│   ├── generate_embeddings.py   # Pre-compute embeddings
│   └── validate_data.py         # Data validation
│
├── evaluation/                   # Evaluation scripts
│   ├── run_ragas.py             # RAGAS evaluation
│   ├── generate_test_set.py     # Generate synthetic test set
│   ├── analyze_results.py       # Analyze evaluation results
│   └── compare_versions.py      # Version comparison
│
├── optimization/                # Optimization scripts
│   ├── compile_dspy.py          # DSPy compilation
│   ├── tune_parameters.py       # Parameter tuning
│   └── benchmark.py             # Performance benchmarking
│
├── deployment/                  # Deployment scripts
│   ├── build_image.sh           # Build Docker image
│   ├── deploy_k8s.sh            # Kubernetes deployment
│   └── health_check.sh          # Health check
│
├── maintenance/                 # Maintenance scripts
│   ├── cleanup_old_data.py      # Clean up old data
│   ├── backup_database.py       # Database backup
│   └── monitor_costs.py         # Monitor costs
│
└── dev/                         # Development helper scripts
    ├── setup_dev_env.sh         # Setup dev environment
    ├── generate_api_docs.py     # Generate API docs
    └── format_code.sh           # Code formatting
```

### 7.2 Script Conventions

| Script Type | Extension | First line | Example |
|------------|-----------|-----------|---------|
| **Python script** | .py | `#!/usr/bin/env python3` | `ingest_data.py` |
| **Shell script** | .sh | `#!/bin/bash -e` | `deploy_k8s.sh` |
| **Executable** | none | corresponding first line | `setup_dev_env` |

---

## 8. Infrastructure Directory (infra/)

### 8.1 Infrastructure Code

```
infra/
├── docker/                       # Docker-related
│   ├── Dockerfile               # Multi-stage build
│   ├── Dockerfile.dev           # Dev image
│   ├── docker-compose.yml       # Local dev orchestration
│   └── .dockerignore
│
├── kubernetes/                   # Kubernetes manifests
│   ├── namespace.yaml            # Namespace
│   ├── configmap.yaml            # ConfigMap
│   ├── secret.yaml               # Secret (injected from KeyVault)
│   ├── deployment.yaml           # Application Deployment
│   ├── service.yaml              # Service exposure
│   ├── ingress.yaml              # Ingress configuration
│   ├── hpa.yaml                  # Horizontal Pod Autoscaling
│   └── monitoring/               # Monitoring-related
│       ├── servicemonitor.yaml
│       └── grafana.yaml
│
├── skaffold/                     # Cloud Native development
│   ├── skaffold.yaml             # Skaffold configuration
│   └── skaffold-dev.yaml         # Dev mode configuration
│
├── terraform/                    # Infrastructure as Code (optional)
│   ├── main.tf                   # Main configuration
│   ├── variables.tf              # Variable definitions
│   ├── outputs.tf                # Output definitions
│   └── azure/                    # Azure-specific resources
│       ├── container_apps.tf
│       ├── cosmosdb.tf
│       └── keyvault.tf
│
└── scripts/                      # Infrastructure scripts
    ├── setup_cluster.sh
    ├── deploy_monitoring.sh
    └── cleanup.sh
```

---

## 9. GitHub Configuration (.github/)

### 9.1 GitHub Configuration Structure

```
.github/
├── workflows/                    # GitHub Actions workflows
│   ├── ci.yml                    # CI (testing, linting)
│   ├── cd.yml                    # CD (deployment)
│   ├── evaluation.yml            # Periodic evaluation tasks
│   ├── cost-tracking.yml         # Cost monitoring
│   └── security-scan.yml         # Security scanning
│
├── prompts/                      # Copilot Chat prompt configs
│   ├── .prompts.json             # Root configuration file
│   ├── project-context.md        # Project context
│   ├── coding-standards.md       # Coding standards
│   ├── rag-development.md        # RAG development guide
│   └── testing-strategy.md       # Testing strategy
│
├── skills/                       # Copilot Skills (optional)
│   ├── SKILLS.md                 # Skills index
│   ├── rag-engineering/          # RAG engineering skill
│   │   ├── SKILL.md
│   │   ├── examples.md
│   │   └── best_practices.md
│   ├── evaluation-design/        # Evaluation design skill
│   │   ├── SKILL.md
│   │   └── checklist.md
│   └── cloud-native-dev/         # Cloud Native dev skill
│       ├── SKILL.md
│       └── skaffold-guide.md
│
├── issue_template/               # Issue templates
│   ├── bug_report.md
│   ├── feature_request.md
│   └── documentation.md
│
└── pull_request_template.md      # PR template
```

### 9.2 Copilot Prompts Example Structure

**.prompts.json** - Root configuration
```json
{
  "version": "0.1.0",
  "defaultContext": {
    "codebase": "Python RAG Agent System",
    "includeFiles": [
      ".github/prompts/project-context.md",
      ".github/prompts/coding-standards.md"
    ]
  }
}
```

**Coding standards prompt example** (`coding-standards.md`)
```markdown
# VedaAide Coding Standards

## Python Style
- PEP 8 compliance
- Type hints mandatory
- Docstring format: Google style
- Line length limit: 100 characters

## Module Organization
- Single Responsibility Principle (SRP)
- Dependency injection
- Avoid circular imports

## Error Handling
- Use custom exceptions
- Provide clear error messages
- Log complete stack traces
```

---

## 10. VSCode Configuration (.vscode/)

### 10.1 VSCode Structure

```
.vscode/
├── settings.json                 # VSCode project settings
├── launch.json                   # Debug configuration
├── tasks.json                    # Task configuration
├── extensions.json               # Recommended extensions
└── copilot/
    ├── instructions.md           # Copilot instructions
    └── prompt-templates.md       # Prompt templates
```

### 10.2 VSCode Settings Example

**`settings.json`**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true
  }
}
```

---

## 11. Cloud Native Development Workflow

### 11.1 Skaffold for Development

#### Purpose
- Auto-sync code to K8s cluster
- Hot reload (see code changes instantly)
- Simplified local development

#### Skaffold Configuration Example

**`skaffold.yaml`**
```yaml
apiVersion: skaffold/v4beta6
kind: Config
metadata:
  name: vedaaide

build:
  artifacts:
    - image: vedaaide-api
      docker:
        dockerfile: infra/docker/Dockerfile.dev

deploy:
  kubectl: {}

portForward:
  - resourceType: deployment
    resourceName: vedaaide-api
    port: 8080
    localPort: 8080

sync:
  manual:
    - src: "src/**/*.py"
      dest: /app/src

dev:
  watch:
    - infra/docker/Dockerfile.dev
    - src/**/*.py
```

#### Development Workflow

1. **Initialize**
   ```bash
   skaffold config set default-repo localhost:5000
   skaffold debug --port-forward
   ```

2. **Code Sync**
   - Modify Python files in `src/`
   - Skaffold auto-syncs to container
   - App auto-restarts or hot-reloads

3. **Debug**
   - Connect VSCode remote debugger
   - Set breakpoints and debug code

4. **View Logs**
   ```bash
   skaffold logs -f
   ```

#### Performance Considerations

| Aspect | Details | Optimization |
|--------|---------|--------------|
| **Sync delay** | Typically 1-3s | Sync only changed files |
| **Network overhead** | Depends on cluster network | Use local cluster (Kind/Minikube) |
| **Large files** | May cause delay | Exclude `__pycache__`, `*.pyc` |
| **Cold start** | First build slower | Use layer caching |

### 11.2 Local vs Cluster Development Comparison

| Aspect | Local (docker-compose) | Cluster (Skaffold) |
|--------|----------------------|-----------------|
| **Startup time** | Fast (< 10s) | Medium (20-30s) |
| **Resource usage** | Low | Medium-high |
| **Debug capability** | Excellent | Good |
| **Env consistency** | Medium | Excellent |
| **Production simulation** | Medium | Excellent |

**Recommended strategy**:
- Early development: `docker-compose`
- Integration testing & fine-tuning: `Skaffold`

---

## 12. CI/CD Pipeline

### 12.1 GitHub Actions Workflows

#### CI Process (ci.yml)

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Format check
        run: poetry run black --check src/ tests/
      - name: Lint
        run: poetry run pylint src/ tests/
      - name: Type check
        run: poetry run mypy src/
      - name: Run tests
        run: poetry run pytest tests/ --cov=src/
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

#### CD Process (cd.yml)

```yaml
name: CD

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push image
        run: |
          docker build -t ghcr.io/${{ github.repository }}:latest .
          docker push ghcr.io/${{ github.repository }}:latest
      - name: Deploy to ACA
        run: |
          az container app update \
            --name vedaaide-api \
            --image ghcr.io/${{ github.repository }}:latest
```

---

## 13. Naming Conventions Summary

### 13.1 Global Naming Conventions

```
Level          Convention         Example
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Module file    snake_case         agent_state.py
Class name     PascalCase         AgentStateManager
Function name  snake_case         calculate_similarity()
Constant       UPPER_CASE         MAX_RETRIEVAL_K
Private        prefix_            _internal_method()
Test file      test_*.py          test_retriever.py
Test function  test_*             test_retrieve_basic()
Config file    snake_case.yaml    llm_config.yaml
Data file      snake_case_v*.json resumes_v1.json
Documentation  UPPER_CASE.md      DEVELOPMENT.md
```

### 13.2 Branch Naming Conventions

```
Type/Description    Example
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
feature/            feature/agent-reflection
bugfix/             bugfix/retrieval-recall
docs/               docs/cloud-native-guide
refactor/           refactor/agent-tools
perf/               perf/embedding-caching
ci/                 ci/github-actions
```

---

## 14. Best Practices

### 14.1 Code Organization

✅ **Recommended**
- Single responsibility per module (SRP)
- Import ordering: stdlib → third-party → local
- Type hints on all functions
- Unit-testable functions

❌ **Avoid**
- Oversized files (> 500 lines)
- Circular imports
- Magic numbers (use constants)
- Deep nesting (> 3 levels)

### 14.2 Test Organization

✅ **Recommended**
- AAA pattern: Arrange → Act → Assert
- Descriptive test names
- Use fixtures for shared setup
- Mock external dependencies

❌ **Avoid**
- Test interdependencies
- Business logic in tests
- Ignoring edge cases

### 14.3 Documentation Maintenance

✅ **Recommended**
- Docstring on every public function
- README always up-to-date
- Auto-generated API docs
- Architecture Decision Records (ADR)

❌ **Avoid**
- Outdated documentation
- Redundant documentation
- Documentation without examples

---

## 15. Quick Reference

### Initialize New Feature

```bash
# 1. Create branch
git checkout -b feature/new-feature

# 2. Implement feature
vim src/core/agent/new_tool.py
vim tests/unit/test_new_tool.py

# 3. Run local tests
poetry run pytest tests/unit/test_new_tool.py -v

# 4. Format and lint
poetry run black src/ tests/
poetry run pylint src/

# 5. Commit and PR
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### Add New Documentation

```bash
# 1. Determine doc location
docs/guides/NEW_GUIDE.md          # New guide
docs/architecture/NEW_DESIGN.md   # New architecture

# 2. Use template
# Reference docs/README.md for templates

# 3. Create bilingual versions
docs/guides/NEW_GUIDE.cn.md
docs/guides/NEW_GUIDE.en.md

# 4. Update index
# Edit docs/INDEX.md to add links
```

---

## 16. Related Files

- [Project Vision & Tech Stack](index.md)
- [Basic Considerations](00.basics.md)
- [Agent Scenario Design](AgentScenarios.en.md)
- [Development Guide](../guides/DEVELOPMENT.md) - To be created
- [Testing Guide](../guides/TESTING.md) - To be created
- [Cloud Native Guide](../guides/CLOUD_NATIVE.md) - To be created
