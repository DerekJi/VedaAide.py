# VedaAide: 面试准备 RAG Agent 系统

## 1. 项目愿景

构建一个能够进行个性化面试对话的智能 Agent 系统。通过对脱敏经历库的分析理解，利用 Agentic RAG 技术，为用户呈现逼真的面试互动体验。

**核心价值**：
- **技术展示**：向招聘方展示 RAG + Agent 的端到端工程能力（LlamaIndex 索引、LangGraph Agent、DSPy 优化）
- **可运行演示**：以 CLI 工具形式发布，招聘方可通过 `pip install vedaaide` 直接试用
- **学习参考**：作为开发者理解 RAG 完整链路（从索引到评估）的实用示例
- **精简务实**：聚焦 RAG/Agent 核心能力，不在 Infra/DevOps 方面投入不必要的时间


## 2. 技术栈架构 (Tech Stack)

### 核心语言 & LLM 编排
- **开发语言**：Python 3.10+
- **Orchestration**：
  - LangChain / LangGraph：Agent 的状态管理、多步规划和工具调用
  - LlamaIndex：数据层检索增强，支持分层索引、混合搜索（Hybrid Search）
  - DSPy：Prompt 编译优化，减少手动调优成本

### 向量数据库 & 配置
- **向量 DB**：Qdrant（本地 Docker 运行）
- **配置管理**：`.env` + `python-dotenv`（简单直接，无需 KeyVault）
- **数据脱敏**：统一的敏感信息掩码层，确保演示安全

### 模型接入 (LLM & Embedding)
- **本地推理**：Ollama (Llama-3 / Phi-3)
- **云端 API**：
  - Azure OpenAI：gpt-4o, gpt-4o-mini（LLM）、text-embedding-3-small（Embedding）
  - DeepSeek API（成本优化备选）

### 评估与可观测性（轻量）
- **链路追踪**：LangFuse（本地 Docker，可选，用于演示 Agent 执行链路）
- **质量评估**：RAGAS（Faithfulness、Relevance、Recall 等核心指标）

### 发布方式
- ✓ PyPI 包（`pip install vedaaide`）
- ✓ GitHub 源码（含示例数据集）
- ✓ GitHub Pages（文档）



## 3. 核心功能设计 (Key Features)

### A. 数据分层索引与脱敏 (LlamaIndex 侧重)
- **多维数据入库**：不仅是简历，还包括个人项目复盘、技术博客、常见面试题库（Q&A 对）
- **统一脱敏框架**：在入库前对身份证、手机号、邮箱等敏感信息进行掩码处理 `[REDACTED]`，确保演示过程中的安全性
- **层级检索策略**：实现"摘要检索 -> 子块锁定"的递归检索（Recursive Retrieval），确保 Agent 既能回答大概，也能深挖细节
- **混合搜索**：BM25 + Vector Search 结合，针对专有名词（Kafka、Redis 等）的精准匹配

### B. Agentic 工作流与自适应策略 (LangChain/LangGraph 侧重)
- **工具箱设计**：
  1. `ExperienceComparator`：对比当前 JD 与个人简历的匹配度，自动标记 Gap
  2. `TechnicalDeepDive`：针对特定技术栈从库中检索深度案例和细节
  3. `InterviewStrategySelector`：根据对方提问语气（HR vs 技术主管）动态调整回答侧重点
- **自反思循环**：Agent 在回答前自评"找回来的资料能完全回答这个问题吗？"，如不能则自动触发二次检索
- **多轮对话记忆**：维护对话历史，避免重复和遗漏，支持跨问题的论证连贯性

### C. 评估框架 (RAGAS & DSPy)
- **合成测试集生成**：基于个人文档生成 50+ 标准面试问题（TestsetGenerator）
- **RAGAS 量化评估**：计算 Faithfulness、Relevance、Recall
- **DSPy 编译优化**：针对 Azure OpenAI 和 Ollama 分别编译最优 Prompt，解决本地模型理解力的痛点

### D. 可观测性（可选演示）
- **LangFuse 本地实例**：已有 `langfuse_storage/` 数据，可在演示时展示完整 Agent 执行链路
- **用途**：诊断幻觉（Hallucination）根源、展示 Retrieval → Reasoning 的可见性

### E. CLI 工具
- **安装**：`pip install vedaaide`
- **使用场景**（待详细设计）：
  - `vedaaide index <docs_dir>`：索引文档
  - `vedaaide chat`：开始面试对话
  - `vedaaide eval`：运行 RAGAS 评估



## 4. 实施阶段规划 (Implementation Roadmap)

### 第一阶段：基础数据管道 (Week 1-2)

**环境搭建**
- 启动本地 Qdrant（Docker）
- 配置 `.env`：Azure OpenAI API Key、Qdrant 连接信息
- 可选：启动本地 LangFuse（已有 `langfuse_storage/`）

**数据处理**
- 编写脱敏工具：识别并掩码身份证、手机号、邮箱、家庭地址
- 准备公开示例数据集（模拟简历、招聘广告）
- 使用 LlamaIndex 完成文档清洗、分块、向量化入库

**基础验证**
- 打通 Azure OpenAI + LlamaIndex 基础 RAG 接口
- 验证 Qdrant 混合检索（BM25 + Vector）效果
- 单元测试覆盖脱敏工具

### 第二阶段：Agent 核心 (Week 3-4)

**LangGraph Agent**
- 定义状态机：Query → Retrieval → Reasoning → Reflection → Response
- 实现三个核心工具：`ExperienceComparator`、`TechnicalDeepDive`、`InterviewStrategySelector`
- 多轮对话记忆管理

