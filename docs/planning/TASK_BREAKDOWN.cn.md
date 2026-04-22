# VedaAide 项目任务分解 (Task Breakdown)

本文档将项目规划的每个阶段分解成具体的可执行任务，每个任务包含：
- **任务目标**：明确的最终状态
- **测试标准**：完成的验收条件
- **预计工时**：小时数估算
- **优先级**：P0/P1/P2

---

## 第一阶段：基础设施与数据打通 (Week 1-2)

### 任务 1.1：部署 Qdrant 本地开发环境

**目标**
- [ ] 本地 Docker 运行 Qdrant
- [ ] 创建初始集合（Collection）
- [ ] 验证 HTTP API 和 Python SDK 连接

**测试标准**
- [ ] `podman compose ps` 显示 qdrant 服务正常运行
- [ ] `curl http://localhost:6333/health` 返回 200
- [ ] Python 脚本能够连接并执行基础操作（插入向量、检索）
- [ ] Qdrant 配置文档已更新

**预计工时**：2 小时 | **优先级**：P0

**相关资源**
- docker-compose.yml
- 文档：.github/prompts/cloud-native-dev.md

---

### 任务 1.2：配置 LangFuse 本地开发环境

**目标**
- [ ] 部署 LangFuse Docker 容器（PostgreSQL + ClickHouse + LangFuse）
- [ ] 验证 LangFuse UI 可访问
- [ ] 配置 LangFuse Python SDK

**测试标准**
- [ ] `podman compose ps` 显示所有 LangFuse 相关服务正常运行
- [ ] http://localhost:3000 可访问，能登录默认账户
- [ ] Python 脚本能够连接 LangFuse 并记录 trace
- [ ] 文档：README.md 中 LangFuse 配置已更新（中英文同步）

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- docker-compose.yml
- docs：README.md、README.cn.md

---

### 任务 1.3：配置 Azure CosmosDB 连接

**目标**
- [ ] 创建 Azure CosmosDB 账户或使用现有账户
- [ ] 创建数据库和必要的容器（retrieval_logs、feedback、metadata）
- [ ] 验证 Python SDK 连接

**测试标准**
- [ ] `python -c "from src.infrastructure.db.cosmosdb import CosmosDBClient; client = CosmosDBClient(); print(client.list_databases())"` 能成功执行
- [ ] 能够执行基础 CRUD 操作（创建、读取、更新、删除文档）
- [ ] 索引策略已配置（为查询字段创建复合索引）
- [ ] 成本估算已记录（Free Tier 或预算设置）

**预计工时**：2.5 小时 | **优先级**：P0

**相关资源**
- config/cosmosdb.yaml
- 文档：docs/architecture/DATA_FLOW.md

---

### 任务 1.4：编写数据脱敏工具

**目标**
- [ ] 实现脱敏函数：识别并掩码 SSN、电话、邮箱、地址
- [ ] 编写单元测试和集成测试
- [ ] 验证脱敏效果和性能

**测试标准**
- [ ] 所有脱敏函数覆盖率 ≥ 90%
- [ ] 能正确处理边界情况（空字符串、多语言、特殊字符）
- [ ] 脱敏性能：处理 1000 条简历 < 5 秒
- [ ] 验证规则：脱敏后的数据中无原始敏感信息
- [ ] 代码审查通过
- [ ] 文档：src/core/retrieval/deidentifier.py 中有清晰的使用示例

**预计工时**：4 小时 | **优先级**：P0

**相关资源**
- src/core/retrieval/deidentifier.py
- tests/unit/test_deidentification.py

---

### 任务 1.5：导入和清洗示例数据

**目标**
- [ ] 准备示例简历、项目文档等数据
- [ ] 使用脱敏工具处理数据
- [ ] 使用 LlamaIndex 构建多维数据模型

