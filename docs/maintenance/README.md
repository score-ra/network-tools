# Maintenance Documentation

Quick guides for maintaining Symphony Core repositories.

---

## 📋 Available Guides

### [Documentation Cleanup Prompt](documentation-cleanup-prompt.md)

**Purpose**: Audit and clean up documentation to enforce best practices

**When to use**:
- Every 2-4 weeks during active development
- Before major releases
- After merging sprints
- When onboarding new team members
- When repository has drifted from standards

**What it does**:
- ✅ Organizes misplaced files (prds/, specs/, sprints/)
- ✅ Enforces lowercase-with-hyphens naming
- ✅ Archives old sprint documents
- ✅ Fixes broken internal links
- ✅ Updates document status fields
- ✅ Validates project structure
- ✅ Checks for missing required files

**How to use**:
1. Open [documentation-cleanup-prompt.md](documentation-cleanup-prompt.md)
2. Copy the entire prompt (from "PROMPT STARTS HERE" to "PROMPT ENDS HERE")
3. Open Claude for Web (claude.ai)
4. Paste the prompt
5. Review Claude's proposed changes
6. Apply using the provided git commands

**Time**: ~10-15 minutes per repository

---

## 🔄 Recommended Maintenance Schedule

### Weekly (Active Development)
- [ ] Run documentation cleanup prompt

### Bi-Weekly (Moderate Development)
- [ ] Run documentation cleanup prompt
- [ ] Review and archive completed sprint docs

### Monthly (Low Activity / Maintenance)
- [ ] Run documentation cleanup prompt
- [ ] Update process documentation if needed
- [ ] Review template usage and update if needed

### Before Major Releases
- [ ] Run documentation cleanup prompt
- [ ] Verify all PRDs and specs are current
- [ ] Update README.md with latest version info
- [ ] Archive all completed sprint docs

---

## 📝 Adding New Maintenance Guides

If you create additional maintenance prompts or guides:

1. Add markdown file to this directory
2. Update this README.md with link and description
3. Update [docs/INDEX.md](../INDEX.md) if widely applicable
4. Commit with message: `docs: Add [name] maintenance guide`

---

**Last Updated**: 2025-11-22
**Maintained By**: Symphony Core Team
