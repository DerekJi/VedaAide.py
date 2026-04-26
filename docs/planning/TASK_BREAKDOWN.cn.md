# VedaAide 项目任务分解 (Task Breakdown)

本文档将项目规划的每个阶段分解成具体的可执行任务，每个任务包含：
- **任务目标**：明确的最终状态
- **测试标准**：完成的验收条件
- **预计工时**：小时数估算
- **优先级**：P0/P1/P2

---

## 第一阶段：基础数据管道 + CLI 骨架 (Week 1-2)

> 目标：搭建可运行的基础 RAG 管道，建立 CLI 框架（命令结构、LLM 选择、参数体系），
> 为后续各阶段提供稳定的工程底座。

### 任务 1.1：部署 Qdrant 本地开发环境

**目标**
- 本地 Docker 运行 Qdrant
- 创建初始集合（Collection）
- 验证 HTTP API 和 Python SDK 连接

**测试标准**
- `docker compose ps` 显示 qdrant 服务正常运行
- `curl http://localhost:6333/health` 返回 200
- Python 脚本能够连接并执行基础操作（插入向量、检索）

**预计工时**：2 小时 | **优先级**：P0

---

### 任务 1.2：配置环境变量

**目标**
- 创建 `.env.example` 模板文件（含所有必需变量）
- 验证 `python-dotenv` 读取配置
- 文档化各变量说明

**测试标准**
- `.env.example` 包含 Azure OpenAI Key、Qdrant URL、模型名称等所有必需变量
- 代码中无硬编码 API Key
- README 中有环境变量配置说明

**预计工时**：1 小时 | **优先级**：P0

**相关资源**
- `.env.example`
- `src/utils/config.py`

---

### 任务 1.3：编写数据脱敏工具

**目标**
- 实现脱敏函数：识别并掩码 SSN、电话、邮箱、地址
- 编写单元测试
- 验证脱敏效果和性能

**测试标准**
- 所有脱敏函数覆盖率 >= 90%
- 能正确处理边界情况（空字符串、多语言、特殊字符）
- 脱敏性能：处理 1000 条简历 < 5 秒
- 脱敏后的数据中无原始敏感信息

**预计工时**：4 小时 | **优先级**：P0

**相关资源**
- `src/core/retrieval/deidentifier.py`
- `tests/unit/test_deidentifier.py`

---

### 任务 1.4：准备公开示例数据集

**目标**
- 创建模拟简历（>= 10 份）、招聘广告（>= 10 份）
- 确保所有数据无隐私敏感信息
- 数据格式文档化

**测试标准**
- 所有数据文件位于 `data/public_samples/` 目录，格式清晰
- 脱敏工具在示例数据上 100% 验证通过
- `data/public_samples/README.md` 已更新

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- `data/public_samples/`

---

### 任务 1.5：LlamaIndex 文档索引管道（基础版）

**目标**
- 实现文档加载（PDF、Markdown、文本）
- 实现分块策略（递归检索：摘要 -> 子块）
- 使用 Azure OpenAI Embedding 向量化并写入 Qdrant

**测试标准**
- 能成功导入示例数据集中的所有文档
- Qdrant Collection 中包含预期数量的向量
- 单元测试覆盖索引核心逻辑 >= 80%

**预计工时**：4 小时 | **优先级**：P0

**相关资源**
- `src/core/retrieval/indexer.py`
- `tests/unit/test_indexer.py`

---

### 任务 1.6：基础 RAG 查询验证

**目标**
- 实现简单的 RAG 查询：Query -> Retrieval -> Generation
- 验证基础检索效果（毛坯验收）

**测试标准**
- 能成功执行端到端查询
- 检索到语义相关文档（手工验证相关性 >= 0.6）
- 单次查询延迟 < 5 秒
- 集成测试编写并通过

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- `src/core/rag/pipeline.py`
- `tests/integration/test_rag_pipeline.py`

---

### 任务 1.7：CLI 骨架设计与实现

**目标**
- 确定 CLI 命令体系（`index` / `chat` / `eval`）
- 实现 LLM 选择参数（`--llm azure|ollama|deepseek`）
- 实现通用参数（`--verbose`、`--config`、`--collection`）
- 配置 pyproject.toml CLI entry points
- 实现 `vedaaide --help` 和各子命令帮助文档

**CLI 设计规格**

