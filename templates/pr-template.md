# Pull Request

## Ticket Reference
**Ticket ID**: [TICKET-XXX]
**Link**: [URL to ticket/issue]

---

## Description

### Summary
[1-2 sentence summary of what this PR does]

### Changes Made
- [Change 1: Brief description]
- [Change 2: Brief description]
- [Change 3: Brief description]

### Motivation
[Why are these changes needed? What problem do they solve?]

---

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactoring (code change that neither fixes a bug nor adds a feature)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Test coverage improvement
- [ ] Configuration change

---

## Files Modified

### New Files
```
src/module/new_file1.py
src/module/new_file2.py
tests/test_new_feature.py
```

### Modified Files
```
src/shared/config.py          # Added authentication section
src/main.py                   # Registered new routes
src/utils/validators.py       # Added email validation
```

### Deleted Files
```
(None)
```

### High-Risk Files Touched
- [x] `src/main.py` - Entry point (HIGH-RISK)
- [ ] `src/shared/config.py` - Configuration (HIGH-RISK)
- [ ] `src/shared/validators.py` - Validation (MEDIUM-RISK)

---

## Merge Priority
**Priority Level**: [P1 / P2 / P3 / P4]

**Justification**:
- [ ] P1: Isolated module, no dependencies, no shared files
- [ ] P2: Shared files modified in separate sections
- [ ] P3: Depends on another PR (specify: [PR #XXX])
- [ ] P4: Depends on P3 PR (specify: [PR #XXX])

---

## Dependencies

### Depends On
- [ ] [TICKET-XXX / PR #XXX]: [Description]
- [ ] None

### Blocks
- [ ] [TICKET-XXX]: [Description]
- [ ] None

### External Dependencies
- [ ] Third-party library: [Library name @ version]
- [ ] API changes required
- [ ] Database migration required
- [ ] Configuration changes required
- [ ] None

---

## Testing

### Test Coverage
- **Lines covered**: [XX%]
- **Branches covered**: [XX%]
- **Overall coverage**: [XX%]

### Unit Tests
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Edge cases covered
- [ ] Error handling tested

**Test files**:
```
tests/test_module/test_feature.py
tests/test_integration/test_api.py
```

### Integration Tests
- [ ] Integration tests added
- [ ] Integration tests pass
- [ ] API contracts validated

### Manual Testing
- [ ] Tested on development environment
- [ ] Tested on staging environment
- [ ] Tested with realistic data
- [ ] Tested edge cases manually

**Manual Test Scenarios**:
1. [Scenario 1: Description and result]
2. [Scenario 2: Description and result]
3. [Scenario 3: Description and result]

---

## Code Quality

### Pre-Merge Checklist
- [ ] Rebased on latest master
- [ ] All tests passing locally
- [ ] Linter passing (0 errors, 0 warnings)
- [ ] Code formatted with [Prettier/Black/etc]
- [ ] Type checker passing (if applicable)
- [ ] No commented-out code
- [ ] No debug/console statements
- [ ] No hardcoded values (use config)

### Code Review
- [ ] Self-reviewed the code
- [ ] AI code review completed (Claude Code)
- [ ] Addressed all AI suggestions
- [ ] Code follows project coding standards
- [ ] Complex logic has comments explaining "why"
- [ ] Function/method names are descriptive
- [ ] No duplicate code (DRY principle)

---

## Security

### Security Checklist
- [ ] No sensitive data in code (passwords, API keys, etc)
- [ ] Input validation implemented
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection (if applicable)
- [ ] Authentication/authorization checks in place
- [ ] No security vulnerabilities introduced
- [ ] Dependencies scanned for vulnerabilities

### Security Scan Results
```
<paste security scan output or "No issues found">
```

---

## Performance

### Performance Impact
- [ ] No performance impact
- [ ] Positive performance impact (faster execution)
- [ ] Negative performance impact (documented and justified below)

**Justification** (if negative impact):
[Explain why the performance trade-off is acceptable]

### Performance Testing
- [ ] Response time tested (target: <200ms)
- [ ] Load tested (if applicable)
- [ ] Database queries optimized
- [ ] N+1 queries avoided
- [ ] Appropriate caching implemented

---

## Database Changes

### Migration Required
- [ ] Yes (migration file included)
- [ ] No

**Migration File**:
```
migrations/YYYY-MM-DD-XXX-description.sql
```

### Schema Changes
- [ ] New tables
- [ ] Modified tables
- [ ] Deleted tables
- [ ] New indexes
- [ ] Modified indexes
- [ ] No schema changes

**Backward Compatibility**:
- [ ] Migration is backward compatible
- [ ] Migration requires downtime
- [ ] Rollback migration included

---

## Documentation

### Documentation Updated
- [ ] Code comments added for complex logic
- [ ] API documentation updated (OpenAPI/Swagger)
- [ ] README updated
- [ ] Architecture docs updated (if applicable)
- [ ] start-here.md updated
- [ ] No documentation changes needed

### Breaking Changes Documentation
- [ ] Breaking changes documented
- [ ] Migration guide provided
- [ ] Not applicable (no breaking changes)

---

## Deployment

### Deployment Notes
[Any special instructions for deployment]

### Configuration Changes
- [ ] New environment variables required
- [ ] Existing environment variables modified
- [ ] No configuration changes

**Environment Variables**:
```
NEW_VAR=value           # Description of what it does
MODIFIED_VAR=new_value  # What changed and why
```

### Rollback Plan
[How to rollback if issues are found after deployment]

---

## Potential Conflicts

### Conflict Assessment
- [ ] Low risk: Isolated changes, no shared files
- [ ] Medium risk: Shared files modified in separate sections
- [ ] High risk: Same functions/classes modified as other PRs

### Known Conflicts
- [ ] Expected conflict with [PR #XXX] in file [filename]
- [ ] No known conflicts

### Coordination Required
- [ ] Coordinated with [Developer Name] on [filename]
- [ ] No coordination required

---

## Screenshots (if applicable)

### Before
[Insert screenshot or "N/A"]

### After
[Insert screenshot or "N/A"]

---

## Checklist for Reviewers

### Code Review Focus Areas
- [ ] Logic correctness
- [ ] Error handling
- [ ] Security considerations
- [ ] Performance implications
- [ ] Test coverage adequacy
- [ ] Code maintainability
- [ ] Adherence to coding standards

### Questions for Reviewer
1. [Question 1 about specific design decision]
2. [Question 2 about alternative approach]

---

## Additional Notes

[Any additional context, gotchas, or information for reviewers]

---

## Post-Merge Tasks

- [ ] Monitor error logs for 24 hours
- [ ] Monitor performance metrics
- [ ] Update project documentation
- [ ] Notify stakeholders
- [ ] Close related tickets
- [ ] Delete feature branch

---

**Ready for Review**: [Yes / No]
**Merge After**: [Date/time or "Immediately after approval"]

---

**PR Created By**: [Your Name]
**Date**: [YYYY-MM-DD]