**测试标准**
- [ ] 数据集包含至少 10 份脱敏简历
- [ ] 所有敏感信息已被掩码
- [ ] 数据版本号和时间戳已记录
- [ ] Qdrant 中已索引所有文档（验证 collection 中的向量数）
- [ ] 数据管理文档已更新

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- data/ 目录
- scripts/data/load_samples.py

---

### 任务 1.6：验证基础 RAG 管道

**目标**
- [ ] 实现简单的 RAG 查询：Query → Retrieval → Generation
- [ ] 验证 Qdrant 检索质量
- [ ] 建立基础日志记录

**测试标准**
- [ ] 能成功执行端到端查询（从简历中检索相关信息）
- [ ] 检索精度和召回率手工验证 ≥ 0.7
- [ ] LangFuse 记录了完整的 trace
- [ ] CosmosDB 存储了查询和结果
- [ ] 性能：单次查询延迟 < 3 秒
- [ ] 集成测试编写并通过

**预计工时**：4 小时 | **优先级**：P1

**相关资源**
- src/core/rag/pipeline.py
- tests/integration/test_rag_pipeline.py

---

## 第二阶段：Agent 与可观测性 (Week 3-4)

### 任务 2.1：设计和实现 Agent 状态机

**目标**
- [ ] 使用 LangGraph 定义 Agent 状态
- [ ] 实现五个核心状态节点：Query → Retrieval → Reasoning → Reflection → Response
- [ ] 编写状态转移逻辑

**测试标准**
- [ ] Agent 能成功执行完整的状态转移流程
- [ ] 状态机可视化图表已生成
- [ ] 单元测试覆盖所有状态节点 ≥ 85%
- [ ] 代码文档清晰（每个状态的输入/输出/转移条件）
- [ ] 代码审查通过

**预计工时**：5 小时 | **优先级**：P0

**相关资源**
- src/core/agent/state.py
- src/core/agent/graph.py
- tests/unit/test_agent_state_machine.py

---

### 任务 2.2：实现三个核心工具

**目标**
- [ ] 实现 `Experience_Comparator`：匹配 JD 和简历
- [ ] 实现 `Technical_Deep_Dive`：深度检索技术相关内容
- [ ] 实现 `Interview_Strategy_Agent`：根据提问风格调整回答

**测试标准**
- [ ] 每个工具都有单元测试 ≥ 80% 覆盖率
- [ ] 集成测试验证工具在 Agent 中的工作
- [ ] 错误处理健壮（null、超时等）
- [ ] 代码审查通过
- [ ] 使用文档已编写

**预计工时**：6 小时 | **优先级**：P0

**相关资源**
- src/core/agent/tools.py
- tests/unit/test_agent_tools.py

---

### 任务 2.3：实现多轮对话记忆管理

**目标**
- [ ] 实现对话历史存储和检索
- [ ] 实现上下文感知（避免重复回答）
- [ ] 验证长对话（10+ 轮）中的连贯性

**测试标准**
- [ ] 对话历史正确存储在 CosmosDB 中
- [ ] Agent 能正确引用之前的回答（不重复）
- [ ] 长对话测试通过（10 轮对话无遗漏或重复）
- [ ] 内存占用在可接受范围内（< 50MB）
- [ ] 代码审查通过

**预计工时**：3 小时 | **优先级**：P1

**相关资源**
- src/core/agent/memory.py
- tests/integration/test_multi_turn_conversation.py

---

### 任务 2.4：集成 LangFuse 追踪

**目标**
- [ ] 配置 LangFuse SDK
- [ ] 为所有关键步骤添加 trace 记录
- [ ] 验证 LangFuse UI 中的完整执行树

**测试标准**
- [ ] LangFuse Dashboard 显示完整的 Agent 执行树
- [ ] 所有工具调用都被记录
- [ ] Token 消耗数据准确记录
- [ ] 性能影响 < 5%（trace 开销）
- [ ] 代码审查通过
- [ ] 文档：LangFuse 使用指南已编写

**预计工时**：3 小时 | **优先级**：P1

