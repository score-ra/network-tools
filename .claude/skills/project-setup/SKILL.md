---
name: project-setup
description: Automates new project setup from the software-dev-project-template including customization, documentation generation, and initial sprint planning
version: "1.0.0"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Project Setup Automation Skill

## Overview

This skill automates the complete setup of a new software development project using the `software-dev-project-template` GitHub template repository. It handles:

- Repository initialization and cloning
- Template file customization
- Initial documentation generation (PRD, Technical Spec)
- Project-specific tech stack setup
- Sprint planning and ticket creation
- Environment configuration
- Git initialization and first commit

## When to Use

Use this skill when:
- Starting a new project from the template
- Setting up a fresh development environment
- Onboarding a new AI-assisted Agile project
- Converting an existing project to this template structure

## Prerequisites

Before running this skill, ensure:
- Git is installed and configured
- You have GitHub access (if cloning template)
- You know your project's basic details (name, type, tech stack)
- You have permissions to create repositories (if needed)

## Phase 1: Gather Project Information

**IMPORTANT**: Before proceeding with any setup, ask the user for ALL of the following information. Wait for their complete responses before moving to Phase 2.

### Required Information

Ask the user these questions:

1. **Project Name**: What is your project name? (e.g., "content-conductor", "api-gateway")
2. **Project Description**: Provide a one-sentence description of what this project does
3. **Project Objective**: What is the main goal or problem this project solves?
4. **Project Type**: What type of project is this?
   - Web application (full-stack)
   - REST API service
   - CLI tool
   - Data pipeline
   - Library/Package
   - Mobile app backend
   - Other (specify)

5. **Primary Tech Stack**: What is your primary programming language/framework?
   - Python (specify version, e.g., 3.11+)
   - Node.js/TypeScript (specify version)
   - Go
   - Java/Kotlin
   - Other (specify)

6. **Testing Framework**: Which testing framework do you prefer?
   - Python: pytest (default), unittest, nose2
   - Node.js: Jest (default), Mocha, Vitest
   - Go: testing (built-in), Ginkgo
   - Other (specify)

7. **Repository Setup**: How is your repository set up?
   - I need to create from GitHub template (provide org/name)
   - Already cloned locally (provide path)
   - I'll create manually and come back

8. **Additional Features** (optional):
   - Docker support? (yes/no)
   - CI/CD setup? (GitHub Actions/GitLab CI/None)
   - Database? (PostgreSQL/MySQL/MongoDB/SQLite/None)
   - Environment variables? (yes/no)

### Defaults if User Doesn't Specify

If the user doesn't provide specific answers, use these sensible defaults:
- Project Type: Web application
- Tech Stack: Python 3.11+
- Testing: pytest (Python) or Jest (Node.js)
- Docker: No
- CI/CD: None (can add later)
- Database: None initially

## Phase 2: Repository Setup

Based on the user's repository setup response:

### Option A: Create from GitHub Template

If the user wants to create from the template:

1. Guide them to create the repository:
   - Go to https://github.com/symphonycore-org/software-dev-project-template
   - Click "Use this template" → "Create a new repository"
   - Enter repository name and description
   - Choose public/private
   - Click "Create repository"

2. Once created, clone the repository:
   ```bash
   git clone https://github.com/<org>/<project-name>.git
   cd <project-name>
   ```

3. Verify you're in the correct directory:
   ```bash
   pwd
   ls -la
   ```

### Option B: Already Cloned Locally

If the user has already cloned:

1. Navigate to the project directory:
   ```bash
   cd /path/to/project
   ```

2. Verify template structure exists:
   ```bash
   ls -la templates/ docs/ CLAUDE.md README.md TEMPLATE-SETUP.md
   ```

### Option C: Copy Template Locally

If working without GitHub:

1. Copy the template structure to a new directory
2. Initialize git:
   ```bash
   mkdir <project-name>
   cd <project-name>
   git init
   ```

## Phase 3: Tech Stack Initialization

Based on the primary tech stack specified, initialize the appropriate dependencies and configuration files.

### Python Projects

Create the following files:

