---
name: github-cli-workflow
description: GitHub CLI (gh) workflow best practices for VedaAide project operations, including issue management, PR workflows, and batch operations
applyTo: "**"
keywords:
  - gh
  - github cli
  - issue
  - pull request
  - pr
  - workflow
  - automation
  - batch
  - create issue
  - GitHub
  - 工作流
  - 批量操作
whenToUse: |
  When working with:
  - Creating, updating, or managing GitHub Issues
  - Pull request operations and reviews
  - GitHub automation and batch operations
  - Repository management tasks
  - Issue tracking and project planning
---

# GitHub CLI (gh) Workflow for VedaAide

## Prerequisites

### Installation Check
```bash
# Verify gh is installed
which gh
# or on Windows
where gh

# Show version
gh --version
```

### Authentication

```bash
# Check authentication status
gh auth status

# Show all logged-in accounts
gh auth status --show-token

# Switch between accounts (if multiple)
gh auth switch -u <username>

# Login/re-authenticate
gh auth login
```

#### ⚠️ IMPORTANT: Required Account for VedaAide

**When working in VedaAide.py repository, you MUST use the `DerekJi` GitHub account.**

- ✅ **Correct account**: `DerekJi`
- ❌ **Wrong account**: `derekj_youi` (or any other account)

**Always check before performing any gh CLI operations:**

```bash
# Verify current account
gh auth status

# You should see: github.com account DerekJi
# If not, switch to the correct account:
gh auth switch
# Select "DerekJi" from the list
```

**Why this matters**: The `derekj_youi` account is for other projects and may not have the correct permissions or status for this repository. Using the wrong account could cause permission issues, failed pushes, or incorrect attribution.

**Before each workflow session:**
1. Run `gh auth status` to verify you're using `DerekJi`
2. If using `derekj_youi`, run `gh auth switch` and select `DerekJi`
3. Proceed with your operations (issues, PRs, pushes, etc.)

## Issue Management

### Creating Issues

#### Single Issue

**Basic creation**:
```bash
gh issue create \
  --title "Issue Title" \
  --body "Issue description"
```

**With labels and assignee**:
```bash
gh issue create \
  --title "Phase 1.1: Deploy Qdrant" \
  --body "Setup local Qdrant environment" \
  --label "phase-1" \
  --label "infrastructure" \
  --assignee @me
```

**With multiple labels** (use multiple `--label` flags):
```bash
gh issue create \
  --title "Task Title" \
  --body "Description" \
  --label "type:bug" \
  --label "priority:high" \
  --label "team:backend"
```

#### Batch Issue Creation (Multiple Issues)

**Best Practice: Create shell script**:
```bash
#!/bin/bash

# issues.sh - Create multiple issues

gh issue create \
  --title "Phase 1.1: Deploy Qdrant" \
  --body "Setup environment" \
  --label "phase-1" && echo "✓ Issue 1 created"

gh issue create \
  --title "Phase 1.2: Configure LangFuse" \
  --body "Setup LangFuse" \
  --label "phase-1" && echo "✓ Issue 2 created"

gh issue create \
  --title "Phase 1.3: Configure CosmosDB" \
  --body "Setup database" \
  --label "phase-1" && echo "✓ Issue 3 created"

echo "✓ All issues created successfully"
```

Run with:
```bash
bash create_issues.sh
```

**Alternative: Loop through CSV data**:
```bash
# issues.csv format: title|labels|body
cat issues.csv | while IFS='|' read title labels body; do
  gh issue create \
    --title "$title" \
    --body "$body" \
    $(echo "$labels" | sed 's/,/ --label /g' | sed 's/^/--label /')
done
```

### Listing Issues

**View all issues**:
```bash
# All open issues
gh issue list --state open

# All issues (including closed)
gh issue list --state all

# Limit results
gh issue list --state all --limit 20
```

**Filter by labels**:
```bash
# Issues with specific label
gh issue list --label "phase-1"

# Multiple labels
gh issue list --label "phase-1,infrastructure"
```

**Search issues**:
```bash
# Search by title/body
gh issue list -S "Qdrant" --state all

# Search by author
gh issue list --author "@me"

# Search by assignee
gh issue list --assignee "@me"
```

**JSON output for programmatic access**:
```bash
# Get specific fields as JSON
gh issue list --json number,title,labels

# Pretty print JSON
gh issue list --json number,title,state | jq '.'

# Extract specific values
gh issue list --json number,title | jq '.[].number'
```

### Viewing Issues

```bash
# View specific issue
gh issue view <number>

# View with details
gh issue view <number> --json state,assignees,labels,body

# Open in browser
gh issue view <number> --web
```

### Updating Issues

