# Documentation Cleanup & Best Practices Enforcement

**Purpose**: Reusable prompt for cleaning up and organizing documentation in Symphony Core repositories
**Frequency**: Run every 2-4 weeks or before major releases
**Tool**: Copy this entire document and paste into Claude for Web (claude.ai)

---

## 📋 Instructions for Use

1. **Open the target repository** in your IDE/file browser
2. **Copy this entire prompt** (from "PROMPT STARTS HERE" to "PROMPT ENDS HERE")
3. **Paste into Claude for Web** (claude.ai)
4. **Review Claude's proposed changes** before applying
5. **Commit changes** with message: `docs: Clean up documentation and enforce best practices`

---

## 🎯 PROMPT STARTS HERE

---

I need you to audit and clean up the documentation in this repository according to Symphony Core best practices. This repository uses the **AI-Assisted Agile Development** process documented in the software-dev-project-template.

## Your Task

Perform a comprehensive documentation cleanup covering:

1. **File Organization**
2. **Naming Conventions**
3. **Content Updates**
4. **Structure Enforcement**
5. **Link Validation**

---

## 📁 1. File Organization

### Step 1.1: Identify Misplaced Files

Search the **root directory** for documentation files that should be in `/docs`:

- Sprint planning documents (`sprint-*.md`, `*-sprint.md`, `backlog-*.md`)
- PRD/Requirements documents (`prd-*.md`, `*-requirements.md`, `requirements-*.md`)
- Technical specifications (`*-spec.md`, `tech-spec-*.md`, `architecture-*.md`)
- Retrospectives (`retro-*.md`, `retrospective-*.md`, `*-retro.md`)
- Decision logs (`decision-*.md`, `*-decisions.md`, `adr-*.md`)
- Meeting notes (`notes-*.md`, `*-notes.md`, `meeting-*.md`)

**Action**: List all misplaced files and recommend new locations.

### Step 1.2: Organize by Type

Files should be organized into these directories:

```
docs/
├── prds/                          # Product Requirements Documents
│   ├── 2025-01-authentication-prd.md
│   ├── 2025-02-publishing-prd.md
│   └── 2025-03-analytics-prd.md
├── specs/                         # Technical Specifications
│   ├── 2025-01-authentication-spec.md
│   ├── 2025-02-publishing-spec.md
│   └── 2025-03-analytics-spec.md
├── sprints/                       # Sprint Planning
│   ├── current/
│   │   └── sprint-05-analytics.md
│   └── archive/
│       ├── .gitkeep
│       ├── sprint-01-foundation.md
│       ├── sprint-02-validation.md
│       ├── sprint-03-conversion.md
│       └── sprint-04-publishing.md
├── decisions/                     # Architecture Decision Records
│   ├── .gitkeep
│   ├── adr-001-database-choice.md
│   ├── adr-002-api-framework.md
│   └── decision-log.md            # Consolidated log (optional)
├── retrospectives/                # Sprint Retrospectives
│   ├── .gitkeep
│   ├── retro-2025-01-sprint-01.md
│   ├── retro-2025-02-sprint-02.md
│   └── retro-2025-03-sprint-03.md
├── investigation/                 # Discovery & research documents
│   ├── .gitkeep
│   ├── discovery-status.md
│   └── research-findings.md
├── project-management/            # Execution plans & status reports
│   ├── .gitkeep
│   ├── execution-plan.md
│   └── phase-completion-status.md
├── maintenance/                   # Maintenance guides
│   ├── README.md
│   └── documentation-cleanup-prompt.md
└── [existing process docs]        # Keep INDEX.md, PROCESS-OVERVIEW.md, etc.
```

**Action**: Create missing directories and propose file moves.

### Step 1.3: Archive Old Sprint Documents

For completed sprints (status: complete, merged, or older than 30 days):

- Move from `docs/sprints/current/` → `docs/sprints/archive/`
- Move from root → `docs/sprints/archive/`
- Ensure chronological naming: `sprint-01-*`, `sprint-02-*`, etc.

**Action**: List files to archive with proposed names.

### Step 1.4: Organize Asset and Data Files

Check **root directory** for misplaced files that should be organized:

**Images** (PNG, JPG, SVG, GIF, WebP):
- Move to `assets/images/` or create if needed
- Keep images out of git if very large (>1MB each)
- Example patterns: `*.png`, `category-*.png`, `screenshot-*.jpg`

**Data Files** (JSON, CSV, TXT, XML):
- Configuration data → `config/` or `data/` folder
- Documentation text → Convert to `.md` and move to `docs/`
- Temporary/test data → `tests/fixtures/` or delete if obsolete
- Example: `target-urls.json` → `config/target-urls.json`