**1. requirements.txt**
```bash
cat > requirements.txt << 'EOF'
# Core dependencies
pyyaml>=6.0
click>=8.1.0

# Testing
pytest>=7.4
pytest-cov>=4.1
pytest-mock>=3.11

# Code quality
black>=23.0
flake8>=6.0
mypy>=1.5

# Add project-specific dependencies below
EOF
```

**2. pytest.ini**
```bash
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
EOF
```

**3. .env.example** (if environment variables requested)
```bash
cat > .env.example << 'EOF'
# Environment Configuration
# Copy this file to .env and update with your values

# Application
APP_NAME=<project-name>
ENV=development
LOG_LEVEL=INFO

# Database (if applicable)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys (if applicable)
# API_KEY=your_api_key_here

# Other settings
# Add your environment variables here
EOF
```

**4. Update .gitignore**
Add Python-specific entries:
```bash
cat >> .gitignore << 'EOF'

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
.pytest_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/
.mypy_cache/
.env
EOF
```

**5. Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**6. Create initial src structure**
```bash
mkdir -p src/shared
touch src/__init__.py
touch src/shared/__init__.py
touch src/shared/config.py
touch src/shared/utils.py
```

### Node.js/TypeScript Projects

Create the following files:

**1. package.json**
```bash
cat > package.json << 'EOF'
{
  "name": "<project-name>",
  "version": "0.1.0",
  "description": "<project-description>",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/ tests/",
    "format": "prettier --write \"src/**/*.ts\" \"tests/**/*.ts\""
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@types/jest": "^29.5.0",
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.50.0",
    "jest": "^29.7.0",
    "prettier": "^3.0.0",
    "ts-jest": "^29.1.0",
    "ts-node": "^10.9.0",
    "typescript": "^5.2.0"
  },
  "dependencies": {}
}
EOF
```

**2. tsconfig.json**
```bash
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
EOF
```

**3. jest.config.js**
```bash
cat > jest.config.js << 'EOF'
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
EOF
```

**4. .eslintrc.json**
```bash
cat > .eslintrc.json << 'EOF'
{
  "parser": "@typescript-eslint/parser",
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module"
  },
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "off"
  }
}
EOF
```

**5. .prettierrc**
```bash
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
EOF
```

**6. .env.example**
```bash
cat > .env.example << 'EOF'
# Environment Configuration
NODE_ENV=development
PORT=3000
LOG_LEVEL=info

# Database
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys
# API_KEY=your_api_key_here
EOF
```

**7. Update .gitignore**
```bash
cat >> .gitignore << 'EOF'

# Node.js
node_modules/
dist/
build/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env
.DS_Store
coverage/
EOF
```

**8. Install dependencies**
```bash
npm install
```

**9. Create initial src structure**
```bash
mkdir -p src/shared
touch src/index.ts
touch src/shared/config.ts
touch src/shared/utils.ts
```

### Go Projects

**1. Initialize Go module**
```bash
go mod init github.com/<org>/<project-name>
```

**2. Create project structure**
```bash
mkdir -p cmd/<project-name>
mkdir -p internal/app
mkdir -p pkg
mkdir -p tests
```

**3. .env.example**
```bash
cat > .env.example << 'EOF'
# Environment Configuration
ENV=development
PORT=8080
LOG_LEVEL=info

# Database
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
EOF
```

**4. Update .gitignore**
```bash
cat >> .gitignore << 'EOF'

# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
.env
EOF
```

## Phase 4: Customize Template Files

Replace placeholder text and customize template files with project-specific information.

### 1. Update README.md

Replace the following placeholders:
- `[YOUR_PROJECT_NAME]` → actual project name
- Update "Executive Summary" section with project description
- Update "What This Template Provides" → "What This Project Provides"
- Add project-specific tech stack details
- Update installation and usage instructions
- Remove template-specific sections

Use the Edit tool to make these changes.

### 2. Update CLAUDE.md (if needed)

