# VedaAide: Intelligent RAG Agent for Recruitment Interview Simulation

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**An intelligent, cost-optimized RAG Agent that simulates realistic recruitment interviews using deidentified candidate data**

[中文版本](README.cn.md) | [Documentation](docs/INDEX.en.md) | [Project Structure](docs/PROJECT_STRUCTURE.en.md)

</div>

## 🎯 What is VedaAide?

VedaAide is a practical RAG (Retrieval-Augmented Generation) Agent designed to:

- **Simulate interview conversations** using deidentified candidate profiles
- **Explore RAG patterns and implementation** through a realistic application
- **Optimize costs** via hybrid LLM strategy (Azure OpenAI, Ollama, DeepSeek)
- **Demonstrate systematic design** through observability, evaluation, and security practices

The system combines **hierarchical document indexing**, **agentic workflows**, **cost-aware LLM routing**, and **quantitative evaluation metrics**.

## ✨ Key Features

### 1. **Intelligent Data Indexing**
- Hybrid search combining BM25 (lexical) and vector-based (semantic) retrieval
- Recursive retrieval strategy across 3 levels: summary → document → chunk
- Qdrant vector database with custom metadata filtering
- Support for incremental and batch index updates

### 2. **Agentic Interview Workflow**
- State machine-based agent orchestration using LangGraph
- Dynamic context retrieval based on interview progression
- Multi-turn conversation with context awareness
- Automatic tool selection and execution

### 3. **Deidentification & Privacy**
- Unified masking layer for PII (SSN, email, phone, address)
- Consistent deidentification across retrieval and generation
- Verification rules to prevent accidental exposure
- Audit trails for compliance

### 4. **Quantitative Evaluation**
- RAGAS metrics: Faithfulness (≥0.90), Relevance (≥0.90), Recall (≥0.85)
- DSPy automatic prompt compilation and optimization
- User feedback collection and analysis
- Daily, weekly, and monthly evaluation cycles

### 5. **Production-Grade Observability**
- LangFuse tracing for complete chain instrumentation
- Query → Retrieval → Generation → Reflection pipeline visibility
- Custom observability decorators
- Performance and cost monitoring

### 6. **Cost Optimization**
- Intelligent LLM routing (gpt-4o for reference → gpt-4o-mini for cost)
- Ollama local inference for development and non-critical tasks
- DeepSeek API as fallback option
- Cost-per-query tracking and optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry 1.8+
- Docker & Docker Compose
- Podman Machine (for local K8s development with Kind)
- Azure credentials (OpenAI API key, CosmosDB connection string)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/yourusername/VedaAide.git
cd VedaAide

# Install dependencies using Poetry
poetry install

# Activate virtual environment
poetry shell
```

### 2. Configure Environment

Create `.env` file in project root:

```bash
# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-4o

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Azure CosmosDB
COSMOS_CONNECTION_STRING=your-connection-string
COSMOS_DATABASE=vedaaide
COSMOS_CONTAINER=candidates

# LangFuse (v3 - uses PostgreSQL and ClickHouse)
LANGFUSE_URL=http://localhost:3000

# Environment
ENV=development
LOG_LEVEL=INFO
```

### 3. Start Services

```bash
# Start Qdrant, PostgreSQL, ClickHouse, and LangFuse
podman compose up -d

# Verify services are running
podman compose ps

# Check services are accessible
curl http://localhost:6333/health  # Qdrant
curl http://localhost:3000/api/health  # LangFuse
```

**Available services:**
- **Qdrant** (http://localhost:6333) - Vector database for embeddings
- **LangFuse** (http://localhost:3000) - Tracing and monitoring for LLM calls
- **PostgreSQL** (localhost:5432) - Database backend for LangFuse
- **ClickHouse** (http://localhost:8123) - Analytics database for LangFuse

### 4. Run First Interview

```bash
# Load sample data
poetry run python scripts/data/load_samples.py

# Start interactive interview
poetry run python -m vedaaide.cli interview --profile-id sample-001

# Or run as API
poetry run python -m vedaaide.api --host 0.0.0.0 --port 8080
```

## 📋 Project Structure

```
VedaAide/
├── src/                        # Source code root (planned)
│   ├── core/                    # Business logic
│   ├── infrastructure/         # DB, LLM, Observability adapters
│   ├── api/                    # REST API server
│   ├── cli/                    # Command-line interface
│   └── utils/                  # Shared utilities
│
├── tests/                      # Test code (planned)
├── config/                     # Configuration files (planned)
│
├── docs/
│   ├── INDEX.md / INDEX.en.md  # Documentation index
│   ├── PROJECT_STRUCTURE.cn/en.md
│   ├── planning/               # Planning docs & roadmap
│   ├── JD/                     # Job descriptions
│   └── guides/ architecture/ api/ evaluation/  # To be created
│
├── data/                       # Sample & evaluation data
├── scripts/
│   └── k8s/                    # Deployment scripts
├── infra/
│   ├── docker/                 # Dockerfile templates
│   └── k8s/                    # Kubernetes manifests
├── .github/
│   ├── instructions/           # Copilot instruction files
│   ├── prompts/               # Copilot Chat prompts
│   └── ISSUE_TEMPLATE/
├── docker-compose.yml
├── skaffold.yaml
└── README.md / README.cn.md

