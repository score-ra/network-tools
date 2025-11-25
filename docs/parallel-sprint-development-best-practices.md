# Parallel Sprint Development: Best Practices for Claude Code Cloud Agents

**Document Type**: Universal Development Standards
**Version**: 4.0
**Applicability**: Any repository using multiple Claude Code Cloud agents for parallel development
**Key Principle**: **Human delegates tasks to independent Claude Code Cloud agents, NOT AI-to-AI delegation**

---

## Claude Code: Cloud vs CLI

### ☁️ Claude Code Cloud (Web/Mobile) - RECOMMENDED for Parallel Development

**Best for:**
- ✅ **Parallel execution** - Multiple tasks running simultaneously in isolated sandboxes
- ✅ **Bug backlogs** - Well-defined, isolated fixes across codebase
- ✅ **Backend changes** - TDD with automated test verification
- ✅ **GitHub integration** - Automatic PR creation and real-time progress tracking
- ✅ **Mobile workflows** - Monitor and steer tasks via iOS app
- ✅ **Routine tasks** - Clearly scoped work with defined acceptance criteria

**Capabilities:**
- Runs in Anthropic-managed cloud infrastructure
- Each session in isolated sandbox with network/filesystem restrictions
- Real-time progress tracking across multiple sessions
- Automatic PR creation with change summaries
- Configurable network access (npm, pypi, custom domains)

### 💻 Claude Code CLI - Better for

- ✅ **Local iteration** - Quick edit-test-debug cycles
- ✅ **Complex debugging** - Need direct terminal/filesystem access
- ✅ **Private repos** - No GitHub connection required
- ✅ **Single-task focus** - One feature at a time, hands-on approach

---

## Core Philosophy

### Human-Driven Delegation Model

```
                    ┌─────────────────┐
                    │  Human (You)    │
                    │  Sprint Manager │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │ Claude Code │  │ Claude Code │  │ Claude Code │
    │  Cloud 1    │  │  Cloud 2    │  │  Cloud 3    │
    │ (Track 1)   │  │ (Track 2)   │  │ (Track 3)   │
    └─────────────┘  └─────────────┘  └─────────────┘
         │                 │                 │
         │                 │                 │
         ▼                 ▼                 ▼
    feature/          feature/          feature/
    TRACK-1           TRACK-2           TRACK-3
    branch            branch            branch
```

**YOU assign tracks to Cloud agents. Agents DO NOT coordinate with each other.**

---

## Prerequisites

### Repository Setup
- Git repository connected to GitHub
- Protected master/main branch
- Test suite with fast execution (<10 minutes)
- Linting/formatting tools configured
- Branch naming convention established
- Network access configured (npm, pypi, custom domains)

### Sprint Planning Output
- **Sprint backlog** broken into independent tracks
- **Track assignment document** with module isolation
- **Shared file matrix** identifying potential conflicts
- **Merge priority** defined (P1/P2/P3/P4)

---

## Sprint Planning Phase

### Step 1: Create Sprint Backlog

**Goal**: Break sprint into **isolated tracks** suitable for parallel Cloud execution.

**Output**: Sprint plan document with:

```markdown
# Sprint N: [Feature Name]

## Track 1: [Component A]
- Branch: feature/SPRINT-N-001-component-a
- Priority: P1 (no dependencies - parallel)
- Estimated: X days
- Files to create: [list]
- Files to modify: [list with section markers]
- Dependencies: None

## Track 2: [Component B]
- Branch: feature/SPRINT-N-002-component-b
- Priority: P1 (no dependencies - parallel)
- Estimated: Y days
- Files to create: [list]
- Files to modify: [list with section markers]
- Dependencies: None

## Track 3: [Component C]
- Branch: feature/SPRINT-N-003-component-c
- Priority: P3 (depends on Track 1 + 2)
- Estimated: Z days
- Files to create: [list]
- Files to modify: [list with section markers]
- Dependencies: Track 1 + Track 2 merged
```

**Key Requirements**:
- ✅ Each track creates primarily **new isolated files** (90%+ new code)
- ✅ Shared file modifications use **section-based patterns**
- ✅ Dependencies explicitly documented
- ✅ Merge priority assigned (P1/P2/P3/P4)

---

### Step 2: Validate Module Isolation

**Human reviews sprint plan**:

1. **Can Track 1 and Track 2 run simultaneously?**
   - ✅ Yes → P1 priority for both (parallel)
   - ❌ No → Serialize (Track 2 becomes P3)

2. **Do tracks modify the same section of shared files?**
   - ✅ Different sections → OK (use delimiters)
   - ❌ Same section → Serialize

3. **Can each track be tested independently?**
   - ✅ Yes → Good isolation
   - ❌ No → Refactor sprint plan

---

## Launching Cloud Agents

