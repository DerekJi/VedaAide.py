# VedaAide Project Skills

This directory contains specialized SKILL files for VedaAide project development. These skills are automatically recognized and loaded by the AI agent based on keywords in your requests.

## Available Skills

### 0. GitHub CLI Workflow (Meta Skill)
**File**: `github-cli-workflow/SKILL.md`

Essential workflow for GitHub automation and issue management:
- Creating, updating, and managing GitHub Issues
- Pull request operations and reviews
- Batch operations and automation
- Authentication and multi-account management
- Integration with CI/CD pipelines

**Triggers on keywords**:
- English: gh, github cli, issue, pull request, pr, workflow, automation, create issue
- 中文: GitHub, gh, 工作流, 批量操作, Issue, 拉取请求

---

### 1. RAG Engineering
**File**: `rag-engineering/SKILL.md`

Covers VedaAide's RAG (Retrieval-Augmented Generation) system:
- Hybrid search optimization (BM25 + Vector)
- Qdrant vector database management
- Embedding models and chunking strategies
- Retrieval pipeline architecture
- Metadata filtering and recursive retrieval
- Prompt version control

**Triggers on keywords**:
- English: retrieval, rag, embedding, qdrant, ranking, hybrid-search, vector, semantic
- 中文: 检索, RAG, 嵌入, 向量, 重排序, 混合搜索, 语义搜索, 向量数据库

---

### 2. Testing Strategy
**File**: `testing/SKILL.md`

Comprehensive testing framework for VedaAide:
- Unit tests with pytest and mocking
- Integration tests for RAG pipeline
- End-to-end tests for complete workflows
- Fixtures and parametrized tests
- RAGAS evaluation integration
- Persistence and integration testing patterns

**Triggers on keywords**:
- English: test, unit, integration, e2e, benchmark, ragas, pytest, mock, coverage
- 中文: 测试, 单元测试, 集成测试, E2E, 基准测试, 测试覆盖率, 测试金字塔

---

### 3. Legacy Infrastructure (Deprecated)
**File**: `cloud-native/SKILL.md`

This skill is kept only for historical context and migration notes.
Current project workflow is local CLI + Docker Compose.

**Triggers on keywords**:
- English: legacy infra, deprecated infrastructure, migration notes
- 中文: 历史基础设施, 已废弃流程, 迁移说明

---

### 4. Evaluation Strategy
**File**: `evaluation/SKILL.md`

RAG evaluation and optimization framework:
- RAGAS metrics (Faithfulness, Relevance, Recall)
- Synthetic test set generation
- DSPy prompt optimization
- User feedback mechanisms
- Evaluation reports and analysis
- Compilation-based prompt improvement

**Triggers on keywords**:
- English: evaluation, ragas, metrics, feedback, optimization, faithfulness, relevance, recall, dspy
- 中文: 评估, 反馈, RAGAS, 指标, 优化, 忠实度, 相关性, 质量评估

---

## How It Works

When you ask a question or request work on VedaAide:

1. **Agent detects keywords** in your message
2. **Matching SKILL is automatically loaded** with best practices
3. **Context-aware guidance** is applied to your work

### Examples

```
User: "I need to optimize Qdrant retrieval performance"
→ rag-engineering SKILL loaded (detected: qdrant, retrieval, optimize)

User: "写单元测试"
→ testing SKILL loaded (detected: 测试)

User: "How do I migrate old infra docs?"
→ cloud-native SKILL loaded (detected: legacy infra, migration)

User: "改进RAGAS指标"
→ evaluation SKILL loaded (detected: RAGAS, 指标, 改进)
```

## File Structure

```
.github/skills/
├── README.md (this file)
├── github-cli-workflow/
│   └── SKILL.md
├── rag-engineering/
│   └── SKILL.md
├── testing/
│   └── SKILL.md
├── cloud-native/
│   └── SKILL.md
└── evaluation/
    └── SKILL.md
```

## Adding New Skills

To create a new SKILL:

1. Create a new directory under `.github/skills/`
2. Create a `SKILL.md` file with metadata header:

```yaml
---
name: Skill Name
description: Clear description of what this skill covers
applyTo: "applicable/file/patterns/**"
keywords:
  - keyword1
  - keyword2
  - 关键词1
  - 关键词2
whenToUse: |
  When working on specific tasks...
---

# Skill Content

Your best practices and guidelines here...
```

3. Use both English and Chinese keywords for better discoverability
4. Include practical examples and code snippets

## Migration from .prompts.json

These project-level skills replace the manual configuration in `.prompts.json`. The prompts.json configuration is kept for backward compatibility but is no longer the primary mechanism for context loading.

### Previous vs. Current

**Before**:
- Manually configured `.prompts.json`
- Required keyword matching configuration
- Project-specific prompts in a separate location

**Now**:
- Dedicated `.github/skills/` directory
- Automatic SKILL detection
- Better integration with AI agent workflows
- Standard SKILL.md format

---

**Last Updated**: April 22, 2026
