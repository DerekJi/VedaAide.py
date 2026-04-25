# VedaAide 项目目录结构与命名规则

## 概述

本文档定义 VedaAide 项目的目录组织、命名规范和开发工作流。项目专注于 RAG + Agent 核心能力展示，以 CLI 工具的形式发布。

---

## 1. 顶级目录结构

```
VedaAide.py/
├── src/                          # 源代码
├── tests/                        # 测试代码
├── docs/                         # 文档
├── data/                         # 数据目录
├── scripts/                      # 工具脚本
├── infra/                        # 基础设施资产（仅 Docker）
├── .github/                      # GitHub 配置（CI/CD、Copilot 指令）
├── docker-compose.yml            # 本地 Qdrant + LangFuse（可选）
├── pyproject.toml                # Python 包配置
├── .env.example                  # 环境变量模板
└── README.md / README.cn.md
```

**仓库已移除（范围简化）**：
- `infra/k8s/` — 不再维护 Kubernetes 部署清单
- `scripts/k8s/` — 已移除 K8s 部署辅助脚本
- `skaffold.yaml` 与 `.skaffoldignore` — 已移除 Skaffold 工作流

**范围说明**：
- `config/` — 配置通过 `.env` + `pyproject.toml` 管理，无需单独目录

---

## 2. 源代码目录 (src/)

### 2.1 核心分层架构

```
src/
├── __init__.py
├── core/                         # 核心业务逻辑层
│   ├── __init__.py
│   ├── agent/                    # Agent 相关模块
│   │   ├── __init__.py
│   │   ├── state.py              # Agent 状态定义
│   │   ├── graph.py              # LangGraph 状态机
│   │   ├── tools.py              # Agent 工具定义
│   │   └── memory.py             # 多轮对话记忆
│   │
│   ├── retrieval/                # 检索层
│   │   ├── __init__.py
│   │   ├── indexer.py            # 索引管理（LlamaIndex + Qdrant）
│   │   ├── retriever.py          # 混合检索（BM25 + Vector）
│   │   └── deidentifier.py       # 数据脱敏工具
│   │
│   ├── rag/                      # RAG 管道
│   │   ├── __init__.py
│   │   ├── pipeline.py           # RAG 流程编排
│   │   ├── prompt_manager.py     # Prompt 管理
│   │   └── dspy_compiler.py      # DSPy 编译优化
│   │
│   └── evaluation/               # 评估框架
│       ├── __init__.py
│       ├── ragas_evaluator.py    # RAGAS 量化评估
│       └── test_set_generator.py # 合成测试集生成
│
├── infrastructure/               # 基础设施层
│   ├── __init__.py
│   ├── db/                       # 数据库接口
│   │   ├── __init__.py
│   │   └── qdrant.py             # Qdrant 客户端
│   │
│   ├── llm/                      # LLM 接口层
│   │   ├── __init__.py
│   │   ├── azure_openai.py       # Azure OpenAI 集成
│   │   ├── ollama.py             # Ollama 本地推理
│   │   └── embeddings.py         # Embedding 管理
│   │
│   └── observability/            # 可观测性（可选）
│       ├── __init__.py
│       └── tracing.py            # LangFuse 集成（可选依赖）
│
├── cli/                          # CLI 工具
│   ├── __init__.py
│   ├── __main__.py               # CLI 入口
│   └── commands/
│       ├── __init__.py
│       ├── index.py              # vedaaide index
│       ├── chat.py               # vedaaide chat
│       └── evaluate.py           # vedaaide eval
│
└── utils/                        # 工具函数
    ├── __init__.py
    ├── config.py                 # 配置加载（python-dotenv）
    └── constants.py              # 常量定义
```

### 2.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块文件 | snake_case | `agent_state.py`, `qdrant_client.py` |
| 类名 | PascalCase | `AgentStateManager`, `HybridRetriever` |
| 函数名 | snake_case，动词开头 | `retrieve_documents()`, `mask_pii()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRIEVAL_K`, `DEFAULT_TEMPERATURE` |
| 私有成员 | 单下划线前缀 | `_validate_query()` |