### Step 3: Create Cloud Tasks (Parallel or Sequential)

**Using Claude Code Cloud** (claude.com/code):

#### 1. Connect Repository (One-time Setup)
- Visit claude.com/code
- Authorize GitHub repository
- Configure network access for dependencies

#### 2. Launch Tasks

**For Parallel Tracks (P1):**

**Task 1:**
```
Branch: feature/SPRINT-N-001-component-a

Implement Track 1 from docs/SPRINT-N-plan.md:
- Read track specification
- Create module at src/module_a/
- Write tests in tests/module_a/
- Use TDD: write test → implement → verify
- Run full test suite before completion

Work autonomously. Don't ask permission at each step.
Create PR when all acceptance criteria met.
```

**Task 2:**
```
Branch: feature/SPRINT-N-002-component-b

Implement Track 2 from docs/SPRINT-N-plan.md:
- Read track specification
- Create module at src/module_b/
- Write tests in tests/module_b/
- Use TDD: write test → implement → verify
- Run full test suite before completion

Work autonomously. Don't ask permission at each step.
Create PR when all acceptance criteria met.
```

**For Dependent Tracks (P3):**

**Task 3:**
```
Branch: feature/SPRINT-N-003-component-c

⚠️ WAIT: Depends on Track 1 + Track 2

Once PRs #[X] and #[Y] are merged:
1. Rebase on latest master
2. Read Track 3 from docs/SPRINT-N-plan.md
3. Implement using module_a and module_b
4. Write integration tests
5. Create PR when complete

Work autonomously after dependencies merged.
```

#### 3. Monitor Progress
- View real-time progress in Cloud dashboard
- Review logs and command output
- Steer agent if going off track
- Answer questions as needed

---

## 📝 Effective Prompts for Cloud Agents

### Prompt Template for Independent Tracks

```
# Context
Branch: [branch-name]
Sprint: [sprint-name]
Track: [track-number]

# Task
Implement [feature-name] per docs/[sprint-plan].md

# Requirements
- Read specification from [file]
- Create files: [list]
- Modify files: [list with section markers - use Pattern X]
- Write tests: [list]
- Run tests: [command]
- Target coverage: ≥80%

# Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

# Workflow
1. Create branch from master
2. Implement using TDD
3. Run tests after each major change
4. Create PR when all criteria met

# Important
- Work autonomously (no permission needed)
- Follow existing code patterns
- For shared file [filename]: use [pattern name]
- Run `[test-command]` to verify
```

### Example: Bug Fix Track

```
# Bug Fix: User Authentication Timeout

Branch: bugfix/TICKET-456-auth-timeout
Files: src/auth/session.py, tests/test_auth.py

## Issue
Users logged out after 5 minutes instead of 30 minutes.
Session timeout hardcoded to 300 seconds.

## Fix
1. Move timeout to config/settings.py
2. Update session handler to use config value
3. Add test for configurable timeout
4. Verify all existing tests pass

## Verification
pytest tests/test_auth.py -v
All tests must pass.

Work autonomously. Create PR when complete.
```

### Example: Feature Track

```
# Feature: Export Data to CSV

Branch: feature/SPRINT-2-001-csv-export
Module: src/export/csv_exporter.py
Tests: tests/export/test_csv_exporter.py

## Specification
Read full spec from docs/SPRINT-2-plan.md Track 1

## Shared Files
- src/export/__init__.py: Add CSVExporter to exports (append-only)
- config/export_settings.py: Add CSV_CONFIG section (lines 45-55)

## Acceptance Criteria
- [ ] Exports user data to CSV format
- [ ] Handles 10K+ records efficiently
- [ ] Includes proper error handling
- [ ] Test coverage ≥80%
- [ ] All tests passing

Work autonomously. Create PR with summary when complete.
```

---

## When to Use Sequential vs Parallel

### ✅ Use Sequential Cloud Agents When:
- Track 2 depends on Track 1 code/API
- Learning from Track 1 informs Track 2 design
- Small project (1-2 features only)
- Tight coupling between features

**Sequential Pattern:**
```
Task 1 Complete → Review Results → Adjust Task 2 → Launch Task 2
```

### ✅ Use Parallel Cloud Agents When:
- Tracks are independent (different modules)
- No code dependencies between tracks
- 3+ isolated features to implement
- Time-to-market critical

**Parallel Pattern:**
```
Launch all P1 tasks simultaneously
Monitor dashboards
Merge in priority order (P1 → P2 → P3)
```

---

## Pull Request Management

### Cloud vs CLI PR Creation

**Claude Code Cloud**:
- ✅ Automatic PR creation when task completes
- ✅ Auto-generated description with change summary
- Human reviews auto-generated PR
- Human approves or requests changes

**Claude Code CLI**:
- Human or CLI creates PR manually using `gh pr create`
- Fill PR template manually

