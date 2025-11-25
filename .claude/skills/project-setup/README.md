# Project Setup Skill

**Version:** 1.0.0
**Author:** Symphony Core Team
**Type:** Claude Code Skill

## Overview

The **project-setup** skill automates the complete setup of a new software development project using the `software-dev-project-template` GitHub template repository. It provides an interactive, guided experience that handles everything from repository initialization to initial sprint planning.

## What It Does

This skill automates:

1. **Information Gathering** - Interactively prompts for project details
2. **Repository Setup** - Guides GitHub template usage or local setup
3. **Tech Stack Initialization** - Sets up Python/Node.js/Go with appropriate dependencies
4. **Template Customization** - Replaces placeholders with project-specific information
5. **Documentation Generation** - Creates initial PRD and Technical Specification
6. **Session Context** - Creates `start-here.md` for ongoing development
7. **Sprint Planning** (optional) - Helps create initial sprint plan
8. **Docker & CI/CD** (optional) - Sets up containerization and automation
9. **Verification** - Validates setup and creates initial git commit
10. **Summary** - Provides comprehensive next steps

## When to Use

Use this skill when:
- ✅ Starting a new project from the template
- ✅ Setting up a fresh development environment
- ✅ Onboarding a new AI-assisted Agile project
- ✅ Converting an existing project to this template structure

## Installation

This skill is included with the `software-dev-project-template` and located at:

```
.claude/skills/project-setup/
```

### For Other Projects

To use this skill in other projects:

**Option 1: Project-Specific (Recommended for teams)**
```bash
# From your project root
mkdir -p .claude/skills
cp -r /path/to/template/.claude/skills/project-setup .claude/skills/
```

**Option 2: Personal (Available to all your projects)**
```bash
# Install to personal skills directory
mkdir -p ~/.claude/skills
cp -r /path/to/template/.claude/skills/project-setup ~/.claude/skills/
```

## How to Use

### Automatic Invocation

Claude Code will automatically detect when this skill is relevant based on your request:

```
User: "Set up a new Python project for a REST API"
```

Claude will recognize this matches the skill's purpose and invoke it automatically.

### Explicit Invocation

You can explicitly request the skill:

```
User: "Use the project-setup skill to initialize a new Node.js project"
```

### Example Session

```
User: "I want to create a new Python FastAPI project called 'task-manager'"

Claude: I'll use the project-setup skill to help you! Let me gather some information first.

1. **Project Name**: task-manager
2. **Project Description**: What does this project do?

User: It's a task management API with user authentication

Claude: Great! A few more questions:
3. **Project Type**: Is this a REST API service? (yes/no)
4. **Primary Tech Stack**: You mentioned Python FastAPI - should I use Python 3.11+?
5. **Testing Framework**: pytest (recommended), unittest, or other?
6. **Repository Setup**: Should I guide you to create from GitHub template, or is it already cloned?

[... and so on through the setup process]
```

## File Structure

```
.claude/skills/project-setup/
├── SKILL.md                        # Main skill instructions (Claude reads this)
├── README.md                       # This file - documentation for humans
├── scripts/
│   ├── validate-setup.sh          # Validates project setup completeness
│   ├── detect-tech-stack.sh       # Detects current tech stack
│   └── customize-templates.sh     # Replaces placeholders in files
└── resources/
    ├── setup-checklist.md         # Step-by-step checklist
    ├── project-types-guide.md     # Guide for different project types
    └── common-tech-stacks.md      # Popular tech stack configurations
```

## Supported Tech Stacks

### Python
- **FastAPI** - Modern REST APIs, microservices
- **Flask** - Web applications, simple APIs
- **Click/Typer** - CLI tools
- **Pandas** - Data pipelines

**Features:**
- pytest testing framework
- black code formatting
- flake8 linting
- mypy type checking
- Virtual environment setup

### Node.js/TypeScript
- **Express** - REST APIs, web servers
- **NestJS** - Enterprise applications
- **Commander** - CLI tools

**Features:**
- Jest testing framework
- ESLint linting
- Prettier formatting
- TypeScript configuration
- npm package management

### Go
- **Gin/Echo** - High-performance APIs
- **Cobra** - CLI tools

**Features:**
- Built-in testing
- Standard formatting
- Go modules

## What Gets Created

After running this skill, you'll have:

### Configuration Files

**Python Projects:**
- `requirements.txt` - Dependencies
- `pytest.ini` - Test configuration
- `.env.example` - Environment template
- `.gitignore` - Updated for Python

**Node.js Projects:**
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript configuration
- `jest.config.js` - Test configuration
- `.eslintrc.json` - Linting rules
- `.prettierrc` - Formatting rules
- `.env.example` - Environment template
- `.gitignore` - Updated for Node.js

**Go Projects:**
- `go.mod` - Module definition
- `.env.example` - Environment template
- `.gitignore` - Updated for Go

