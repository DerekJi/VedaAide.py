## 1. 项目愿景

构建一个不仅能"回答问题"且能"推销自己"的智能 Agent 系统。它能够基于个人脱敏的详细经历库，通过 Agentic RAG 技术，为用户（招聘方）提供深度、逻辑严密且具有策略性的互动面试体验。

**核心价值**：
- **实用场景**：作为招聘面试的个人助手，展示在 RAG、Agentic workflow 和 LLM 工程化方面的端到端能力
- **能力展示**：不仅演示功能价值，还通过可观测性、可评估性、安全性等方面体现高水准的开发和工程能力
- **学习实验基地**：作为开发者学习、测试和演示 RAG 工业级全链路（从开发到评估）的完整参考实现
- **成本优化**：在仅使用已有免费/优惠 Azure、GitHub、Ollama 资源的约束下实现完整系统


## 2. 技术栈架构 (Tech Stack)

### 核心语言 & LLM 编排
- **开发语言**：Python 3.10+
- **Orchestration**：
  - LangChain / LangGraph：Agent 的状态管理、多步规划和工具调用
  - LlamaIndex：数据层检索增强，支持分层索引、混合搜索（Hybrid Search）
  - DSPy：Prompt 编译优化，减少手动调优成本

### 向量数据库 & 数据存储
- **向量 DB**：Qdrant (本地 Docker + 云端托管选项)
- **持久化存储**：Azure CosmosDB (NoSQL) - 存储每次 retrieval 的详细数据，支持评估与回放
- **数据脱敏**：统一的敏感信息掩码层，确保演示与评估过程中的数据安全

### 模型接入 (LLM & Embedding)
- **本地推理**：Ollama (Llama-3 / Phi-3)
- **云端 API**：
  - Azure OpenAI：gpt-4o, gpt-4o-mini（LLM）、text-embedding-3-small（Embedding）
  - DeepSeek API（成本优化备选）

### 可观测性 & 评估框架
- **链路追踪**：
  - LangFuse（替代 LangSmith）：本地 Docker + 云端托管，成本更优，更好的隐私控制
  - 自定义观测层：装饰器拦截 Query、Contexts、Answer，写入 CosmosDB
- **质量评估**：
  - RAGAS：Faithfulness、Relevance、Recall 等核心指标量化
  - Reference-free 评估：用户反馈标签（赞/踩）作为优化的真实信号
- **监控告警**：成本监控、检索质量异常告警、模型 API 频率控制

### 成本管理资源
- ✓ Azure OpenAI Deployments (现有额度)
- ✓ Azure CosmosDB (Free Tier / 预算)
- ✓ Azure Container Apps (运行部署)
- ✓ Azure KeyVault (密钥管理)
- ✓ GitHub Pages (文档/演示)
- ✓ GitHub Container Registry (镜像存储)



## 3. 核心功能设计 (Key Features)

### A. 数据分层索引与脱敏 (LlamaIndex 侧重)
- **多维数据入库**：不仅是简历，还包括个人项目复盘、技术博客、常见面试题库（Q&A 对）
- **统一脱敏框架**：在入库前对身份证、手机号、邮箱等敏感信息进行掩码处理 `[REDACTED]`，确保演示和评估过程中的安全性
- **层级检索策略**：实现"摘要检索 -> 子块锁定"的递归检索（Recursive Retrieval），确保 Agent 既能回答大概，也能深挖细节
- **混合搜索**：BM25 + Vector Search 结合，针对专有名词（Kubernetes、Redis 等）的精准匹配

### B. Agentic 工作流与自适应策略 (LangChain/LangGraph 侧重)
- **工具箱设计**：
  1. `Experience_Comparator`：对比当前 JD 与个人简历的匹配度，自动标记 Gap
  2. `Technical_Deep_Dive`：针对特定技术栈从库中检索深度案例和细节
  3. `Interview_Strategy_Agent`：根据对方提问语气（HR vs 技术主管）动态调整回答侧重点
