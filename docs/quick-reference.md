# Quick Reference Guide

**For**: AI-Assisted Agile Development with Claude Code & Claude Cloud

---

## 🚀 Getting Started

### First Time Setup
1. Clone repository
2. Read [start-here.md](../start-here.md)
3. Read [AI-Assisted Agile Process](ai-assisted-agile-process.md)
4. Review current sprint planning

### Starting Each Session (Claude Code)
```bash
# 1. Read context
cat start-here.md

# 2. Check branch status
git status
git log -3

# 3. Rebase if in morning window (8-10 AM)
git fetch origin master
git rebase origin/master
<run-tests>
```

---

## 🎯 Tools Usage

### Claude Cloud (Projects)
**Use for**:
- Sprint planning & task breakdown
- Architecture design
- Complex problem solving
- API contract design
- Cross-feature coordination
- Retrospective analysis

### Claude Code CLI
**Use for**:
- Code implementation
- Writing tests
- Git operations
- Bug fixing
- Pre-merge checklist
- Code reviews

---

## 📋 Daily Workflow

### Morning (8-10 AM): Rebase Window
```bash
git fetch origin master
git rebase origin/master
git push origin <branch> --force-with-lease
<run-tests>
```
**⚠️ No merges to master during this window**

### Development (10 AM - 4 PM)
- Work in assigned module
- Update [start-here.md](../start-here.md) regularly
- Run tests frequently
- Push changes to feature branch

### Afternoon (4-5 PM): Review Window
- Run pre-merge checklist
- Create/update PR
- Request reviews

### Evening (5-6 PM): Merge Window
- Merge in priority order (P1 → P2 → P3 → P4)
- Run full test suite after each merge
- Notify team of merges

---

## 🌿 Branch Strategy

### Naming
```
feature/<ticket-id>-<description>
bugfix/<ticket-id>-<description>
hotfix/<ticket-id>-<description>
```

### Lifecycle
1. Create from latest master
2. Develop single feature
3. Rebase daily
4. Merge after approval
5. Delete after merge

---

## 🎨 Module Isolation Patterns

### Rule 1: Isolated Modules
```
Feature A → src/module_a/ only
Feature B → src/module_b/ only
Result: Zero conflicts
```

### Rule 2: Shared Files - Different Sections
```python
# src/shared/config.py

# === Feature A (TICKET-123) ===
FEATURE_A_SETTING = "value"

# === Feature B (TICKET-456) ===
FEATURE_B_SETTING = "value"
```

### Rule 3: Entry Points - Registration
```python
# src/main.py

def create_app():
    app = Application()
    app.register(feature_a)  # TICKET-123
    app.register(feature_b)  # TICKET-456
    return app
```

### Rule 4: Validators - Pipeline
```python
# src/shared/validators.py

def validate(data):
    # Feature A: Pre-validation
    if not pre_check(data): return Error()

    # Existing (unchanged)
    if not existing(data): return Error()

    # Feature B: Post-validation
    if not post_check(data): return Error()
```

---

## ✅ Pre-Merge Checklist

### Quick Version
```bash
# 1. Rebase
git fetch origin master && git rebase origin/master

# 2. Quality
<linter> && <formatter> && <type-checker>

# 3. Tests
<test-command> && <coverage-command>

# 4. Verify
- Changes in assigned module
- Shared files use patterns
- start-here.md updated

# 5. Create PR
Use templates/pr-template.md
```

---

## 🏆 Merge Priorities

| Priority | Type | Merge Order |
|----------|------|-------------|
| **P1** | Isolated module, no dependencies | First |
| **P2** | Shared files, different sections | Second |
| **P3** | Depends on P1/P2 | Third |
| **P4** | Depends on P3 | Fourth |

---

## 📊 Quality Targets

| Metric | Target |
|--------|--------|
| Test Coverage | ≥80% |
| Linter Errors | 0 |
| Security Vulnerabilities | 0 |
| Conflict Rate | <10% |
| Resolution Time | <30 min |
| Test Pass Rate | 100% |

