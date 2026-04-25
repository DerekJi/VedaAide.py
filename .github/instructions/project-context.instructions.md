# VedaAide Project Core Context

## Project Goal

VedaAide is a CLI-based RAG Agent system that:
- Demonstrates end-to-end RAG engineering (deidentification, indexing, hybrid retrieval, evaluation)
- Showcases agentic workflow design (LangGraph state machine + LlamaIndex hierarchical retrieval)
- Distributed as a PyPI package (`pip install vedaaide`)
- Runs locally with minimal infrastructure (Qdrant + optional LangFuse via Docker Compose)

## Core Tech Stack

| Layer | Technology | Purpose |
|------|------|------|
| LLM Orchestration | LangChain / LangGraph | Agent state machine, tool invocation |
| Data Indexing | LlamaIndex | Hierarchical indexing, hybrid retrieval |
| Prompt Optimization | DSPy | Prompt compilation and optimization |
| Vector Database | Qdrant | Local Docker (no cloud) |
| Configuration | python-dotenv (.env) | Environment variable management |
| Retrieval Strategy | Hybrid Search | BM25 + Vector Search |
| Inference Models | Azure OpenAI | gpt-4o-mini (default), text-embedding-3-small |
| Local Inference | Ollama | Llama-3, Phi-3 (optional) |
| Observability | LangFuse | Chain tracing (optional, local Docker only) |
| RAG Evaluation | RAGAS | Faithfulness, Relevance, Recall |
| Distribution | PyPI | `pip install vedaaide` |

## Module Structure

| Module | Responsibility | Main Classes |
|------|------|--------|
| `src/core/agent/` | Agent state machine, tools, memory | `AgentGraph`, `ToolRegistry`, `AgentMemory` |
| `src/core/retrieval/` | Indexing, hybrid retrieval, deidentification | `Indexer`, `HybridRetriever`, `Deidentifier` |
| `src/core/rag/` | RAG pipeline, prompt management, DSPy | `RAGPipeline`, `PromptManager`, `DSPyCompiler` |
| `src/core/evaluation/` | RAGAS evaluation, test set generation | `RAGASEvaluator`, `TestSetGenerator` |
| `src/infrastructure/db/` | Qdrant client | `QdrantClient` |
| `src/infrastructure/llm/` | LLM interfaces | `AzureOpenAIProvider`, `OllamaProvider`, `EmbeddingManager` |
| `src/infrastructure/observability/` | LangFuse tracing (optional) | `LangFuseTracer` |
| `src/utils/` | Config loading, constants | `ConfigLoader` |
| `src/cli/` | CLI commands | `index`, `chat`, `eval` |

## CLI Commands

```bash
vedaaide index <docs_dir>   # Index documents into Qdrant
vedaaide chat               # Start interactive interview session
vedaaide eval               # Run RAGAS evaluation
```

## Mandatory Design Principles

- **SRP**: Each class/function has one responsibility
- **DRY**: Abstract shared logic, no copy-paste
- **Dependency Injection**: Dependencies injected via constructors
- **Async First**: All I/O operations use `async/await`
- **Externalized Configuration**: All keys/configs read from `.env` via `python-dotenv`

## Dependency Management

- Package Manager: `poetry`, config: `pyproject.toml` + `poetry.lock`
- Python Version: 3.10+
- Linting: `ruff` (replaces black + isort + flake8 + pylint)
- Import Order: stdlib → third-party → local
