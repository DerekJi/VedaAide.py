# VedaAide Project Context

> **Purpose of this document**: Quick reference handbook for development scenarios (debugging, deployment, feature development workflow).
>
> **Project core context** (tech stack, module structure, design principles) is defined in
> `.github/instructions/project-context.instructions.md` and applies automatically to all files.

---

## Project Goal

VedaAide is an intelligent RAG Agent system that:
- Simulates personalized interview conversations based on deidentified experience data
- Demonstrates end-to-end RAG engineering capability (data deidentification, indexing, retrieval, evaluation)
- Showcases systematic design rigor (observability, security, cost control)
- Uses only available free/discounted Azure, GitHub, Ollama resources

## Key Tech Stack

### LLM Orchestration
- **LangChain / LangGraph**: Agent state management, tool invocation
- **LlamaIndex**: Data indexing, retrieval augmentation
- **DSPy**: Prompt compilation and optimization

### Data and Vectors
- **Qdrant**: Vector database (local Docker + cloud)
- **Azure CosmosDB**: Persistent storage (retrieval data, feedback)
- **Hybrid Search**: BM25 + Vector Search

### Model Integration
- **Azure OpenAI**: gpt-4o (reasoning), gpt-4o-mini (cost optimization), text-embedding-3-small
- **Ollama**: Local inference (Llama-3, Phi-3)
- **DeepSeek API**: Cost optimization alternative

### Observability and Evaluation
- **LangFuse**: Chain tracing (replaces LangSmith)
- **RAGAS**: Quantitative evaluation (Faithfulness, Relevance, Recall)
- **Custom Observability**: Decorator interception, CosmosDB persistence, cost monitoring

### Deployment
- **Packaging**: PyPI distribution (`pip install vedaaide`)
- **Local runtime**: Docker Compose for optional local services

## Core Modules

| Module | Responsibility | Main Classes |
|------|------|--------|
| `core/agent/` | Agent logic, tools, strategies | `AgentStateManager`, `ToolRegistry` |
| `core/retrieval/` | Indexing, retrieval, reranking | `Indexer`, `HybridRetriever`, `Ranker` |
| `core/rag/` | RAG pipeline, prompt management | `RAGPipeline`, `PromptManager` |
| `core/evaluation/` | Evaluation and feedback | `RAGASEvaluator`, `FeedbackHandler` |
| `infrastructure/db/` | Database drivers | `CosmosDBClient`, `QdrantClient` |
| `infrastructure/llm/` | LLM interfaces | `AzureOpenAIProvider`, `OllamaProvider` |
| `infrastructure/observability/` | Observability | `LangFuseTracer`, `MetricsCollector` |
| `utils/` | Utility functions, config, constants | `ConfigManager`, `SecretsManager` |
| `cli/` | Command-line tools | Various CLI commands |

## Code Organization Principles

### SRP (Single Responsibility)
- Each class/function has one clear responsibility
- Avoid "all-purpose" utility classes
- Use design patterns (Factory, Strategy)

### Dependency Management
- Dependency injection (DI) over hardcoding
- Complete type hints (Python 3.10+ typing)
- Import order: stdlib → third-party → local

### Test-Driven Development
- Unit tests (80%+ coverage)
- Integration tests (100% critical paths)
- E2E tests (100% business flows)
- Mocking external dependencies (LLM, DB)

### Async and Performance
- Use `async/await` for I/O operations
- Background task processing: evaluation, logging
- Caching optimization: embedding, retrieval results

## 12-Factor App Principles

1. **Codebase**: Single Git repository
2. **Dependencies**: `pyproject.toml` + `poetry.lock`
3. **Config**: Environment variables + Azure KeyVault
4. **Backing services**: Qdrant, CosmosDB, Azure OpenAI as attached services
5. **Build/Run/Release**: Docker containerization
6. **Processes**: Stateless, easily horizontally scalable
7. **Port binding**: Self-contained HTTP service
8. **Concurrency**: Support for process and thread concurrency
9. **Disposability**: Fast startup/shutdown, graceful shutdown
10. **Dev/Prod Parity**: Consistent environment between local and cloud
11. **Logs**: Output to stdout/stderr
12. **Admin tasks**: CLI tooling support

## Common Scenarios

### Developing New Features
1. Branch from `develop`: `git checkout -b feature/xxx`
2. Implement in `src/`, write tests in `tests/`
3. Run `pytest` locally to verify
4. Format and lint: `poetry run ruff check --fix src/ && poetry run ruff format src/`
5. Submit PR, CI checks automatically

### Debugging Issues
1. Enable LangFuse tracing: `LANGFUSE_PUBLIC_KEY=xxx`
2. Check retrieval data in CosmosDB
3. Use VSCode debugger or `pdb`
4. Check information recorded by observability decorators

### Deploying to Production
1. Build package: `poetry build`
2. Publish to PyPI (manual or CI workflow)
3. Verify install: `pip install vedaaide`
4. Verify CLI: `vedaaide --help`
5. Monitor runtime logs in local/dev environments

## More Information

- **[Complete Project Vision](../../docs/planning/index.md)** - Tech stack, feature design, implementation roadmap
- **[Project Structure](../../docs/planning/PROJECT_STRUCTURE.en.md)** - Directory organization, naming conventions, test structure
- **[Basic Considerations](../../docs/planning/00.basics.en.md)** - Project constraints and design considerations
- **[Agent Scenarios Design](../../docs/planning/AgentScenarios.en.md)** - Different usage scenarios