```bash
# Add comment
gh issue comment <number> --body "Comment text"

# Close issue
gh issue close <number>

# Reopen issue
gh issue reopen <number>

# Add label
gh issue edit <number> --add-label "label-name"

# Remove label
gh issue edit <number> --remove-label "label-name"

# Change assignee
gh issue edit <number> --assignee <username>
```

### Deleting Issues

```bash
# Delete single issue
gh issue delete <number> --yes

# Delete multiple issues
gh issue delete <number1> <number2> <number3> --yes
```

## Pull Request Management

### Creating PRs

```bash
# Create PR from current branch
gh pr create \
  --title "PR Title" \
  --body "PR description" \
  --base main

# Create draft PR
gh pr create \
  --title "WIP: Feature" \
  --draft \
  --base main
```

### Reviewing PRs

```bash
# View specific PR
gh pr view <number>

# List PRs
gh pr list --state open

# Add review
gh pr review <number> \
  --approve \
  --body "Looks good!"

# Request changes
gh pr review <number> \
  --request-changes \
  --body "Need to fix X"
```

### Merging PRs

```bash
# Merge PR
gh pr merge <number>

# Merge with squash
gh pr merge <number> --squash

# Merge with delete branch
gh pr merge <number> --delete-branch
```

## Common Workflows for VedaAide

### Create Issues from Task Breakdown

```bash
# 1. Parse TASK_BREAKDOWN.cn.md to extract tasks
# 2. Use awk/grep to extract task info
# 3. Batch create with gh issue create

# Example:
awk '/^### 任务/{print $0}' TASK_BREAKDOWN.cn.md | \
  while read task; do
    gh issue create \
      --title "$task" \
      --body "Auto-created from task breakdown" \
      --label "auto-created"
  done
```

### Check Issue Status Dashboard

```bash
# Quick status check
echo "=== Phase 1 Issues ==="
gh issue list --label "phase-1" --json number,title,state

echo ""
echo "=== Assigned to Me ==="
gh issue list --assignee "@me" --json number,title,state

echo ""
echo "=== High Priority ==="
gh issue list --label "priority:high" --json number,title,state
```

### Auto-link Issues from PRs

```bash
# When creating PR, reference related issues
gh pr create \
  --title "Implement RAG Pipeline" \
  --body "Closes #7 #8
  
Implements Phase 1.4 and 1.5 tasks." \
  --base main
```

## Tips & Troubleshooting

### Authentication Issues

**Problem**: "Unauthorized: As an Enterprise Managed User"
**Solution**:
```bash
# Switch to correct account
gh auth switch -u <username>

# Verify active account
gh auth status
```

### Working with Multiple Accounts

```bash
# List all authenticated accounts
gh auth status --show-token

# Switch between accounts
gh auth switch -u DerekJi

# Use specific account for single command
GITHUB_USER=DerekJi gh issue create --title "Test"
```

### Batch Operations with Errors

**Handle errors gracefully**:
```bash
#!/bin/bash
set -e  # Exit on error

for issue in "Issue 1" "Issue 2" "Issue 3"; do
  if gh issue create --title "$issue"; then
    echo "✓ Created: $issue"
  else
    echo "✗ Failed: $issue"
    # Uncomment to continue despite errors:
    # continue
  fi
done
```

### Performance Tips

**For large batch operations**:
```bash
# Don't add labels that don't exist (creates warning)
# Pre-create labels:
gh label create "phase-1" --description "Phase 1 tasks"
gh label create "infrastructure" --description "Infrastructure tasks"

# Then batch create issues
# Labels now add instantly without warnings
```

## Integration with VedaAide Workflow

### Create Issues from TASK_BREAKDOWN

```bash
# scripts/github/create_phase1_issues.sh
#!/bin/bash

cd "$(dirname "$0")"

# Create Phase 1 issues
gh issue create --title "Phase 1.1: Deploy Qdrant" --body "..." --label "phase-1"
gh issue create --title "Phase 1.2: Configure LangFuse" --body "..." --label "phase-1"
# ... etc
```

### Link to CI/CD Pipeline

```bash
# In GitHub Actions workflow
- name: Create Phase Issues
  if: github.event_name == 'workflow_dispatch'
  run: bash scripts/github/create_phase_issues.sh
```

### Dashboard View

```bash
# Create dashboard script
#!/bin/bash

echo "=== VedaAide Project Status ==="
echo ""
echo "Phase 1: $(gh issue list --label phase-1 | wc -l) tasks"
echo "Phase 2: $(gh issue list --label phase-2 | wc -l) tasks"
echo "Phase 3: $(gh issue list --label phase-3 | wc -l) tasks"
echo ""
echo "Recent Issues:"
gh issue list --state all --limit 5 --json number,title
```

## Resources

- [GitHub CLI Documentation](https://cli.github.com/manual)
- [GitHub CLI GitHub Issues](https://github.com/cli/cli/issues)
- [VedaAide Task Breakdown](docs/planning/TASK_BREAKDOWN.cn.md)
