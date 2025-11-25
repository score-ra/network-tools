# Sprint Planning

**Sprint ID**: [SPRINT-XX]
**Sprint Duration**: [2 weeks / 3 weeks]
**Start Date**: [YYYY-MM-DD]
**End Date**: [YYYY-MM-DD]
**Team Capacity**: [X story points / X developer-days]

---

## Sprint Goal

[1-2 sentence description of what the team aims to achieve this sprint]

---

## Team Composition

| Name | Role | Capacity | Focus Area |
|------|------|----------|------------|
| [Name] | [Developer / QA / etc] | [X points] | [Module A] |
| [Name] | [Developer / QA / etc] | [X points] | [Module B] |
| [Name] | [Developer / QA / etc] | [X points] | [Module C] |

**Total Capacity**: [X story points]

---

## Selected User Stories

### High Priority (Must Have)

#### [TICKET-001] Feature A - User Authentication
**User Story**: As a user, I want to log in securely so that my data is protected

**Story Points**: 8
**Assigned To**: [Developer Name]
**Module**: `src/auth/`
**Branch**: `feature/TICKET-001-user-authentication`
**Priority**: P1

**Acceptance Criteria**:
- [ ] User can log in with email and password
- [ ] JWT token is generated and stored securely
- [ ] Invalid credentials show appropriate error
- [ ] Password is hashed with bcrypt

**Technical Tasks**:
- [ ] Create User model and database schema
- [ ] Implement authentication service
- [ ] Create login API endpoint
- [ ] Add JWT token generation
- [ ] Write unit tests (≥80% coverage)
- [ ] Write integration tests
- [ ] Update API documentation

**Files to Modify**:
- `src/auth/models.py` (new)
- `src/auth/services.py` (new)
- `src/auth/handlers.py` (new)
- `src/shared/config.py` (HIGH-RISK: add auth section)
- `src/main.py` (HIGH-RISK: register auth routes)
- `tests/test_auth/` (new)

**Dependencies**: None
**Blocks**: TICKET-002

---

#### [TICKET-002] Feature B - User Profile Management
**User Story**: As a user, I want to manage my profile so that my information is up to date

**Story Points**: 5
**Assigned To**: [Developer Name]
**Module**: `src/profile/`
**Branch**: `feature/TICKET-002-user-profile`
**Priority**: P3 (Depends on TICKET-001)

**Acceptance Criteria**:
- [ ] User can view their profile
- [ ] User can update profile information
- [ ] Changes are validated before saving
- [ ] Unauthorized users cannot access other profiles

**Technical Tasks**:
- [ ] Create Profile model
- [ ] Implement profile service
- [ ] Create profile API endpoints (GET, PUT)
- [ ] Add input validation
- [ ] Write unit tests
- [ ] Write integration tests

**Files to Modify**:
- `src/profile/models.py` (new)
- `src/profile/services.py` (new)
- `src/profile/handlers.py` (new)
- `src/shared/validators.py` (HIGH-RISK: add profile validation)
- `src/main.py` (HIGH-RISK: register profile routes)
- `tests/test_profile/` (new)

**Dependencies**: TICKET-001 (needs authentication)
**Blocks**: None

---

### Medium Priority (Should Have)

#### [TICKET-003] Feature C - Data Export
**User Story**: As a user, I want to export my data so that I can use it elsewhere

**Story Points**: 3
**Assigned To**: [Developer Name]
**Module**: `src/export/`
**Branch**: `feature/TICKET-003-data-export`
**Priority**: P2

**Acceptance Criteria**:
- [ ] User can export data as CSV
- [ ] User can export data as JSON
- [ ] Export includes all user-owned data
- [ ] Large exports are handled asynchronously

**Technical Tasks**:
- [ ] Create export service
- [ ] Implement CSV formatter
- [ ] Implement JSON formatter
- [ ] Create export API endpoint
- [ ] Add background job for large exports
- [ ] Write unit tests
- [ ] Write integration tests