- **自反思循环**：Agent 在回答前自评"找回来的资料能完全回答这个问题吗？"，如不能则自动触发二次检索
- **多轮对话记忆**：维护对话历史，避免重复和遗漏，支持跨问题的论证连贯性

### C. 可观测性与可审计性
- **完整链路追踪**：LangFuse 记录每个 Agent Step、Retrieval、Tool Call 和推理过程
- **检索数据持久化**：每次 retrieval 的 Query、Top-K 结果、相关度分数存储到 CosmosDB，支持：
  - 后续分析和优化
  - 性能基准测试
  - 用户反馈关联
- **成本监控**：Token 消耗、API 调用频率、模型选择（本地 vs 云端）的实时追踪

### D. 自动化评估与优化流水线 (RAGAS & DSPy)
- **合成测试集生成**：基于个人文档生成 50+ 标准面试问题（TestsetGenerator）
- **多模型评估**：
  - 使用 gpt-4o 作为参考标准进行评估
  - 使用 gpt-4o-mini 进行成本优化的快速评估
- **DSPy 编译优化**：针对 Azure OpenAI 和 Ollama 分别编译最优 Prompt，解决本地模型理解力的痛点
- **Reference-free 反馈循环**：用户对每条回答的赞/踩，作为真实标签用于迭代优化
- **离线评估报表**：可视化展示 Faithfulness、Relevance、Recall 分数趋势

### E. 多场景支持
- **招聘场景**：1-1 面试模拟，招聘官角色扮演
- **演示场景**：技术分享、招聘宣讲、能力验证
- **学习场景**：RAG 系统诊断、提示词工程、评估方法论参考



## 4. 实施阶段规划 (Implementation Roadmap)

### 第一阶段：基础设施与数据打通 (Week 1-2)

**基础设施**
- 部署本地 Qdrant Docker 和 Ollama
- 配置 Azure CosmosDB (NoSQL) 连接池和索引策略
- 设置 LangFuse (本地 Docker 容器 + 可选的云端托管账户)
- 配置 Azure KeyVault 存储 API 密钥和连接字符串

**数据处理**
- 编写脱敏工具：识别并掩码身份证、手机号、邮箱、家庭地址等敏感信息
- 使用 LlamaIndex 实现个人简历、项目文档的结构化清洗与入库
- 构建多维数据模型（简历、项目、Q&A、博客）
- 建立数据版本管理机制（便于后续评估追踪）

**集成验证**
- 打通 Azure OpenAI + LlamaIndex 基础 RAG 接口
- 验证 Qdrant 检索质量（精排、召回率）
- 建立基础日志和追踪框架

### 第二阶段：Agent 与可观测性 (Week 3-4)

**Agent 核心**
- 使用 LangGraph 定义 Agent 状态机：Query -> Retrieval -> Reasoning -> Reflection -> Response
- 实现三个核心 Tool：Experience_Comparator、Technical_Deep_Dive、Interview_Strategy_Agent
- 多轮对话记忆管理，避免重复和遗漏

**可观测性与持久化**
- 装饰器实现自动化观测：拦截 Query、Top-K Contexts、LLM Response 并写入 CosmosDB
- 集成 LangFuse Trace：所有 Agent Step 和工具调用的完整链路
- 建立查询/回答的评价反馈机制（User Feedback 字段）
- 成本监控面板：Token 消耗、API 调用统计、模型使用分布

**测试与优化**
- 使用脱敏数据手工测试基本工作流
- 针对常见问题类型的定性评估

### 第三阶段：评估框架与智能优化 (Week 5-6)

**RAGAS 评估流水线**
- 使用 LlamaIndex TestsetGenerator 基于个人文档生成 50+ 面试问题合成测试集
- 实现 RAGAS 评估脚本：计算 Faithfulness、Relevance、Recall
- 使用 gpt-4o 作为参考模型，gpt-4o-mini 作为快速评估
- 建立评估报表（可视化分数趋势、问题分类统计）

