---
applyTo: "**"
---

# GitHub CLI (gh) Account Configuration for VedaAide.py

## ⚠️ CRITICAL: Required GitHub Account

When working in the **VedaAide.py** repository, you **MUST** use the `DerekJi` GitHub account for all gh CLI operations.

### Correct and Incorrect Accounts

| Account | Status | Notes |
|---------|--------|-------|
| `DerekJi` | ✅ **REQUIRED** | Use this account for all VedaAide.py operations |
| `derekj_youi` | ❌ **DO NOT USE** | This account is for other projects, may cause permission issues |
| Any other account | ❌ **DO NOT USE** | Not authorized for this repository |

## Before Every Workflow Session

**Always verify your current account before performing any gh CLI operations:**

```bash
# Check current account
gh auth status

# Expected output should show:
# github.com account DerekJi
```

### If Using Wrong Account

```bash
# Switch to the correct account
gh auth switch

# When prompted, select: DerekJi
```

## Operations That Require This Check

Always verify the `DerekJi` account is active when using:

- Creating issues: `gh issue create`
- Creating pull requests: `gh pr create`
- Pushing to repository: `git push` (which uses gh auth)
- Any repository modification or CI/CD workflow triggering

## For More Details

See the detailed workflow guide: [GitHub CLI Workflow SKILL](.github/skills/github-cli-workflow/SKILL.md)
