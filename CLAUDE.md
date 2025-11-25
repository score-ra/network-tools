# Claude Code Instructions - Software Development Project

## Project Overview
This is an AI-assisted software development project using Agile methodology with parallel sprint workflows. Focus on code quality, maintainability, module isolation, and collaborative development practices.

## 🔄 Development Process

**IMPORTANT**: This project uses a structured AI-assisted Agile process. Before starting work:
1. Read [start-here.md](start-here.md) for current sprint context
2. Review [AI-Assisted Agile Process](docs/ai-assisted-agile-process.md) for complete workflow
3. Check [Parallel Development Best Practices](docs/parallel-sprint-development-best-practices.md)

### Your Role (Claude Code CLI)
You are primarily used for **implementation**:
- Writing and editing code
- Running tests and builds
- Git operations (commit, rebase, push)
- Debugging and fixing issues
- Pre-merge checklist execution
- Code reviews

**Note**: For architecture design and sprint planning, the team uses Claude Cloud (Projects).

## Session Management

### Always Start Here
1. **Read** [start-here.md](start-here.md) to understand:
   - Current sprint objective
   - Your assigned ticket and module
   - What's been done already
   - What needs to be done next
   - Any blockers or dependencies

2. **Verify branch context**:
   ```bash
   git status
   git log -3
   ```

3. **Check for updates** (if during rebase window 8-10 AM):
   ```bash
   git fetch origin master
   git rebase origin/master
   pytest
   ```

### Always End Here
1. **Update** [start-here.md](start-here.md) with:
   - Completed tasks
   - Files modified
   - Next immediate actions
   - Any blockers discovered
   - Last updated timestamp

2. **Commit work** if requested:
   ```bash
   git add <files>
   git commit -m "Clear description"
   git push origin <branch>
   ```

## Development Standards

### Code Quality
- Write clean, readable code with meaningful variable names
- Follow DRY (Don't Repeat Yourself) principle
- Keep functions small and focused on single responsibility
- Add comments only when necessary to explain "why", not "what"
- Follow project coding standards documented in technical spec

### Project Structure
- Source code goes in `/src` organized by modules
- Tests go in `/tests` (mirror the src structure)
- Configuration files in `/config`
- Utility scripts in `/scripts`
- Documentation in `/docs`
- Templates in `/templates`

### Protected Files (NEVER Modify or Delete)
**⚠️ CRITICAL**: The following files are human-maintained and MUST NEVER be modified, edited, or deleted by AI:
- `docs/project-notes-ra.md` - Human project notes (owner: RA)
- Any file matching pattern: `docs/project-notes-*.md`

These files contain:
- SQL queries and database snippets
- Future sprint ideas and backlog
- Configuration values and environment notes
- Personal reference materials
- Meeting notes and decisions

**If you need to suggest additions**: Ask the human to update these files themselves.

### Module Isolation (CRITICAL for Parallel Development)
**Before modifying any file, check if it's high-risk**:

**High-Risk Shared Files** (check [start-here.md](start-here.md) and sprint planning):
- `src/main.py` or entry point - Use **registration pattern**
- `src/shared/config.py` - Use **section-based pattern**
- `src/shared/validators.py` - Use **pipeline pattern**

**Isolation Rules**:
1. **One feature = One module** - Stay in your assigned module
2. **Shared files** - Use designated patterns to prevent conflicts
3. **Same function modification** - Coordinate with team first

### Testing
- Write tests for new features and bug fixes
- Maintain test coverage above **80%**
- Run tests before committing
- Include both unit and integration tests
- Test files go in `tests/test_<module>/`

### Version Control

**Branch Naming**:
```
feature/<ticket-id>-<description>
bugfix/<ticket-id>-<description>
hotfix/<ticket-id>-<description>
```

**Daily Workflow**:
- **Morning (8-10 AM)**: Rebase window - rebase on master
- **Development**: Work on assigned module
- **Afternoon (4-5 PM)**: Review window - prepare PR
- **Evening (5-6 PM)**: Merge window - PRs get merged

**Commit Messages**:
- Clear, descriptive commit messages
- Keep commits atomic and focused
- Reference ticket ID when applicable

## Task Guidelines

### When Starting a New Feature
1. **Context check**: Read [start-here.md](start-here.md) and ticket details
2. **Module assignment**: Verify your assigned module path
3. **High-risk files**: Check what shared files you might touch
4. **Tests first**: Create test structure (TDD when appropriate)
5. **Implementation**: Code in isolated module
6. **Update docs**: Keep [start-here.md](start-here.md) current

### When Adding New Features
- Create tests first (TDD approach when appropriate)
- Update relevant documentation
- Follow existing code patterns and conventions
- Consider backwards compatibility
- Stay within assigned module boundaries

### When Fixing Bugs
- Reproduce the issue first
- Write a test that fails
- Fix the bug
- Verify the test passes
- Check for similar issues elsewhere

### When Refactoring
- Ensure tests pass before and after
- Refactor in small, incremental steps
- Don't change behavior, only structure
- Update documentation if needed

### When Modifying Shared Files

**Pattern 1: Config Files** (section-based)
```python
# === Feature A (TICKET-123) ===
FEATURE_A_CONFIG = "value"

# === Feature B (TICKET-456) ===
FEATURE_B_CONFIG = "value"
```

**Pattern 2: Entry Points** (registration)
```python
def create_app():
    app = Application()
    app.register(feature_a)  # TICKET-123
    app.register(feature_b)  # TICKET-456
    return app
```

**Pattern 3: Validators** (pipeline)
```python
def validate(data):
    # Feature A: Pre-validation
    if not pre_check(data):
        return Error()

    # Existing (unchanged)
    if not existing_validation(data):
        return Error()

    # Feature B: Post-validation
    if not post_check(data):
        return Error()
```

## Pre-Merge Checklist

**ALWAYS run before creating PR**:

### 1. Rebase on Master
```bash
git fetch origin master
git rebase origin/master
```

### 2. Code Quality
```bash
flake8 src/ tests/       # Zero errors
black src/ tests/        # Code formatted
mypy src/                # Type safety
```

### 3. Test Coverage
```bash
pytest                   # All tests pass
pytest --cov=src --cov-report=term  # ≥80% coverage for new code
```

### 4. Verify Module Isolation
- [ ] Changes primarily in assigned module
- [ ] Shared files use designated patterns
- [ ] No unexpected file modifications

### 5. Update Documentation
- [ ] [start-here.md](start-here.md) updated
- [ ] Code comments added for complex logic
- [ ] API docs updated (if applicable)

### 6. Create PR
Use [PR template](templates/pr-template.md):
- Fill out all sections
- List files modified
- Mark high-risk files
- Indicate merge priority
- Document testing done

## Security Standards

- No sensitive data in code (passwords, API keys, etc)
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)
- CSRF protection where applicable
- Proper authentication/authorization checks

