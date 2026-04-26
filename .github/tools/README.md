# PR Monitor Daemon (with VS Code Copilot Chat)

自动监控 GitHub PR Comments，并根据 **Copilot Chat** 的智能判断自动执行修改。

## 🎯 核心特性

- ✅ **VS Code Copilot Chat 集成**：使用 Copilot Chat 的 Auto 模型进行智能评估
- ✅ **自动启动**：VS Code 打开工作区时自动启动监控
- ✅ **定时轮询**：每 30 分钟检查一次 PR Comments
- ✅ **智能判断**：综合考虑 Issue 描述、PR 改动、Comment 内容
- ✅ **安全执行**：只有高可信度且低风险的修改才会自动执行
- ✅ **完整审计**：所有修改都提交到 Git，可追溯

## 系统架构

```
VS Code
  ├── .vscode/extensions/pr-monitor-chat (TypeScript Extension)
  │   └── HTTP API on localhost:3456
  │       ├── POST /evaluate → Copilot Chat 评估 Comment
  │       └── POST /generate-implementation → 生成实现代码
  │
  └── .github/tools (Python Daemon)
      ├── pr_monitor.py (主监控循环)
      ├── pr_evaluator.py (评估器)
      └── pr_executor.py (执行器)
```

## 🚀 快速开始

### 步骤 1：安装依赖

```bash
cd /d/source/VedaAide.py/.github/tools
pip install -r requirements.txt
```

### 步骤 2：配置环境变量

```bash
cp .env.example .env
# 编辑 .env，至少填写：
# GITHUB_TOKEN=ghp_...
# COPILOT_CHAT_HOST=localhost
# COPILOT_CHAT_PORT=3456
```

### 步骤 3：在 VS Code 中启动

**选项 A：自动启动（推荐）**
- VS Code 打开 VedaAide.py 工作区时会自动启动
- 或手动运行任务：`Ctrl+Shift+D` → "Start PR Monitor (with Copilot Chat)"

**选项 B：手动启动**
```bash
python /d/source/VedaAide.py/.github/tools/pr_monitor.py
```

### 步骤 3b：验证 Copilot Chat Extension 已加载

在 VS Code 输出中应该看到：
```
PR Monitor Chat extension activating...
PR Monitor Chat API listening on http://localhost:3456
```

## 📖 工作流程

### 监控循环

1. **定时检查**（每 30 分钟）
   - 获取所有 open 的 PR
   - 获取每个 PR 的 review comments

2. **评估 Comment**
   - 跳过已处理过的 comment
   - 跳过非信任用户的 comment
   - 调用 **Copilot Chat** 评估：
     - "这个 Comment 清晰明确吗？"
     - "请求的改动合理吗？"
     - "有安全风险吗？"
     - 返回 JSON: `{"is_actionable": bool, "confidence": 0-1, "risk_level": "low|medium|high"}`

3. **执行决策**
   - 如果 `confidence >= 0.7` 且 `risk_level != "high"` → 执行
   - 否则 → 记录日志，跳过

4. **执行修改**
   - Checkout PR 分支
   - 调用 **Copilot Chat** 生成实现代码
   - 应用修改到本地
   - Commit + Push

### 示例 Comment 流程

**GitHub PR #25 中的 Comment：**
```
@monitor: The Chinese documentation is missing.
Please create README.cn.md following the same structure as README.md.
```

**系统执行：**
```
2026-04-26 10:30:17 - Processing Comment
2026-04-26 10:30:18 - Evaluating with Copilot Chat...
2026-04-26 10:30:19 - Evaluation: actionable=true confidence=0.92 risk=low
2026-04-26 10:30:19 - Generating implementation...
2026-04-26 10:30:21 - Applying changes to README.cn.md
2026-04-26 10:30:21 - Commit: Auto: docs_update
2026-04-26 10:30:22 - Push to feat/branch
2026-04-26 10:30:22 - ✓ Successfully executed
```

**PR 自动更新** ✅

## 🧠 Copilot Chat Auto 模式

VS Code Copilot Chat 支持 **Auto** 模式，自动选择最优的模型：
- 简单任务 → 用轻量模型（快速、便宜）
- 复杂任务 → 用强大模型（准确、完整）

本系统已配置为 Auto 模式，提高性价比。

## 📋 环境配置

### `.env` 参数说明

```bash
# GitHub 配置
GITHUB_OWNER=DerekJi
GITHUB_REPO=VedaAide.py
GITHUB_TOKEN=ghp_your_token_here    # 必需

# Copilot Chat 配置
COPILOT_CHAT_HOST=localhost
COPILOT_CHAT_PORT=3456

# 监控配置
PR_MONITOR_INTERVAL=1800            # 检查间隔（秒）
AUTO_COMMIT=true
AUTO_PUSH=true

# 信任用户
TRUSTED_USERS=DerekJi,derekj_youi
```

## 📊 监控日志

日志位置：`.github/tools/state/monitor.log`

### 查看日志

```bash
# 实时查看
tail -f .github/tools/state/monitor.log

# VS Code 任务
Ctrl+Shift+P → "View PR Monitor Logs"
```

### 日志示例