**Binary Files** (PDF, ZIP, TAR, GZ):
- Documentation assets → `assets/downloads/` if needed
- Otherwise remove from git (binary files bloat repository)
- Use external hosting for large files

**Text Files** (TXT):
- Status summaries → Convert to markdown and move to `docs/project-management/`
- Example: `Final Status Summary.txt` → `docs/project-management/final-status-summary.md`

**Exceptions** (DO NOT MOVE):
- `README.md`, `CLAUDE.md`, `LICENSE.md`
- `.gitignore`, `.env.example`
- `package.json`, `requirements.txt`, `go.mod`

**Action**: List all non-documentation files in root and propose organization.

---

## 📝 2. Naming Conventions

### Step 2.1: Enforce Lowercase-With-Hyphens

All documentation files **MUST** use lowercase-with-hyphens:

- ✅ **Good**: `2025-01-authentication-prd.md`, `sprint-03-validation.md`
- ❌ **Bad**: `Feature_Authentication_PRD.md`, `Sprint03Validation.md`, `auth-prd-v2.md`

**Rules**:
- All lowercase letters
- Hyphens for word separation (no underscores, no spaces)
- No version numbers in filenames (use git history)
- Maximum 50 characters (excluding extension)
- Descriptive, not generic (`api-gateway-spec.md` not `spec.md`)

**Action**: List files that violate naming conventions and propose renames.

### Step 2.2: Standardize Prefixes and Date Stamps

Use consistent naming patterns for document types:

| Type | Pattern | Example |
|------|---------|---------|
| Product Requirements | `YYYY-MM-feature-name-prd.md` | `2025-01-authentication-prd.md` |
| Technical Spec | `YYYY-MM-feature-name-spec.md` | `2025-01-authentication-spec.md` |
| Sprint Plan | `sprint-NN-name.md` | `sprint-05-publishing.md` |
| Retrospective | `retro-YYYY-MM-sprint-NN.md` | `retro-2025-01-sprint-05.md` |
| Decision Record | `adr-NNN-topic.md` | `adr-001-database-choice.md` |

**Date Stamp Rules**:
- Use `YYYY-MM` format (year-month from creation date)
- Apply to: PRDs, specs, retrospectives
- Do NOT use for: process docs, templates, README files, sprint plans (use sprint-NN instead)

**Action**: List files needing naming updates with date stamps.

### Step 2.3: Validate File Types in Documentation Folders

**Check for non-documentation files in `/docs`**:

