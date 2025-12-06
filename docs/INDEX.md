# Documentation Index

**AI-Assisted Agile Development with Claude Cloud + Claude Code**

---

## 🚀 Quick Start (Read These First)

### For Everyone
1. **[PROCESS-OVERVIEW.md](PROCESS-OVERVIEW.md)** ⭐ START HERE
   - Visual overview of entire process
   - Tool responsibilities
   - Daily workflow diagrams
   - Key patterns and metrics

2. **[Quick Reference Guide](quick-reference.md)**
   - Cheat sheet for daily tasks
   - Common commands
   - Patterns quick lookup
   - Troubleshooting tips

### For Developers (Claude Code Users)
3. **[start-here.md](../start-here.md)** 📍 READ EVERY SESSION
   - Current sprint context
   - Your assigned work
   - Progress tracking
   - Next actions

4. **[CLAUDE.md](../CLAUDE.md)**
   - Claude Code CLI instructions
   - Session management
   - Module isolation rules
   - Code patterns

---

## 📚 Core Process Documentation

### Complete Process Guide
**[ai-assisted-agile-process.md](ai-assisted-agile-process.md)**
- Complete end-to-end process (comprehensive)
- All 8 phases in detail
- Tool usage guidelines
- Template references
- Success metrics

### Parallel Development
**[parallel-sprint-development-best-practices.md](parallel-sprint-development-best-practices.md)**
- Module isolation strategy
- Branch structure
- Daily workflow details
- Conflict resolution
- Merge priority system

---

## 📋 Templates (Use These!)

All templates are in the [templates](../templates/) directory.

### Planning Phase
1. **[prd-template.md](../templates/prd-template.md)**
   - Product Requirement Document
   - User stories
   - Acceptance criteria
   - Owner: Product Manager

2. **[technical-spec-template.md](../templates/technical-spec-template.md)**
   - Architecture design
   - API specifications
   - Database schema
   - Owner: Tech Lead

3. **[sprint-planning-template.md](../templates/sprint-planning-template.md)**
   - Sprint goals
   - Task breakdown
   - Module assignments
   - Merge priorities
   - Owner: Team

### Development Phase
4. **[start-here.md](../start-here.md)**
   - Session context (NOT in templates/ - lives in root)
   - Progress tracking
   - Current status
   - Owner: Developer (update every session)

5. **[pr-template.md](../templates/pr-template.md)**
   - Pull request format
   - Pre-merge checklist
   - Testing documentation
   - Owner: Developer

### Review Phase
6. **[decision-log-template.md](../templates/decision-log-template.md)**
   - Architecture decisions (ADR)
   - Pattern library
   - Technical debt tracking
   - Owner: Tech Lead

7. **[retrospective-template.md](../templates/retrospective-template.md)**
   - Sprint review
   - Metrics analysis
   - Action items
   - Owner: Team

---

## 🎯 Documentation by Role

