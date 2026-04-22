# VedaAide 项目目录结构与命名规则

## 概述

本文档定义 VedaAide 项目的目录组织、命名规范、代码分层和开发工作流，以支持高效的协作、测试、评估和云原生部署。

---

## 1. 顶级目录结构

```
VedaAide/
├── src/                          # 源代码根目录（待实现）
├── tests/                        # 测试代码（待实现）
├── docs/                         # 文档（项目规划、API、指南）
├── data/                         # 数据存储（简历、脱敏数据集、评估结果）
├── config/                       # 配置文件（待实现）
├── scripts/                      # 工具脚本
│   └── k8s/                      # K8s 部署脚本
├── infra/                        # 基础设施代码
│   ├── docker/                   # Dockerfile 模板
│   └── k8s/                      # Kubernetes 部署清单
├── .github/                      # GitHub 配置
│   ├── instructions/             # Copilot 指令文件
│   ├── prompts/                  # Copilot Chat 提示词
│   └── ISSUE_TEMPLATE/           # GitHub Issue 模板
├── docker-compose.yml            # 本地开发容器编排（Qdrant、LangFuse 等）
├── skaffold.yaml                 # Cloud Native 开发配置
├── pyproject.toml                # Python 项目配置（待初始化）
├── .gitignore
└── README.md / README.cn.md
```

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
│   │   ├── state.py              # Agent 状态定义（Pydantic models）
│   │   ├── graph.py              # LangGraph 构建和状态机
│   │   ├── tools.py              # Agent 工具定义
│   │   └── strategies.py         # 面试策略（HR/Tech）
│   │
│   ├── retrieval/                # 检索层
│   │   ├── __init__.py
│   │   ├── indexer.py            # 索引管理（Qdrant 集成）
│   │   ├── retriever.py          # 检索逻辑（向量/混合搜索）
│   │   ├── ranker.py             # 结果重排序
│   │   └── deidentifier.py       # 数据脱敏工具
│   │
│   ├── rag/                      # RAG 管道
│   │   ├── __init__.py
│   │   ├── pipeline.py           # RAG 流程编排
│   │   ├── prompt_manager.py     # Prompt 管理和版本控制
│   │   └── dspy_compiler.py      # DSPy 编译优化
│   │
│   └── evaluation/               # 评估框架
│       ├── __init__.py
│       ├── ragas_evaluator.py    # RAGAS 量化评估
│       ├── metrics.py            # 自定义评估指标
│       └── feedback.py           # 用户反馈处理
│
├── infrastructure/               # 基础设施层
│   ├── __init__.py
│   ├── db/                       # 数据库管理
│   │   ├── __init__.py
│   │   ├── cosmosdb.py           # Azure CosmosDB 驱动
│   │   ├── qdrant.py             # Qdrant 驱动和连接池
│   │   └── models.py             # ORM/数据模型定义
│   │
│   ├── llm/                      # LLM 接口层
│   │   ├── __init__.py
│   │   ├── azure_openai.py       # Azure OpenAI 集成
│   │   ├── ollama.py             # Ollama 本地推理
│   │   ├── embeddings.py         # Embedding 管理
│   │   └── base.py               # LLM 基类和协议
│   │
│   ├── observability/            # 可观测性
│   │   ├── __init__.py
│   │   ├── tracing.py            # LangFuse 集成
│   │   ├── metrics.py            # 指标收集（Token、成本）
│   │   ├── logger.py             # 自定义日志记录
│   │   └── decorators.py         # 观测装饰器
│   │
│   └── cache/                    # 缓存层
│       ├── __init__.py
│       └── redis_cache.py        # 可选：Redis 缓存
│
├── api/                          # API 层（可选：REST/WebSocket）
│   ├── __init__.py
│   ├── routes.py                 # FastAPI 路由
│   ├── schemas.py                # 请求/响应数据模型
│   └── middleware.py             # 中间件（认证、限流）
│
├── utils/                        # 工具函数
│   ├── __init__.py
│   ├── config.py                 # 配置加载（从 KeyVault）
│   ├── secrets.py                # 密钥管理
│   ├── validators.py             # 数据验证
│   ├── converters.py             # 数据转换
│   └── constants.py              # 常量定义
│
├── cli/                          # 命令行工具
│   ├── __init__.py
│   ├── __main__.py               # CLI 入口
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── init.py               # 初始化项目
│   │   ├── ingest.py             # 数据入库
│   │   ├── evaluate.py           # 运行评估
│   │   ├── serve.py              # 启动服务
│   │   └── demo.py               # 演示命令
│   └── args.py                   # 参数定义
│
└── main.py                       # 应用入口点
```

### 2.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| **模块文件** | snake_case，描述性 | `agent_state.py`, `cosmosdb_driver.py` |
| **类名** | PascalCase，带有后缀 | `AgentStateManager`, `CosmosDBConnector` |
| **函数名** | snake_case，动词开头 | `retrieve_contexts()`, `calculate_similarity()` |
| **常量** | UPPER_SNAKE_CASE | `MAX_RETRIEVAL_K`, `DEFAULT_MODEL_TEMPERATURE` |
| **Private 函数/属性** | 单下划线前缀 | `_validate_query()`, `_cache_key` |
| **Protected 函数/属性** | 双下划线前缀 | `__init_embeddings__()` |
| **类型提示** | 完整注解，使用 `typing` 模块 | `def retrieve(...) -> List[Document]:` |

---

## 3. 测试目录 (tests/)

### 3.1 测试结构

```
tests/
├── __init__.py
├── conftest.py                   # pytest 配置和 fixtures
├── fixtures/                     # 测试数据和 mocks
│   ├── __init__.py
│   ├── sample_data.py            # 示例文档、JD、简历
│   ├── mocks.py                  # Mock 对象（LLM、数据库）
│   └── deidentified_data.py      # 脱敏测试数据
│
├── unit/                         # 单元测试
│   ├── __init__.py
│   ├── test_deidentifier.py      # 数据脱敏测试
│   ├── test_retriever.py         # 检索模块测试
│   ├── test_ranker.py            # 重排序测试
│   ├── test_agent_tools.py       # Agent 工具测试
│   ├── test_dspy_compiler.py     # DSPy 优化测试
│   ├── test_evaluation.py        # 评估逻辑测试
│   └── test_utils.py             # 工具函数测试
│
├── integration/                  # 集成测试
│   ├── __init__.py
│   ├── test_rag_pipeline.py      # RAG 端到端流程
│   ├── test_agent_workflow.py    # Agent 完整工作流
│   ├── test_cosmosdb_persistence.py  # CosmosDB 数据持久化
│   ├── test_llm_integration.py   # LLM 集成（Mock）
│   └── test_observability.py     # LangFuse/日志集成
│
├── e2e/                          # 端到端测试
│   ├── __init__.py
│   ├── test_interview_flow.py    # 完整面试流程
│   ├── test_evaluation_pipeline.py  # 完整评估流程
│   └── test_cost_tracking.py     # 成本监控测试
│
└── benchmarks/                   # 性能测试
    ├── __init__.py
    ├── bench_retrieval.py        # 检索性能基准
    ├── bench_inference.py        # 推理性能基准
    └── bench_evaluation.py       # 评估性能基准
