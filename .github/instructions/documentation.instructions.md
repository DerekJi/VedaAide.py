---
applyTo: "**"
---

# Bilingual Documentation Standards (Mandatory)

## Core Rule

**All documentation updates must synchronously handle both Chinese and English versions.** Merging single-language updates is not allowed.

## File Naming Convention

| Documentation Type | Chinese Version | English Version |
|-------------|---------|----------|
| Planning/Guide/Architecture Docs | `*.cn.md` | `*.en.md` |
| Project README (only exception) | `README.cn.md` | `README.md` |

```
# ✅ Correct
docs/planning/main.cn.md
docs/planning/main.en.md
README.md              ← English (no .en suffix)
README.cn.md

# ❌ Incorrect
docs/SETUP.md          ← Missing another language version
docs/SETUP_EN.md       ← Wrong suffix format
```

## Workflow for New Documentation

1. Create both `*.cn.md` and `*.en.md` files simultaneously
2. Update `docs/INDEX.md` and `docs/INDEX.en.md`
3. PR title format: `docs: add <NAME> documentation (CN/EN)`

## Workflow for Documentation Updates

1. Edit both Chinese and English versions, ensuring consistent structure and content
2. Code examples must be identical in both versions
3. Commit format: `docs(cn/en): update <NAME> with <change>`

## AI Assistant Guidelines

- When requested to create/update documentation, **must simultaneously generate/modify both Chinese and English versions**
- Must not stop after creating only a single language version
- If user specifies only one version, automatically create the other version and notify the user

## Pre-commit Checklist

- [ ] Both Chinese and English versions created/updated
- [ ] File names conform to `.cn.md` / `.en.md` standard (except README)
- [ ] Both versions have consistent structure and identical code examples
- [ ] Related index files updated
