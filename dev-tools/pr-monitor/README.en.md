# PR Monitor - Autonomous PR Management with Copilot Chat

Autonomous GitHub PR monitoring daemon that automatically evaluates and executes code changes based on PR comments using VS Code Copilot Chat.

## Features

✅ **No Token Required** - Uses `gh cli` for GitHub authentication
✅ **Pure TypeScript** - Single language, single runtime (Node.js)
✅ **Copilot Chat Integration** - AI-powered comment evaluation and implementation
✅ **Auto Model Selection** - Copilot Chat intelligently selects best model
✅ **Safety First** - Confidence threshold (0.7), risk assessment, trusted users list
✅ **Complete Audit** - All changes committed to Git with `Auto:` prefix
✅ **Graceful Shutdown** - Clean signal handling (SIGINT, SIGTERM)

## System Architecture

```
GitHub PR
    ↓
PR Monitor (dev-tools/pr-monitor)
    ├─ Uses gh CLI to fetch PRs and reviews
    ├─ HTTP POST /evaluate to Copilot Chat
    │  └─ Copilot judges: actionable? confidence? risk?
    ├─ HTTP POST /generate-implementation to Copilot Chat
    │  └─ Copilot generates code changes
    └─ Git checkout, apply, commit, push
        ↓
GitHub PR Updated
```

## Quick Start (5 minutes)

### Prerequisites

- Node.js 18+
- `gh` CLI installed and authenticated (`gh auth login`)
- VS Code with Copilot Chat Extension running (pr-monitor-chat)

### Setup

```bash
cd dev-tools/pr-monitor

# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env if needed (defaults work for most setups)

# 3. Build TypeScript
npm run build

# 4. Start monitoring
npm start
```

### In VS Code

**Option 1: Automatic (Recommended)**
```
Ctrl+Shift+D → "Start PR Monitor (Copilot Chat)"
```

**Option 2: Manual**
```bash
cd dev-tools/pr-monitor
npm start
```

## Configuration

### Environment Variables

```bash
# Copilot Chat API (ensure Extension is running)
COPILOT_CHAT_URL=http://localhost:3456

# Poll interval (seconds)
PR_MONITOR_INTERVAL=1800    # 30 minutes

# Auto commit/push
AUTO_COMMIT=true
AUTO_PUSH=true

# Verify before committing
VERIFY_BEFORE_COMMIT=true

# Trusted GitHub usernames (comma-separated)
TRUSTED_USERS=DerekJi,derekj_youi
```

### GitHub Authentication

No configuration needed! PR Monitor uses `gh cli` which reads from:
- `~/.config/gh/hosts.yml` (Linux/Mac)
- `%APPDATA%\GitHub CLI\hosts.yml` (Windows)

Verify with:
```bash
gh auth status
```

## How It Works

### 1. Monitoring Loop (Every 30 minutes)

```typescript
while (running) {
  // Fetch open PRs using: gh pr list ...
  const prs = await gitClient.getOpenPRs();

  // Get reviews for each PR using: gh pr view N --json reviews
  for (const pr of prs) {
    const reviews = await gitClient.getPRReviews(pr.number);

    // Process each comment
    for (const review of reviews) {
      await processComment(pr, review);
    }
  }

  // Sleep for interval
  sleep(POLL_INTERVAL);
}
```

### 2. Comment Evaluation

```typescript
// Send to Copilot Chat
const evaluation = await evaluator.evaluate({
  pr_number: 25,
  pr_title: "feat: add feature",
  comment_author: "DerekJi",
  comment_body: "Please add documentation",
  // ... other context
});

// Returns:
{
  "is_actionable": true,
  "confidence": 0.85,        // Must be >= 0.7
  "risk_level": "low",       // Must not be "high"
  "suggested_changes": "...",
  // ... other fields
}
```

### 3. Implementation Generation

```typescript
// If evaluation passed, ask for implementation
const implementation = await executor.getImplementation(
  commentBody,
  evaluation
);

// Format:
// FILE: src/utils.ts
// ACTION: create
// ---
// <file content>
// ---
```

### 4. Execution

```typescript
// Check out PR branch
git checkout feat/branch

// Apply changes
fs.writeFile("src/utils.ts", content);

// Commit
git commit -m "Auto: feature_addition"

// Push
git push origin feat/branch
```

## Security Features

### Trusted Users Only

Only comments from configured users are processed:
```bash
TRUSTED_USERS=DerekJi,derekj_youi
```

### Confidence Threshold