```
2026-04-26 10:30:15 - pr_monitor - INFO - Starting PR Monitor (interval: 1800s)
2026-04-26 10:30:15 - pr_monitor - INFO - Trusted users: DerekJi, derekj_youi
2026-04-26 10:30:16 - pr_monitor - INFO - Checking PRs...
2026-04-26 10:30:17 - pr_monitor - INFO - Found 2 open PRs
2026-04-26 10:30:17 - pr_monitor - INFO - Processing PR #25: feat(data): complete Task 1.4
2026-04-26 10:30:18 - pr_monitor - INFO -   Evaluating comment #1234567890 by DerekJi
2026-04-26 10:30:19 - pr_monitor - INFO -     Evaluation: actionable=True confidence=0.85 risk=low
2026-04-26 10:30:19 - pr_monitor - INFO -     Executing changes for PR #25...
2026-04-26 10:30:21 - pr_monitor - INFO -     ✓ Successfully executed changes
```

## VS Code Task 集成

### 可用任务

在 VS Code 中 (`Ctrl+Shift+P` → "Tasks: Run Task")：

| 任务 | 说明 |
|------|------|
| Start PR Monitor (with Copilot Chat) | 启动监控守护程序 |
| Install PR Monitor Dependencies | 安装 Python 依赖 |
| Setup PR Monitor (.env from .env.example) | 初始化配置文件 |
| View PR Monitor Logs | 查看监控日志 |

### 自动启动配置

在 `runOptions` 中配置 `runOn: "folderOpen"`，VS Code 打开工作区时自动启动。

可在 `.vscode/tasks.json` 中修改或关闭此功能。

## 🔒 安全特性

| 特性 | 说明 |
|------|------|
| **信任列表** | 只有 `TRUSTED_USERS` 中的用户的 Comment 会被处理 |
| **置信度检查** | 必须 >= 0.7（70%）置信度才会执行 |
| **风险评估** | high 风险的修改会被拒绝 |
| **保护路径** | `.git/`、`.github/` 等受保护目录无法修改 |
| **分支隔离** | 改动只应用到 PR 分支，不直接改 main |
| **完整审计** | 所有执行都提交到 Git，可完整回溯 |
| **Dry-Run 模式** | 可配置先预览改动而不实际执行 |

## 🐛 故障排除

### 问题 1：Copilot Chat Extension 未找到

**症状：**
```
Cannot connect to Copilot Chat API at http://localhost:3456
```

**解决：**
1. 确认安装了 GitHub Copilot Chat 扩展
2. VS Code 扩展面板搜索 "Copilot Chat"
3. 重启 VS Code
4. 查看输出：`Copilot Chat extension activating...`

### 问题 2：监控程序无法启动

**症状：**
```
GITHUB_TOKEN not set
```

**解决：**
```bash
cp .env.example .env
# 编辑 .env，填入 GITHUB_TOKEN
# 从 https://github.com/settings/tokens 生成
```

### 问题 3：Comment 未被执行

**可能原因：**
- 置信度太低（< 0.7）
- 风险等级太高（high）
- 用户不在信任列表
- Comment 内容不够清晰
- Copilot Chat 暂时离线

**检查日志：**
```bash
grep "Evaluation:" .github/tools/state/monitor.log
```

## 🧪 测试

### 手动测试 Copilot Chat API

```bash
# 1. 启动监控（包括 Extension）
python .github/tools/pr_monitor.py

# 2. 测试评估端点
curl -X POST http://localhost:3456/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "pr_number": 25,
    "pr_title": "test",
    "pr_body": "test",
    "pr_branch": "test",
    "pr_author": "DerekJi",
    "comment_author": "DerekJi",
    "comment_body": "Add docs",
    "repository": "DerekJi/VedaAide.py"
  }'

# 应返回 JSON：
# {
#   "is_actionable": true/false,
#   "confidence": 0.0-1.0,
#   ...
# }
```

## 📚 文件结构

```
.github/tools/
├── config.py                    # 全局配置
├── pr_evaluator.py             # 评估器（HTTP 调用 Copilot Chat）
├── pr_executor.py              # 执行器
├── pr_monitor.py               # 主循环
├── requirements.txt            # Python 依赖
├── .env.example                # 环境变量模板
├── .gitignore                  # 忽略 .env 和 state/
├── start.sh / start.bat        # 启动脚本
└── state/                      # 运行时状态
    ├── processed_comments.json # 已处理的 Comment
    └── monitor.log             # 监控日志

.vscode/
├── tasks.json                  # VS Code Task 配置
├── extensions.json             # 推荐扩展
└── extensions/pr-monitor-chat/ # Copilot Chat API Extension
    ├── package.json
    ├── tsconfig.json
    └── src/extension.ts        # HTTP 服务 + Copilot Chat 集成
```

## 🚧 限制和未来改进

### 当前限制
- 一个 Comment 只处理一次（已处理过的不再处理）
- 不支持跨仓库修改
- 仅支持 GitHub（不支持 GitLab 等）

### 未来改进
- [ ] 支持手动重新处理某个 Comment
- [ ] WebSocket 实时通知而不是轮询
- [ ] 支持多个仓库
- [ ] VS Code 状态栏显示监控状态
- [ ] Comment 中集成修改预览
- [ ] 支持自定义评估规则

---

**下一步：** 见本文档开头的"快速开始"部分开始使用！
