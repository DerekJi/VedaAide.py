# VedaAide: 智能 RAG Agent 招聘面试模拟系统

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**一个智能、成本优化的 RAG Agent，使用脱敏候选人数据模拟逼真的招聘面试**

[English Version](README.md) | [文档](docs/INDEX.md) | [项目结构](docs/PROJECT_STRUCTURE.cn.md)

</div>

## 🎯 VedaAide 是什么？

VedaAide 是一个探索实用 RAG（检索增强生成）技术的智能 Agent，设计用于：

- **面试对话模拟**：使用脱敏数据模拟对话体验
- **RAG 技术探索**：通过真实应用深入了解 RAG 实现
- **成本优化**：采用混合 LLM 策略（Azure OpenAI、Ollama、DeepSeek）
- **系统化设计**：体现可观测性、评估机制、安全实践

整个系统结合了**分层文档索引**、**Agent 工作流**、**成本意识的 LLM 路由**和**量化评估指标**。

## ✨ 核心特性

### 1. **智能数据索引**
- 混合搜索：结合 BM25（词汇）和向量（语义）检索
- 递归检索策略：跨 3 个层级（摘要 → 文档 → 段落）
- Qdrant 向量数据库：支持自定义元数据过滤
- 增量和批量索引更新支持

### 2. **Agent 面试工作流**
- 基于状态机的 Agent 编排（使用 LangGraph）
- 基于面试进度的动态上下文检索
- 多轮对话与上下文感知
- 自动工具选择和执行

### 3. **隐私保护与脱敏**
- 统一 PII 脱敏层（SSN、邮箱、电话、地址）
- 检索和生成过程的一致性脱敏
- 防止意外泄露的验证规则
- 合规审计日志

### 4. **量化评估**
- RAGAS 指标：忠实度（≥0.90）、相关性（≥0.90）、召回率（≥0.85）
- DSPy 自动 Prompt 编译和优化
- 用户反馈收集和分析
- 日/周/月评估周期

### 5. **生产级可观测性**
- LangFuse 追踪：完整链路可视化
- 查询 → 检索 → 生成 → 自我反思 管道可见性
- 自定义可观测性装饰器
- 性能和成本监控

### 6. **成本优化**
- 智能 LLM 路由（gpt-4o 用于参考 → gpt-4o-mini 用于成本）
- Ollama 本地推理：开发和非关键任务
- DeepSeek API 作为备选方案
- 单位查询成本追踪和优化

## 🚀 快速开始

### 前置要求
- Python 3.10 或更高版本
- Poetry 1.8+
- Docker & Docker Compose
- Podman Machine（用于使用 Kind 的本地 K8s 开发）
- Azure 凭证（OpenAI API 密钥、CosmosDB 连接字符串）

### 1. 克隆并设置

```bash
# 克隆仓库
git clone https://github.com/yourusername/VedaAide.git
cd VedaAide

# 使用 Poetry 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

### 2. 配置环境

在项目根目录创建 `.env` 文件：

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

# LangFuse（v3 - 使用 PostgreSQL 和 ClickHouse）
LANGFUSE_URL=http://localhost:3000

# 环境
ENV=development
LOG_LEVEL=INFO
```

### 3. 启动服务

```bash
# 启动 Qdrant、PostgreSQL、ClickHouse 和 LangFuse
podman compose up -d

# 验证服务是否运行
podman compose ps

# 检查服务可访问性
curl http://localhost:6333/health  # Qdrant
curl http://localhost:3000/api/health  # LangFuse
```