---

## 3. 测试目录 (tests/)

### 3.1 测试结构

```
tests/
├── __init__.py
├── conftest.py                   # pytest fixtures
├── fixtures/                     # 测试数据和 mocks
│   ├── sample_data.py            # 示例文档、JD、简历
│   └── mocks.py                  # Mock 对象（LLM、Qdrant）
│
├── unit/                         # 单元测试
│   ├── __init__.py
│   ├── test_deidentifier.py      # 脱敏测试
│   ├── test_indexer.py           # 索引模块测试
│   ├── test_retriever.py         # 检索模块测试
│   ├── test_agent_tools.py       # Agent 工具测试
│   ├── test_agent_state_machine.py # 状态机测试
│   ├── test_agent_memory.py      # 记忆管理测试
│   ├── test_dspy_compiler.py     # DSPy 优化测试
│   └── test_ragas_evaluator.py   # 评估逻辑测试
│
└── integration/                  # 集成测试
    ├── __init__.py
    ├── test_rag_pipeline.py      # RAG 端到端流程
    ├── test_agent_workflow.py    # Agent 完整工作流
    └── test_end_to_end_workflow.py # 面试流程端到端
```

### 3.2 测试覆盖率目标

- **单元测试**：≥ 80% 行覆盖
- **集成测试**：关键路径 100%
- **整体覆盖**：≥ 75%

---

## 4. 文档目录 (docs/)

```
docs/
├── INDEX.md / INDEX.en.md        # 文档索引
├── PROJECT_STRUCTURE.cn.md / .en.md  # 本文档
│
├── planning/                     # 项目规划
│   ├── main.cn.md / main.en.md   # 项目愿景和技术栈
│   ├── TASK_BREAKDOWN.cn.md / .en.md  # 任务分解
│   ├── AgentScenarios.cn.md / .en.md  # Agent 场景设计
│   └── 00.basics.md / .en.md    # 基本约束和考虑
│
├── guides/                       # 开发指南
│   ├── DEVELOPMENT.cn.md / .en.md  # 开发工作流
│   └── CI_CD_SETUP.md            # CI/CD 配置
│
└── JD/                           # 职位描述（参考）
    └── JD-001.md
```

---

## 5. 数据目录 (data/)

```
data/
├── public_samples/               # 公开示例数据集（无隐私信息，可提交 Git）
│   ├── README.md
│   ├── sample_resumes.json       # 模拟简历（≥ 10 份）
│   └── sample_job_postings.json  # 模拟招聘广告（≥ 10 份）
│
├── working_datasets/             # 用户私有数据（.gitignore 排除）
│   └── README.md                 # 说明如何放置个人数据
│
├── test_sets/                    # RAGAS 评估测试集
│   └── interview_questions.json  # 合成面试问题（50+）
│
└── evaluation-results/           # 评估结果（本地，.gitignore 排除）
    └── README.md
```

---

## 6. 脚本目录 (scripts/)

```
scripts/
├── data/                         # 数据处理脚本
│   ├── data_generator.py         # 示例数据生成
│   └── load_public_samples.py    # 加载公开数据集
│
└── evaluation/                   # 评估脚本（待创建）
    ├── generate_test_set.py       # 生成合成测试集
    ├── run_ragas.py               # RAGAS 评估
    └── optimize_prompts.py        # DSPy Prompt 优化
```

---

## 7. GitHub 配置 (.github/)

```
.github/
├── workflows/
│   ├── ci.yml                    # CI：测试与基础检查
│   └── code-quality.yml          # CI：扩展质量检查
│
├── instructions/                 # Copilot 指令文件
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

## 8. 关键配置文件

### pyproject.toml
- 包元数据、依赖、CLI entry points
- 开发工具配置（ruff、pytest）
- 可选依赖组（`langfuse` 等）

### docker-compose.yml
仅包含本地开发所需服务：
- **qdrant**：向量数据库（必需）
- **langfuse + postgres + clickhouse**：链路追踪（可选，用于演示）

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