**Files to Modify**:
- `src/export/services.py` (new)
- `src/export/formatters.py` (new)
- `src/export/handlers.py` (new)
- `src/main.py` (HIGH-RISK: register export routes)
- `tests/test_export/` (new)

**Dependencies**: None
**Blocks**: None

---

## Module Isolation Plan

### Module Assignment Matrix

| Feature | Module Path | Developer | High-Risk Files | Isolation Level |
|---------|-------------|-----------|-----------------|-----------------|
| TICKET-001 | src/auth/ | Dev A | config.py, main.py | High |
| TICKET-002 | src/profile/ | Dev B | validators.py, main.py | Medium |
| TICKET-003 | src/export/ | Dev C | main.py | High |

### High-Risk Shared Files

#### src/shared/config.py
**Risk Level**: HIGH
**Expected Modifications**: 3 features

**Mitigation Strategy**: Section-based pattern
```python
# === TICKET-001: Authentication Config ===
AUTH_SECRET_KEY = "..."
AUTH_TOKEN_EXPIRY = 3600

# === TICKET-002: Profile Config ===
PROFILE_MAX_BIO_LENGTH = 500
```

**Merge Priority**: P1 (TICKET-001) merges first, others rebase

---

#### src/main.py
**Risk Level**: HIGH
**Expected Modifications**: 3 features

**Mitigation Strategy**: Registration pattern
```python
def create_app():
    app = FastAPI()

    # TICKET-001: Auth routes
    app.include_router(auth.router)

    # TICKET-002: Profile routes
    app.include_router(profile.router)

    # TICKET-003: Export routes
    app.include_router(export.router)

    return app
```

**Merge Priority**: P1 → P2 → P3 (sequential merges with rebase)

---

#### src/shared/validators.py
**Risk Level**: MEDIUM
**Expected Modifications**: 1 feature (TICKET-002)

**Mitigation Strategy**: Pipeline pattern (if multiple validators needed)

**Merge Priority**: Standard

---

## Merge Priority Plan

### Priority Levels

**P1 - Merge First** (Zero Dependencies):
- TICKET-001: Authentication (isolated module)
- TICKET-003: Data Export (isolated module)

**P2 - Merge Second** (Parallel Tracks):
- (None this sprint)

**P3 - Merge Third** (Depends on P1):
- TICKET-002: Profile (depends on TICKET-001 auth)

**P4 - Merge Fourth** (Depends on P3):
- (None this sprint)

### Merge Schedule

| Day | Merge Window (5-6 PM) | Tickets | Action |
|-----|----------------------|---------|--------|
| Day 1-3 | Development | All | Daily rebase |
| Day 4 | First merge window | TICKET-001 | Review & merge if ready |
| Day 5 | Second merge window | TICKET-003 | Review & merge if ready |
| Day 6-7 | Development | TICKET-002 | Rebase on latest master |
| Day 8 | Third merge window | TICKET-002 | Review & merge if ready |
| Day 9-10 | Buffer | All | Fix issues, tech debt |

---

## Daily Workflow Schedule

### Morning (8-10 AM): Rebase Window
**All Developers**:
```bash
git fetch origin master
git rebase origin/master
git push origin <branch> --force-with-lease
<run-tests>
```

**No merges to master during this window**

### Midday (10 AM - 4 PM): Development
**All Developers**:
- Work on assigned tasks
- Update `start-here.md` with progress
- Run tests frequently
- Push changes to feature branch

### Afternoon (4-5 PM): Review Window
**All Developers**:
- Run pre-merge checklist
- Create or update PR
- Request AI code review
- Address review comments

### Evening (5-6 PM): Merge Window
**Merge Master** (Tech Lead or designated person):
- Review PRs in priority order
- Merge approved PRs
- Run full test suite after each merge
- Notify team of merges
- Document any issues

---

## Success Metrics

### Sprint Metrics
- **Velocity**: [Target story points]
- **Commitment accuracy**: [% of committed stories completed]
- **Cycle time**: [Average days from start to merge]

### Code Quality Metrics
- **Test coverage**: ≥80%
- **Linter errors**: 0
- **Security vulnerabilities**: 0
- **Code review comments**: <10 per PR