**相关资源**
- src/infrastructure/observability/tracing.py
- docs/guides/LANGFUSE_SETUP.md

---

### 任务 2.5：实现自定义可观测装饰器

**目标**
- [ ] 编写装饰器自动捕获函数输入/输出
- [ ] 配置 CosmosDB 持久化
- [ ] 记录性能指标

**测试标准**
- [ ] 装饰器正确捕获所有参数
- [ ] CosmosDB 中的记录完整准确
- [ ] 性能开销 < 2%
- [ ] 单元测试覆盖 ≥ 85%
- [ ] 代码审查通过

**预计工时**：3 小时 | **优先级**：P2

**相关资源**
- src/infrastructure/observability/decorators.py
- tests/unit/test_observability_decorators.py

---

### 任务 2.6：用户反馈机制

**目标**
- [ ] 设计反馈数据模型
- [ ] 实现反馈收集接口
- [ ] 与 CosmosDB 集成存储

**测试标准**
- [ ] 能记录用户的 👍/👎 反馈
- [ ] 反馈关联到正确的查询/响应
- [ ] 能按反馈分数查询（支持低分问题集合）
- [ ] 集成测试通过
- [ ] API 文档已更新

**预计工时**：2 小时 | **优先级**：P2

**相关资源**
- src/core/evaluation/feedback.py
- tests/integration/test_feedback_mechanism.py

---

### 任务 2.7：集成测试 - 端到端工作流

**目标**
- [ ] 使用脱敏示例数据进行完整工作流测试
- [ ] 验证 Agent 的多轮对话
- [ ] 手工评估回答质量

**测试标准**
- [ ] 能成功执行 5+ 轮完整对话
- [ ] LangFuse 中有完整的 trace
- [ ] CosmosDB 中有完整的记录
- [ ] 回答质量手工评估：相关性和正确性 ≥ 0.7
- [ ] 没有看到敏感信息泄露
- [ ] 集成测试编写完成

**预计工时**：4 小时 | **优先级**：P1

**相关资源**
- tests/integration/test_end_to_end_workflow.py

---

## 第三阶段：评估框架与优化 (Week 5-6)

### 任务 3.1：生成合成测试集

**目标**
- [ ] 使用 LlamaIndex TestsetGenerator 生成 50+ 面试问题
- [ ] 人工审核并调整问题质量
- [ ] 保存测试集到 data/test_sets/

**测试标准**
- [ ] 生成至少 50 个多样化的问题
- [ ] 问题覆盖多个技能领域（架构、编程、项目管理等）
- [ ] 问题的难度分布合理（简单、中等、难）
- [ ] 没有重复问题
- [ ] 人工审核完成，质量评分 ≥ 4/5

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- scripts/evaluation/generate_test_set.py
- data/test_sets/interview_questions.json

---

### 任务 3.2：实现 RAGAS 评估脚本

**目标**
- [ ] 实现 Faithfulness、Relevance、Recall 评估
- [ ] 支持批量评估
- [ ] 生成评估报告

**测试标准**
- [ ] 能对 50 个问题进行完整评估（预期耗时 30-60 分钟）
- [ ] 评估结果结构化存储（JSON/CSV）
- [ ] 生成可视化报告（折线图、分布图）
- [ ] 评估重现性 > 0.9（相同输入的分数差异 < 5%）
- [ ] 代码覆盖率 ≥ 80%
- [ ] 文档完整

**预计工时**：5 小时 | **优先级**：P0

**相关资源**
- src/core/evaluation/ragas_evaluator.py
- scripts/evaluation/run_ragas_evaluation.py
- tests/evaluation/test_ragas_evaluator.py

---

### 任务 3.3：DSPy Prompt 编译优化

**目标**
- [ ] 为 Azure OpenAI 编译优化 Prompt
- [ ] 为 Ollama 编译优化 Prompt
- [ ] 生成优化前后的对比报告

