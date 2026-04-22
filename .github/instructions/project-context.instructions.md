# VedaAide Project Core Context

## Project Goal

VedaAide is an intelligent RAG Agent system that:
- Explores interactive dialogue simulation with deidentified candidate data
- Demonstrates end-to-end RAG engineering (deidentification, indexing, retrieval, evaluation)
- Showcases systematic design approach (observability, security, cost control)
- Operates within resource constraints: only using free/discounted Azure, GitHub, Ollama resources

## Core Tech Stack

| Layer | Technology | Purpose |
|------|------|------|
| LLM Orchestration | LangChain / LangGraph | Agent state management, tool invocation |
| Data Indexing | LlamaIndex | Data indexing, retrieval augmentation |
| Prompt Optimization | DSPy | Prompt compilation and optimization |
| Vector Database | Qdrant | Local Docker + Cloud |
| Persistent Storage | Azure CosmosDB | Retrieval data, user feedback |
| Retrieval Strategy | Hybrid Search | BM25 + Vector Search |
| Inference Models | Azure OpenAI | gpt-4o (reasoning), gpt-4o-mini (cost optimization), text-embedding-3-small |
| Local Inference | Ollama | Llama-3, Phi-3 |
| Observability | LangFuse | Chain tracing (replaces LangSmith) |
| RAG Evaluation | RAGAS | Faithfulness, Relevance, Recall |
| Deployment | Docker + Kubernetes | Kind local + AKS production |
| Development Workflow | Skaffold | Cloud Native hot-reload |

## Module Structure

| Module | Responsibility | Main Classes |
|------|------|--------|
| `src/core/agent/` | Agent logic, tools, strategies | `AgentStateManager`, `ToolRegistry` |
| `src/core/retrieval/` | Indexing, retrieval, reranking | `Indexer`, `HybridRetriever`, `Ranker` |
| `src/core/rag/` | RAG pipeline, prompt management | `RAGPipeline`, `PromptManager` |
| `src/core/evaluation/` | Evaluation and feedback | `RAGASEvaluator`, `FeedbackHandler` |
| `src/infrastructure/db/` | Database drivers | `CosmosDBClient`, `QdrantClient` |
| `src/infrastructure/llm/` | LLM interfaces | `AzureOpenAIProvider`, `OllamaProvider` |
| `src/infrastructure/observability/` | Observability | `LangFuseTracer`, `MetricsCollector` |
| `src/utils/` | Utility functions, config, constants | `ConfigManager`, `SecretsManager` |
| `src/cli/` | Command-line tools | Various CLI commands |

## Mandatory Design Principles

- **SRP**: Each class/function has only one clear responsibility, avoiding "all-purpose" utility classes
- **DRY**: Abstract shared logic, prohibit copy-pasting business code
- **Dependency Injection**: Dependencies injected via constructors, prohibit hardcoding external service instantiation inside classes
- **Async First**: All I/O operations must use `async/await`, no blocking calls allowed
- **Observability**: All LLM and retrieval calls must be traced through LangFuse
- **Externalized Configuration**: Keys and configs read via `ConfigManager` from environment variables, no hardcoding

## Dependency Management

- Package Manager: `poetry`, config files: `pyproject.toml` + `poetry.lock`
- Python Version: 3.10+
- Import Order: stdlib → third-party → local