```

### 3.2 测试命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| **测试文件** | test_*.py 或 *_test.py | `test_retriever.py` |
| **测试函数** | test_* | `test_retrieve_with_empty_query()` |
| **测试类** | Test* | `TestRetriever` |
| **Fixture** | snake_case | `@pytest.fixture def sample_resume():` |
| **参数化测试** | 描述 case | `@pytest.mark.parametrize("model,expected", ...)` |

### 3.3 测试覆盖率目标

- **单元测试**：≥ 80% 行覆盖
- **集成测试**：关键路径 100%
- **E2E 测试**：核心业务流程 100%
- **整体覆盖**：≥ 75%

---

## 4. 文档目录 (docs/)

### 4.1 文档结构

```
docs/
├── README.md                     # 文档主入口
├── INDEX.md                      # 文档索引和快速导航
│
├── planning/                     # 项目规划文档
│   ├── index.md                  # 项目愿景（已有）
│   ├── index.en.md               # English version
│   ├── PROJECT_STRUCTURE.md      # 本文档
│   ├── PROJECT_STRUCTURE.en.md   # English version
│   ├── 00.basics.md              # 基本考虑（已有）
│   ├── AgentScenarios.cn.md      # Agent 场景设计
│   ├── AgentScenarios.en.md      # English version
│   └── ROADMAP.md                # 完整实施路线图
│
├── guides/                       # 开发指南
│   ├── SETUP.md                  # 开发环境设置
│   ├── SETUP.en.md               # English version
│   ├── DEVELOPMENT.md            # 开发工作流
│   ├── TESTING.md                # 测试指南
│   ├── DEPLOYMENT.md             # 部署指南
│   ├── CLOUD_NATIVE.md           # Cloud Native 开发指南
│   └── TROUBLESHOOTING.md        # 故障排查指南
│
├── architecture/                 # 架构文档
│   ├── OVERVIEW.md               # 系统架构概览
│   ├── DATA_FLOW.md              # 数据流设计
│   ├── AGENT_STATE_MACHINE.md    # Agent 状态机设计
│   ├── RAG_PIPELINE.md           # RAG 管道设计
│   ├── OBSERVABILITY.md          # 可观测性架构
│   └── SECURITY.md               # 安全设计
│
├── api/                          # API 文档
│   ├── REST_API.md               # REST API 规范
│   ├── SCHEMAS.md                # 数据模型规范
│   └── EXAMPLES.md               # 使用示例
│
├── evaluation/                   # 评估相关文档
│   ├── RAGAS_METRICS.md          # RAGAS 指标说明
│   ├── EVALUATION_FRAMEWORK.md   # 评估框架设计
│   ├── FEEDBACK_MECHANISM.md     # 反馈机制
│   └── BENCHMARK_REPORTS.md      # 基准测试报告
│
├── JD/                           # 需求文档
│   ├── JD-001.md                 # 原始职位描述（已有）
│   └── REQUIREMENTS.md           # 项目需求分析
│
└── reports/                      # 定期输出报告
    ├── evaluation_results/       # 评估结果报告
    ├── cost_analysis/            # 成本分析
    └── performance_metrics/      # 性能指标