**Allowed in docs/**:
- ✅ `.md` (markdown documentation)
- ✅ `.html` (HTML documentation, if needed)
- ✅ `.csv` (data tables for documentation)
- ✅ `.txt` (plain text docs, convert to .md preferred)

**NOT allowed in docs/** (move to appropriate location):
- ❌ `.png`, `.jpg`, `.svg` (move to `assets/images/`)
- ❌ `.json`, `.yaml`, `.xml` (move to `config/` or `data/`)
- ❌ `.js`, `.py`, `.ts` (move to `src/` or `scripts/`)
- ❌ `.pdf`, `.zip` (move to `assets/downloads/` or remove)

**Action**: List files in docs/ with incorrect file types and recommend moves.

---

## 🔍 3. Content Updates

### Step 3.1: Update Document Status

Check YAML frontmatter (if present) or document headers for status fields:

- **Active sprints**: Status should be `in-progress` or `active`
- **Completed sprints**: Status should be `complete` or `archived`
- **Deprecated docs**: Status should be `deprecated` with note about replacement

**Action**: List documents with incorrect or missing status.

### Step 3.2: Fix Broken Links

Scan all markdown files for broken internal links:

- Files that were moved/renamed
- References to deleted files
- Links to old sprint documents (update to archive path)
- Links to `start-here.md` (only valid if file exists)

**Action**: List broken links and propose fixes.

### Step 3.3: Update Cross-References

Common issues:

- PRDs referencing "current sprint" (should specify sprint number)
- Technical specs referencing old/moved PRDs
- Decision logs referencing deleted/moved documents

**Action**: List documents with outdated cross-references.

---

## 🏗️ 4. Structure Enforcement

### Step 4.1: Verify Required Documentation

According to Symphony Core standards, every project should have:

**Core Process Docs** (in `/docs`):
- [ ] `INDEX.md` - Documentation navigation
- [ ] `PROCESS-OVERVIEW.md` - Visual workflow guide
- [ ] `ai-assisted-agile-process.md` - Complete methodology
- [ ] `parallel-sprint-development-best-practices.md` - Parallel development guide
- [ ] `quick-reference.md` - Common commands & patterns

**Root Files**:
- [ ] `README.md` - Project overview
- [ ] `CLAUDE.md` - Claude Code instructions
- [ ] `.gitignore` - Git ignore rules

**Templates** (in `/templates`):
- [ ] `prd-template.md`
- [ ] `technical-spec-template.md`
- [ ] `sprint-planning-template.md`
- [ ] `pr-template.md`
- [ ] `decision-log-template.md`
- [ ] `retrospective-template.md`

**Action**: List missing required files.

### Step 4.2: Check Project Structure

Verify these directories exist and have `.gitkeep` if empty:

```
project/
├── src/.gitkeep
├── tests/.gitkeep
├── config/.gitkeep
├── scripts/.gitkeep
├── docs/.gitkeep
└── templates/
```

**Action**: List missing structure directories.

### Step 4.3: Verify .gitkeep Files in Documentation Folders

Check that empty documentation directories have `.gitkeep` files:

**Required .gitkeep files**:
- `docs/sprints/archive/.gitkeep`
- `docs/decisions/.gitkeep`
- `docs/retrospectives/.gitkeep`
- `docs/investigation/.gitkeep` (if folder exists)
- `docs/project-management/.gitkeep` (if folder exists)
- `docs/maintenance/.gitkeep` (if folder is empty)

**Why .gitkeep is important**:
- Git doesn't track empty directories
- .gitkeep placeholder ensures folders exist after clone
- Prevents confusion when adding first file to category

**Action**: List missing .gitkeep files in empty documentation folders.

---

## 🔗 5. Link Validation

### Step 5.1: Validate Internal Links

Check all `[text](path)` links in markdown files:

- Relative paths are correct after proposed moves
- Files exist at the referenced paths
- Anchors exist for section links (`#heading`)

**Action**: List all broken internal links.

### Step 5.2: Update Navigation

Ensure `docs/INDEX.md` reflects current documentation:

- All PRDs listed under appropriate section
- All sprint plans listed (current vs archive)
- All technical specs accessible
- Quick links to common docs

**Action**: Propose updates to INDEX.md if needed.

---

## 📊 Output Format

Please provide your findings in this format:

### Summary
- Total files reviewed: X
- Files to move/rename: X
- Content issues found: X
- Missing required files: X

### 1. File Organization Changes

```
Move:
  root/sprint-03-validation.md → docs/sprints/archive/sprint-03-validation.md
  root/auth-prd.md → docs/prds/2025-01-authentication-prd.md
  docs/tech-spec-api.md → docs/specs/2025-01-api-gateway-spec.md

Create directories:
  docs/sprints/current/
  docs/sprints/archive/
  docs/prds/
  docs/specs/
  docs/decisions/
  docs/retrospectives/
  docs/investigation/
  docs/project-management/
  docs/maintenance/
  assets/images/
  config/
```

### 2. Asset File Organization

```
Move images to assets/:
  root/category-academy.png → assets/images/category-academy.png
  root/category-ai-agents.png → assets/images/category-ai-agents.png
  root/screenshot-*.png → assets/images/ (19 files total)

Move data files to config/:
  root/comprehensive-target-urls.json → config/target-urls.json
  root/discovered-article-urls.json → config/discovered-urls.json
  root/target-urls.json → config/legacy-target-urls.json

Convert and move text files:
  root/Final Status Summary.txt → docs/project-management/final-status-summary.md
    (Convert plain text to markdown format with proper headers)

Delete (obsolete/temporary):
  root/temp-data.json (if exists)
  root/old-backup-*.png (if exists)
```

### 3. Naming Convention Fixes

```
Rename (with date stamps):
  docs/Feature_Auth_PRD.md → docs/prds/2025-01-authentication-prd.md
  docs/api-spec-v2.md → docs/specs/2025-01-api-gateway-spec.md
  docs/retro-sprint-03.md → docs/retrospectives/retro-2025-02-sprint-03.md

Rename (sprint docs - no date stamps):
  docs/Sprint_03_Validation.md → docs/sprints/archive/sprint-03-validation.md
```

### 3. Content Updates Needed

```
Update status in:
  docs/sprints/archive/sprint-01-foundation.md (status: complete)
  docs/sprints/archive/sprint-02-validation.md (status: complete)

Fix broken links in:
  docs/prds/2025-01-authentication-prd.md
    - Line 45: [Tech Spec](../tech-spec-api.md) → [Tech Spec](../specs/2025-01-api-gateway-spec.md)
  README.md
    - Line 23: [Sprint Plan](sprint-03.md) → [Sprint Plan](docs/sprints/archive/sprint-03-validation.md)
    - Line 67: [Auth PRD](docs/auth-prd.md) → [Auth PRD](docs/prds/2025-01-authentication-prd.md)
```

### 4. Missing Required Files

```
Missing:
  docs/quick-reference.md (create from template)
  templates/decision-log-template.md (copy from template repo)
  docs/sprints/archive/.gitkeep (create for empty folder)
  docs/decisions/.gitkeep (create for empty folder)
```

### 5. File Type Violations

```
Files in docs/ with wrong type:
  docs/diagram.png → assets/images/diagram.png
  docs/config.json → config/config.json

Files in root with wrong location:
  (See section 2: Asset File Organization above)
```

### 6. Recommended Git Commands

```bash
# Create directories
mkdir -p docs/sprints/current docs/sprints/archive docs/prds docs/specs docs/decisions docs/retrospectives docs/investigation docs/project-management docs/maintenance assets/images config

# Create .gitkeep files for empty folders
touch docs/sprints/archive/.gitkeep docs/decisions/.gitkeep docs/retrospectives/.gitkeep docs/investigation/.gitkeep docs/project-management/.gitkeep

# Move documentation files
git mv root/sprint-03-validation.md docs/sprints/archive/sprint-03-validation.md
git mv root/auth-prd.md docs/prds/2025-01-authentication-prd.md
git mv docs/tech-spec-api.md docs/specs/2025-01-api-gateway-spec.md

# Move asset files
git mv category-*.png assets/images/
git mv *.json config/ (review each file individually)

# Rename files (with date stamps)
git mv docs/Feature_Auth_PRD.md docs/prds/2025-01-authentication-prd.md
git mv docs/api-spec-v2.md docs/specs/2025-01-api-gateway-spec.md
git mv docs/retro-sprint-03.md docs/retrospectives/retro-2025-02-sprint-03.md

# Rename sprint docs (no date stamps)
git mv docs/Sprint_03_Validation.md docs/sprints/archive/sprint-03-validation.md

# Commit
git add -A
git commit -m "docs: Clean up documentation and enforce Symphony Core best practices

- Organize files into proper directories (prds/, specs/, sprints/, investigation/, project-management/)
- Move asset files to assets/images/ and config/
- Enforce lowercase-with-hyphens naming convention
- Add YYYY-MM date stamps to PRDs, specs, and retrospectives
- Archive completed sprint documents
- Fix broken internal links
- Update document status fields
- Add .gitkeep files to empty directories
- Clean up root directory (moved 19 PNGs + data files)

🤖 Generated with Claude for Web"
```

---

## ✅ Validation Checklist

After cleanup, verify:

- [ ] No documentation files in root (except README.md, CLAUDE.md)
- [ ] All filenames are lowercase-with-hyphens
- [ ] Sprint docs organized: current/ vs archive/
- [ ] PRDs in docs/prds/
- [ ] Technical specs in docs/specs/
- [ ] No broken internal links
- [ ] INDEX.md reflects current structure
- [ ] All required files present
- [ ] .gitkeep in empty structure folders

---

## 🚫 Protected Files (DO NOT MODIFY)

**CRITICAL**: These files are human-maintained and must NOT be modified:

- `docs/project-notes-ra.md` - Human project notes
- Any file matching `docs/project-notes-*.md`

If you find these files misplaced, recommend the move but **DO NOT** modify their content.

---

## Additional Context

**Repository-Specific Notes**:
(Add any project-specific documentation standards here when using this prompt)

-
-
-

---

**End of Analysis Request**

---

## 🎯 PROMPT ENDS HERE

---

## 📝 Post-Cleanup Actions

After applying Claude's recommended changes:

1. **Review the changes** in git diff before committing
2. **Test links** by opening README.md and clicking through key links
3. **Update this prompt** if you discover additional patterns to check
4. **Commit changes** with the suggested git commands
5. **Push to remote** after verification

---

## 🔄 Maintenance Schedule

**Recommended frequency**:
- **Weekly**: During active development (multiple PRs/week)
- **Bi-weekly**: During moderate development
- **Monthly**: During maintenance/low activity

**Triggers for immediate cleanup**:
- After merging a sprint
- Before major releases
- When onboarding new team members
- After repository structure changes

---

**Last Updated**: 2025-11-22
**Version**: 1.0.0
**Maintained By**: Symphony Core Team