### Documentation

- `docs/<project-name>-prd.md` - Product Requirements Document
- `docs/<project-name>-technical-spec.md` - Technical Specification
- `start-here.md` - Session context (always check this first!)
- Updated `README.md` - Project-specific information
- Updated `docs/INDEX.md` - Documentation navigation

### Project Structure

```
your-project/
├── src/                   # Source code
│   ├── shared/           # Shared utilities
│   └── __init__.py       # Package init (Python)
├── tests/                # Test files
├── docs/                 # Documentation
├── config/               # Configuration
├── scripts/              # Utility scripts
├── .env.example         # Environment template
├── requirements.txt      # Dependencies (Python)
├── package.json         # Dependencies (Node.js)
├── pytest.ini           # Test config (Python)
├── jest.config.js       # Test config (Node.js)
└── start-here.md        # Session context
```

### Optional Features

**Docker:**
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

**CI/CD:**
- `.github/workflows/ci.yml` (GitHub Actions)
- OR `.gitlab-ci.yml` (GitLab CI)

## Helper Scripts

### validate-setup.sh

Validates that your project setup is complete and correct.

**Usage:**
```bash
./.claude/skills/project-setup/scripts/validate-setup.sh
```

**Checks:**
- ✅ Directory structure
- ✅ Required files
- ✅ Tech stack configuration
- ✅ Dependencies installed
- ✅ Git repository
- ✅ Customization complete
- ✅ No placeholders remaining

**Exit codes:**
- `0` - Setup is complete and valid
- `1` - Errors found (missing files, etc.)

### detect-tech-stack.sh

Detects the current tech stack in the project.

**Usage:**
```bash
./.claude/skills/project-setup/scripts/detect-tech-stack.sh
```

**Detects:**
- Python (requirements.txt, pytest.ini)
- Node.js (package.json, tsconfig.json)
- Go (go.mod)
- Java (pom.xml, build.gradle)
- Ruby (Gemfile)
- Rust (Cargo.toml)

### customize-templates.sh

Replaces placeholders in template files.

**Usage:**
```bash
./.claude/skills/project-setup/scripts/customize-templates.sh <project-name> [description] [tech-stack]
```

**Example:**
```bash
./scripts/customize-templates.sh "task-manager" "Task management API" "Python 3.11"
```

**Updates:**
- README.md
- start-here.md
- package.json (if exists)
- .env.example
- Generated documentation

## Resource Files

### setup-checklist.md

A comprehensive checklist covering all 10 phases of project setup. Use this to track progress or verify nothing was missed.

### project-types-guide.md

Detailed guide for different project types:
- Web Application (Full-Stack)
- REST API Service
- CLI Tool
- Data Pipeline
- Library/Package
- Mobile App Backend
- Microservice

Includes:
- Characteristics
- Recommended tech stacks
- Initial features to implement
- Directory structure suggestions

### common-tech-stacks.md

Quick reference for popular tech stack combinations with:
- Complete dependency lists
- Configuration file examples
- Common commands
- Environment variable templates

## Workflow

The skill follows this workflow:

```
1. Gather Information
   ├─ Project details
   ├─ Tech stack preferences
   └─ Optional features

2. Setup Repository
   ├─ GitHub template (if new)
   ├─ Clone locally
   └─ Verify structure

3. Initialize Tech Stack
   ├─ Create config files
   ├─ Install dependencies
   └─ Set up tooling

4. Customize Templates
   ├─ Replace placeholders
   └─ Update documentation

5. Generate Docs
   ├─ Create PRD
   ├─ Create Tech Spec
   └─ Create start-here.md

6. Optional Features
   ├─ Docker (if requested)
   ├─ CI/CD (if requested)
   └─ Sprint planning (if requested)

7. Verify & Commit
   ├─ Run validation
   ├─ Create git commit
   ├─ Push to remote (optional)
   └─ Display summary
```

## Customization

### Adding New Tech Stacks

To add support for additional tech stacks:

1. **Update SKILL.md** - Add new Phase 3 section for your stack
2. **Add to detect-tech-stack.sh** - Add detection logic
3. **Add to common-tech-stacks.md** - Document the stack
4. **Test thoroughly** - Ensure all phases work correctly

### Modifying Questions

To change what information is gathered, edit Phase 1 in `SKILL.md`:

```markdown
## Phase 1: Gather Project Information

Ask the user these questions:
1. Your custom question
2. Another custom question
...
```

### Adding Pre-configured Templates

Add common project configurations to `resources/`:

```bash
resources/
├── presets/
│   ├── rest-api-python.json
│   ├── rest-api-nodejs.json
│   └── cli-tool-python.json
```

## Troubleshooting

### Skill Not Activating

**Problem:** Claude doesn't invoke the skill automatically.