Add project-specific instructions:
- Custom linter/formatter commands for your tech stack
- Project-specific coding standards
- Module organization specific to your project
- Update command placeholders with actual commands:
  - `<test-command>` → actual test command (e.g., `pytest`, `npm test`)
  - `<linter-command>` → actual linter (e.g., `flake8 src/`, `npm run lint`)
  - `<formatter-command>` → actual formatter (e.g., `black src/`, `npm run format`)
  - `<coverage-command>` → coverage command (e.g., `pytest --cov=src`)

### 3. Update TEMPLATE-SETUP.md Status

Mark steps as completed in TEMPLATE-SETUP.md to track progress.

## Phase 5: Generate Initial Documentation

Create initial PRD and Technical Specification documents from the templates.

### 1. Generate Product Requirements Document (PRD)

Read `/templates/prd-template.md` and create a new file `docs/<project-name>-prd.md` with:

- **Project Name**: Fill in actual project name
- **Date**: Current date (YYYY-MM-DD)
- **Owner**: User's name or "TBD"
- **Status**: "Draft"
- **Executive Summary**: Use the project description provided
- **Business Objectives**: Generate 2-3 goals based on project objective
- **User Stories**: Create 1-2 initial epics with stories based on project type
- **Functional Requirements**: List 3-5 initial requirements
- Keep other sections as placeholders to be filled later

### 2. Generate Technical Specification

Read `/templates/technical-spec-template.md` and create `docs/<project-name>-technical-spec.md` with:

- **Project**: Actual project name
- **Date**: Current date
- **Owner**: "Tech Lead" or user's name
- **Status**: "Draft"
- **Related PRD**: Link to the PRD created above
- **Executive Summary**: Technical overview based on project type and tech stack
- **Technology Stack**: Fill in based on user's tech stack choices
- **Module Structure**: Customize the module structure example for the specific tech stack
- **High-Risk Files**: Update file paths to match actual tech stack
- Keep other sections as templates to be completed during architecture design

### 3. Link Documentation

Update `docs/INDEX.md` to include links to the new PRD and technical spec.

## Phase 6: Create start-here.md

Create `start-here.md` in the project root with initial session context:

```markdown
# 🚀 Start Here - Session Context

> **📖 New to this project?** Read [PROCESS-OVERVIEW.md](docs/PROCESS-OVERVIEW.md) first!
> **🤖 Claude Code?** Read [CLAUDE.md](CLAUDE.md) for development guidelines!

---

## 📊 Project Overview

**Project**: <project-name>
**Description**: <project-description>
**Tech Stack**: <primary-tech-stack>
**Status**: ✅ Initial Setup Complete

---

## 📊 Current Work

**Branch**: `main` (or `master`)
**Status**: 🚀 Ready for First Sprint
**Sprint**: Sprint 0 - Initial Setup
**Priority**: P0

**Goal**: Complete initial project setup and plan first sprint

---

## ✅ Setup Completed

### Initial Configuration
1. ✅ Repository created/cloned
2. ✅ Tech stack initialized (<tech-stack>)
3. ✅ Dependencies installed
4. ✅ Configuration files created
5. ✅ Initial documentation generated
6. ✅ Project structure set up

### Files Created/Modified
- `README.md` - Updated with project info
- `requirements.txt` or `package.json` - Dependencies configured
- `pytest.ini` or `jest.config.js` - Test configuration
- `.env.example` - Environment template
- `.gitignore` - Updated for <tech-stack>
- `docs/<project-name>-prd.md` - Initial PRD
- `docs/<project-name>-technical-spec.md` - Initial technical spec
- `src/` - Basic structure created

---

## 🔜 Next Actions

### Immediate Next Steps
1. 🎯 Review and refine PRD (`docs/<project-name>-prd.md`)
2. 🎯 Complete technical architecture design
3. 🎯 Create Sprint 1 plan using `templates/sprint-planning-template.md`
4. 🎯 Break down features into tickets
5. 🎯 Create feature branch for first ticket
6. 🎯 Start development!

### Sprint Planning Guidance
- Review `templates/sprint-planning-template.md`
- Use Claude Cloud (Projects) for architecture and sprint planning
- Use Claude Code CLI for implementation
- Follow the AI-Assisted Agile Process in `docs/ai-assisted-agile-process.md`

---

## 📚 Key Documentation

- **Process**: [AI-Assisted Agile Process](docs/ai-assisted-agile-process.md)
- **Claude Instructions**: [CLAUDE.md](CLAUDE.md)
- **PRD**: [docs/<project-name>-prd.md](docs/<project-name>-prd.md)
- **Technical Spec**: [docs/<project-name>-technical-spec.md](docs/<project-name>-technical-spec.md)

---

## 🛠 Development Commands

### Testing
```bash
<test-command>              # Run all tests
<coverage-command>          # Run with coverage
```

### Code Quality
```bash
<linter-command>            # Run linter
<formatter-command>         # Format code
```

### Development
```bash
# Add project-specific dev commands here
```

---

**📅 Last Updated**: <current-date>
**🔄 Session**: #1 - Initial Setup
**👤 Updated By**: Claude Code (project-setup skill)
```