**DSPy 编译优化**
- 针对 Azure OpenAI 的 Prompt 编译优化
- 针对 Ollama 本地模型的 Prompt 编译优化
- 对比本地 vs 云端模型的评估结果，确定最优配置

**闭环反馈**
- Reference-free 反馈循环：用户赞/踩 → 标签积累 → 微调 Prompt/检索策略
- 异常检测：识别高频错误模式，精准优化
- 持续基准测试：建立性能基线，追踪改进进度

### 第四阶段：演示与文档（可选）

- 准备面试演示脚本：展示 DSPy 优化效果、LangFuse Trace、RAGAS 评估报告
- 编写系统设计文档和踩坑指南
- 发布 GitHub Pages 技术文章（可观测 RAG 系统设计）



## 5. 关键细节与最佳实践

### 数据安全与隐私
- **脱敏策略**：在入库前编写统一的敏感信息掩码工具，对身份证、手机号、邮箱、地址等进行 `[REDACTED]` 处理
- **多阶段脱敏**：原始数据 → 脱敏数据存储 → CosmosDB 持久化 → LangFuse 追踪，每个环节都验证敏感信息
- **演示模式**：支持一键切换到完全脱敏的演示数据集，用于对外展示

### 性能与成本优化
- **异步评估**：RAGAS 评估耗时且费 Token，使用后台任务（Celery 或 asyncio）处理，不阻塞实时回复
- **模型选择**：
  - 实时回复：优先 Ollama（本地、免费）→ gpt-4o-mini（成本低）→ gpt-4o（质量高，评估用）
  - 离线评估：批量使用 gpt-4o-mini，仅在必要时用 gpt-4o
- **向量数据库优化**：
  - 启用 Qdrant 的 Hybrid Search（BM25 + Vector）处理专有名词
  - 调参 top_k、similarity_threshold 平衡召回率与精度
  - 定期清理冗余向量，控制存储成本

### 可观测性与可审计性
- **链路追踪**：
  - LangFuse 记录完整的 Agent execution 树
  - CosmosDB 保存每条检索的 Query、Context、Score、Response
  - 自定义指标：检索延迟、Token 消耗、模型选择
- **监控告警**：
  - 检索召回率异常：< 0.5 时告警
  - 评估分数下降：Faithfulness 下降 > 5% 时告警
  - 成本超出预期：Token 消耗超过月预算 80% 时告警

### 混合搜索与召回优化
- **简历中的专有名词问题**：单纯向量检索容易遗漏 Kubernetes、Redis 等关键词
- **Hybrid Search 配置**：
  - BM25 权重：0.3（精准关键词匹配）
  - Vector 权重：0.7（语义相关性）
  - 支持 Metadata Filtering：按技术栈、时间段、项目类型过滤
- **递归检索**：总结文档 → 相关章节 → 具体段落，多层级精准定位

### Reference-free 监控与反馈
- **用户反馈机制**：
  - 每条回答后收集 👍 / 👎 反馈
  - 将反馈写入 CosmosDB，关联 Query、Context、Response、用户ID
  - 定期分析反馈分布，识别高频错误模式
- **迭代优化**：
  - 低分问题集合 → 手工分析 → 调整 Prompt / 检索策略 / 数据补充
  - 版本对比：新旧 Prompt 在同一问题集上的 A/B 测试

### 技能与 JD 映射
本项目直接覆盖 JD-001 中的所有核心要求：

| JD 技能要求 | 项目中的实现 |
|-----------|----------|
| Production RAG systems end-to-end | 完整流水线：数据脱敏 → 索引 → 检索 → Agent → 评估 |
| Vector databases (Qdrant, etc.) | Qdrant 本地 + 云端托管，Hybrid Search 优化 |
| LLM orchestration (LangChain, LlamaIndex, DSPy) | LangGraph Agent、LlamaIndex 分层索引、DSPy 编译优化 |
| Strong Python + modern LLM APIs | Python 3.10+、Azure OpenAI、Ollama、DeepSeek API |
| Evaluation (RAGAS, hallucination detection) | RAGAS 量化评估、Reference-free 反馈、异常告警 |
| Debug retrieval quality systematically | CosmosDB 持久化、LangFuse 链路追踪、可视化分析 |