```
vedaaide index <docs_dir>
    --llm azure|ollama|deepseek     # Embedding 使用的 LLM 后端
    --collection <name>             # Qdrant Collection 名称（默认 vedaaide）
    --recursive                     # 递归扫描子目录
    --verbose                       # 显示详细进度

vedaaide chat
    --llm azure|ollama|deepseek     # 推理使用的 LLM 后端
    --model <model_name>            # 指定模型名（如 llama3、gpt-4o-mini）
    --collection <name>             # 指定数据集
    --temperature <float>           # 温度参数（默认 0.1）
    --top-k <int>                   # 检索 Top-K（默认 5）
    --verbose                       # 显示检索上下文

vedaaide eval
    --test-set <path>               # 测试集路径
    --llm azure|ollama|deepseek     # 评估使用的 LLM 后端
    --output <path>                 # 评估报告输出路径
    --compare <v1_result> <v2_result>  # 对比两次评估结果
```

**测试标准**
- `vedaaide --help` 输出清晰的命令说明
- `vedaaide index --help` 显示所有参数
- `--llm azure` 使用 Azure OpenAI，`--llm ollama` 使用 Ollama
- 参数缺失时有合理的默认值和友好提示
- 无效参数时有清晰的错误信息

**预计工时**：4 小时 | **优先级**：P0

**相关资源**
- `src/cli/__main__.py`
- `src/cli/commands/`
- `pyproject.toml`

---

## 第二阶段：RAG 质量提升 (Week 3-4)

> 目标：将毛坯 RAG 升级为生产可用的检索质量。
> 覆盖：数据去重、混合检索精调、重排序、幻觉防御。

### 任务 2.1：数据去重与增量索引

**目标**
- 实现文档指纹（content hash）防止重复索引
- 实现增量更新：只索引新增/修改的文档
- 实现删除：从 Qdrant 中移除已删除文档的向量

**测试标准**
- 同一文件索引两次，Qdrant 中不产生重复向量
- 修改文件后重新索引，旧向量被更新
- 删除文件后重新索引，对应向量被移除
- 单元测试覆盖率 >= 85%

**预计工时**：4 小时 | **优先级**：P0

**相关资源**
- `src/core/retrieval/indexer.py`
- `tests/unit/test_indexer.py`

---

### 任务 2.2：混合检索精调（Hybrid Retrieval）

**目标**
- 调优 BM25 权重与 Vector 权重的融合比例
- 验证专有名词（Kafka、Redis 等）的召回精度
- 实现元数据过滤（按技术栈、时间段、文档类型）
- 实现 Query 预处理（扩展缩写、标准化专有名词）

**测试标准**
- 专有名词召回率 >= 95%
- 元数据过滤：指定技术栈只返回相关段落
- A/B 测试：混合检索 vs 纯向量检索，相关性提升 >= 10%
- 单元测试覆盖 Hybrid 融合逻辑

**预计工时**：5 小时 | **优先级**：P0

**相关资源**
- `src/core/retrieval/retriever.py`
- `tests/unit/test_retriever.py`

---

### 任务 2.3：Reranking（重排序）

**目标**
- 集成 Cross-Encoder 重排序（使用 `sentence-transformers` 或 Azure Reranker）
- 实现两阶段检索：Recall -> Rerank
- 调优召回数量（Top-N for rerank -> Top-K final）

**测试标准**
- Rerank 后的 Top-3 相关性 >= Recall 阶段 Top-3 相关性
- 延迟增加控制在 1 秒以内（Reranker 不成为瓶颈）
- 单元测试覆盖 Reranker 接口 >= 80%
- 集成测试验证两阶段检索流程

**预计工时**：5 小时 | **优先级**：P0

**相关资源**
- `src/core/retrieval/retriever.py`（新增 `TwoStageRetriever`）
- `tests/unit/test_retriever.py`

---

### 任务 2.4：幻觉防御（Anti-Hallucination）

**目标**
- 实现答案溯源验证：每个答案片段必须能追溯到源文档
- 实现置信度阈值：检索得分低于阈值时拒绝生成，提示"信息不足"
- 实现来源引用：答案末尾附带 `[Source: ...]`
- 实现自检循环（Self-Check）：生成后让 LLM 验证答案与上下文的一致性

**测试标准**
- 对故意不相关的查询，系统应返回"未找到相关信息"而非编造答案
- 所有答案末尾包含可追溯的源文档引用
- Self-Check 能拦截 >= 80% 的明显错误答案（基于测试集验证）
- 单元测试覆盖置信度逻辑和 Self-Check 流程