### PR Review Checklist

```markdown
## Track: SPRINT-1-001-export-orchestrator

**Stories Completed**:
- ✅ Story 1.1: [Description]
- ✅ Story 1.2: [Description]

**Files Created** (count):
- [list]

**Files Modified** (count):
- [list with section markers]

**Shared File Sections**:
- [filename]: lines X-Y (pattern used)

**Merge Priority**: P1/P2/P3

**Tests**: X/Y passing
**Coverage**: XX%

**Manual Testing**:
- ✅ [Test scenario 1]
- ✅ [Test scenario 2]

**Ready for merge**: ✅ Yes / ❌ No
```

---

## Module Isolation Strategy

### Rule 1: One Track = One Module (Zero Conflicts)

```
Track 1 → src/services/new-module-a.js (new file)
Track 2 → src/services/new-module-b.js (new file)
```
✅ **Best case** - parallel execution, no conflicts

### Rule 2: Shared Files = Different Sections

```javascript
// src/config/database.js

// === SPRINT-1-001: Track 1 - Export Config ===
function getExportConfig() {
  return { /* Track 1 settings */ };
}

// === SPRINT-1-002: Track 2 - Comparison Config ===
function getComparisonConfig() {
  return { /* Track 2 settings */ };
}
```
✅ **Acceptable** - clear delimiters, parallel safe

### Rule 3: Same Function = Serialize

```javascript
// BAD: Both modify same function
Track 1: utils/validator.js → validate() method
Track 2: utils/validator.js → validate() method

// SOLUTION: Serialize
Track 1 → P1 (merge first)
Track 2 → P3 (wait, then rebase)
```
❌ **Last resort** - sequential execution

---

## Shared File Patterns

### Pattern 1: Configuration Files (Section-Based)

```javascript
// config/settings.js

module.exports = {
  // === SPRINT-1-001: Track 1 ===
  export: {
    format: 'csv',
    batchSize: 1000
  },

  // === SPRINT-1-002: Track 2 ===
  comparison: {
    algorithm: 'fuzzy',
    threshold: 0.8
  }
};
```

### Pattern 2: Entry Points (Registration)

```javascript
// src/index.js

async function main() {
  await initializeApp();

  // === SPRINT-1-001: Track 1 ===
  registerExportCommands();

  // === SPRINT-1-002: Track 2 ===
  registerComparisonCommands();

  await startApp();
}
```

### Pattern 3: Database Migrations (Separate Files)

```
db/migrations/
├── 018_sprint1_track1_export_tables.sql
├── 019_sprint1_track2_comparison_tables.sql
└── 020_sprint1_track3_report_tables.sql
```

### Pattern 4: Test Files (Separate Files)

```
tests/
├── sprint1_track1_export.test.js
├── sprint1_track2_comparison.test.js
└── sprint1_track3_report.test.js
```

---

## Merge Priority System

### P1: Zero Dependencies
- Isolated module, new files only
- **Merge first** (all P1s merge same day)
- Parallel execution safe

**Example:**
```
Track 1: src/services/export.js (new)
Track 2: src/services/compare.js (new)
→ Both P1, merge in parallel
```

### P2: Shared Files, Different Sections
- Modify shared files (different sections)
- No functional dependencies
- **Merge same cycle as P1**

**Example:**
```
Track 1: package.json (add script)
Track 2: package.json (add dependency)
→ Both P2, parallel (different keys)
```

### P3: Depends on P1
- Uses P1 functionality
- **Rebase after P1 merge, then merge**

**Example:**
```
Track 1: Build API client (P1)
Track 3: Build report using API (P3)
→ Track 3 waits for Track 1
```

### P4: Depends on P3
- Uses P3 functionality (which depends on P1)
- **Rebase after P3 merge, then merge**

**Example:**
```
Track 1: API (P1)
Track 2: Database (P3, uses API)
Track 4: CLI (P4, uses DB)
→ Sequential: 1 → 2 → 4
```

---

## Human Coordinator Responsibilities

**You (human) are essential for:**

### 1. Sprint Planning
- Review/create sprint backlog
- Validate module isolation
- Approve plan before launching

### 2. Cloud Task Assignment
- Launch Claude Code Cloud tasks (3-5 agents)
- Provide clear, autonomous directives
- Stagger dependent tasks (P1 first, P3 later)

### 3. Progress Monitoring
- Check Cloud dashboard for progress
- Answer agent questions/blockers
- Steer agents if off track

### 4. PR Management
- Review auto-generated PRs
- Verify tests pass
- Merge in priority order (P1 → P2 → P3 → P4)
- Delete branches after merge

### 5. Dependency Coordination
- Notify P3 agents when P1 merged
- Trigger rebases for dependent tracks
- Resolve any merge conflicts

---

## Agent Communication Protocol