## Environment Setup
- Copy `.env.example` to `.env` and configure
- Never commit `.env` or secrets
- Document all required environment variables
- Use development values in `.env.example`

## Communication

### Update [start-here.md](start-here.md) When:
- Starting work on a task
- Completing a task
- Discovering a blocker
- Modifying high-risk files
- Finding a dependency issue
- Ending a development session

### Flag Issues Immediately:
- Merge conflicts encountered
- Test failures after rebase
- Unexpected dependencies on other features
- Blockers preventing progress
- Security concerns

## Templates Available

Use these templates for consistency:
- [PRD Template](templates/prd-template.md) - Product requirements
- [Technical Spec Template](templates/technical-spec-template.md) - Architecture
- [Sprint Planning Template](templates/sprint-planning-template.md) - Sprint setup
- [PR Template](templates/pr-template.md) - Pull requests
- [Decision Log Template](templates/decision-log-template.md) - Architecture decisions
- [Retrospective Template](templates/retrospective-template.md) - Sprint review

## Important Reminders

- **Context**: ALWAYS read [start-here.md](start-here.md) at session start
- **Isolation**: Stay in assigned module to prevent conflicts
- **Patterns**: Use designated patterns for shared files
- **Testing**: Maintain ≥80% coverage
- **Rebase**: Rebase daily during morning window
- **Updates**: Keep [start-here.md](start-here.md) current
- **Files**: NEVER create files unless explicitly requested
- **Editing**: ALWAYS prefer editing existing files
- **Process**: Follow the AI-Assisted Agile Process

## Reference Documentation

- **Main Process**: [AI-Assisted Agile Process](docs/ai-assisted-agile-process.md)
- **Best Practices**: [Parallel Development Best Practices](docs/parallel-sprint-development-best-practices.md)
- **Current Context**: [start-here.md](start-here.md)