```

### 4.2 文档命名规范

| 文档类型 | 规范 | 示例 |
|---------|------|------|
| **指南文档** | UPPER_SNAKE_CASE.md | `DEVELOPMENT.md`, `CLOUD_NATIVE.md` |
| **规划文档** | 小写或 index.md | `00.basics.md`, `index.md` |
| **架构文档** | UPPER_SNAKE_CASE.md | `DATA_FLOW.md`, `AGENT_STATE_MACHINE.md` |
| **中文版** | 文件名.cn.md | `SETUP.cn.md` |
| **英文版** | 文件名.en.md 或 文件名.md | `SETUP.en.md` |
| **报告** | 格式_日期.md | `evaluation_results_2026-04-22.md` |

---

## 5. 数据目录 (data/)

### 5.1 数据组织

```
data/
├── raw/                          # 原始数据
│   ├── resumes/                  # 个人简历
│   ├── projects/                 # 项目描述
│   ├── blogs/                    # 技术博客
│   └── job_descriptions/         # 职位描述
│
├── processed/                    # 处理后的数据
│   ├── deidentified/             # 脱敏数据集
│   │   ├── resumes_v1/
│   │   ├── projects_v1/
│   │   └── metadata.json         # 脱敏映射表
│   └── embeddings/               # 预计算 embedding
│
├── test/                         # 测试数据
│   ├── synthetic_qa/             # 合成问答对
│   ├── benchmark_queries/        # 基准测试查询
│   └── edge_cases/               # 边界情况测试数据
│
├── evaluation/                   # 评估相关数据
│   ├── test_sets/                # 评估测试集
│   ├── ragas_results/            # RAGAS 评估结果
│   ├── user_feedback/            # 用户反馈数据
│   └── metrics/                  # 指标数据
│
└── snapshots/                    # 数据快照（版本控制）
    ├── 2026-04-20/
    ├── 2026-04-21/
    └── 2026-04-22/
```

### 5.2 数据命名规范

| 数据类型 | 规范 | 示例 |
|---------|------|------|
| **数据文件** | snake_case_v<version>.json | `resumes_v1.json`, `embeddings_v2.pkl` |
| **测试集** | 类型_size_seed.json | `qa_pairs_100_seed42.json` |
| **评估结果** | ragas_<model>_<date>.json | `ragas_gpt4o_2026-04-22.json` |
| **快照目录** | YYYY-MM-DD | `2026-04-22/` |

---

## 6. 配置目录 (config/)

### 6.1 配置结构

```
config/
├── default.yaml                  # 默认配置
├── development.yaml              # 开发环境配置
├── staging.yaml                  # 暂存环境配置
├── production.yaml               # 生产环境配置
│
├── models/                       # 模型配置
│   ├── llm_config.yaml          # LLM 参数（温度、max_tokens 等）
│   ├── embedding_config.yaml    # Embedding 配置
│   └── dspy_config.yaml         # DSPy 编译配置
│
├── databases/                    # 数据库配置
│   ├── qdrant.yaml              # Qdrant 连接参数
│   ├── cosmosdb.yaml            # CosmosDB 连接参数
│   └── redis.yaml               # Redis 缓存配置（可选）
│
├── prompts/                      # Prompt 模板
│   ├── system_prompts.yaml      # 系统 Prompt
│   ├── interview_prompts.yaml   # 面试相关 Prompt
│   ├── evaluation_prompts.yaml  # 评估 Prompt
│   └── reflection_prompts.yaml  # 自反思 Prompt
│
├── observability/               # 可观测性配置
│   ├── langfuse.yaml            # LangFuse 配置
│   ├── logging.yaml             # 日志配置
│   └── metrics.yaml             # 指标收集配置
│
└── security/                    # 安全配置
    ├── deidentification.yaml    # 脱敏规则
    └── rate_limits.yaml         # 速率限制
