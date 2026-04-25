# VedaAide: RAG Agent for Interview Simulation

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**A CLI-based RAG Agent that simulates interview conversations using deidentified candidate documents**

[中文版本](README.cn.md) | [Documentation](docs/INDEX.en.md) | [Project Structure](docs/PROJECT_STRUCTURE.en.md)

</div>

## What is VedaAide?

VedaAide is a practical RAG (Retrieval-Augmented Generation) Agent that demonstrates end-to-end LLM engineering skills:

- **Agentic RAG**: LangGraph state machine + LlamaIndex hierarchical retrieval
- **Hybrid Search**: BM25 + Vector search for domain-term precision
- **Quantitative Evaluation**: RAGAS metrics (Faithfulness, Relevance, Recall)
- **Prompt Optimization**: DSPy compilation for Azure OpenAI and Ollama
- **Privacy-first**: Unified PII deidentification before indexing

## Quick Start

### Install

```bash
pip install vedaaide
```

### Configure

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your Azure OpenAI key and Qdrant URL
```

Start Qdrant locally:

```bash
docker compose up qdrant -d
```

### Use

```bash
# Index your documents
vedaaide index ./my_documents/

# Start interview conversation
vedaaide chat

# Run RAGAS evaluation
vedaaide eval
```

## Key Features

### 1. Hierarchical Data Indexing (LlamaIndex)
- Recursive retrieval: summary → section → chunk
- Hybrid search: BM25 + Vector for precise matching on domain terms (Kafka, Redis, etc.)
- Metadata filtering by tech stack, time period, project type

### 2. Agentic Interview Workflow (LangGraph)
- State machine: Query → Retrieval → Reasoning → Reflection → Response
- Three tools: `ExperienceComparator`, `TechnicalDeepDive`, `InterviewStrategySelector`
- Multi-turn memory with context awareness

### 3. Quantitative Evaluation (RAGAS + DSPy)
- RAGAS: Faithfulness, Relevance, Recall metrics
- DSPy prompt compilation for local (Ollama) and cloud (Azure OpenAI) models
- Synthetic test set generation (50+ interview questions)

### 4. Optional: LangFuse Tracing
```bash
# Start LangFuse locally (for demo/debugging)
docker compose up -d

# Access at http://localhost:3000
```

## Project Structure

```
VedaAide.py/
├── src/
│   ├── core/
│   │   ├── agent/         # LangGraph state machine + tools
│   │   ├── retrieval/     # LlamaIndex indexer + hybrid retriever + deidentifier
│   │   ├── rag/           # RAG pipeline + DSPy compiler
│   │   └── evaluation/    # RAGAS evaluator + test set generator
│   ├── infrastructure/
│   │   ├── db/qdrant.py   # Qdrant client
│   │   ├── llm/           # Azure OpenAI + Ollama
│   │   └── observability/ # LangFuse tracing (optional)
│   └── cli/               # vedaaide index / chat / eval
├── tests/
│   ├── unit/
│   └── integration/
├── data/
│   ├── public_samples/    # Sample resumes + job postings
│   └── evaluation-results/
├── scripts/evaluation/    # RAGAS + DSPy scripts
└── docker-compose.yml     # Qdrant + LangFuse (optional)
```

See [docs/PROJECT_STRUCTURE.en.md](docs/PROJECT_STRUCTURE.en.md) for full details.

## Development Setup

```bash
# Clone and install
git clone https://github.com/DerekJi/VedaAide.py.git
cd VedaAide.py
poetry install

# Run tests
poetry run pytest tests/unit/

# Lint
poetry run ruff check src/ tests/
```

## Documentation

- [Project Vision & Roadmap](docs/planning/main.en.md)
- [Task Breakdown](docs/planning/TASK_BREAKDOWN.en.md)
- [Project Structure](docs/PROJECT_STRUCTURE.en.md)
- [Agent Scenarios](docs/planning/AgentScenarios.en.md)