See [PROJECT_STRUCTURE.en.md](docs/PROJECT_STRUCTURE.en.md) for detailed structure.
```

## 🛠️ Development

### Code Quality Standards

All contributions follow:
- **PEP 8** with 100-character line limit
- **Type hints** for all functions (mandatory)
- **Google-style docstrings**
- **≥80% test coverage** for new code
- **Black** for formatting, **Pylint** for linting

```python
# Example: RAG module with proper standards
def generate_answer(
    query: str,
    contexts: list[str],
    metadata: dict[str, Any] | None = None
) -> str:
    """
    Generate answer using contexts with deidentification.
    
    Args:
        query: User question
        contexts: Retrieved context chunks
        metadata: Optional metadata for filtering
    
    Returns:
        Generated answer with deidentified content
    
    Raises:
        ValueError: If contexts are empty
        PII_EXPOSURE_ERROR: If deidentification fails
    """
    # Implementation
```

### Running Tests

```bash
# Unit tests (fast)
poetry run pytest tests/unit/ -v

# Integration tests
poetry run pytest tests/integration/ -v

# All tests with coverage
poetry run pytest --cov=src --cov-report=html

# E2E tests (marked as slow, run separately)
poetry run pytest -m e2e -v
```

### Code Review Checklist

- [ ] Type hints on all functions
- [ ] Tests for new functionality (≥80% coverage)
- [ ] No hardcoded secrets or credentials
- [ ] Docstrings follow Google style
- [ ] Logging at appropriate levels
- [ ] No duplicate code (DRY principle)
- [ ] Updated related documentation

See [coding-standards.md](.github/prompts/coding-standards.md) for detailed guidelines.

## ☸️ Cloud Native Development

### Skaffold Workflow (Local Development)

VedaAide uses **Skaffold** for rapid local Kubernetes development:

```bash
# Initialize Kind cluster and local registry
skaffold config set --global default-repo 172.25.16.1:5000
skaffold debug

# Code changes automatically sync (1-2 second latency)
# Edit src/core/agent.py → automatically deployed to cluster
```

**Benefits:**
- Code synchronization in 1-2 seconds
- Hot reload without rebuilding images
- Real Kubernetes environment for integration testing
- Debugging with VSCode integration

### Local Deployment

```bash
# Using podman compose (quick start)
podman compose up -d

# Using Kubernetes (integration testing)
skaffold run

# Cleanup
skaffold delete
```

See [cloud-native-dev.md](.github/prompts/cloud-native-dev.md) for detailed setup.

## 📊 Evaluation & Metrics

### RAGAS Evaluation

Run quantitative evaluation on retrieval and generation:

```bash
# Daily evaluation (100 samples)
poetry run python scripts/evaluation/run_ragas.py \
  --dataset data/evaluation/qa_dataset.json \
  --sample-size 100

# Weekly evaluation (all samples) + DSPy optimization
poetry run python scripts/evaluation/full_evaluation.py \
  --compile-dspy \
  --output weekly_report
```

**Target Metrics:**
| Metric | Target | Purpose |
|--------|--------|---------|
| Faithfulness | ≥0.90 | Answer based on retrieved context |
| Relevance | ≥0.90 | Context relevant to query |
| Recall | ≥0.85 | Retrieved all relevant documents |
| Latency | ≤500ms | Total query → answer time |
| Satisfaction | ≥85% | User feedback score |

### DSPy Optimization

Automatically optimize prompts using training examples:

```python
from src.core.rag.dspy_compiler import compile_prompt