**测试标准**
- [ ] 优化后的 Prompt 在相同测试集上评估 ≥ 原版本
- [ ] Token 消耗减少 ≥ 20%（如适用）
- [ ] 延迟改善可测量
- [ ] A/B 测试数据已记录
- [ ] 文档：Prompt 版本化管理已实现

**预计工时**：6 小时 | **优先级**：P1

**相关资源**
- src/core/rag/dspy_compiler.py
- scripts/evaluation/optimize_prompts.py

---

### 任务 3.4：基准测试和持续改进

**目标**
- [ ] 建立性能基线
- [ ] 实现自动化对比测试
- [ ] 记录改进进度

**测试标准**
- [ ] 基线报告已生成（Faithfulness、Relevance、Recall）
- [ ] 实现了版本对比功能
- [ ] 改进前后的数据清晰可见
- [ ] 性能趋势图已生成
- [ ] 文档：评估方法论已编写

**预计工时**：4 小时 | **优先级**：P2

**相关资源**
- scripts/evaluation/compare_versions.py
- data/evaluation-results/
- docs/evaluation/EVALUATION_FRAMEWORK.md

---

## 第四阶段：Cloud Native 开发与部署 (Week 7-8)

### 任务 4.1：编写 Dockerfile 多阶段构建

**目标**
- [ ] 创建开发 Dockerfile（src/Lab.Api/Dockerfile 为参考）
- [ ] 创建生产 Dockerfile
- [ ] 支持热重载和快速构建

**测试标准**
- [ ] 开发镜像能支持代码热更新（Skaffold 集成）
- [ ] 生产镜像大小 < 300MB
- [ ] 构建时间 < 2 分钟（冷缓存）
- [ ] 镜像能正确启动应用
- [ ] 安全扫描无高危漏洞

**预计工时**：2 小时 | **优先级**：P0

**相关资源**
- infra/docker/Dockerfile（主应用）
- infra/docker/Dockerfile.dev
- docs/guides/DOCKER_BUILD.md

---

### 任务 4.2：编写 Kubernetes 部署清单

**目标**
- [ ] 创建 Deployment、Service、ConfigMap、Secret
- [ ] 配置环境隔离（dev、test、prod）
- [ ] 配置资源限制和健康检查

**测试标准**
- [ ] 清单 YAML 通过 kubeval 验证
- [ ] 能在本地 Kind 集群部署
- [ ] 能正确处理滚动更新
- [ ] 健康检查工作正常
- [ ] 文档完整（部署指南）

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- kubernetes/base/
- kubernetes/overlays/{dev,test,prod}/
- docs/guides/KUBERNETES_DEPLOYMENT.md

---

### 任务 4.3：配置 Skaffold 本地开发

**目标**
- [ ] 编写 skaffold.yaml
- [ ] 配置代码同步（hot reload）
- [ ] 配置日志和端口转发
- [ ] 验证本地开发工作流

**测试标准**
- [ ] 修改代码后自动重新构建、推送、部署（< 10 秒）
- [ ] 容器内代码已同步
- [ ] 日志能在本地查看（kubectl logs）
- [ ] 端口转发工作正常
- [ ] 文档：本地开发快速开始

**预计工时**：2 小时 | **优先级**：P0

**相关资源**
- skaffold.yaml
- docs/guides/SKAFFOLD_DEV.md

---

### 任务 4.4：设置 GitHub Actions CI/CD

**目标**
- [ ] 创建测试工作流（单元测试、集成测试）
- [ ] 创建构建工作流（镜像构建、推送到 GCR）
- [ ] 创建部署工作流（自动部署到开发/测试环境）

**测试标准**
- [ ] 代码推送自动触发测试
- [ ] 测试通过才能合并 PR
- [ ] 推送到 main 分支后自动构建镜像
- [ ] 镜像自动推送到镜像仓库
- [ ] 自动部署到开发环境
- [ ] 工作流错误处理和通知配置完整

**预计工时**：4 小时 | **优先级**：P0

**相关资源**
- .github/workflows/
- docs/guides/CI_CD_SETUP.md

