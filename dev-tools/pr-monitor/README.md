# PR Monitor - 使用 Copilot Chat 的自主 PR 管理系统

自动监控 GitHub PR 并基于 PR Comments 使用 VS Code Copilot Chat 自动评估和执行代码改动的守护程序。

## 核心特性

✅ **无需 Token** - 使用 `gh cli` 进行 GitHub 认证
✅ **纯 TypeScript** - 单一语言，单一运行时（Node.js）
✅ **Copilot Chat 集成** - AI 驱动的评论评估和代码生成
✅ **Auto 模型自选** - Copilot Chat 智能选择最优模型
✅ **安全第一** - 置信度阈值（0.7）、风险评估、信任用户列表
✅ **完整审计** - 所有改动都提交到 Git，前缀为 `Auto:`
✅ **优雅关闭** - 支持信号处理（SIGINT、SIGTERM）

## 系统架构

```
GitHub PR
    ↓
PR Monitor (dev-tools/pr-monitor)
    ├─ 使用 gh CLI 获取 PR 和 review
    ├─ HTTP POST /evaluate 到 Copilot Chat
    │  └─ Copilot 判断：可实施？置信度？风险？
    ├─ HTTP POST /generate-implementation 到 Copilot Chat
    │  └─ Copilot 生成代码改动
    └─ Git checkout、应用、提交、推送
        ↓
GitHub PR 自动更新
```

## 快速开始（5 分钟）

### 前置要求

- Node.js 18+
- 已安装并认证 `gh` CLI（`gh auth login`）
- VS Code 安装 Copilot Chat Extension 并运行（pr-monitor-chat）

### 设置步骤

```bash
cd dev-tools/pr-monitor

# 1. 安装依赖
npm install

# 2. 配置环境
cp .env.example .env
# 编辑 .env（大多数情况下默认值已足够）

# 3. 构建 TypeScript
npm run build

# 4. 启动监控
npm start
```

### 在 VS Code 中

**选项 1：自动启动（推荐）**
```
Ctrl+Shift+D → "Start PR Monitor (Copilot Chat)"
```

**选项 2：手动启动**
```bash
cd dev-tools/pr-monitor
npm start
```

## 配置说明

### 环境变量

```bash
# Copilot Chat API（确保 Extension 运行中）
COPILOT_CHAT_URL=http://localhost:3456

# 轮询间隔（秒）
PR_MONITOR_INTERVAL=1800    # 30 分钟

# 自动提交/推送
AUTO_COMMIT=true
AUTO_PUSH=true

# 提交前验证
VERIFY_BEFORE_COMMIT=true

# 信任的 GitHub 用户（逗号分隔）
TRUSTED_USERS=DerekJi,derekj_youi
```

### GitHub 认证

**无需配置！** PR Monitor 使用 `gh cli` 自动读取：
- `~/.config/gh/hosts.yml`（Linux/Mac）
- `%APPDATA%\GitHub CLI\hosts.yml`（Windows）

验证：
```bash
gh auth status
```

## 工作原理

### 1. 监控循环（每 30 分钟）

```typescript
while (running) {
  // 使用 gh pr list 获取开放的 PR
  const prs = await gitClient.getOpenPRs();

  // 获取每个 PR 的 reviews：gh pr view N --json reviews
  for (const pr of prs) {
    const reviews = await gitClient.getPRReviews(pr.number);

    // 处理每个 comment
    for (const review of reviews) {
      await processComment(pr, review);
    }
  }

  // 等待下一轮
  sleep(POLL_INTERVAL);
}
```

### 2. Comment 评估

```typescript
// 发送到 Copilot Chat
const evaluation = await evaluator.evaluate({
  pr_number: 25,
  pr_title: "feat: 添加功能",
  comment_author: "DerekJi",
  comment_body: "请添加文档",
  // ... 其他上下文
});

// 返回结果：
{
  "is_actionable": true,
  "confidence": 0.85,        // 必须 >= 0.7
  "risk_level": "low",       // 必须不是 "high"
  "suggested_changes": "...",
  // ... 其他字段
}
```

### 3. 实现生成

```typescript
// 如果评估通过，请求实现
const implementation = await executor.getImplementation(
  commentBody,
  evaluation
);

// 格式：
// FILE: src/utils.ts
// ACTION: create
// ---
// <文件内容>
// ---
```

### 4. 执行

```typescript
// 切换到 PR 分支
git checkout feat/branch

// 应用改动
fs.writeFile("src/utils.ts", content);

// 提交
git commit -m "Auto: feature_addition"

// 推送
git push origin feat/branch
```

## 安全特性

### 仅信任用户

只处理配置的用户的 Comment：
```bash
TRUSTED_USERS=DerekJi,derekj_youi
```

### 置信度阈值