optimized_agent = compile_prompt(
    task=interview_agent,
    train_set=training_examples,  # 100 examples
    metric=faithfulness_score,
    num_trials=50
)
# Expected improvement: 0.75 → 0.92 Faithfulness
```

See [evaluation-strategy.md](.github/prompts/evaluation-strategy.md) for details.

## 🤖 AI-Assisted Development

VedaAide is configured for **VSCode Copilot Chat**:

```
Copilot detects your question → loads project context automatically
"How do I write a retrieval function?" 
→ Loads: project context + RAG development guide + coding standards
```

**Available Skills:**
- `rag-engineering` - Retrieval and generation best practices
- `testing` - Unit, integration, E2E testing strategies  
- `cloud-native` - Skaffold and Kubernetes workflows
- `evaluation` - RAGAS metrics and DSPy optimization

Configured in [.github/prompts/.prompts.json](.github/prompts/.prompts.json).

## 📚 Documentation

- **[Index](docs/INDEX.en.md)** - Quick navigation by purpose
- **[Project Vision & Roadmap](docs/planning/main.en.md)** - Goals and roadmap
- **[Project Structure](docs/PROJECT_STRUCTURE.en.md)** - Directory organization and naming conventions
- **[Coding Standards](.github/prompts/coding-standards.md)** - Python best practices
- **[RAG Development](.github/prompts/rag-development.md)** - Retrieval and generation patterns
- **[Testing Strategy](.github/prompts/testing-strategy.md)** - Test structure and examples
- **[Cloud Native](.github/prompts/cloud-native-dev.md)** - Skaffold and Kubernetes
- **[Evaluation](.github/prompts/evaluation-strategy.md)** - RAGAS and DSPy

## 🔄 Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/add-interview-warmup
# or: feature/*, bugfix/*, docs/*
```

### 2. Make Changes Following Standards
- Write type-hinted code
- Add tests (≥80% coverage for your code)
- Use Copilot Chat for guidance: `How do I implement...?`

### 3. Run Quality Checks
```bash
# Formatting
poetry run black src/ tests/

# Linting
poetry run pylint src/

# Type checking
poetry run mypy src/

# Tests
poetry run pytest --cov=src
```

### 4. Commit with Conventional Commits
```bash
git commit -m "feat(agent): add interview warmup context loading

- Loads recent interview patterns for continuity
- Implements 3-level recursive retrieval
- Adds 15 new unit tests (coverage: 92%)

Closes #123"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/add-interview-warmup
# Create PR on GitHub, request review
```

See [docs/guides/DEVELOPMENT.md](docs/guides/DEVELOPMENT.md) for detailed workflow.

## 🚢 Deployment

### Production Deployment

```bash
# Build production image
docker build -f Dockerfile.prod -t registry.example.com/vedaaide:v1.0.0 .

# Deploy to AKS
kubectl apply -f infra/production/deployment.yaml

# Verify deployment
kubectl get pods -n vedaaide -w
kubectl logs -f -n vedaaide svc/vedaaide-api
```

### Monitoring

```bash
# View metrics in LangFuse dashboard
# https://cloud.langfuse.com/

# Check application logs
poetry run tail -f logs/vedaaide.log

# Performance monitoring
poetry run python scripts/monitoring/check_performance.py
```

## 🤝 Contributing

We welcome contributions! Please:

1. **Read** [PROJECT_STRUCTURE.en.md](docs/PROJECT_STRUCTURE.en.md) to understand the codebase
2. **Follow** [coding-standards.md](.github/prompts/coding-standards.md)
3. **Write tests** for any new functionality
4. **Update documentation** if adding new features
5. **Use Copilot Chat** in VSCode for assistance: `@workspace How do I...?`

### Report Issues

- **Bug**: Use template in `.github/ISSUE_TEMPLATE/bug.md`
- **Feature**: Use template in `.github/ISSUE_TEMPLATE/feature.md`
- **Question**: Open a discussion

## 📈 Roadmap

**Phase 1: Foundation** ✅
- Core RAG agent implementation
- Hybrid search and retrieval
- Basic evaluation framework

**Phase 2: Enhancement** (Current)
- Deidentification layer
- Multi-scenario interview support
- DSPy prompt optimization

**Phase 3: Optimization**
- Cost optimization with LLM routing
- Performance benchmarking
- User feedback loop

**Phase 4: Scale**
- Multi-candidate batch processing
- Enterprise integration
- Advanced analytics

See [docs/planning/main.en.md](docs/planning/main.en.md) for details.

## 🔐 Security

- All credentials stored in `.env` (never committed)
- Azure KeyVault integration for production
- Deidentification on all PII fields
- Audit logs for all data access
- No hardcoded secrets in code

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/VedaAide/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/VedaAide/discussions)

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - LLM orchestration
- [LlamaIndex](https://www.llamaindex.ai/) - Document indexing
- [Qdrant](https://qdrant.tech/) - Vector database
- [RAGAS](https://ragas.io/) - Evaluation metrics
- [DSPy](https://github.com/stanfordnlp/dspy) - Prompt optimization
- [LangFuse](https://langfuse.com/) - Observability

---

<div align="center">

**[📖 Documentation](docs/INDEX.en.md) | [🚀 Quick Start](#-quick-start) | [💬 Discussions](https://github.com/yourusername/VedaAide/discussions)**

Made with ❤️ for intelligent recruitment

</div>