**预计工时**：6 小时 | **优先级**：P0

**相关资源**
- `src/core/rag/pipeline.py`（新增 `AnswerVerifier`）
- `tests/unit/test_rag_pipeline.py`

---

### 任务 2.5：上下文压缩与过滤（Contextual Compression）

**目标**
- 实现 LLM-based 上下文压缩：从长段落中提取与 Query 相关的关键句子
- 减少噪音上下文，提高 LLM 生成质量
- 降低 Token 消耗

**测试标准**
- 压缩后的上下文长度减少 >= 30%（与原始上下文对比）
- RAGAS Faithfulness 不下降（与未压缩版对比）
- Token 消耗减少 >= 20%
- 单元测试覆盖压缩逻辑

**预计工时**：4 小时 | **优先级**：P1

**相关资源**
- `src/core/retrieval/retriever.py`（新增 `ContextCompressor`）
- `tests/unit/test_retriever.py`

---

### 任务 2.6：RAG 质量集成测试

**目标**
- 编写端到端测试：覆盖去重、混合检索、Reranking、幻觉防御全链路
- 建立基准评估指标（作为后续优化对比基准）

**测试标准**
- 所有 RAG 质量功能集成测试通过
- 基准 RAGAS 指标已记录（Faithfulness / Relevance / Recall）
- 测试覆盖边界场景：无结果查询、超长文档、多语言混合

**预计工时**：3 小时 | **优先级**：P1

**相关资源**
- `tests/integration/test_rag_pipeline.py`

---

## 第三阶段：Agent 核心 (Week 5-6)

> 目标：在高质量 RAG 基础上构建 Agent 工作流，实现多轮对话面试模拟。

### 应用场景概述

本阶段所构建的 Agent 将服务于以下三个核心应用场景（详见 [AgentScenarios.cn.md](AgentScenarios.cn.md)）：

1. **个人简历深度访谈 Agent**：主动引导面试对话，能够识别多段相关经历、调用 `Skill_Analyzer` 工具对比 JD 与简历匹配度、多步推理决定回答优先级，并在回答后反向提问（如询问是否需要了解 Flink 优化细节）。
2. **全自动猎头助手**：给定 JD，自动在简历库中检索最合适人选并撰写推荐信。若匹配度低于 70% 则自主扩大搜索范围，并集成 `Salary_Calculator` 和 `Email_Generator` 工具。
3. **私人技术债务/文档扫描 Agent**：输入历年代码片段、技术文档和报错日志，跨文档横向对比技术思路演进，主动探究技术变更背后的原因。

> **评测依据**：第四阶段的 RAGAS 评估测试集（Task 4.1）需围绕以上三个场景设计，覆盖主动提问、工具调用、多轮记忆、自纠错等 Agent 能力。

### 任务 3.1：设计和实现 Agent 状态机

**目标**
- 使用 LangGraph 定义 Agent 状态
- 实现五个核心状态节点：Query -> Retrieval -> Reasoning -> Reflection -> Response
- 编写状态转移逻辑

**测试标准**
- Agent 能成功执行完整的状态转移流程
- 单元测试覆盖所有状态节点 >= 85%
- 代码文档清晰（每个状态的输入/输出/转移条件）

**预计工时**：5 小时 | **优先级**：P0

**相关资源**
- `src/core/agent/state.py`
- `src/core/agent/graph.py`
- `tests/unit/test_agent_state_machine.py`

---

### 任务 3.2：实现三个核心 Agent 工具

**目标**
- 实现 `ExperienceComparator`：匹配 JD 和简历，标记 Gap
- 实现 `TechnicalDeepDive`：深度检索特定技术栈内容
- 实现 `InterviewStrategySelector`：根据提问风格（HR/技术）调整回答

**测试标准**
- 每个工具都有单元测试 >= 80% 覆盖率
- 集成测试验证工具在 Agent 中的工作
- 错误处理健壮（null、超时等）

**预计工时**：6 小时 | **优先级**：P0

**相关资源**
- `src/core/agent/tools.py`
- `tests/unit/test_agent_tools.py`

---

### 任务 3.3：实现多轮对话记忆管理

**目标**
- 实现对话历史存储和检索（内存中，无需数据库）
- 实现上下文感知（避免重复回答）
- 验证长对话（10+ 轮）中的连贯性

