# VedaAide Documentation Index

## 📚 Quick Navigation

### 🎯 Project Planning (planning/)

- **[Project Vision & Implementation Roadmap](planning/main.en.md)** - Project vision, tech stack, core features, implementation roadmap, showcase highlights
- **[Task Breakdown](planning/TASK_BREAKDOWN.en.md)** - Break down each phase into actionable tasks with objectives, acceptance criteria, time estimates
- **[Project Structure & Naming Conventions](PROJECT_STRUCTURE.en.md)** - Code repository organization, naming rules, test structure, CI/CD, Cloud Native development
- **[Basic Considerations](planning/00.basics.md)** - Project constraints (cost, data, scenarios, etc.)
- **[Agent Scenario Design](planning/AgentScenarios.en.md)** - Agent configurations for different use cases

### 📖 Development Guides (guides/)

- **[Development Environment Setup](guides/SETUP.en.md)** - To be created
- **[Development Workflow](guides/DEVELOPMENT.md)** - To be created
- **[Testing Guide](guides/TESTING.md)** - To be created
- **[Deployment Guide](guides/DEPLOYMENT.md)** - To be created
- **[Cloud Native Development](guides/CLOUD_NATIVE.md)** - To be created
- **[Troubleshooting](guides/TROUBLESHOOTING.md)** - To be created

### 🏗️ Architecture Documentation (architecture/)

- **[System Architecture Overview](architecture/OVERVIEW.md)** - To be created
- **[Data Flow Design](architecture/DATA_FLOW.md)** - To be created
- **[Agent State Machine](architecture/AGENT_STATE_MACHINE.md)** - To be created
- **[RAG Pipeline Design](architecture/RAG_PIPELINE.md)** - To be created
- **[Observability Architecture](architecture/OBSERVABILITY.md)** - To be created
- **[Security Design](architecture/SECURITY.md)** - To be created

### 🔌 API Documentation (api/)

- **[REST API Specification](api/REST_API.md)** - To be created
- **[Data Model Specification](api/SCHEMAS.md)** - To be created
- **[Usage Examples](api/EXAMPLES.md)** - To be created

### 📊 Evaluation Documentation (evaluation/)

- **[RAGAS Metrics Explanation](evaluation/RAGAS_METRICS.md)** - To be created
- **[Evaluation Framework Design](evaluation/EVALUATION_FRAMEWORK.md)** - To be created
- **[Feedback Mechanism](evaluation/FEEDBACK_MECHANISM.md)** - To be created
- **[Benchmark Test Reports](evaluation/BENCHMARK_REPORTS.md)** - To be created

### 📋 Requirements Documentation (JD/)

- **[Job Description JD-001](JD/JD-001.md)** - Original job requirements
- **[Project Requirements Analysis](JD/REQUIREMENTS.md)** - To be created

---

## 📑 Organize by Purpose

### 🎯 Project Planning & Task Management

1. Understand the project: [Project Vision & Roadmap](planning/main.en.md)
2. Review the roadmap: [Implementation Roadmap](planning/main.en.md)
3. **Get task list**: [Task Breakdown Document](planning/TASK_BREAKDOWN.en.md) - includes time estimates, priorities, acceptance criteria
4. Create GitHub Issues: Use [task template](.github/ISSUE_TEMPLATE/task.md)

### 🚀 Getting Started (First-time Contributors)

1. Read [Project Vision & Roadmap](planning/main.en.md) - Understand project goals
2. Check [Project Structure](PROJECT_STRUCTURE.en.md) - Learn code organization
3. Follow [Development Environment Setup](guides/SETUP.en.md) - Configure dev environment
4. Start [Development Workflow](guides/DEVELOPMENT.md) - Begin coding

### 💡 Submitting Code

1. Review [Project Structure](PROJECT_STRUCTURE.en.md) - **Naming Conventions**
2. Reference [Testing Guide](guides/TESTING.md) - Write tests
3. Follow [Development Workflow](guides/DEVELOPMENT.md) - Workflow steps
4. Run CI checks before submitting PR

### 🧪 Evaluation & Optimization

