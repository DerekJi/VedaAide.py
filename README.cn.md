# VedaAide: 面试模拟 RAG Agent

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**一个基于 CLI 的 RAG Agent，使用脱敏候选人文档模拟面试对话**

[English Version](README.md) | [文档](docs/INDEX.md) | [项目结构](docs/PROJECT_STRUCTURE.cn.md)

</div>

## VedaAide 是什么？

VedaAide 是一个实用的 RAG（检索增强生成）Agent，展示端到端的 LLM 工程能力：

- **Agentic RAG**：LangGraph 状态机 + LlamaIndex 分层检索
- **混合搜索**：BM25 + Vector，精准匹配专有名词
- **量化评估**：RAGAS 指标（Faithfulness、Relevance、Recall）
- **Prompt 优化**：DSPy 编译，支持 Azure OpenAI 和 Ollama
- **隐私优先**：入库前统一 PII 脱敏

## 快速开始

### 安装

```bash
pip install vedaaide
```

### 配置

复制 `.env.example` 为 `.env` 并填写你的凭证：

```bash
cp .env.example .env
# 编辑 .env，填写 Azure OpenAI Key 和 Qdrant URL
```

在本地启动 Qdrant：

```bash
docker compose up qdrant -d
```

### 使用

```bash
# 索引你的文档
vedaaide index ./my_documents/

# 开始面试对话
vedaaide chat

# 运行 RAGAS 评估
vedaaide eval
```

## 核心特性

### 1. 分层文档索引（LlamaIndex）
- 递归检索：摘要 → 章节 → 段落
- 混合搜索：BM25 + Vector，精准匹配 Kafka、Redis 等专有名词
- 元数据过滤：按技术栈、时间段、项目类型过滤

### 2. Agentic 面试工作流（LangGraph）
- 状态机：Query → Retrieval → Reasoning → Reflection → Response
- 三个工具：`ExperienceComparator`、`TechnicalDeepDive`、`InterviewStrategySelector`
- 多轮对话记忆，上下文感知

### 3. 量化评估（RAGAS + DSPy）
- RAGAS：Faithfulness、Relevance、Recall 指标
- DSPy Prompt 编译：支持本地（Ollama）和云端（Azure OpenAI）模型
- 合成测试集生成（50+ 面试问题）

### 4. 可选：LangFuse 链路追踪
```bash
# 本地启动 LangFuse（用于演示/调试）
docker compose up -d

# 访问 http://localhost:3000
```

## 项目结构

```
VedaAide.py/
├── src/
│   ├── core/
│   │   ├── agent/         # LangGraph 状态机 + 工具
│   │   ├── retrieval/     # LlamaIndex 索引 + 混合检索 + 脱敏
│   │   ├── rag/           # RAG 管道 + DSPy 编译
│   │   └── evaluation/    # RAGAS 评估 + 测试集生成
│   ├── infrastructure/
│   │   ├── db/qdrant.py   # Qdrant 客户端
│   │   ├── llm/           # Azure OpenAI + Ollama
│   │   └── observability/ # LangFuse 追踪（可选）
│   └── cli/               # vedaaide index / chat / eval
├── tests/
│   ├── unit/
│   └── integration/
├── data/
│   ├── public_samples/    # 示例简历 + 招聘广告
│   └── evaluation-results/
├── scripts/evaluation/    # RAGAS + DSPy 脚本
└── docker-compose.yml     # Qdrant + LangFuse（可选）
```

详细结构见 [docs/PROJECT_STRUCTURE.cn.md](docs/PROJECT_STRUCTURE.cn.md)。

## 开发环境

```bash
# 克隆并安装
git clone https://github.com/DerekJi/VedaAide.py.git
cd VedaAide.py
poetry install

# 运行测试
poetry run pytest tests/unit/

# 代码检查
poetry run ruff check src/ tests/
```

## 文档

- [项目愿景与规划](docs/planning/main.cn.md)
- [任务分解](docs/planning/TASK_BREAKDOWN.cn.md)
- [项目结构](docs/PROJECT_STRUCTURE.cn.md)
- [Agent 场景设计](docs/planning/AgentScenarios.cn.md)