---

### 任务 4.5：配置秘钥管理和环境变量

**目标**
- [ ] 集成 Azure KeyVault
- [ ] 配置环境变量注入
- [ ] 验证敏感信息不会泄露

**测试标准**
- [ ] 秘钥从 KeyVault 正确读取
- [ ] 环境变量安全注入（无日志泄露）
- [ ] 本地开发和云端部署都能正确读取秘钥
- [ ] 安全审计通过
- [ ] 文档：秘钥管理指南

**预计工时**：2 小时 | **优先级**：P1

**相关资源**
- config/secrets.yaml
- docs/guides/SECRETS_MANAGEMENT.md

---

### 任务 4.6：部署到 Kind 集群测试

**目标**
- [ ] 在本地 Kind 集群部署完整的应用栈
- [ ] 测试所有服务的互连
- [ ] 验证可观测性工作正常

**测试标准**
- [ ] 所有 Pod 运行正常
- [ ] Service 间通信工作
- [ ] LangFuse 能记录到来自应用的 trace
- [ ] 应用日志可查看
- [ ] 健康检查通过
- [ ] 能成功执行端到端查询

**预计工时**：3 小时 | **优先级**：P0

**相关资源**
- kubernetes/
- scripts/deploy/

---

## 第五阶段：演示与文档 (Week 9+)

### 任务 5.1：准备面试演示脚本

**目标**
- [ ] 编写演示脚本和演示数据
- [ ] 准备演示幻灯片
- [ ] 录制或排演演示

**测试标准**
- [ ] 演示能在 15 分钟内完成
- [ ] 演示覆盖所有关键亮点
- [ ] 演示数据完全脱敏
- [ ] 演示稳定（无明显错误）

**预计工时**：4 小时 | **优先级**：P2

**相关资源**
- scripts/demo/
- docs/DEMO_GUIDE.md

---

### 任务 5.2：编写系统设计文档

**目标**
- [ ] 完整的架构文档
- [ ] 设计决策和权衡说明
- [ ] 踩坑指南和最佳实践

**测试标准**
- [ ] 文档覆盖所有主要组件
- [ ] 设计决策有清晰的理由
- [ ] 踩坑指南至少包含 10+ 常见问题及解决方案
- [ ] 中英文版本同步

**预计工时**：6 小时 | **优先级**：P2

**相关资源**
- docs/architecture/
- docs/guides/TROUBLESHOOTING.md

---

### 任务 5.3：发布 GitHub Pages 技术文章

**目标**
- [ ] 编写 1-2 篇深度技术文章
- [ ] 发布到 GitHub Pages
- [ ] 分享到社交媒体或技术社区

**测试标准**
- [ ] 文章清晰、有见地、实用
- [ ] GitHub Pages 成功构建和发布
- [ ] 至少获得 10+ 赞或评论

**预计工时**：4 小时 | **优先级**：P3

**相关资源**
- docs/_posts/
- docs/index.md

---

## 优先级和依赖关系

```
P0 任务（必做）：
├── 1.1, 1.2, 1.3, 1.4, 1.5, 1.6
├── 2.1, 2.2, 2.4, 2.7
├── 3.1, 3.2
└── 4.1-4.6

P1 任务（强烈推荐）：
├── 1.7 依赖 1.1-1.6
├── 2.3, 2.5, 2.6
├── 3.3
└── 4.5

P2 任务（可选但有价值）：
└── 3.4, 5.1, 5.2

P3 任务（锦上添花）：
└── 5.3
```

## 创建 GitHub Issues

使用 [.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md) 模板为每个任务创建对应的 GitHub Issue。

**示例命令**：
```bash
# Issue 编号参考以上任务编号（1.1, 1.2 等）
# 标题格式：[PHASE] Task Description
# 例：[Phase 1] Task 1.1: Deploy Qdrant Local Development Environment
```

---

**最后更新**：2025-04-22  
**维护者**：VedaAide 团队