## 6. 面试演示亮点 (Showcase)

### 技术深度亮点

**亮点 1：DSPy 编译优化 - 0.5ms 推理，接近 GPT-3.5 质量**
- 演示如何在不修改一行 Prompt 的情况下，通过 DSPy 自动编译，让本地 Llama-3 达到接近 gpt-3.5-turbo 的 RAG 表现
- 对比图表：本地 Ollama vs Azure OpenAI 的评估分数、延迟、成本
- 亮点：成本 ↓ 99%，延迟 ↓ 90%，质量 ↑ 接近

**亮点 2：LangFuse 完整链路追踪 - 诊断幻觉问题**
- 打开 LangFuse Dashboard，展示某一次面试 Agent 的完整执行树
- 指出某个"幻觉（Hallucination）"的根源：是检索精度问题还是 LLM 推理问题
- 演示如何通过 CosmosDB 数据回放，精准定位问题，迭代改进
- 亮点：可观测、可审计、可重现

**亮点 3：RAGAS 量化评估 - 数据驱动优化**
- 拿出系统迭代前后的 RAGAS 报告：
  - Faithfulness：0.75 → 0.92（通过改进数据质量）
  - Relevance：0.80 → 0.95（通过 Hybrid Search 优化）
  - Recall：0.70 → 0.88（通过分层索引优化）
- 用数据证明你的 Agent 在处理"简历匹配"任务时的可靠性
- 亮点：量化、可验证、持续改进

**亮点 4：多模型成本优化 - 生产级系统设计**
- 展示如何通过智能模型选择（Ollama → gpt-4o-mini → gpt-4o）实现成本控制
- Token 消耗监控面板：实时成本计算与预测
- 月度成本对比：单用 Azure OpenAI vs 混合本地 Ollama 的成本差异
- 亮点：工程化思维，成本意识，生产就绪

### 系统设计亮点

**亮点 5：数据脱敏全链路**
- 展示脱敏工具的工作原理：识别、掩码、验证
- 演示从原始简历到脱敏后的完整转换过程
- 多阶段验证：存储层、追踪层、展示层都无敏感信息
- 亮点：隐私第一，生产级安全考虑

**亮点 6：Hybrid Search 的威力**
- 对比纯向量搜索 vs Hybrid Search 的检索质量
- Case Study：如何通过 BM25 + Vector 精准匹配 Kubernetes、Redis、CI/CD 等专有名词
- Metadata Filtering 实战：按技术栈和时间段精细化过滤
- 亮点：细致的工程实现，考虑真实场景

### 能力展示亮点

**亮点 7：Reference-free 持续改进机制**
- 展示用户反馈如何转化为改进信号
- 例子：低分问题的集合 → 模式识别 → Prompt 优化 → 新旧版本 A/B 测试
- 用最近 3 次迭代的数据展示改进趋势
- 亮点：闭环思维，数据驱动决策

**亮点 8：工程化最佳实践**
- 代码结构：模块化、单一职责、易于测试
- 配置管理：环境变量、KeyVault 集成、安全密钥存储
- 异步处理：评估、日志写入都通过后台任务，不阻塞实时回复
- 版本控制：每个重要迭代的代码标签、数据快照、评估报告
- 亮点：高水准的代码质量

---

## 相关文档

- **[项目结构与目录规范](PROJECT_STRUCTURE.cn.md)** - 完整的代码库组织、命名规则、测试结构、CI/CD 流程、Cloud Native 开发指南
- **[Agent 场景设计](AgentScenarios.cn.md)** - 不同应用场景的 Agent 配置
- **[基本考虑](00.basics.md)** - 项目约束条件和设计考虑因素