**测试标准**
- Agent 能正确引用之前的回答（不重复）
- 长对话测试通过（10 轮对话无遗漏或重复）
- 单元测试覆盖记忆管理逻辑

**预计工时**：3 小时 | **优先级**：P1

**相关资源**
- `src/core/agent/memory.py`
- `tests/unit/test_agent_memory.py`

---

### 任务 3.4：完善 CLI `vedaaide chat`

**目标**
- 将 Agent 工作流接入 Phase 1 的 CLI 骨架
- 实现交互式对话模式（流式输出 / 非流式可选）
- 实现对话日志保存（可选，`--save-log`）

**测试标准**
- `vedaaide chat` 能完成至少 5 轮对话
- 流式输出模式下用户体验流畅
- Phase 1 中所有 CLI 参数（`--llm`, `--model`, `--top-k` 等）正常工作

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- `src/cli/commands/chat.py`

---

### 任务 3.5：LangFuse 本地集成（可选，用于演示）

**目标**
- 为主要 Agent 步骤添加 LangFuse trace 记录
- 验证 LangFuse UI 中能看到完整执行链

**测试标准**
- LangFuse Dashboard (http://localhost:3000) 显示 Agent 执行树
- 所有 RAG 步骤和工具调用都有 trace 记录
- LangFuse 为**可选依赖**，不启动时代码正常运行

**预计工时**：3 小时 | **优先级**：P2

**相关资源**
- `src/infrastructure/observability/tracing.py`

---

### 任务 3.6：集成测试 - 端到端 Agent 工作流

**目标**
- 使用脱敏示例数据进行完整工作流测试
- 验证 Agent 的多轮对话和工具调用

**测试标准**
- 能成功执行 5+ 轮完整对话
- 没有发现敏感信息泄露
- 集成测试编写完成并通过

**预计工时**：3 小时 | **优先级**：P1

**相关资源**
- `tests/integration/test_end_to_end_workflow.py`

---

## 第四阶段：评估与 DSPy 优化 (Week 7-8)

> 目标：量化 RAG 质量，使用 DSPy 优化 Prompt，建立持续评估体系。

### 任务 4.1：生成合成测试集

**目标**
- 使用 LlamaIndex TestsetGenerator 生成 50+ 面试问题
- 人工审核问题质量
- 保存测试集

**测试标准**
- 生成至少 50 个多样化的问题
- 问题覆盖多个技能领域（架构、编程、项目经历等）
- 人工审核通过，质量评分 >= 4/5

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- `scripts/evaluation/generate_test_set.py`
- `data/test_sets/`

---

### 任务 4.2：实现 RAGAS 评估脚本

**目标**
- 实现 Faithfulness、Relevance、Recall 评估
- 支持批量评估
- 生成评估报告（JSON + 可视化）

**测试标准**
- 能对 50 个问题进行完整评估
- 评估结果结构化存储（JSON）
- 生成基础可视化报告
- 代码覆盖率 >= 80%

**预计工时**：5 小时 | **优先级**：P0

**相关资源**
- `src/core/evaluation/ragas_evaluator.py`
- `scripts/evaluation/run_ragas.py`
- `tests/unit/test_ragas_evaluator.py`

---

### 任务 4.3：DSPy Prompt 编译优化

**目标**
- 为 Azure OpenAI 编译优化 Prompt
- 为 Ollama 编译优化 Prompt
- 生成优化前后的 RAGAS 对比报告

**测试标准**
- 优化后的 RAGAS 分数 >= 优化前
- Token 消耗减少（如适用）
- A/B 对比数据已记录在 `data/evaluation-results/`

**预计工时**：6 小时 | **优先级**：P1

**相关资源**
- `src/core/rag/dspy_compiler.py`
- `scripts/evaluation/optimize_prompts.py`

---

### 任务 4.4：CLI 评估命令 (`vedaaide eval`)

**目标**
- 将 RAGAS 评估接入 Phase 1 的 CLI 骨架
- 实现 `vedaaide eval`：运行 RAGAS 评估并输出报告
- 实现 `vedaaide eval --compare <v1> <v2>`：对比两个版本的评估结果

**测试标准**
- `vedaaide eval` 能完整运行评估流程
- 输出清晰的评估摘要到终端
- 报告保存到 `data/evaluation-results/`
- Phase 1 中的 `--llm` 参数控制评估用 LLM 后端

**预计工时**：3 小时 | **优先级**：P1

**相关资源**
- `src/cli/commands/evaluate.py`

---

## 第五阶段：发布与文档 (Week 9-10)

> 目标：将项目打包发布为可安装的 PyPI 包，完善文档和 CI/CD 流程。

### 任务 5.1：完善 pyproject.toml 包配置

**目标**
- 配置 package metadata（name、version、description、classifiers）
- 确认 CLI entry points 与 Phase 1 定义一致
- 配置 optional dependencies（`langfuse` 等）

**测试标准**
- `poetry build` 成功生成 dist/ 文件
- `pip install dist/*.whl` 安装后 `vedaaide --help` 可用
- `pip install vedaaide[langfuse]` 安装 LangFuse 可选依赖

**预计工时**：2 小时 | **优先级**：P0

**相关资源**
- `pyproject.toml`

---

### 任务 5.2：GitHub Actions CI/CD

**目标**
- 创建测试工作流：代码推送自动运行单元测试
- 创建发布工作流：打 tag 自动发布到 PyPI

**测试标准**
- PR 合并前自动运行所有单元测试
- `git tag v1.0.0` 后自动发布到 PyPI
- CI 失败时有清晰的错误信息

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`

---

### 任务 5.3：完善 README（5 分钟快速开始）

**目标**
- 用户 5 分钟内能安装并运行基础演示
- 中英文同步更新
- 包含安装、配置、CLI 使用示例（含完整参数说明）

**测试标准**
- 按 README 步骤操作，全部命令成功执行
- `pip install vedaaide` + 配置 `.env` + `vedaaide chat` 全流程可跑通
- 中文（README.cn.md）和英文（README.md）内容同步

**预计工时**：3 小时 | **优先级**：P0

---

### 任务 5.4：发布到 PyPI

**目标**
- 注册 PyPI 账号（如果还没有）
- 配置 GitHub Secrets（PyPI token）
- 发布第一个版本（v0.1.0）

**测试标准**
- `pip install vedaaide` 从 PyPI 安装成功
- 安装后能正常运行 `vedaaide --help`
- PyPI 页面显示正确的描述和版本信息

**预计工时**：1 小时 | **优先级**：P0

---

## 附录：任务优先级汇总

| 阶段 | 任务 | 优先级 | 预计工时 |
|------|------|--------|--------|
| Phase 1 | 1.1 部署 Qdrant | P0 | 2h |
| Phase 1 | 1.2 配置环境变量 | P0 | 1h |
| Phase 1 | 1.3 数据脱敏工具 | P0 | 4h |
| Phase 1 | 1.4 公开示例数据 | P0 | 3h |
| Phase 1 | 1.5 LlamaIndex 索引管道 | P0 | 4h |
| Phase 1 | 1.6 基础 RAG 验证 | P0 | 3h |
| Phase 1 | 1.7 CLI 骨架设计 | P0 | 4h |
| Phase 2 | 2.1 数据去重与增量索引 | P0 | 4h |
| Phase 2 | 2.2 混合检索精调 | P0 | 5h |
| Phase 2 | 2.3 Reranking | P0 | 5h |
| Phase 2 | 2.4 幻觉防御 | P0 | 6h |
| Phase 2 | 2.5 上下文压缩 | P1 | 4h |
| Phase 2 | 2.6 RAG 质量集成测试 | P1 | 3h |
| Phase 3 | 3.1 Agent 状态机 | P0 | 5h |
| Phase 3 | 3.2 三个核心工具 | P0 | 6h |
| Phase 3 | 3.3 多轮对话记忆 | P1 | 3h |
| Phase 3 | 3.4 完善 CLI chat | P0 | 3h |
| Phase 3 | 3.5 LangFuse 集成 | P2 | 3h |
| Phase 3 | 3.6 端到端集成测试 | P1 | 3h |
| Phase 4 | 4.1 合成测试集 | P0 | 3h |
| Phase 4 | 4.2 RAGAS 评估脚本 | P0 | 5h |
| Phase 4 | 4.3 DSPy 优化 | P1 | 6h |
| Phase 4 | 4.4 CLI 评估命令 | P1 | 3h |
| Phase 5 | 5.1 pyproject.toml 包配置 | P0 | 2h |
| Phase 5 | 5.2 GitHub Actions CI/CD | P0 | 3h |
| Phase 5 | 5.3 README 完善 | P0 | 3h |
| Phase 5 | 5.4 发布到 PyPI | P0 | 1h |
| **合计** | | | **~87 小时** |
