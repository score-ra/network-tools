# Project Setup Checklist

Use this checklist to track progress during project setup.

## Phase 1: Information Gathering
- [ ] Project name determined
- [ ] Project description written
- [ ] Project objective defined
- [ ] Project type selected
- [ ] Tech stack decided
- [ ] Testing framework chosen
- [ ] Repository approach decided
- [ ] Optional features identified (Docker, CI/CD, etc.)

## Phase 2: Repository Setup
- [ ] GitHub template used (if applicable)
- [ ] Repository created
- [ ] Repository cloned locally
- [ ] Template structure verified

## Phase 3: Tech Stack Initialization
- [ ] Package manager initialized (pip/npm/go mod)
- [ ] Dependencies file created (requirements.txt/package.json/go.mod)
- [ ] Test framework configured
- [ ] Linter configured
- [ ] Formatter configured
- [ ] Type checker configured (if applicable)
- [ ] .env.example created (if needed)
- [ ] .gitignore updated for tech stack
- [ ] Dependencies installed
- [ ] Basic src/ structure created

## Phase 4: Template Customization
- [ ] README.md placeholders replaced
- [ ] Project name updated throughout
- [ ] CLAUDE.md commands updated
- [ ] TEMPLATE-SETUP.md reviewed

## Phase 5: Documentation Generation
- [ ] PRD created from template
- [ ] PRD customized with project details
- [ ] Technical Spec created from template
- [ ] Technical Spec customized
- [ ] docs/INDEX.md updated
- [ ] start-here.md created
- [ ] start-here.md customized

## Phase 6: Optional Features
- [ ] Docker setup (if requested)
  - [ ] Dockerfile created
  - [ ] docker-compose.yml created
  - [ ] .dockerignore created
- [ ] CI/CD setup (if requested)
  - [ ] .github/workflows/ci.yml created (GitHub Actions)
  - [ ] OR .gitlab-ci.yml created (GitLab CI)
  - [ ] Pipeline tested

## Phase 7: Sprint Planning
- [ ] Sprint planning decision made (now or later)
- [ ] If now: Sprint 1 objective defined
- [ ] If now: Initial features identified
- [ ] If now: Sprint 1 plan created
- [ ] If now: Tickets created with priorities
- [ ] start-here.md updated with sprint info

## Phase 8: Verification
- [ ] Directory structure validated
- [ ] All config files present
- [ ] Dependencies install successfully
- [ ] Tests run (even if 0 tests)
- [ ] Linter runs without errors
- [ ] Build succeeds (if applicable)
- [ ] No placeholders remaining
- [ ] Git repository initialized
- [ ] Git user configured

## Phase 9: Git Commit
- [ ] All changes staged
- [ ] Initial commit created
- [ ] Commit message descriptive
- [ ] Pushed to remote (if applicable)

## Phase 10: Summary
- [ ] Setup summary provided to user
- [ ] Next steps clearly outlined
- [ ] Documentation links shared
- [ ] TEMPLATE-SETUP.md marked complete
- [ ] Project ready for development! 🎉

---

## Quick Validation Commands

**Check structure:**
```bash
ls -la src/ tests/ docs/ templates/
```

**Check tech stack:**
```bash
# Python
python3 --version && pip --version
cat requirements.txt

# Node.js
node --version && npm --version
cat package.json

# Go
go version
cat go.mod
```

**Run tests:**
```bash
# Python
pytest

# Node.js
npm test

# Go
go test ./...
```

**Run validation script:**
```bash
./.claude/skills/project-setup/scripts/validate-setup.sh
```