**可用的服务：**
- **Qdrant** (http://localhost:6333) - 嵌入向量数据库
- **LangFuse** (http://localhost:3000) - LLM 调用的追踪和监控
- **PostgreSQL** (localhost:5432) - LangFuse 的数据库后端
- **ClickHouse** (http://localhost:8123) - LangFuse 的分析数据库

### 4. 运行第一个面试

```bash
# 加载示例数据
poetry run python scripts/data/load_samples.py

# 启动交互式面试
poetry run python -m vedaaide.cli interview --profile-id sample-001

# 或作为 API 运行
poetry run python -m vedaaide.api --host 0.0.0.0 --port 8080
```

## 📋 项目结构

```
VedaAide/
├── src/                        # 源代码根目录（待实现）
│   ├── core/                    # 核心业务逻辑
│   ├── infrastructure/         # DB、LLM、可观测性适配器
│   ├── api/                    # REST API 服务器
│   ├── cli/                    # 命令行接口
│   └── utils/                  # 共享工具函数
│
├── tests/                      # 测试代码（待实现）
├── config/                     # 配置文件（待实现）
│
├── docs/
│   ├── INDEX.md / INDEX.en.md  # 文档索引
│   ├── PROJECT_STRUCTURE.cn/en.md
│   ├── planning/               # 规划文档和路线图
│   ├── JD/                     # 职位描述
│   └── guides/ architecture/ api/ evaluation/  # 待创建
│
├── data/                       # 示例和评估数据
├── scripts/
│   └── k8s/                    # 部署脚本
├── infra/
│   ├── docker/                 # Dockerfile 模板
│   └── k8s/                    # Kubernetes 清单
├── .github/
│   ├── instructions/           # Copilot 指令文件
│   ├── prompts/               # Copilot Chat 提示词
│   └── ISSUE_TEMPLATE/
├── docker-compose.yml
├── skaffold.yaml
└── README.md / README.cn.md

详见 [PROJECT_STRUCTURE.cn.md](docs/PROJECT_STRUCTURE.cn.md)
```

## 🛠️ 开发

### 代码质量标准

所有贡献必须遵循：
- **PEP 8**（100 字符行限制）
- **类型提示**（强制要求）
- **Google 风格 Docstring**
- **≥80% 测试覆盖率**（新代码）
- **Black** 格式化、**Pylint** Lint 检查

```python
# 示例：具有适当标准的 RAG 模块
def generate_answer(
    query: str,
    contexts: list[str],
    metadata: dict[str, Any] | None = None
) -> str:
    """
    使用上下文生成答案并进行脱敏处理。

    参数：
        query: 用户问题
        contexts: 检索的上下文块
        metadata: 可选的过滤元数据

    返回值：
        带有脱敏内容的生成答案

    异常：
        ValueError: 如果上下文为空
        PII_EXPOSURE_ERROR: 如果脱敏失败
    """
    # 实现
```

### 运行测试

```bash
# 单元测试（快速）
poetry run pytest tests/unit/ -v

# 集成测试
poetry run pytest tests/integration/ -v

# 所有测试（含覆盖率）
poetry run pytest --cov=src --cov-report=html

# E2E 测试（标记为慢速，单独运行）
poetry run pytest -m e2e -v
```

### 代码审查清单

- [ ] 所有函数都有类型提示
- [ ] 新功能都有测试（≥80% 覆盖率）
- [ ] 没有硬编码的密钥或凭证
- [ ] Docstring 遵循 Google 风格
- [ ] 日志级别适当
- [ ] 没有重复代码（DRY 原则）
- [ ] 已更新相关文档

详见 [coding-standards.md](.github/prompts/coding-standards.md)

## ☸️ Cloud Native 开发

### Skaffold 工作流（本地开发）

VedaAide 使用 **Skaffold** 实现快速本地 Kubernetes 开发：

```bash
# 初始化 Kind 集群和本地镜像仓库
skaffold config set --global default-repo 172.25.16.1:5000
skaffold debug

# 代码变化自动同步（1-2 秒延迟）
# 编辑 src/core/agent.py → 自动部署到集群
```

**优势：**
- 代码同步延迟 1-2 秒
- 无需重新构建镜像的热重载
- 真实 Kubernetes 环境用于集成测试
- VSCode 集成调试

### 本地部署

```bash
# 使用 podman compose（快速开始）
podman compose up -d

# 使用 Kubernetes（集成测试）
skaffold run

# 清理
skaffold delete
```

详见 [cloud-native-dev.md](.github/prompts/cloud-native-dev.md)

## 📊 评估和指标

### RAGAS 评估

在检索和生成上运行量化评估：

```bash
# 日评估（100 个样本）
poetry run python scripts/evaluation/run_ragas.py \
  --dataset data/evaluation/qa_dataset.json \
  --sample-size 100

# 周评估（所有样本）+ DSPy 优化
poetry run python scripts/evaluation/full_evaluation.py \
  --compile-dspy \
  --output weekly_report
```

**目标指标：**
| 指标 | 目标 | 说明 |
|------|------|------|
| 忠实度 | ≥0.90 | 答案基于检索内容 |
| 相关性 | ≥0.90 | 内容与查询相关 |
| 召回率 | ≥0.85 | 检索到所有相关文档 |
| 延迟 | ≤500ms | 查询到答案总时间 |
| 满意度 | ≥85% | 用户反馈评分 |

### DSPy 优化

使用训练示例自动优化 Prompt：

```python
from src.core.rag.dspy_compiler import compile_prompt

optimized_agent = compile_prompt(
    task=interview_agent,
    train_set=training_examples,  # 100 个示例
    metric=faithfulness_score,
    num_trials=50
)
# 预期改进：0.75 → 0.92 忠实度
```

详见 [evaluation-strategy.md](.github/prompts/evaluation-strategy.md)

## 🤖 AI 辅助开发

VedaAide 配置了 **VSCode Copilot Chat**：

```
Copilot 检测问题 → 自动加载项目上下文
"我如何编写检索函数？"
→ 加载：项目上下文 + RAG 开发指南 + 编码标准
```

**可用技能：**
- `rag-engineering` - 检索和生成最佳实践
- `testing` - 单元、集成、E2E 测试策略
- `cloud-native` - Skaffold 和 Kubernetes 工作流
- `evaluation` - RAGAS 指标和 DSPy 优化

配置在 [.github/prompts/.prompts.json](.github/prompts/.prompts.json)

## 📚 文档

- **[索引](docs/INDEX.md)** - 按用途的快速导航
- **[项目愿景与路线规划](docs/planning/main.cn.md)** - 目标和路线图
- **[项目结构](docs/PROJECT_STRUCTURE.cn.md)** - 目录组织和命名规范
- **[编码标准](.github/prompts/coding-standards.md)** - Python 最佳实践
- **[RAG 开发](.github/prompts/rag-development.md)** - 检索和生成模式
- **[测试策略](.github/prompts/testing-strategy.md)** - 测试结构和示例
- **[Cloud Native](.github/prompts/cloud-native-dev.md)** - Skaffold 和 Kubernetes
- **[评估](.github/prompts/evaluation-strategy.md)** - RAGAS 和 DSPy

## 🔄 开发工作流

### 1. 创建功能分支
```bash
git checkout -b feature/add-interview-warmup
# 或: feature/*, bugfix/*, docs/*
```

### 2. 按照标准进行更改
- 编写带类型提示的代码
- 添加测试（你的代码 ≥80% 覆盖率）
- 使用 Copilot Chat 获取指导：`我如何实现...?`

### 3. 运行质量检查
```bash
# 格式化
poetry run black src/ tests/

# Lint 检查
poetry run pylint src/

# 类型检查
poetry run mypy src/

# 测试
poetry run pytest --cov=src
```

### 4. 提交符合约定的提交消息
```bash
git commit -m "feat(agent): 添加面试热身上下文加载

- 为连续性加载最近的面试模式
- 实现 3 级递归检索
- 添加 15 个新单元测试（覆盖率：92%）

关闭 #123"
```

### 5. 推送并创建 Pull Request
```bash
git push origin feature/add-interview-warmup
# 在 GitHub 上创建 PR，请求审查
```

详见 [docs/guides/DEVELOPMENT.md](docs/guides/DEVELOPMENT.md)

## 🚢 部署

### 生产部署

```bash
# 构建生产镜像
docker build -f Dockerfile.prod -t registry.example.com/vedaaide:v1.0.0 .

# 部署到 AKS
kubectl apply -f infra/production/deployment.yaml

# 验证部署
kubectl get pods -n vedaaide -w
kubectl logs -f -n vedaaide svc/vedaaide-api
```

### 监控

```bash
# 在 LangFuse 仪表盘查看指标
# https://cloud.langfuse.com/

# 检查应用日志
poetry run tail -f logs/vedaaide.log

# 性能监控
poetry run python scripts/monitoring/check_performance.py
```

## 🤝 贡献

我们欢迎贡献！请：

1. **阅读** [PROJECT_STRUCTURE.cn.md](docs/PROJECT_STRUCTURE.cn.md) 理解代码库
2. **遵循** [coding-standards.md](.github/prompts/coding-standards.md)
3. **编写测试**（任何新功能）
4. **更新文档**（添加新功能时）
5. **使用 Copilot Chat** 在 VSCode 中获取帮助：`@workspace 我如何...?`

### 报告问题

- **Bug**：使用 `.github/ISSUE_TEMPLATE/bug.md` 模板
- **功能**：使用 `.github/ISSUE_TEMPLATE/feature.md` 模板
- **问题**：开启讨论

## 📈 路线图

**第 1 阶段：基础** ✅
- 核心 RAG Agent 实现
- 混合搜索和检索
- 基础评估框架

**第 2 阶段：增强**（进行中）
- 脱敏层
- 多场景面试支持
- DSPy Prompt 优化

**第 3 阶段：优化**
- LLM 路由成本优化
- 性能基准测试
- 用户反馈循环

**第 4 阶段：规模化**
- 多候选人批处理
- 企业集成
- 高级分析

详见 [docs/planning/main.cn.md](docs/planning/main.cn.md)

## 🔐 安全性

- 所有凭证存储在 `.env`（永不提交）
- 生产环境使用 Azure KeyVault 集成
- 所有 PII 字段脱敏
- 所有数据访问审计日志
- 代码中无硬编码密钥

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 支持

- **文档**：[docs/](docs/)
- **问题**：[GitHub Issues](https://github.com/yourusername/VedaAide/issues)
- **讨论**：[GitHub Discussions](https://github.com/yourusername/VedaAide/discussions)

## 🙏 致谢

使用的开源项目：
- [LangChain](https://langchain.com/) - LLM 编排
- [LlamaIndex](https://www.llamaindex.ai/) - 文档索引
- [Qdrant](https://qdrant.tech/) - 向量数据库
- [RAGAS](https://ragas.io/) - 评估指标
- [DSPy](https://github.com/stanfordnlp/dspy) - Prompt 优化
- [LangFuse](https://langfuse.com/) - 可观测性

---

<div align="center">

**[📖 文档](docs/INDEX.md) | [🚀 快速开始](#-快速开始) | [💬 讨论](https://github.com/yourusername/VedaAide/discussions)**

用 ❤️ 构建的智能招聘系统

</div>
