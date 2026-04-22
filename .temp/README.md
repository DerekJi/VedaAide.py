# .temp/ 目录使用指南

此目录用于存放 AI 辅助开发过程中产生的临时文件，包括：

## 📝 文件分类

### 1. 临时文档 (temp-docs/)
- 脑暴笔记
- 需求分析草稿
- 设计草案
- API 文档初稿

示例：
```
.temp/temp-docs/
├── brainstorm-retrieval-strategy.md
├── api-design-draft.md
└── dspy-optimization-notes.md
```

### 2. 测试脚本 (test-scripts/)
- AI 生成的测试脚本
- 临时调试脚本
- 概念验证代码
- Jupyter Notebook 实验

示例：
```
.temp/test-scripts/
├── test_hybrid_search.py
├── debug_agent_state.py
├── experiment_dspy_prompt.ipynb
└── verify_deidentification.py
```

### 2.5 GitHub 工作流脚本
- GitHub CLI (gh) 自动化脚本
- 批量 Issue/PR 操作脚本
- GitHub Actions 辅助脚本

示例：
```
.temp/
├── create_phase1_issues.sh       # 批量创建 Phase 1 Issues
├── issues.txt                    # Issue 数据源
└── github-automation-template.sh # GitHub 工作流模板
```

使用方法：
```bash
cd .temp
bash create_phase1_issues.sh
```

### 3. 评估报告 (evaluation-reports/)
- RAGAS 评估临时结果
- 性能基准测试数据
- 对比分析报告

示例：
```
.temp/evaluation-reports/
├── ragas-baseline-2025-04-22.json
├── model-comparison-ollama-vs-gpt4o.csv
└── retrieval-quality-analysis.html
```

### 4. 构建工件 (build-artifacts/)
- Docker 构建日志
- 编译错误日志
- 部署测试结果

示例：
```
.temp/build-artifacts/
├── docker-build.log
├── kubectl-deploy.log
└── integration-test-results.xml
```

## ⚙️ .gitignore 配置

```gitignore
# 忽略整个 .temp 目录及其所有文件
.temp/**
# 但保留 .gitkeep 以维持目录结构
!.temp/.gitkeep
!.temp/README.md
```

## 📋 最佳实践

### 命名规范
- 使用 ISO 日期格式：`YYYY-MM-DD`
- 包含简短描述：`retrieval-optimization-2025-04-22.md`
- 避免空格，使用 kebab-case

### 文件管理
- **生成时**：在文件头部注明生成时间和用途
- **整理时**：定期（每周）审查，将有价值的文件移入正式目录
- **清理时**：超过 30 天的临时文件考虑删除

### 迁移到正式目录
当临时文件成熟后，应移动到相应的正式目录：

| 来源 | 目标 |
|-----|------|
| temp-docs/*.md | docs/{planning,guides,architecture}/ |
| test-scripts/*.py | tests/{unit,integration,evaluation}/ |
| evaluation-reports/*.json | data/evaluation-results/ |
| build-artifacts/*.log | (清理或存档) |

## 📚 示例工作流

```bash
# 1. 创建新的临时文档
echo "# API 设计草案" > .temp/temp-docs/api-design-2025-04-22.md

# 2. 开发和迭代
# ... 多次编辑和测试 ...

# 3. 文档成熟后，移至正式目录
mv .temp/temp-docs/api-design-2025-04-22.md docs/architecture/API_DESIGN.md

# 4. 更新到版本控制
git add docs/architecture/API_DESIGN.md
git commit -m "docs: add API design documentation"
```

## 🔍 不应该在这里存放的文件

❌ **不在 .temp 中存放：**
- 源代码文件（应在 src/）
- 配置文件（应在 config/ 或项目根目录）
- 数据文件（应在 data/）
- 已完成的文档（应在 docs/）

## 📌 常见场景

### 场景 1：生成测试脚本
```bash
# AI 生成的快速验证脚本
.temp/test-scripts/verify-qdrant-setup.py

# 测试后，如果是通用的，复制到 tests/integration/
cp .temp/test-scripts/verify-qdrant-setup.py tests/integration/test_qdrant.py
```

### 场景 2：记录优化思路
```bash
# 临时记录 DSPy 优化想法
.temp/temp-docs/dspy-optimization-ideas.md

# 想法验证后，融入正式文档
# docs/architecture/RAG_PIPELINE.md
```

### 场景 3：CI/CD 调试
```bash
# 保存 Docker 构建失败的日志
.temp/build-artifacts/dockerfile-debug-2025-04-22.log

# 问题解决后删除
rm .temp/build-artifacts/dockerfile-debug-2025-04-22.log
```