```

### 6.2 配置管理

- **环境变量优先**：`CONFIG_ENV=production`
- **密钥存储**：Azure KeyVault，通过 `config.py` 加载
- **本地开发**：`.env.local`（不提交 Git）
- **版本控制**：所有 `.yaml` 提交，`.env` 文件 ignored

---

## 7. 脚本目录 (scripts/)

### 7.1 脚本组织

```
scripts/
├── data/                         # 数据处理脚本
│   ├── ingest_data.py           # 数据入库脚本
│   ├── deidentify_data.py       # 数据脱敏脚本
│   ├── generate_embeddings.py   # 预计算 embedding
│   └── validate_data.py         # 数据验证
│
├── evaluation/                   # 评估脚本
│   ├── run_ragas.py             # RAGAS 评估
│   ├── generate_test_set.py     # 生成合成测试集
│   ├── analyze_results.py       # 分析评估结果
│   └── compare_versions.py      # 版本对比
│
├── optimization/                # 优化脚本
│   ├── compile_dspy.py          # DSPy 编译
│   ├── tune_parameters.py       # 参数调优
│   └── benchmark.py             # 性能基准测试
│
├── deployment/                  # 部署脚本
│   ├── build_image.sh           # 构建 Docker 镜像
│   ├── deploy_k8s.sh            # Kubernetes 部署
│   └── health_check.sh          # 健康检查
│
├── maintenance/                 # 维护脚本
│   ├── cleanup_old_data.py      # 清理旧数据
│   ├── backup_database.py       # 数据库备份
│   └── monitor_costs.py         # 监控成本
│
└── dev/                         # 开发辅助脚本
    ├── setup_dev_env.sh         # 设置开发环境
    ├── generate_api_docs.py     # 生成 API 文档
    └── format_code.sh           # 代码格式化
```

### 7.2 脚本规范

| 脚本类型 | 扩展名 | 首行 | 示例 |
|---------|------|------|------|
| **Python 脚本** | .py | `#!/usr/bin/env python3` | `ingest_data.py` |
| **Shell 脚本** | .sh | `#!/bin/bash -e` | `deploy_k8s.sh` |
| **可执行** | 无 | 对应的首行 | `setup_dev_env` |

---

## 8. 基础设施目录 (infra/)

### 8.1 基础设施代码

```
infra/
├── docker/                       # Docker 相关
│   ├── Dockerfile               # 多阶段构建
│   ├── Dockerfile.dev           # 开发镜像
│   ├── docker-compose.yml       # 本地开发编排（MySQL、Redis 等）
│   └── .dockerignore
│
├── kubernetes/                   # Kubernetes 清单
│   ├── namespace.yaml            # 命名空间
│   ├── configmap.yaml            # 配置映射
│   ├── secret.yaml               # 密钥（从 KeyVault 外注入）
│   ├── deployment.yaml           # 应用 Deployment
│   ├── service.yaml              # 服务暴露
│   ├── ingress.yaml              # 入口配置
│   ├── hpa.yaml                  # 水平自动扩展
│   └── monitoring/               # 监控相关
│       ├── servicemonitor.yaml
│       └── grafana.yaml
│
├── skaffold/                     # Cloud Native 开发
│   ├── skaffold.yaml             # Skaffold 配置
│   └── skaffold-dev.yaml         # 开发模式配置
│
├── terraform/                    # 基础设施即代码（可选）
│   ├── main.tf                   # 主配置
│   ├── variables.tf              # 变量定义
│   ├── outputs.tf                # 输出定义
│   └── azure/                    # Azure 特定资源
│       ├── container_apps.tf
│       ├── cosmosdb.tf
│       └── keyvault.tf
│
└── scripts/                      # 基础设施脚本
    ├── setup_cluster.sh
    ├── deploy_monitoring.sh
    └── cleanup.sh
```

