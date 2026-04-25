# VedaAide Project Structure and Naming Conventions

## Overview

This document defines the directory organization, naming conventions, and development workflow for the VedaAide project. The project focuses on demonstrating RAG + Agent core capabilities, distributed as a CLI tool.

---

## 1. Top-Level Directory Structure

```
VedaAide.py/
├── src/                          # Source code
├── tests/                        # Test code
├── docs/                         # Documentation
├── data/                         # Data directory
├── scripts/                      # Utility scripts
├── infra/                        # Infra assets (Docker only)
├── .github/                      # GitHub config (CI/CD, Copilot instructions)
├── docker-compose.yml            # Local Qdrant + LangFuse (optional)
├── pyproject.toml                # Python package config
├── .env.example                  # Environment variable template
└── README.md / README.cn.md
```

**Removed from repository (scope simplification)**:
- `infra/k8s/` — Kubernetes deployment manifests are no longer maintained
- `scripts/k8s/` — K8s deploy helpers are removed
- `skaffold.yaml` and `.skaffoldignore` — Skaffold workflow removed

**Scope notes**:
- `config/` — Configuration managed via `.env` + `pyproject.toml`, no separate directory needed

---

## 2. Source Code Directory (src/)

### 2.1 Core Layered Architecture

```
src/
├── __init__.py
├── core/                         # Core business logic layer
│   ├── __init__.py
│   ├── agent/                    # Agent modules
│   │   ├── __init__.py
│   │   ├── state.py              # Agent state definitions
│   │   ├── graph.py              # LangGraph state machine
│   │   ├── tools.py              # Agent tool definitions
│   │   └── memory.py             # Multi-turn conversation memory
│   │
│   ├── retrieval/                # Retrieval layer
│   │   ├── __init__.py
│   │   ├── indexer.py            # Index management (LlamaIndex + Qdrant)
│   │   ├── retriever.py          # Hybrid retrieval (BM25 + Vector)
│   │   └── deidentifier.py       # Data deidentification tool
│   │
│   ├── rag/                      # RAG pipeline
│   │   ├── __init__.py
│   │   ├── pipeline.py           # RAG orchestration
│   │   ├── prompt_manager.py     # Prompt management
│   │   └── dspy_compiler.py      # DSPy compilation optimization
│   │
│   └── evaluation/               # Evaluation framework
│       ├── __init__.py
│       ├── ragas_evaluator.py    # RAGAS quantitative evaluation
│       └── test_set_generator.py # Synthetic test set generation
│
├── infrastructure/               # Infrastructure layer
│   ├── __init__.py
│   ├── db/                       # Database interfaces
│   │   ├── __init__.py
│   │   └── qdrant.py             # Qdrant client
│   │
│   ├── llm/                      # LLM interface layer
│   │   ├── __init__.py
│   │   ├── azure_openai.py       # Azure OpenAI integration
│   │   ├── ollama.py             # Ollama local inference
│   │   └── embeddings.py         # Embedding management
│   │
│   └── observability/            # Observability (optional)
│       ├── __init__.py
│       └── tracing.py            # LangFuse integration (optional dependency)
│
├── cli/                          # CLI tool
│   ├── __init__.py
│   ├── __main__.py               # CLI entry point
│   └── commands/
│       ├── __init__.py
│       ├── index.py              # vedaaide index
│       ├── chat.py               # vedaaide chat
│       └── evaluate.py           # vedaaide eval
│
└── utils/                        # Utility functions
    ├── __init__.py
    ├── config.py                 # Config loading (python-dotenv)
    └── constants.py              # Constant definitions
```