### Parallel Development Metrics
- **Conflict rate**: <10% (target)
- **Resolution time**: <30 minutes (target)
- **Successful merges**: [X/Y]
- **Rollbacks**: 0 (target)

---

## Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Multiple features modifying main.py | High | High | Registration pattern + sequential merges |
| Authentication complexity | Medium | Medium | Start early, allocate extra time |
| Third-party API downtime | Low | Low | Mock in tests, circuit breaker pattern |

### Schedule Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| TICKET-001 delayed | High | Medium | Start immediately, daily check-ins |
| Unexpected scope creep | Medium | Medium | Stick to acceptance criteria |
| Team member unavailable | Medium | Low | Cross-training, documentation |

---

## Communication Plan

### Daily Standup (9:00 AM)
**Format**: 15 minutes, async or sync
**Questions**:
1. What did you accomplish yesterday?
2. What will you work on today?
3. Any blockers?

**Focus**: Coordination on shared files

### Mid-Sprint Review (Day 5)
**Purpose**:
- Check progress vs. plan
- Adjust priorities if needed
- Identify blockers early

### Sprint Demo (Last Day)
**Attendees**: Team + stakeholders
**Format**:
- Demo completed features
- Discuss challenges
- Gather feedback

### Sprint Retrospective (Last Day)
**Purpose**:
- What went well
- What to improve
- Action items for next sprint

---

## Definition of Done

A story is considered "Done" when:

- [ ] All acceptance criteria are met
- [ ] Code follows project coding standards
- [ ] All tests pass (unit + integration)
- [ ] Test coverage ≥80% for new code
- [ ] Code has been reviewed (AI + peer)
- [ ] No linter errors or warnings
- [ ] Documentation updated
- [ ] Merged to master branch
- [ ] Deployed to staging environment
- [ ] Manual testing completed
- [ ] No known bugs or regressions

---

## Pre-Merge Checklist Template

For each PR, verify:

**Code Quality**:
- [ ] Rebased on latest master
- [ ] Linter passing (0 errors)
- [ ] Formatter applied
- [ ] Type checker passing
- [ ] No commented-out code
- [ ] No debug statements

**Testing**:
- [ ] All tests passing
- [ ] New tests added for new features
- [ ] Coverage ≥80%
- [ ] Edge cases covered
- [ ] Manual testing completed

**Documentation**:
- [ ] Code comments for complex logic
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] start-here.md updated

**Review**:
- [ ] AI code review passed
- [ ] Peer review approved
- [ ] All comments addressed
- [ ] No merge conflicts

---

## Tools & Resources

### Development Tools
- **IDE**: [VSCode / PyCharm]
- **Git Client**: [CLI / GitKraken]
- **API Testing**: [Postman / Insomnia]
- **Database Client**: [DBeaver / DataGrip]

### Claude AI Usage

**Claude Cloud** (Projects):
- Sprint planning analysis
- Architecture design
- Cross-feature coordination
- Retrospective insights

**Claude Code CLI**:
- Code implementation
- Test writing
- Git operations
- Pre-merge checks

### Documentation
- Technical Spec: [Link]
- API Docs: [Link]
- Database Schema: [Link]
- Coding Standards: [Link]

---

## Appendix

### Sprint Backlog Summary

| Ticket | Title | Points | Priority | Status |
|--------|-------|--------|----------|--------|
| TICKET-001 | User Authentication | 8 | P1 | To Do |
| TICKET-002 | User Profile | 5 | P3 | To Do |
| TICKET-003 | Data Export | 3 | P2 | To Do |
| **Total** | | **16** | | |

### Burndown Chart Tracking

| Day | Points Remaining | Target Line |
|-----|------------------|-------------|
| Day 0 | 16 | 16 |
| Day 1 | 16 | 14.4 |
| Day 2 | 16 | 12.8 |
| ... | ... | ... |
| Day 10 | 0 | 0 |

---

**Sprint Planning Approved By**:
- Tech Lead: _________________ Date: _______
- Product Owner: _____________ Date: _______