---

## 🗂️ Templates Available

| Template | Purpose | Location |
|----------|---------|----------|
| **PRD** | Product requirements | [templates/prd-template.md](../templates/prd-template.md) |
| **Tech Spec** | Architecture & design | [templates/technical-spec-template.md](../templates/technical-spec-template.md) |
| **Sprint Planning** | Sprint setup | [templates/sprint-planning-template.md](../templates/sprint-planning-template.md) |
| **PR** | Pull requests | [templates/pr-template.md](../templates/pr-template.md) |
| **Decision Log** | Architecture decisions | [templates/decision-log-template.md](../templates/decision-log-template.md) |
| **Retrospective** | Sprint review | [templates/retrospective-template.md](../templates/retrospective-template.md) |

---

## 🔍 Common Commands

### Git Operations
```bash
# Daily rebase
git fetch origin master
git rebase origin/master
git push origin <branch> --force-with-lease

# Create feature branch
git checkout -b feature/TICKET-123-description

# Check what changed
git diff master..HEAD
git log master..HEAD --oneline

# Resolve conflicts
git status
git diff
# Edit files
git add <resolved-files>
git rebase --continue
```

### Testing
```bash
# Run all tests
<test-command>

# Run with coverage
<coverage-command>

# Run specific test
<test-command> path/to/test_file.py::test_name
```

### Code Quality
```bash
# Lint
<linter-command>

# Format
<formatter-command>

# Type check
<type-checker-command>

# All at once
<linter> && <formatter> && <type-checker>
```

---

## 🚨 High-Risk Files

Always check [start-here.md](../start-here.md) and sprint planning for current list.

**Common high-risk files**:
- Entry points (main.py, index.js, etc.)
- Configuration files (config.py, settings.py, etc.)
- Shared utilities (validators.py, helpers.py, etc.)
- Test fixtures (conftest.py, etc.)

**When modifying**: Use designated patterns!

---

## 📝 Session Management

### Start Session
```bash
# 1. Read context
cat start-here.md

# 2. Verify status
git status
git log -3

# 3. Rebase if needed
git fetch origin master
git rebase origin/master
```

### End Session
```bash
# 1. Update start-here.md with:
- Completed tasks
- Files modified
- Next actions
- Blockers
- Timestamp

# 2. Commit if ready
git add <files>
git commit -m "Description"
git push origin <branch>
```

---

## 🆘 Troubleshooting

### Merge Conflict
```bash
git status                    # See conflicts
git diff                      # Review differences

# Edit conflicted files
# Different sections → Keep both
# Same section → Coordinate with team

git add <resolved-files>
git rebase --continue
<run-tests>
```

### Tests Failing After Rebase
```bash
# 1. Check what changed in master
git log master --oneline -10

# 2. Review diff
git diff master

# 3. Fix breaking changes
# 4. Re-run tests
<test-command>
```

### Can't Push (Force-with-lease fails)
```bash
# Someone pushed to your branch
git fetch origin <branch>
git rebase origin/<branch>
git push origin <branch>
```

---

## 📚 Documentation Links

- [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Complete workflow
- [Parallel Development Best Practices](parallel-sprint-development-best-practices.md) - Detailed practices
- [start-here.md](../start-here.md) - Current sprint context
- [CLAUDE.md](../CLAUDE.md) - Claude Code instructions
- [README.md](../README.md) - Project overview

---

## 💡 Pro Tips

1. **Always read [start-here.md](../start-here.md) first** - Context is everything
2. **Rebase daily** - Small conflicts are easier than big ones
3. **Stay in your module** - Prevents most conflicts
4. **Update [start-here.md](../start-here.md) often** - Future you will thank you
5. **Use patterns for shared files** - They work!
6. **Run tests frequently** - Catch issues early
7. **Push often** - Don't lose work
8. **Document decisions** - Add to decision log
9. **Ask for help** - When blocked, communicate
10. **Follow the process** - It's designed to help you succeed

---

**Last Updated**: [Auto-generated from process docs]