**CLI 初步实现**
- `vedaaide index`：文档索引命令
- `vedaaide chat`：交互式面试对话

**测试**
- 单元测试覆盖所有 Agent 工具
- 集成测试：端到端 RAG 查询流程

### 第三阶段：评估与优化 (Week 5-6)

**RAGAS 评估**
- 合成测试集（50+ 面试问题）
- 计算 Faithfulness、Relevance、Recall
- 评估报表生成

**DSPy 优化**
- 针对 Azure OpenAI 和 Ollama 分别编译 Prompt
- 对比优化前后的 RAGAS 分数

**CLI 完善**
- `vedaaide eval`：运行评估命令
- `vedaaide eval --compare`：对比不同配置的评估结果

### 第四阶段：发布与文档 (Week 7-8)

**PyPI 发布**
- 完善 `pyproject.toml`（包配置、CLI entry points）
- 编写安装指南和快速开始文档
- 发布到 PyPI

**文档完善**
- README 5 分钟快速开始
- 系统设计文档
- 演示脚本（LangFuse 链路展示、RAGAS 报告）

### 后续（待规划）

- CLI UX 详细设计（用户交互流程、帮助文档）



## 5. 关键细节与最佳实践

### 数据安全与隐私
- **脱敏策略**：在入库前编写统一的敏感信息掩码工具，对身份证、手机号、邮箱、地址等进行 `[REDACTED]` 处理
- **演示模式**：仓库中包含完全脱敏的公开示例数据集，用户无需提供个人数据即可试用

### 混合搜索与召回优化
- **简历中的专有名词问题**：单纯向量检索容易遗漏 Kafka、Redis 等关键词
- **Hybrid Search 配置**：
  - BM25 权重：0.3（精准关键词匹配）
  - Vector 权重：0.7（语义相关性）
  - 支持 Metadata Filtering：按技术栈、时间段、项目类型过滤
- **递归检索**：总结文档 → 相关章节 → 具体段落，多层级精准定位

### 模型与成本策略
- **实时对话**：优先 Ollama（本地、免费）→ gpt-4o-mini（成本低）→ gpt-4o（质量高）
- **离线评估**：批量使用 gpt-4o-mini，仅在必要时用 gpt-4o
- **配置**：通过 `.env` 切换模型，无需改代码

### 技能与 JD 映射
本项目直接覆盖 JD-001 中的核心 RAG/Agent 技术要求：

| JD 技能要求 | 项目中的实现 |
|-----------|----------|
| Production RAG systems end-to-end | 完整流水线：脱敏 → 索引 → 混合检索 → Agent → RAGAS 评估 |
| Vector databases (Qdrant, etc.) | Qdrant 本地，Hybrid Search（BM25 + Vector）优化 |
| LLM orchestration (LangChain, LlamaIndex, DSPy) | LangGraph Agent、LlamaIndex 分层索引、DSPy 编译优化 |
| Strong Python + modern LLM APIs | Python 3.10+、Azure OpenAI、Ollama、DeepSeek API |
| Evaluation (RAGAS, hallucination detection) | RAGAS 量化评估、LangFuse 链路追踪（可选） |
| Debug retrieval quality systematically | RAGAS 指标分析、LangFuse Trace 诊断、评估报表对比 |



## 6. 面试演示亮点 (Showcase)

### 技术深度亮点

**亮点 1：DSPy 编译优化 - 本地模型接近云端质量**
- 演示如何通过 DSPy 自动编译，让本地 Llama-3 达到接近 gpt-3.5-turbo 的 RAG 表现
- 对比图表：本地 Ollama vs Azure OpenAI 的 RAGAS 评估分数、延迟对比
- 核心价值：成本优化 + 理解 Prompt 编译原理

**亮点 2：RAGAS 量化评估 - 数据驱动优化**
- 展示系统迭代前后的 RAGAS 报告（Faithfulness、Relevance、Recall 趋势）
- 演示如何通过评估指标定位问题（召回率低 → 检索策略问题 / Faithfulness 低 → 生成问题）
- 核心价值：量化、可验证、持续改进

**亮点 3：Hybrid Search 的威力**
- 对比纯向量搜索 vs Hybrid Search 的检索质量
- Case Study：如何通过 BM25 + Vector 精准匹配 Kafka、Redis、CI/CD 等专有名词
- 核心价值：理解检索系统设计权衡

**亮点 4：LangFuse Agent 执行链路（可选演示）**
- 打开本地 LangFuse Dashboard，展示面试 Agent 的完整执行树
- 指出某个"幻觉"的根源：是检索精度问题还是 LLM 推理问题
- 核心价值：可观测、可调试、可复现

### 工程能力亮点

**亮点 5：数据脱敏全链路**
- 展示脱敏工具的工作原理：识别、掩码、验证
- 演示从原始简历到脱敏后的完整转换过程
- 核心价值：隐私意识，实际工程考量

**亮点 6：CLI 工具设计**（Phase 4 后）
- `pip install vedaaide` 后 5 分钟即可运行演示
- 设计合理的命令结构，考虑用户体验
- 核心价值：工程化思维，产品意识

---

## 相关文档

- **[项目结构与目录规范](../PROJECT_STRUCTURE.cn.md)** - 代码库组织、命名规则、测试结构
- **[Agent 场景设计](AgentScenarios.cn.md)** - 不同应用场景的 Agent 配置
- **[基本考虑](00.basics.md)** - 项目约束条件和设计考虑因素
- **[任务分解](TASK_BREAKDOWN.cn.md)** - 详细的可执行任务列表