---

## 9. GitHub 配置 (.github/)

### 9.1 GitHub 配置结构

```
.github/
├── workflows/                    # GitHub Actions 工作流
│   ├── ci.yml                    # 持续集成（测试、linting）
│   ├── cd.yml                    # 持续部署
│   ├── evaluation.yml            # 定期评估任务
│   ├── cost-tracking.yml         # 成本监控
│   └── security-scan.yml         # 安全扫描
│
├── prompts/                      # Copilot Chat 提示配置
│   ├── .prompts.json             # 根配置文件
│   ├── project-context.md        # 项目上下文
│   ├── coding-standards.md       # 编码标准
│   ├── rag-development.md        # RAG 开发指南
│   └── testing-strategy.md       # 测试策略
│
├── skills/                       # Copilot Skills（可选）
│   ├── SKILLS.md                 # Skills 索引
│   ├── rag-engineering/          # RAG 工程 Skill
│   │   ├── SKILL.md
│   │   ├── examples.md
│   │   └── best_practices.md
│   ├── evaluation-design/        # 评估设计 Skill
│   │   ├── SKILL.md
│   │   └── checklist.md
│   └── cloud-native-dev/         # Cloud Native 开发 Skill
│       ├── SKILL.md
│       └── skaffold-guide.md
│
├── issue_template/               # Issue 模板
│   ├── bug_report.md
│   ├── feature_request.md
│   └── documentation.md
│
└── pull_request_template.md      # PR 模板
```

### 9.2 Copilot Prompts 示例结构

**`.prompts.json`** - 根配置
```json
{
  "version": "0.1.0",
  "defaultContext": {
    "codebase": "Python RAG Agent System",
    "includeFiles": [
      ".github/prompts/project-context.md",
      ".github/prompts/coding-standards.md"
    ]
  }
}
```

**编码标准提示示例** (`coding-standards.md`)
```markdown
# VedaAide 编码标准

## Python 风格
- PEP 8 遵循
- Type hints 必须
- Docstring 格式：Google 风格
- 行长限制：100 字符

## 模块组织
- 单一职责原则（SRP）
- 依赖注入
- 避免循环导入

## 错误处理
- 使用自定义异常
- 提供明确的错误消息
- 记录完整的堆栈跟踪
```

---

## 10. VSCode 配置 (.vscode/)

### 10.1 VSCode 结构

```
.vscode/
├── settings.json                 # VSCode 项目设置
├── launch.json                   # 调试配置
├── tasks.json                    # 任务配置
├── extensions.json               # 推荐扩展
└── copilot/
    ├── instructions.md           # Copilot 指令
    └── prompt-templates.md       # Prompt 模板
```

### 10.2 VSCode 设置示例

**`settings.json`**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true
  }
}
```

---

## 11. Cloud Native 开发工作流

### 11.1 使用 Skaffold 进行开发

#### 目的
- 自动同步代码到 K8s 集群
- 热更新（即刻看到代码变化）
- 简化本地开发流程

#### Skaffold 配置示例

**`skaffold.yaml`**
```yaml
apiVersion: skaffold/v4beta6
kind: Config
metadata:
  name: vedaaide

build:
  artifacts:
    - image: vedaaide-api
      docker:
        dockerfile: infra/docker/Dockerfile.dev

deploy:
  kubectl: {}

portForward:
  - resourceType: deployment
    resourceName: vedaaide-api
    port: 8080
    localPort: 8080

sync:
  manual:
    - src: "src/**/*.py"
      dest: /app/src

dev:
  watch:
    - infra/docker/Dockerfile.dev
    - src/**/*.py