### 2.2 Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Module files | snake_case | `agent_state.py`, `qdrant_client.py` |
| Class names | PascalCase | `AgentStateManager`, `HybridRetriever` |
| Function names | snake_case, verb-first | `retrieve_documents()`, `mask_pii()` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIEVAL_K`, `DEFAULT_TEMPERATURE` |
| Private members | single underscore prefix | `_validate_query()` |

---

## 3. Test Directory (tests/)

### 3.1 Test Structure

```
tests/
├── __init__.py
├── conftest.py                   # pytest fixtures
├── fixtures/                     # Test data and mocks
│   ├── sample_data.py            # Sample documents, JDs, resumes
│   └── mocks.py                  # Mock objects (LLM, Qdrant)
│
├── unit/                         # Unit tests
│   ├── __init__.py
│   ├── test_deidentifier.py      # Deidentification tests
│   ├── test_indexer.py           # Indexer module tests
│   ├── test_retriever.py         # Retriever module tests
│   ├── test_agent_tools.py       # Agent tool tests
│   ├── test_agent_state_machine.py # State machine tests
│   ├── test_agent_memory.py      # Memory management tests
│   ├── test_dspy_compiler.py     # DSPy optimization tests
│   └── test_ragas_evaluator.py   # Evaluation logic tests
│
└── integration/                  # Integration tests
    ├── __init__.py
    ├── test_rag_pipeline.py      # RAG end-to-end flow
    ├── test_agent_workflow.py    # Agent complete workflow
    └── test_end_to_end_workflow.py # Interview flow end-to-end
```

### 3.2 Coverage Targets

- **Unit tests**: ≥ 80% line coverage
- **Integration tests**: 100% for critical paths
- **Overall coverage**: ≥ 75%

---

## 4. Documentation Directory (docs/)

```
docs/
├── INDEX.md / INDEX.en.md        # Documentation index
├── PROJECT_STRUCTURE.cn.md / .en.md  # This document
│
├── planning/                     # Project planning
│   ├── main.cn.md / main.en.md   # Project vision and tech stack
│   ├── TASK_BREAKDOWN.cn.md / .en.md  # Task breakdown
│   ├── AgentScenarios.cn.md / .en.md  # Agent scenario design
│   └── 00.basics.md / .en.md    # Basic constraints and considerations
│
├── guides/                       # Development guides
│   ├── DEVELOPMENT.cn.md / .en.md  # Development workflow
│   └── CI_CD_SETUP.md            # CI/CD configuration
│
└── JD/                           # Job descriptions (reference)
    └── JD-001.md
```

---

## 5. Data Directory (data/)

```
data/
├── public_samples/               # Public sample datasets (no PII, committed to Git)
│   ├── README.md
│   ├── sample_resumes.json       # Mock resumes (≥ 10)
│   └── sample_job_postings.json  # Mock job postings (≥ 10)
│
├── working_datasets/             # User private data (.gitignore excluded)
│   └── README.md                 # Instructions for placing personal data
│
├── test_sets/                    # RAGAS evaluation test sets
│   └── interview_questions.json  # Synthetic interview questions (50+)
│
└── evaluation-results/           # Evaluation results (local, .gitignore excluded)
    └── README.md
```

---

## 6. Scripts Directory (scripts/)

```
scripts/
├── data/                         # Data processing scripts
│   ├── data_generator.py         # Sample data generation
│   └── load_public_samples.py    # Load public datasets
│
└── evaluation/                   # Evaluation scripts (to be created)
    ├── generate_test_set.py       # Generate synthetic test set
    ├── run_ragas.py               # RAGAS evaluation
    └── optimize_prompts.py        # DSPy prompt optimization
```

---

## 7. GitHub Configuration (.github/)

```
.github/
├── workflows/
│   ├── ci.yml                    # CI: tests and basic checks
│   └── code-quality.yml          # CI: extended quality checks
│
├── instructions/                 # Copilot instruction files
│   ├── project-context.instructions.md
│   ├── coding-standards.instructions.md
│   └── ...
│
├── skills/                       # Copilot Skills
│   ├── rag-engineering/
│   ├── evaluation/
│   └── testing/
│
└── ISSUE_TEMPLATE/
```

---

## 8. Key Configuration Files

### pyproject.toml
- Package metadata, dependencies, CLI entry points
- Dev tool configuration (ruff, pytest)
- Optional dependency groups (`langfuse`, etc.)

### docker-compose.yml
Contains only locally needed services:
- **qdrant**: Vector database (required)
- **langfuse + postgres + clickhouse**: Chain tracing (optional, for demo)

### .env.example
```dotenv
# Azure OpenAI
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_LLM=gpt-4o-mini
AZURE_OPENAI_DEPLOYMENT_EMBEDDING=text-embedding-3-small

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=vedaaide

# Ollama (optional)
OLLAMA_BASE_URL=http://localhost:11434

# LangFuse (optional)
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=http://localhost:3000
```