1. Check [RAGAS Metrics Explanation](evaluation/RAGAS_METRICS.md)
2. Reference [Evaluation Framework Design](evaluation/EVALUATION_FRAMEWORK.md)
3. Review [Benchmark Test Reports](evaluation/BENCHMARK_REPORTS.md)

### 🐳 Deployment & Operations

1. Understand [System Architecture](architecture/OVERVIEW.md)
2. Reference [Deployment Guide](guides/DEPLOYMENT.md)
3. Learn [Cloud Native Development](guides/CLOUD_NATIVE.md)
4. Check [Troubleshooting](guides/TROUBLESHOOTING.md)

### 🔒 Security & Compliance

1. Read [Security Design](architecture/SECURITY.md)
2. Check [Project Structure](PROJECT_STRUCTURE.en.md) - **Data Management** section
3. Reference [Data Flow Design](architecture/DATA_FLOW.md)

### 📊 Monitoring & Observability

1. Read [Observability Architecture](architecture/OBSERVABILITY.md)
2. Reference [Data Flow Design](architecture/DATA_FLOW.md)
3. Check [RAGAS Metrics Explanation](evaluation/RAGAS_METRICS.md)

---

## 📋 Documentation Maintenance

### Bilingual Documentation Policy

**Important Rule**: All documentation updates must synchronize Chinese and English versions

- Chinese version: `filename.cn.md`
- English version: `filename.en.md`
- Exception: README uses `README.md` (English) and `README.cn.md` (Chinese)

For detailed guidelines, see [Documentation Bilingual Guidelines](.github/prompts/documentation-bilingual.instructions.md)

### Update Documentation

All documentation should follow these rules:

1. **Naming Convention**:
   - Planning docs: `*.cn.md` (Chinese) and `*.en.md` (English)
   - Guides/Architecture docs: `UPPER_SNAKE_CASE.cn.md` and `UPPER_SNAKE_CASE.en.md`
   - Exception: README uses `README.md` (English) and `README.cn.md` (Chinese)

2. **Keep Versions Synchronized**:
   - When updating Chinese version, update English version simultaneously
   - When updating English version, update Chinese version simultaneously
   - Avoid allowing one version to become outdated

3. **Structure**:
   - Each major doc should have Chinese and English versions
   - Use clear title hierarchy
   - Add quick reference tables and code examples
   - Include "Related Documents" links

4. **Version Control**:
   - All `.md` files committed to Git
   - Update outdated content regularly
   - Use commit messages to explain changes
   - Reference bilingual versions in commit message: `docs(cn/en):`

### Adding New Documentation

1. **Decide appropriate directory location**
2. **Create both Chinese and English versions**
   - `filename.cn.md` for Chinese
   - `filename.en.md` for English
   - Exception: README uses `README.md` (English) and `README.cn.md` (Chinese)
3. **Use standard naming conventions**
4. **Update this index document** (both Chinese and English)
5. **Add cross-references** to related docs

### Temporary Files

Development process generates many temporary documents and test scripts. Please use `.temp/` directory:
- See [.temp/README.md](.temp/README.md) for guidelines
- This directory is git-ignored but has `.gitkeep`

### Creating GitHub Issues

For each task in [Task Breakdown](planning/TASK_BREAKDOWN.en.md):
1. Use the [task template](.github/ISSUE_TEMPLATE/task.md)
2. Include task number (e.g., "1.1", "2.3") in the issue title
3. Reference acceptance criteria from the task breakdown

---

## 🔗 External Links

- **[GitHub Repository](https://github.com/yourusername/VedaAide)**
- **[GitHub Pages Demo](https://yourusername.github.io/VedaAide)**
- **[LangChain Documentation](https://python.langchain.com/)**
- **[LlamaIndex Documentation](https://docs.llamaindex.ai/)**
- **[Qdrant Documentation](https://qdrant.tech/documentation/)**
- **[RAGAS Documentation](https://ragas.io/)**

---

## 🤝 Contributing

Found documentation issues or have suggestions?

1. Create an Issue: Clearly describe the problem or suggestion
2. Submit a PR: Submit improved documentation
3. Reference [Contributing Guidelines](../CONTRIBUTING.md)

---

## 📝 Last Updated

- **Date**: 2026-04-22
- **Maintainers**: VedaAide Team
- **Version**: 1.0.0