仅当 Copilot 置信度 >= 70% 时执行：
```typescript
if (evaluation.confidence < 0.7) {
  skip();  // 太不确定
}
```

### 风险评估

从不执行高风险改动：
```typescript
if (evaluation.risk_level === "high") {
  skip();  // 需要手动审查
}
```

### 保护路径

无法修改：
- `.git/` - 仓库元数据
- `.github/workflows/` - CI/CD 配置
- 敏感配置文件

### Git 审计

所有改动都提交并带有 `Auto:` 前缀：
```bash
git log --oneline | grep "Auto:"
# 5a2b3c4 Auto: documentation_update
# 7e8f9a0 Auto: bug_fix
```

## 开发

### 从 TypeScript 构建

```bash
npm run build
```

### 开发模式运行

```bash
npm run dev
```

### Lint 代码

```bash
npm run lint
```

### 格式化代码

```bash
npm run format
```

## 使用示例

### 1. 创建带不完整文档的 PR

```
PR #25: feat: 添加用户认证
```

### 2. 添加 review comment

```
@monitor: API 文档需要包含新的认证端点。
请更新 docs/API.md，添加认证流程。
```

### 3. 系统自动执行

```
2026-04-26 10:30:17 Processing PR #25: feat: 添加用户认证
2026-04-26 10:30:18   Evaluating comment by DerekJi
2026-04-26 10:30:19   Evaluation: actionable=true confidence=0.91 risk=low
2026-04-26 10:30:20   Executing changes...
2026-04-26 10:30:21   ✓ Successfully executed changes
2026-04-26 10:30:22   Pushed to origin/feat/branch
```

### 4. PR 自动更新

文档已更新并提交到 PR 分支。

## 故障排除

### "无法连接到 Copilot Chat API"

**问题：** Extension 未运行

**解决：**
1. 确保 GitHub Copilot Chat Extension 已安装
2. 启动 VS Code
3. PR Monitor 会在 Extension 加载时自动连接

### "gh CLI 未配置"

**问题：** `gh auth status` 失败

**解决：**
```bash
gh auth login
# 按照提示进行认证
```

### Comment 未被执行

**可能原因：**
- 用户不在 TRUSTED_USERS 中
- 置信度太低（< 0.7）
- 风险等级太高
- 已处理过该 comment

**调试：**
- 查看监控输出日志
- 检查 `.pr-monitor-state/processed-comments.json`

## 架构详情

### GitHub 客户端 (github-client.ts)

使用 `gh cli` 的 `execSync` 避免 token 管理：

```typescript
// 而不是：axios + GITHUB_TOKEN
// 我们使用：
gh pr list --repo owner/repo ...
gh pr view N --json ...
git checkout branch
git push origin branch
```

### 评估器 (evaluator.ts)

HTTP 客户端连接 Copilot Chat API：

```typescript
POST http://localhost:3456/evaluate
{
  "pr_number": 25,
  "comment_body": "...",
  // ... 上下文
}

返回：
{
  "is_actionable": true,
  "confidence": 0.85,
  ...
}
```

### 执行器 (executor.ts)

解析实现并应用到文件系统：

```
FILE: src/main.ts
ACTION: modify
---
<修改后内容>
---

FILE: tests/main.test.ts
ACTION: create
---
<新测试内容>
---
```

### 监控器 (monitor.ts)

主循环，协调所有组件并处理信号。

## 限制

- Comment 仅处理一次（幂等追踪）
- 无法跨仓库修改
- 无法绕过分支保护
- 30 分钟轮询（可配置）

## 未来改进

- [ ] 实时 webhook 而非轮询
- [ ] 自定义评估规则
- [ ] Slack/Email 通知
- [ ] Web 监控面板
- [ ] Comment 重新评估
- [ ] 预览模式的部分自动执行

## 文件结构

```
dev-tools/pr-monitor/
├── src/
│   ├── index.ts                 # 入口点
│   ├── config.ts                # 配置管理
│   ├── types.ts                 # TypeScript 类型
│   ├── github-client.ts         # gh CLI 包装器
│   ├── evaluator.ts             # Copilot Chat 评估器
│   ├── executor.ts              # 改动执行器
│   └── monitor.ts               # 主监控循环
├── dist/                        # 编译后的 JavaScript（自动生成）
├── package.json
├── tsconfig.json
├── .eslintrc.json
├── .prettierrc
├── .env.example
├── .gitignore
├── README.en.md                 # 英文文档
└── README.md                    # 本文档
```

## 许可证

MIT

## 支持

遇到问题或有疑问：
1. 查看终端/VS Code 输出中的日志
2. 验证 `gh auth status`
3. 检查 `.pr-monitor-state/processed-comments.json` 中的追踪信息
4. 查看 Copilot Chat Extension 的状态

---

**开始自动化工作流吧！🚀**