Replace placeholders:
- `<project-name>` → actual project name
- `<project-description>` → project description
- `<primary-tech-stack>` → e.g., "Python 3.11 + pytest"
- `<tech-stack>` → short name (Python/Node.js/Go)
- `<test-command>` → actual command (pytest/npm test)
- `<coverage-command>` → actual command
- `<linter-command>` → actual command
- `<formatter-command>` → actual command
- `<current-date>` → today's date (YYYY-MM-DD)

## Phase 7: Sprint Planning Assistance (Optional)

Ask the user: "Would you like me to help create an initial Sprint 1 plan now, or would you prefer to do this later with Claude Cloud?"

### If user wants Sprint 1 planning now:

1. Ask for sprint objective: "What is the main objective for Sprint 1?"

2. Ask for initial features: "What are the 3-5 key features you want to build first?"

3. Create `docs/sprint-1-plan.md` using the sprint planning template:
   - Fill in sprint objective
   - Create tickets for each feature
   - Assign priorities (P0, P1, P2)
   - Estimate story points
   - Identify module boundaries
   - List high-risk files
   - Set sprint timeline (suggest 1-2 weeks)

4. Update `start-here.md` to point to Sprint 1 and the first ticket

### If user prefers later:

Add a note in `start-here.md` reminding them to create Sprint 1 plan using Claude Cloud and the sprint planning template.

## Phase 8: Docker Setup (If Requested)

If the user requested Docker support:

### Create Dockerfile

**For Python:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/

# Run application
CMD ["python", "-m", "src.main"]
```

**For Node.js:**
```dockerfile
FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY dist/ ./dist/

