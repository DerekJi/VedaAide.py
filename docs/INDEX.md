# VedaAide 文档索引

## 📚 快速导航

### 🎯 项目规划 (planning/)

- **[项目愿景与路线规划](planning/main.cn.md)** - 项目愿景、技术栈、核心功能、实施路线图、演示亮点
- **[任务分解](planning/TASK_BREAKDOWN.cn.md)** - 将每个阶段细分为可执行任务，包含目标、测试标准、工时估算
- **[项目结构与目录规范](PROJECT_STRUCTURE.cn.md)** - 代码库组织、命名规则、测试结构、CI/CD、Cloud Native 开发
- **[基本考虑](planning/00.basics.md)** - 项目约束条件（成本、数据、场景等）
- **[Agent 场景设计](planning/AgentScenarios.cn.md)** - 不同应用场景的 Agent 配置

### 📖 开发指南 (guides/)

- **[开发环境设置](guides/SETUP.md)** - 待创建
- **[开发工作流](guides/DEVELOPMENT.md)** - 待创建
- **[测试指南](guides/TESTING.md)** - 待创建
- **[部署指南](guides/DEPLOYMENT.md)** - 待创建
- **[Cloud Native 开发](guides/CLOUD_NATIVE.md)** - 待创建
- **[故障排查](guides/TROUBLESHOOTING.md)** - 待创建

### 🏗️ 架构文档 (architecture/)

- **[系统架构概览](architecture/OVERVIEW.md)** - 待创建
- **[数据流设计](architecture/DATA_FLOW.md)** - 待创建
- **[Agent 状态机](architecture/AGENT_STATE_MACHINE.md)** - 待创建
- **[RAG 管道设计](architecture/RAG_PIPELINE.md)** - 待创建
- **[可观测性架构](architecture/OBSERVABILITY.md)** - 待创建
- **[安全设计](architecture/SECURITY.md)** - 待创建

### 🔌 API 文档 (api/)

- **[REST API 规范](api/REST_API.md)** - 待创建
- **[数据模型规范](api/SCHEMAS.md)** - 待创建
- **[使用示例](api/EXAMPLES.md)** - 待创建

### 📊 评估文档 (evaluation/)

- **[RAGAS 指标说明](evaluation/RAGAS_METRICS.md)** - 待创建
- **[评估框架设计](evaluation/EVALUATION_FRAMEWORK.md)** - 待创建
- **[反馈机制](evaluation/FEEDBACK_MECHANISM.md)** - 待创建
- **[基准测试报告](evaluation/BENCHMARK_REPORTS.md)** - 待创建

### 📋 需求文档 (JD/)

- **[职位描述 JD-001](JD/JD-001.md)** - 原始职位要求
- **[项目需求分析](JD/REQUIREMENTS.md)** - 待创建

---

## 📑 按用途分类

### 🎯 项目规划与任务管理

1. 了解项目：[项目愿景与路线规划](planning/main.cn.md)
2. 查看规划：[实施阶段规划](planning/main.cn.md)
3. **获取任务清单**：[任务分解文档](planning/TASK_BREAKDOWN.cn.md) - 包含工时估算、优先级、验收标准
4. 创建 GitHub Issue：使用 [任务模板](.github/ISSUE_TEMPLATE/task.md)

1. 检查 [项目结构](PROJECT_STRUCTURE.cn.md) 中的**命名规范**
2. 参考 [测试指南](guides/TESTING.md) - 编写测试
3. 查看 [开发工作流](guides/DEVELOPMENT.md) - 遵循流程
4. 提交 PR 前运行 CI 检查

### 🧪 评估和优化

1. 查看 [RAGAS 指标说明](evaluation/RAGAS_METRICS.md)
2. 参考 [评估框架设计](evaluation/EVALUATION_FRAMEWORK.md)
3. 阅读 [基准测试报告](evaluation/BENCHMARK_REPORTS.md)

### 🐳 部署和运维

1. 了解 [系统架构](architecture/OVERVIEW.md)
2. 参考 [部署指南](guides/DEPLOYMENT.md)
3. 学习 [Cloud Native 开发](guides/CLOUD_NATIVE.md)
4. 检查 [故障排查](guides/TROUBLESHOOTING.md)

### 🔒 安全和合规

1. 阅读 [安全设计](architecture/SECURITY.md)
2. 查看 [项目结构](PROJECT_STRUCTURE.cn.md) 中的**数据管理**部分
3. 参考 [数据流设计](architecture/DATA_FLOW.md)

### 📊 监控和可观测性

1. 阅读 [可观测性架构](architecture/OBSERVABILITY.md)
2. 参考 [数据流设计](architecture/DATA_FLOW.md)
3. 查看 [RAGAS 指标说明](evaluation/RAGAS_METRICS.md)

---

## 📋 文档维护

### 更新文档

所有文档应该遵循以下规则：

1. **命名规范**：
   - 指南/架构文档：`UPPER_SNAKE_CASE.md`
   - 规划文档：`lowercase` 或 `index.md`
   - 中文版本：`filename.cn.md`
   - 英文版本：`filename.en.md`

2. **结构**：
   - 每个主要文档都应有中英文版本
   - 使用清晰的标题层级
   - 添加快速参考表和代码示例
   - 包含"相关文档"链接

3. **版本控制**：
   - 所有 `.md` 文件提交到 Git
   - 定期更新过时内容
   - 使用 commit message 说明变更

### 添加新文档

1. 决定合适的目录位置
2. 使用标准命名规范
3. 创建中英文版本
4. 更新此索引文档
5. 在相关文档中添加交叉引用

---

## 🔗 外部链接

- **[GitHub Repository](https://github.com/yourusername/VedaAide)**
- **[GitHub Pages 演示](https://yourusername.github.io/VedaAide)**
- **[LangChain 文档](https://python.langchain.com/)**
- **[LlamaIndex 文档](https://docs.llamaindex.ai/)**
- **[Qdrant 文档](https://qdrant.tech/documentation/)**
- **[RAGAS 文档](https://ragas.io/)**

---

## 🤝 贡献

遇到文档问题或有改进建议？

1. 创建 Issue：清晰描述问题或建议
2. 提交 PR：提交改进的文档
3. 参考 [贡献指南](../CONTRIBUTING.md)

---

## 📝 最后更新

- **日期**：2026-04-22
- **维护者**：VedaAide 团队
- **版本**：1.0.0