**Solutions:**
1. Be explicit: "Use the project-setup skill"
2. Check skill is in `.claude/skills/` or `~/.claude/skills/`
3. Verify `SKILL.md` has valid frontmatter

### Dependencies Installation Fails

**Problem:** `pip install` or `npm install` fails.

**Solutions:**
1. Check internet connection
2. Verify package manager is installed
3. Check version compatibility
4. Try manual installation

### Git Operations Fail

**Problem:** Git commands fail during setup.

**Solutions:**
1. Verify git is installed: `git --version`
2. Configure git user: `git config user.name` and `user.email`
3. Check remote repository exists and is accessible
4. Verify SSH keys or credentials

### Placeholders Remaining

**Problem:** Files still contain `[YOUR_PROJECT_NAME]` or `<project-name>`.

**Solutions:**
1. Run customize script manually
2. Use Find & Replace in your editor
3. Check if customization step was skipped

### Tests Don't Run

**Problem:** Test command fails.

**Solutions:**
1. Verify test framework is installed
2. Check test configuration file (pytest.ini, jest.config.js)
3. Ensure test directory exists with proper structure
4. Check test file naming conventions

## Best Practices

### 1. Answer Questions Upfront

Provide as much information as possible when invoking the skill:

✅ **Good:**
```
"Set up a new Python FastAPI project called 'task-manager' for a REST API
with PostgreSQL database. Include Docker support."
```

❌ **Less Efficient:**
```
"Set up a project"
```

### 2. Review Generated Files

Always review the generated documentation:
- PRD may need refinement
- Technical Spec should match your architecture
- start-here.md should reflect current state

### 3. Commit Early and Often

Don't wait until everything is perfect:
- Commit after setup completes
- Make iterative improvements
- Use feature branches

### 4. Use Validation Scripts

Run validation before considering setup complete:
```bash
./.claude/skills/project-setup/scripts/validate-setup.sh
```

### 5. Update start-here.md

Keep `start-here.md` current throughout development:
- Update after each session
- Track completed tasks
- Note blockers and dependencies

## Integration with Development Workflow

### With Claude Cloud (Projects)

**Use Case:** Architecture design and sprint planning

1. Use this skill to set up the project structure
2. Switch to Claude Cloud for:
   - Refining the PRD
   - Designing the architecture
   - Creating detailed sprint plans
   - Breaking down user stories

### With Claude Code CLI

**Use Case:** Implementation and testing

1. This skill sets up the foundation
2. Use Claude Code CLI for:
   - Writing code
   - Running tests
   - Git operations
   - Code reviews
   - Debugging

### Workflow Recommendation

```
Project Setup Skill (one-time)
  ↓
Claude Cloud (architecture & planning)
  ↓
Claude Code CLI (implementation)
  ↓
Repeat: Cloud (planning) → Code (implementation)
```

## Examples

### Example 1: Python REST API

```
User: Use the project-setup skill to create a Python FastAPI REST API
called 'user-service' with PostgreSQL support.

[Skill gathers remaining info, then creates:]
- requirements.txt with FastAPI, SQLAlchemy, pytest
- pytest.ini configured
- src/api/, src/models/, src/services/ structure
- docs/user-service-prd.md
- docs/user-service-technical-spec.md
- start-here.md
- Initial git commit

Result: Ready to implement user authentication endpoints
```

### Example 2: Node.js CLI Tool

```
User: Set up a Node.js TypeScript CLI tool called 'deploy-helper'

[Skill creates:]
- package.json with Commander, chalk, inquirer
- tsconfig.json for TypeScript
- jest.config.js for testing
- src/commands/ structure
- Executable bin/deploy-helper
- Documentation

Result: Ready to implement CLI commands
```

### Example 3: Full-Stack Web App

```
User: Create a full-stack web app 'blog-platform' with Express backend
and React frontend, include Docker

[Skill creates:]
- Monorepo structure
- backend/ with Express + TypeScript
- frontend/ with React + TypeScript
- Docker setup with docker-compose
- Shared types
- CI/CD pipeline

Result: Ready to implement blog features
```

## Version History

### 1.0.0 (2025-11-23)
- Initial release
- Support for Python, Node.js/TypeScript, Go
- Interactive project setup
- Documentation generation
- Docker and CI/CD support
- Sprint planning assistance
- Helper scripts for validation and customization

## Contributing

To improve this skill:

1. **Test thoroughly** - Try different tech stacks and project types
2. **Report issues** - Document problems and edge cases
3. **Suggest improvements** - New features, better workflows
4. **Add examples** - More project type examples
5. **Update docs** - Keep this README current

## License

This skill is part of the Symphony Core software development project template and follows the same license.

## Support

For issues or questions:
- Check this README first
- Review the resource files in `resources/`
- Run validation scripts
- Consult the main template documentation

---

**Ready to set up your next project?** Just ask Claude Code to use this skill! 🚀