```

#### 开发工作流

1. **初始化**
   ```bash
   skaffold config set default-repo localhost:5000
   skaffold debug --port-forward
   ```

2. **代码同步**
   - 修改 `src/` 中的 Python 文件
   - Skaffold 自动同步到容器
   - 应用自动重启或热更新

3. **调试**
   - VSCode 连接到远程调试器
   - 设置断点调试代码

4. **查看日志**
   ```bash
   skaffold logs -f
   ```

#### 性能考虑

| 方面 | 说明 | 优化建议 |
|------|------|---------|
| **同步延迟** | 通常 1-3 秒 | 仅同步改变的文件 |
| **网络开销** | 取决于集群网络 | 使用本地集群（Kind/Minikube）减少延迟 |
| **大文件** | 可能导致延迟 | 排除 `__pycache__`, `*.pyc` |
| **冷启动** | 首次构建较慢 | 使用 layer caching |

### 11.2 本地 vs 集群开发对比

| 方面 | 本地（docker-compose） | 集群（Skaffold） |
|------|----------------------|-----------------|
| **启动时间** | 快（< 10s） | 中等（20-30s） |
| **资源占用** | 低 | 中高 |
| **调试能力** | 很好 | 好 |
| **环境一致性** | 中等 | 很高 |
| **生产模拟** | 中等 | 很好 |

**推荐策略**：
- 早期开发：`docker-compose`
- 集成测试和微调：`Skaffold`

---

## 12. CI/CD 流水线

### 12.1 GitHub Actions 工作流

#### CI 流程 (ci.yml)

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Format check
        run: poetry run black --check src/ tests/
      - name: Lint
        run: poetry run pylint src/ tests/
      - name: Type check
        run: poetry run mypy src/
      - name: Run tests
        run: poetry run pytest tests/ --cov=src/
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

#### CD 流程 (cd.yml)

```yaml
name: CD

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push image
        run: |
          docker build -t ghcr.io/${{ github.repository }}:latest .
          docker push ghcr.io/${{ github.repository }}:latest
      - name: Deploy to ACA
        run: |
          az container app update \
            --name vedaaide-api \
            --image ghcr.io/${{ github.repository }}:latest
```

---

## 13. 命名规范总结

### 13.1 全局命名规范

```
级别          规范              示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模块文件      snake_case        agent_state.py
类名          PascalCase        AgentStateManager
函数名        snake_case        calculate_similarity()
常量          UPPER_CASE        MAX_RETRIEVAL_K
Private       前缀_            _internal_method()
测试文件      test_*.py         test_retriever.py
测试函数      test_*            test_retrieve_basic()
配置文件      snake_case.yaml   llm_config.yaml
数据文件      snake_case_v*.json resumes_v1.json
文档          UPPER_CASE.md     DEVELOPMENT.md
```

### 13.2 分支命名规范

```
类型/功能描述   示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━
feature/        feature/agent-reflection
bugfix/         bugfix/retrieval-recall
docs/           docs/cloud-native-guide
refactor/       refactor/agent-tools
perf/           perf/embedding-caching
ci/             ci/github-actions
```

---

## 14. 最佳实践

### 14.1 代码组织

✅ **推荐**
- 每个模块一个职责（SRP）
- 导入排序：stdlib → third-party → local
- 类型提示在所有函数
- 单元可测试的函数

❌ **避免**
- 过大的文件（> 500 行）
- 循环导入
- 魔法数字（使用常量）
- 过度嵌套（> 3 层）

### 14.2 测试组织

✅ **推荐**
- AAA 模式：Arrange → Act → Assert
- 描述性的测试名
- 使用 fixtures 共享设置
- Mock 外部依赖

❌ **避免**
- 测试间依赖
- 测试中的业务逻辑
- 忽略 edge cases

### 14.3 文档维护

✅ **推荐**
- Docstring 在每个公共函数
- README 始终最新
- API 文档自动生成
- 架构决策记录 (ADR)

❌ **避免**
- 过时的文档
- 冗余文档
- 无例子的文档

---

## 15. 快速参考

### 初始化新功能

```bash
# 1. 创建分支
git checkout -b feature/new-feature

# 2. 实现功能
vim src/core/agent/new_tool.py
vim tests/unit/test_new_tool.py

# 3. 本地测试
poetry run pytest tests/unit/test_new_tool.py -v

# 4. 格式化和 Lint
poetry run black src/ tests/
poetry run pylint src/

# 5. 提交和 PR
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### 添加新文档

```bash
# 1. 确定文档位置
docs/guides/NEW_GUIDE.md          # 新指南
docs/architecture/NEW_DESIGN.md   # 新架构

# 2. 使用模板
# 参考 docs/README.md 获取模板

# 3. 中英文版本
docs/guides/NEW_GUIDE.cn.md
docs/guides/NEW_GUIDE.en.md

# 4. 更新索引
# 编辑 docs/INDEX.md 添加链接
```

---

## 16. 相关文件

- [项目愿景与技术栈](index.md)
- [基本考虑](00.basics.md)
- [Agent 场景设计](AgentScenarios.cn.md)
- [开发指南](../guides/DEVELOPMENT.md) - 待创建
- [测试指南](../guides/TESTING.md) - 待创建
- [Cloud Native 指南](../guides/CLOUD_NATIVE.md) - 待创建