### Agents NEVER Communicate With Each Other

**❌ BAD:**
```
Agent 1: "Hey Agent 2, I merged changes"
Agent 2: "OK, I'll rebase"
```

**✅ GOOD:**
```
Human → Agent 1: "Create PR when complete"
Agent 1 → Human: "Track 1 PR #123 created"
Human: [Reviews and merges PR #123]
Human → Agent 2: "Track 1 merged. Rebase and continue"
Agent 2 → Human: "Rebased. Continuing Track 2"
```

### Agent-to-Human Communication

**Agents report:**
- ✅ Completion: "Track 1 complete. PR #123"
- ✅ Blockers: "Can't proceed - need Track 1"
- ✅ Conflicts: "Rebase conflict in X. Resolved."
- ✅ Issues: "Tests failing. Investigating..."

**Agents DO NOT:**
- ❌ Contact other agents
- ❌ Read other agent PRs
- ❌ Modify other agent branches
- ❌ Make architectural decisions

---

## Example: 3-Track Sprint

### Day 1: Launch

**Human launches 3 Cloud tasks:**

**Task 1 (P1):**
```
Branch: feature/SPRINT-1-001-export
Implement Track 1 from docs/SPRINT-1-plan.md
Work autonomously. Create PR when complete.
```

**Task 2 (P1):**
```
Branch: feature/SPRINT-1-002-compare
Implement Track 2 from docs/SPRINT-1-plan.md
Work autonomously. Create PR when complete.
```

**Task 3 (P3):**
```
Branch: feature/SPRINT-1-003-report
WAIT for my signal. Depends on Track 1+2.
I'll tell you when dependencies are merged.
```

### Day 2-4: Parallel Execution

**Agents 1 & 2:**
- Implement stories
- Run tests continuously
- Signal completion Day 4

**Agent 3:**
- Waits for signal

**Human:**
- Monitors progress
- Answers questions

### Day 4: Merge P1

**Human:**
1. Reviews PRs #123, #124
2. Merges Track 1 (tests pass ✅)
3. Merges Track 2 (tests pass ✅)
4. Posts to Agent 3: "Dependencies merged. Proceed with Track 3."

**Agent 3:**
- Rebases on master
- Implements Track 3
- Creates PR Day 7

### Day 7: Merge P3

**Human:**
1. Reviews PR #125
2. Merges Track 3 (tests pass ✅)
3. Sprint complete! 🎉

---

## Success Metrics

**Track per sprint:**
- Features merged / Features planned: 100%
- Conflict rate: <10% (0-1 per 10 tracks)
- Resolution time: <30 min per conflict
- Test pass rate: 100%
- Coverage: ≥80% maintained

---

## When This Works

✅ **Ideal conditions:**
- Sprint broken into isolated modules (90%+ new files)
- Human available for daily coordination
- Fast test suite (<10 min)
- 3-5 Cloud agents in parallel
- 1-2 week sprints

❌ **Not recommended:**
- Tight feature coupling
- Long-running branches (>1 week)
- Slow test suite (>30 min)
- Complex dependencies (everything depends on everything)
- No human coordinator

---

## Sprint Planning Template

```markdown
# Sprint [N]: [Feature Name]

## Track 1: [Component A]
- Branch: feature/SPRINT-[N]-001-[name]
- Priority: P1 (no dependencies)
- Estimated: [X] days

### Files to Create
- src/services/module-a.js
- tests/module-a.test.js

### Files to Modify
- config/settings.js (section lines 45-55)

### Stories
- Story 1.1: [Name] (P0, 5 points)
  - Tasks: [list]
  - Acceptance: [list]

### Testing
- Unit: [describe]
- Integration: [describe]

---

## Track 2: [Component B]
[Same structure]

---

## Shared File Matrix

| File | Track 1 | Track 2 | Conflict Risk |
|------|---------|---------|---------------|
| config.js | Lines 45-55 | Lines 60-70 | Low (sections) |

---

## Merge Order
1. Day 4: Track 1 (P1) + Track 2 (P1) - parallel
2. Day 7: Track 3 (P3) - after rebase

## Success Criteria
- [ ] All tracks complete
- [ ] All tests pass
- [ ] <10% conflict rate
```

---

## Summary

**Human does:**
1. Sprint planning
2. Launch Cloud tasks
3. Monitor progress
4. Review and merge PRs
5. Coordinate dependencies

**Cloud Agents do:**
1. Read track specification
2. Implement autonomously
3. Run tests continuously
4. Create PRs automatically
5. Report status to human

**Cloud Agents NEVER:**
- Communicate with each other
- Make architectural decisions
- Merge PRs (human does this)

---

**Version**: 4.0 - Cloud-First Development
**Last Updated**: 2025-11-21
**Template**: Copy to any repo for parallel Cloud agent development