### Product Manager
**Primary Docs**:
- [PRD Template](../templates/prd-template.md)
- [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 1
- [Sprint Planning Template](../templates/sprint-planning-template.md) - Section 2.1

**Tools**: Claude Cloud for requirements refinement

---

### Tech Lead / Architect
**Primary Docs**:
- [Technical Spec Template](../templates/technical-spec-template.md)
- [Decision Log Template](../templates/decision-log-template.md)
- [AI-Assisted Agile Process](ai-assisted-agile-process.md) - All phases
- [Sprint Planning Template](../templates/sprint-planning-template.md) - Module assignment

**Tools**: Claude Cloud for architecture, Claude Code for verification

---

### Developer
**Primary Docs**:
- [start-here.md](../start-here.md) - **READ EVERY SESSION**
- [CLAUDE.md](../CLAUDE.md) - Claude Code instructions
- [Quick Reference](quick-reference.md) - Daily cheat sheet
- [Parallel Development Best Practices](parallel-sprint-development-best-practices.md)
- [PR Template](../templates/pr-template.md)

**Tools**: Claude Code CLI for implementation

---

### QA / Tester
**Primary Docs**:
- [Technical Spec Template](../templates/technical-spec-template.md) - Testing strategy
- [Sprint Planning Template](../templates/sprint-planning-template.md) - Acceptance criteria
- [PR Template](../templates/pr-template.md) - Testing checklist

**Tools**: Claude Cloud for test planning, Claude Code for test automation

---

### Scrum Master / Project Manager
**Primary Docs**:
- [Sprint Planning Template](../templates/sprint-planning-template.md)
- [Retrospective Template](../templates/retrospective-template.md)
- [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Overview
- [PROCESS-OVERVIEW](PROCESS-OVERVIEW.md) - Visual guide

**Tools**: Claude Cloud for planning and analysis

---

## 🔄 Documentation by Phase

### Phase 1: Requirements & Design
**Docs to Use**:
1. [PRD Template](../templates/prd-template.md)
2. [Technical Spec Template](../templates/technical-spec-template.md)
3. [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 1

**Tool**: Claude Cloud

---

### Phase 2: Sprint Planning
**Docs to Use**:
1. [Sprint Planning Template](../templates/sprint-planning-template.md)
2. [Parallel Development Best Practices](parallel-sprint-development-best-practices.md) - Module assignment
3. [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 2

**Tool**: Claude Cloud

---

### Phase 3-4: Development
**Docs to Use**:
1. [start-here.md](../start-here.md) - Update constantly
2. [CLAUDE.md](../CLAUDE.md) - Follow instructions
3. [Quick Reference](quick-reference.md) - Daily reference
4. [Parallel Development Best Practices](parallel-sprint-development-best-practices.md)

**Tool**: Claude Code CLI

---

### Phase 5: Code Review & Testing
**Docs to Use**:
1. [PR Template](../templates/pr-template.md)
2. [CLAUDE.md](../CLAUDE.md) - Pre-merge checklist
3. [Quick Reference](quick-reference.md) - Quality gates

**Tool**: Claude Code for review, human for approval

---

### Phase 6-7: Integration & Merge
**Docs to Use**:
1. [Parallel Development Best Practices](parallel-sprint-development-best-practices.md) - Merge priorities
2. [Sprint Planning](../templates/sprint-planning-template.md) - Priority reference
3. [Quick Reference](quick-reference.md) - Merge commands

**Tool**: Git + CI/CD

---

### Phase 8: Retrospective
**Docs to Use**:
1. [Retrospective Template](../templates/retrospective-template.md)
2. [Decision Log Template](../templates/decision-log-template.md)
3. [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 8

**Tool**: Claude Cloud for analysis

---

## 🗺️ Reading Paths

### Path 1: "I'm New - Where Do I Start?"
1. [PROCESS-OVERVIEW.md](PROCESS-OVERVIEW.md) - 15 min
2. [Quick Reference](quick-reference.md) - 10 min
3. [start-here.md](../start-here.md) - 5 min
4. [CLAUDE.md](../CLAUDE.md) - 20 min
**Total**: ~50 minutes

---

### Path 2: "I'm a Developer Starting a Sprint"
1. [start-here.md](../start-here.md) - Read your assignment
2. [Sprint Planning doc](../templates/sprint-planning-template.md) - Check your ticket details
3. [Quick Reference](quick-reference.md) - Bookmark for daily use
4. [CLAUDE.md](../CLAUDE.md) - Review module isolation rules
**Total**: ~15 minutes per sprint

---

### Path 3: "I'm Leading Sprint Planning"
1. [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 2
2. [Sprint Planning Template](../templates/sprint-planning-template.md) - Fill out
3. [Parallel Development Best Practices](parallel-sprint-development-best-practices.md) - Module assignment
4. [Technical Spec](../templates/technical-spec-template.md) - Reference
**Total**: ~2 hours (planning session)

---

### Path 4: "I Need to Understand the Architecture"
1. [Technical Spec Template](../templates/technical-spec-template.md) - Example structure
2. [Decision Log Template](../templates/decision-log-template.md) - Past decisions
3. [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 1
**Total**: ~1 hour

---

### Path 5: "I'm Having Merge Conflicts"
1. [Quick Reference](quick-reference.md) - Troubleshooting section
2. [Parallel Development Best Practices](parallel-sprint-development-best-practices.md) - Conflict resolution
3. [CLAUDE.md](../CLAUDE.md) - Shared file patterns
**Total**: ~10 minutes

---

## 📊 Documentation Maintenance

### Update Frequency

| Document | Update When | Owner |
|----------|-------------|-------|
| [start-here.md](../start-here.md) | Every session | Developer |
| PRD | Per feature | Product Manager |
| Technical Spec | Per major feature | Tech Lead |
| Sprint Planning | Per sprint | Team |
| Decision Log | As decisions are made | Tech Lead |
| Retrospective | End of sprint | Team |
| Process docs | Quarterly or as needed | Tech Lead |

### Documentation Cleanup

**[Documentation Cleanup Prompt](maintenance/documentation-cleanup-prompt.md)** 🧹
- Reusable prompt for Claude for Web
- Run every 2-4 weeks
- Enforces naming conventions
- Organizes files into proper directories
- Fixes broken links
- Updates document status
- Use for: Repository cleanup, pre-release audits, onboarding prep

### Version Control
- All docs are in git
- Update dates in footers
- Major changes → git commit message
- Process version: **3.0**

---

## 🔍 Search Guide

### "How do I...?"

**...start a new feature?**
→ [CLAUDE.md](../CLAUDE.md) - "When Starting a New Feature"

**...handle shared files?**
→ [CLAUDE.md](../CLAUDE.md) - "When Modifying Shared Files"
→ [Quick Reference](quick-reference.md) - "Module Isolation Patterns"

**...create a PR?**
→ [PR Template](../templates/pr-template.md)
→ [CLAUDE.md](../CLAUDE.md) - "Pre-Merge Checklist"

**...resolve conflicts?**
→ [Parallel Development Best Practices](parallel-sprint-development-best-practices.md) - "Conflict Resolution"
→ [Quick Reference](quick-reference.md) - "Troubleshooting"

**...plan a sprint?**
→ [Sprint Planning Template](../templates/sprint-planning-template.md)
→ [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 2

**...document an architecture decision?**
→ [Decision Log Template](../templates/decision-log-template.md)

**...use Claude Cloud vs Claude Code?**
→ [PROCESS-OVERVIEW](PROCESS-OVERVIEW.md) - "Tool Responsibilities"
→ [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Phase 4

---

## 🎓 Learning Resources

### Beginner Level
1. [PROCESS-OVERVIEW.md](PROCESS-OVERVIEW.md) - Visual guide
2. [Quick Reference](quick-reference.md) - Commands and patterns
3. [start-here.md](../start-here.md) - Context template

### Intermediate Level
4. [CLAUDE.md](../CLAUDE.md) - Development standards
5. [Parallel Development Best Practices](parallel-sprint-development-best-practices.md)
6. [PR Template](../templates/pr-template.md)

### Advanced Level
7. [AI-Assisted Agile Process](ai-assisted-agile-process.md) - Complete process
8. [Technical Spec Template](../templates/technical-spec-template.md)
9. [Decision Log Template](../templates/decision-log-template.md)

---

## 📞 Support & Contact

### Questions About...

**Process**:
- Review [AI-Assisted Agile Process](ai-assisted-agile-process.md)
- Check [PROCESS-OVERVIEW](PROCESS-OVERVIEW.md)
- Contact: Tech Lead

**Tools (Claude Code/Cloud)**:
- Review [CLAUDE.md](../CLAUDE.md)
- Check [Quick Reference](quick-reference.md)
- Contact: Team Lead

**Merge Conflicts**:
- Review [Parallel Development Best Practices](parallel-sprint-development-best-practices.md)
- Check [Quick Reference](quick-reference.md) - Troubleshooting
- Contact: Senior Developer

**Sprint Planning**:
- Review [Sprint Planning Template](../templates/sprint-planning-template.md)
- Contact: Scrum Master

---

## 🔗 External Resources

### Methodologies
- [Agile Manifesto](https://agilemanifesto.org/)
- [Scrum Guide](https://scrumguides.org/)
- [Architecture Decision Records](https://adr.github.io/)

### Git Workflows
- [Git Rebase](https://git-scm.com/docs/git-rebase)
- [Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows)

### Testing
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

---

## 📈 Success Metrics

Track these metrics using templates:
- Sprint Planning → [Sprint Planning Template](../templates/sprint-planning-template.md)
- Sprint Review → [Retrospective Template](../templates/retrospective-template.md)
- Quality → [PR Template](../templates/pr-template.md) checklists

**Key Metrics**:
- Velocity (story points/sprint)
- Conflict rate (<10% target)
- Test coverage (≥80% target)
- Cycle time (PR creation to merge)

---

## ✅ Documentation Checklist

### For New Projects
- [ ] Copy all templates to your project
- [ ] Customize [start-here.md](../start-here.md) with your sprint info
- [ ] Update [CLAUDE.md](../CLAUDE.md) with your project specifics
- [ ] Create initial [PRD](../templates/prd-template.md)
- [ ] Create [Technical Spec](../templates/technical-spec-template.md)
- [ ] Set up [Decision Log](../templates/decision-log-template.md)

### For Each Sprint
- [ ] Fill out [Sprint Planning](../templates/sprint-planning-template.md)
- [ ] Update [start-here.md](../start-here.md) for each developer
- [ ] Use [PR Template](../templates/pr-template.md) for all PRs
- [ ] Complete [Retrospective](../templates/retrospective-template.md) at end

---

## 🎯 Key Principles (Reminder)

1. **Context is King** - Always read [start-here.md](../start-here.md) first
2. **Module Isolation** - Prevents conflicts
3. **Daily Integration** - Rebase every morning
4. **Use Patterns** - For shared files
5. **Right Tool, Right Job** - Cloud for design, CLI for code
6. **Document Decisions** - Use decision log
7. **Test Everything** - ≥80% coverage
8. **Communicate Often** - Update [start-here.md](../start-here.md)

---

**📅 Last Updated**: 2025-12-06
**📊 Process Version**: 3.0
**👥 Maintained By**: Tech Lead / Team

**🚀 Ready to start? Read [PROCESS-OVERVIEW.md](PROCESS-OVERVIEW.md)!**
