---
applyTo: "**"
---

# VedaAide Project Structure and Directory Guidelines

## Mandatory Directory Organization

### Root Level Structure

```
VedaAide.py/
├── src/                  # 源代码（Python）
├── tests/                # 测试代码
├── docs/                 # 文档
├── scripts/              # 可执行脚本
├── infra/                # 基础设施配置（Docker）
├── config/               # 配置文件
├── data/                 # 数据目录
├── .github/              # GitHub 配置
├── .temp/                # 临时文件（重要！）
├── dev-tools/            # 开发工具（见下方语言规定）
├── docker-compose.yml    # 本地开发环境
├── pyproject.toml        # Python 依赖管理
└── README.md / README.cn.md
```

---

## dev-tools/ 子目录语言规定 (CRITICAL)

| 子目录 | 语言 | 说明 |
|-------|------|------|
| `dev-tools/pr-monitor/` | **TypeScript (Node.js)** | VS Code PR 监控工具，所有代码必须用 `.ts` 文件，用 `tsc` 编译，**禁止生成 `.py` 文件** |

### ⚠️ AI 助手注意事项

当在 `dev-tools/pr-monitor/` 目录内生成或修改代码时：

- ✅ 必须使用 TypeScript（`.ts` 文件）
- ✅ 必须符合该目录的 `tsconfig.json` 配置
- ❌ **严禁生成 Python 文件（`.py`）** — executor 会在运行时自动拒绝 `.py` 文件
- ❌ 严禁覆盖 `package.json`、`tsconfig.json` 等项目配置文件
- ❌ 严禁在文件内容中使用 markdown code fence（` ``` `）

> **强制执行**：`executor.ts` 已在代码层面阻止 `.py` 文件写入，违规时会打印 `Blocked: Python files are not allowed` 并跳过。

---

## .temp/ 目录：临时 AI 生成文件 (CRITICAL)

### 📋 用途

`.temp/` 目录用于存放 **临时的、由 AI 助手生成的文件**，包括但不限于：

- 🤖 AI 生成的脚本和工具
- 📝 临时文档和草稿
- 🧪 测试脚本和 POC 代码
- 📊 临时评估报告
- 📋 GitHub 自动化脚本
- 🔍 诊断和调试文件

### ✅ 应该放在 .temp/ 的文件类型

| 文件类型 | 示例 | 说明 |
|---------|------|------|
| GitHub 工作流脚本 | `create_phase1_issues.sh`, `issues.txt` | gh CLI 自动化脚本 |
| 评估报告 | `ragas_results_20250422.json` | 临时评估结果 |
| 调试脚本 | `test_retrieval_quality.py` | POC 验证脚本 |
| 构建日志 | `docker-build.log` | 临时构建输出 |
| 性能基准 | `benchmark-results.csv` | 临时基准测试数据 |
| 临时分析 | `data-quality-analysis.md` | 草稿分析文档 |

### ❌ 不应该放在 .temp/ 的文件类型

| 文件类型 | 正确位置 | 原因 |
|---------|---------|------|
| 生产代码 | `src/` | .temp/ 被 git 忽略 |
| 单元测试 | `tests/` | 测试应该被版本控制 |
| 最终文档 | `docs/` | 文档应该被版本控制 |
| 配置文件 | `config/` | 配置应该被版本控制 |
| 核心脚本 | `scripts/` | 生产脚本应该被版本控制 |

### 🔧 .gitignore 规则

```gitignore
# 忽略整个 .temp 目录及其所有文件
.temp/**

# 但保留这些文件（git会追踪它们）
!.temp/.gitkeep
!.temp/README.md
```

### 📚 文件管理流程

#### 1. 生成时
```bash
# 创建文件时在头部添加注释
# 生成时间：2026-04-22 15:00 UTC
# 生成工具：GitHub Copilot
# 用途：批量创建 Phase 1 GitHub Issues
# 迁移状态：临时 → 需要评审后迁移到正式位置

#!/bin/bash
# ... script content
```

#### 2. 整理时
- 定期（每周一）审查 `.temp/` 目录中的文件
- 评估文件是否有持久化价值
- 有价值的文件移到正式目录（见迁移表）
- 无价值的文件删除

#### 3. 迁移时
遵循以下迁移规则：

| 来源文件 | 目标位置 | 迁移条件 |
|---------|---------|--------|
| GitHub 工作流脚本 | `scripts/github/` | 经过验证且可重用 |
| 临时文档 | `docs/{planning,guides,architecture}/` | 质量达到发布标准 |
| 测试脚本 | `tests/{unit,integration,evaluation}/` | 已集成到测试套件 |
| 评估报告 | `data/evaluation-results/` | 成为基准数据 |
| 构建工件 | 归档或删除 | 不需要长期保存 |

#### 4. 清理时
```bash
# 查看 .temp/ 中超过 30 天的文件
find .temp -type f -mtime +30

# 删除无用的临时文件
rm .temp/old-debug-script.py

# 注意：.temp/.gitkeep 和 .temp/README.md 保留
```

### 📋 命名规范

遵循以下命名规范以便于管理：

```
.temp/
├── temp-docs/
│   └── task-breakdown-analysis-2026-04-22.md     # YYYY-MM-DD 格式
├── test-scripts/
│   └── test_hybrid_search_debug_2026-04-22.py
├── evaluation-reports/
│   └── ragas-results_2026-04-22_14-30.json       # 包含时间戳
├── github-automation/
│   ├── create_phase1_issues.sh                    # 明确的目的名称
│   └── issues.txt
└── build-artifacts/
    └── docker-build-2026-04-22.log                # 包含日期
```

**命名规则**:
- 使用 kebab-case（单词用 `-` 分隔）
- 包含 ISO 日期格式：`YYYY-MM-DD`
- 避免空格
- 文件名应该自说明其用途

### 🔄 CI/CD 和 .temp/

`.temp/` 目录在 CI/CD 中的处理：

```yaml
# GitHub Actions workflow 示例
- name: Clean .temp directory
  if: github.event_name == 'push'
  run: |
    find .temp -type f -mtime +30 ! -name '.gitkeep' ! -name 'README.md' -delete
```

### 💾 .temp/ 内容示例

当前目录结构：
```
.temp/
├── .gitkeep                          # 保留目录存在
├── README.md                         # 使用指南（保留）
├── create_phase1_issues.sh           # GitHub 自动化脚本
├── issues.txt                        # GitHub Issues 数据源
└── health-check-report.md            # 临时诊断报告
```

---

## 其他重要目录

### src/ - 源代码
- 所有 Python 源代码
- 遵循 SRP、DRY 原则
- 必须有类型注解
- 必须有文档字符串

### tests/ - 测试代码
- 单元测试：`tests/unit/`
- 集成测试：`tests/integration/`
- E2E 测试：`tests/e2e/`
- 所有测试文件都应该被版本控制

### docs/ - 文档
- 规划文档：`docs/planning/`
- 架构文档：`docs/architecture/`
- API 文档：`docs/api/`
- 所有文档都应该被版本控制

### scripts/ - 生产脚本
- 部署脚本
- 数据迁移脚本
- 维护脚本
- 所有脚本都应该被版本控制

### config/ - 配置文件
- 应用配置：`config/app.yaml`
- 数据库配置：`config/database.yaml`
- LLM 配置：`config/llm.yaml`
- 所有配置都应该被版本控制（不包含敏感信息）

### infra/ - 基础设施
- Docker 配置：`infra/docker/`
- 所有基础设施代码都应该被版本控制

---

## 工作流中的目录使用

### 新特性开发
```
1. 在 src/ 中创建新的功能代码
2. 在 tests/ 中编写测试
3. 如果需要临时脚本进行验证，放在 .temp/
4. 验证完成后，如果脚本有价值，移到 scripts/
```

### 数据探索和分析
```
1. 临时数据处理脚本放在 .temp/test-scripts/
2. 生成的分析报告放在 .temp/evaluation-reports/
3. 完成后，如果有价值的发现，记录到 docs/
```

### GitHub 自动化
```
1. 创建自动化脚本，放在 .temp/
2. 经过测试和验证
3. 如果是可重用的工具，移到 scripts/github/
4. 更新 .github/skills/github-cli-workflow/ 中的文档
```

---

## 检查清单

### 对于所有文件
- [ ] 源代码 → `src/` 或 `tests/` 或 `scripts/`（被版本控制）
- [ ] 文档 → `docs/`（被版本控制）
- [ ] 临时文件 → `.temp/`（被 git 忽略）

### 对于 .temp/ 中的文件
- [ ] 文件名遵循命名规范（kebab-case、YYYY-MM-DD）
- [ ] 文件头部有生成时间和用途说明
- [ ] 定期审查（至少每两周一次）
- [ ] 超过 30 天的无用文件已删除
- [ ] 有价值的文件已迁移到正式位置

---

## 参考资源

- [.temp/ README.md](.temp/README.md) - 详细的文件使用指南
- [.gitignore](../.gitignore) - git 忽略规则
- [GitHub CLI Workflow SKILL](.github/skills/github-cli-workflow/SKILL.md) - GitHub 自动化脚本示例