Only execute if Copilot is >= 70% confident:
```typescript
if (evaluation.confidence < 0.7) {
  skip();  // Too uncertain
}
```

### Risk Assessment

Never execute high-risk changes:
```typescript
if (evaluation.risk_level === "high") {
  skip();  // Manual review needed
}
```

### Protected Paths

Cannot modify:
- `.git/` - Repository metadata
- `.github/workflows/` - CI/CD configs
- Sensitive configuration files

### Git Audit

All changes are committed with `Auto:` prefix:
```bash
git log --oneline | grep "Auto:"
# 5a2b3c4 Auto: documentation_update
# 7e8f9a0 Auto: bug_fix
```

## Development

### Build from TypeScript

```bash
npm run build
```

### Run in development mode

```bash
npm run dev
```

### Lint code

```bash
npm run lint
```

### Format code

```bash
npm run format
```

## Example Workflow

### 1. Create PR with incomplete documentation

```
PR #25: feat: add user authentication
```

### 2. Add review comment

```
@monitor: The API documentation needs to include the new auth endpoints.
Please update docs/API.md with the authentication flow.
```

### 3. System executes

```
2026-04-26 10:30:17 Processing PR #25: feat: add user authentication
2026-04-26 10:30:18   Evaluating comment by DerekJi
2026-04-26 10:30:19   Evaluation: actionable=true confidence=0.91 risk=low
2026-04-26 10:30:20   Executing changes...
2026-04-26 10:30:21   ✓ Successfully executed changes
2026-04-26 10:30:22   Pushed to origin/feat/branch
```

### 4. PR automatically updated

Documentation file is updated and committed to PR branch.

## Troubleshooting

### "Cannot connect to Copilot Chat API"

**Problem:** Extension not running

**Solution:**
1. Ensure GitHub Copilot Chat Extension is installed
2. Start VS Code
3. PR Monitor will auto-connect when Extension loads

### "gh CLI not configured"

**Problem:** `gh auth status` fails

**Solution:**
```bash
gh auth login
# Follow prompts to authenticate
```

### Comment not executed

**Reasons:**
- User not in TRUSTED_USERS
- Confidence too low (< 0.7)
- Risk level too high
- Already processed

**Debug:**
- Check logs in monitor output
- Look at `.pr-monitor-state/processed-comments.json`

## Architecture Details

### GitHub Client (github-client.ts)

Uses `gh cli` with `execSync` to avoid token management:

```typescript
// Instead of: axios with GITHUB_TOKEN
// We use:
gh pr list --repo owner/repo ...
gh pr view N --json ...
git checkout branch
git push origin branch
```

### Evaluator (evaluator.ts)

HTTP client to Copilot Chat API:

```typescript
POST http://localhost:3456/evaluate
{
  "pr_number": 25,
  "comment_body": "...",
  // ... context
}

Returns:
{
  "is_actionable": true,
  "confidence": 0.85,
  ...
}
```

### Executor (executor.ts)

Parses implementation and applies to filesystem:

```
FILE: src/main.ts
ACTION: modify
---
<modified content>
---

FILE: tests/main.test.ts
ACTION: create
---
<new test content>
---
```

### Monitor (monitor.ts)

Main loop orchestrating all components with signal handling.

## Limitations

- Comments processed once (idempotent tracking)
- No cross-repo modifications
- No branch protection bypass
- 30-minute polling (configurable)

## Future Enhancements

- [ ] Real-time webhook instead of polling
- [ ] Custom evaluation rules
- [ ] Slack/Email notifications
- [ ] Web UI for monitoring
- [ ] Comment re-evaluation
- [ ] Partial auto-execution with preview

## File Structure

```
dev-tools/pr-monitor/
├── src/
│   ├── index.ts                 # Entry point
│   ├── config.ts                # Configuration
│   ├── types.ts                 # TypeScript types
│   ├── github-client.ts         # gh CLI wrapper
│   ├── evaluator.ts             # Copilot Chat evaluator
│   ├── executor.ts              # Change executor
│   └── monitor.ts               # Main monitor loop
├── dist/                        # Compiled JavaScript (generated)
├── package.json
├── tsconfig.json
├── .eslintrc.json
├── .prettierrc
├── .env.example
├── .gitignore
└── README.md
```

## License

MIT

## Support

For issues or questions:
1. Check logs in terminal/VS Code output
2. Verify `gh auth status`
3. Check `.pr-monitor-state/processed-comments.json` for tracking
4. Review Copilot Chat Extension status

---

**Happy automating! 🚀**