# Run application
CMD ["node", "dist/index.js"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"  # Adjust port as needed
    environment:
      - ENV=development
    volumes:
      - .:/app
    # Add database service if needed
```

### Create .dockerignore

```
node_modules/
venv/
.env
.git/
*.pyc
__pycache__/
dist/
coverage/
.pytest_cache/
```

## Phase 9: CI/CD Setup (If Requested)

If the user requested CI/CD setup:

### GitHub Actions (Python)

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --max-line-length=100

    - name: Type check with mypy
      run: |
        mypy src/

    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### GitHub Actions (Node.js)

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'

    - name: Install dependencies
      run: npm ci

    - name: Lint
      run: npm run lint

    - name: Build
      run: npm run build

    - name: Test
      run: npm run test:coverage

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/coverage-final.json
```

## Phase 10: Final Verification & Git Commit

### 1. Verify Setup Checklist

Run through this checklist and report status to user:

- [ ] Dependencies installed successfully
- [ ] Configuration files created
- [ ] Test framework configured
- [ ] Linter/formatter set up
- [ ] `.gitignore` updated
- [ ] Environment template created (`.env.example`)
- [ ] README.md customized
- [ ] Initial documentation generated (PRD, Tech Spec)
- [ ] `start-here.md` created
- [ ] Project structure initialized (`src/`, `tests/`)
- [ ] Docker setup (if requested)
- [ ] CI/CD configured (if requested)

### 2. Run Initial Tests

Verify the setup works:

```bash
# Run tests (should pass with 0 tests or initial tests)
<test-command>

# Run linter (should pass with 0 errors)
<linter-command>

# Check coverage (may be 0% if no tests yet)
<coverage-command>
```

Report any issues to the user.

### 3. Update TEMPLATE-SETUP.md

Mark all completed steps in TEMPLATE-SETUP.md with checkmarks.

### 4. Create Initial Git Commit

Ask user: "Setup is complete! Would you like me to create an initial git commit?"

If yes:

```bash
git add .
git commit -m "chore: Initial project setup from template

- Initialized <tech-stack> project structure
- Configured dependencies and testing framework
- Generated initial PRD and technical specification
- Created start-here.md with session context
- Updated README and project documentation
- Set up <additional-features>

Project ready for Sprint 1 planning."
```

### 5. Push to Remote (Optional)

Ask user: "Would you like me to push this to the remote repository?"

If yes:

```bash
git push -u origin main  # or master
```

## Phase 11: Summary & Next Steps

Provide the user with a comprehensive summary:

```
✅ Project Setup Complete!

📦 What was created:
- Project structure initialized (<tech-stack>)
- Dependencies configured: <list-main-deps>
- Testing framework: <test-framework>
- Code quality tools: <linter>, <formatter>
- Documentation: PRD, Technical Spec, start-here.md
- <Additional features installed>

📁 Key Files:
- README.md - Project overview
- CLAUDE.md - Development guidelines
- start-here.md - Session context (always check this first!)
- docs/<project-name>-prd.md - Product requirements
- docs/<project-name>-technical-spec.md - Technical architecture
- <tech-stack config files>

🎯 Immediate Next Steps:
1. Review and refine the PRD (docs/<project-name>-prd.md)
2. Complete architecture design in Technical Spec
3. Create Sprint 1 plan using templates/sprint-planning-template.md
4. Start development!

🤖 Pro Tips:
- Always read start-here.md at the beginning of each session
- Use Claude Cloud (Projects) for architecture & sprint planning
- Use Claude Code CLI for implementation & testing
- Follow the AI-Assisted Agile Process (docs/ai-assisted-agile-process.md)
- Maintain ≥80% test coverage
- Keep modules isolated for parallel development

📚 Documentation:
- Process Overview: docs/PROCESS-OVERVIEW.md
- Full Process: docs/ai-assisted-agile-process.md
- Best Practices: docs/parallel-sprint-development-best-practices.md

🚀 You're ready to start building!
```

## Error Handling & Troubleshooting

### Common Issues

**1. Dependencies Installation Failed**
- Check internet connection
- Verify package manager installed (pip/npm/go)
- Check Python/Node.js version compatibility
- Try manual installation: `pip install -r requirements.txt` or `npm install`

**2. Git Operations Failed**
- Verify git is installed: `git --version`
- Check git credentials configured: `git config user.name` and `git config user.email`
- Verify remote repository exists and accessible
- Check branch name (main vs master)

**3. Template Files Not Found**
- Verify you're in correct directory: `pwd`
- Check template structure exists: `ls templates/`
- Ensure template was cloned correctly
- Verify file permissions: `ls -la`

**4. Tests Not Running**
- Check test framework installed correctly
- Verify test configuration file (pytest.ini, jest.config.js)
- Check test file naming conventions
- Ensure test directory exists: `ls tests/`

**5. Permission Denied**
- Check file/directory permissions: `ls -la`
- May need to make scripts executable: `chmod +x scripts/*.sh`
- Check user has write permissions in directory

### Rollback Steps

If setup fails midway:
1. Note what was successfully completed
2. Keep successful changes
3. Fix the specific issue
4. Resume from failed step
5. Don't start over unless necessary

## Skill Completion

Once all phases are complete:
1. ✅ Mark TEMPLATE-SETUP.md tasks as complete
2. ✅ Create git commit with all changes
3. ✅ Optionally push to remote
4. ✅ Display summary and next steps
5. ✅ Update start-here.md with final status

The project is now ready for development! 🎉
