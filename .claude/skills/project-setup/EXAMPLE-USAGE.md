# Project Setup Skill - Example Usage

This document shows real-world examples of using the project-setup skill.

## Example 1: Python FastAPI REST API

### User Request
```
I want to create a new Python FastAPI project called "user-service" for a REST API
that handles user authentication and profile management. Include PostgreSQL support
and Docker.
```

### Skill Interaction

**Phase 1: Confirmation**
```
Claude: I'll use the project-setup skill to set up your project! Let me confirm the details:

1. Project Name: user-service
2. Project Description: REST API for user authentication and profile management
3. Project Type: REST API service
4. Primary Tech Stack: Python 3.11+ with FastAPI
5. Database: PostgreSQL
6. Docker: Yes

Is this correct? (yes/no)
```

**Phase 2: Additional Questions**
```
Claude: A few more questions:

6. Testing Framework: pytest (recommended for Python)? (yes/other)
7. Repository Setup: Should I guide you to create from GitHub template, or is it already cloned?
8. CI/CD: Would you like GitHub Actions CI/CD setup? (yes/no)
9. Initial Sprint Planning: Create Sprint 1 plan now or later? (now/later)
```

**User Response:**
```
Yes to all defaults, already cloned the repo, yes to GitHub Actions, later for sprint planning.
```

### What Gets Created

**Files Created:**
```
user-service/
├── requirements.txt          # FastAPI, SQLAlchemy, psycopg2, pytest, etc.
├── pytest.ini               # Test configuration
├── .env.example            # DATABASE_URL, SECRET_KEY, etc.
├── .gitignore              # Updated for Python
├── Dockerfile              # Python 3.11 container
├── docker-compose.yml      # App + PostgreSQL services
├── .dockerignore
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── middleware/
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── shared/
│       ├── __init__.py
│       ├── config.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   └── fixtures/
├── docs/
│   ├── user-service-prd.md           # Generated PRD
│   └── user-service-technical-spec.md # Generated Tech Spec
├── start-here.md                      # Session context
└── README.md                          # Updated with project info
```

**start-here.md Content:**
```markdown
# 🚀 Start Here - Session Context

## 📊 Project Overview

**Project**: user-service
**Description**: REST API for user authentication and profile management
**Tech Stack**: Python 3.11 + FastAPI + PostgreSQL
**Status**: ✅ Initial Setup Complete

## 🔜 Next Actions

1. 🎯 Review and refine PRD (docs/user-service-prd.md)
2. 🎯 Complete technical architecture design
3. 🎯 Create Sprint 1 plan
4. 🎯 Implement user authentication endpoints
5. 🎯 Set up database migrations

## 🛠 Development Commands

### Testing
```bash
pytest --cov=src              # Run tests with coverage
pytest -v                     # Verbose output
```

### Code Quality
```bash
flake8 src/ tests/            # Lint
black src/ tests/             # Format
mypy src/                     # Type check
```

### Docker
```bash
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose logs -f        # View logs
```
```

**Initial Commit Message:**
```
chore: Initial project setup from template

- Initialized Python 3.11 + FastAPI project structure
- Configured pytest testing framework with 80% coverage threshold
- Generated initial PRD and technical specification
- Created start-here.md with session context
- Updated README and project documentation
- Set up Docker with PostgreSQL database
- Configured GitHub Actions CI/CD pipeline

Project ready for Sprint 1 planning.
```

---

## Example 2: Node.js CLI Tool

### User Request
```
Set up a TypeScript CLI tool called "deploy-helper" that automates deployment
tasks. No database needed.
```

### Skill Interaction

**Gathered Info:**
- Project Name: deploy-helper
- Project Type: CLI tool
- Tech Stack: Node.js 20 + TypeScript
- Testing: Jest
- Database: None
- Docker: No (CLI tools typically don't need it)
- CI/CD: GitHub Actions

### What Gets Created

**Files Created:**
```
deploy-helper/
├── package.json              # Commander, chalk, inquirer, TypeScript
├── tsconfig.json            # TypeScript config
├── jest.config.js           # Test config
├── .eslintrc.json          # ESLint rules
├── .prettierrc             # Prettier config
├── .gitignore              # Node.js patterns
├── .github/workflows/ci.yml
├── src/
│   ├── index.ts            # Entry point
│   ├── commands/           # Command implementations
│   │   ├── deploy.ts
│   │   ├── rollback.ts
│   │   └── status.ts
│   ├── cli/                # CLI framework
│   │   └── parser.ts
│   └── utils/
│       ├── logger.ts
│       └── config.ts
├── tests/
│   ├── commands/
│   └── utils/
├── docs/
│   ├── deploy-helper-prd.md
│   └── deploy-helper-technical-spec.md
└── start-here.md
```

**package.json Scripts:**
```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/ tests/",
    "format": "prettier --write \"src/**/*.ts\" \"tests/**/*.ts\""
  }
}
```

---

## Example 3: Go Microservice

### User Request
```
Create a Go microservice called "notification-service" for sending notifications
via email and SMS. Include Docker and Kubernetes manifests.
```

### Skill Interaction

**Gathered Info:**
- Project Name: notification-service
- Project Type: Microservice
- Tech Stack: Go 1.21
- Framework: Gin
- Testing: Go testing + testify
- Database: PostgreSQL (for notification queue)
- Docker: Yes
- Kubernetes: Yes (additional request)

### What Gets Created

**Files Created:**
```
notification-service/
├── go.mod
├── go.sum
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── k8s/                    # Kubernetes manifests (if requested)
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── cmd/
│   └── notification-service/
│       └── main.go
├── internal/
│   ├── app/
│   │   ├── handlers/
│   │   │   ├── email.go
│   │   │   └── sms.go
│   │   ├── services/
│   │   │   ├── email_service.go
│   │   │   └── sms_service.go
│   │   └── models/
│   │       └── notification.go
│   └── config/
│       └── config.go
├── pkg/
│   └── middleware/
│       ├── auth.go
│       └── logging.go
├── tests/
│   ├── integration/
│   └── unit/
├── docs/
│   ├── notification-service-prd.md
│   └── notification-service-technical-spec.md
└── start-here.md
```

**go.mod (after setup):**
```go
module github.com/your-org/notification-service

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    gorm.io/gorm v1.25.5
    gorm.io/driver/postgres v1.5.4
    github.com/joho/godotenv v1.5.1
    github.com/stretchr/testify v1.8.4
)
```

---

## Example 4: Data Pipeline

### User Request
```
Set up a Python data pipeline called "analytics-pipeline" that processes
user analytics data. Include Apache Airflow setup.
```

### Skill Interaction

**Special Requirements:**
- Project Type: Data Pipeline
- Tech Stack: Python 3.11
- Framework: Pandas + Apache Airflow
- Testing: pytest
- Docker: Yes (for Airflow)
- Database: PostgreSQL (Airflow metadata + data warehouse)

### What Gets Created

**Files Created:**
```
analytics-pipeline/
├── requirements.txt         # Pandas, Airflow, SQLAlchemy, pytest
├── pytest.ini
├── .env.example
├── docker-compose.yml       # Airflow services
├── Dockerfile
├── dags/                    # Airflow DAGs
│   ├── __init__.py
│   └── analytics_dag.py
├── src/
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── api_extractor.py
│   │   └── database_extractor.py
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── aggregator.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── warehouse_loader.py
│   ├── validators/
│   │   ├── __init__.py
│   │   └── schema_validator.py
│   └── shared/
│       ├── config.py
│       └── utils.py
├── tests/
│   ├── test_extractors/
│   ├── test_transformers/
│   └── test_loaders/
├── docs/
│   ├── analytics-pipeline-prd.md
│   └── analytics-pipeline-technical-spec.md
└── start-here.md
```

**requirements.txt (excerpt):**
```
# Core
pandas>=2.1.0
numpy>=1.26.0
apache-airflow>=2.7.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Data validation
great-expectations>=0.18.0

# Testing
pytest>=7.4
pytest-cov>=4.1
```

---

## Example 5: Full-Stack Web App

### User Request
```
Create a full-stack task management app called "taskflow" with Express backend
and React frontend. Include authentication and real-time updates.
```

### Skill Interaction

**Special Setup:**
- Monorepo structure
- Backend: Express + TypeScript + PostgreSQL
- Frontend: React + TypeScript + Vite
- Real-time: Socket.io
- Auth: JWT
- Docker: Yes (all services)

### What Gets Created

**Files Created:**
```
taskflow/
├── package.json             # Root monorepo config
├── docker-compose.yml       # All services
├── .gitignore
├── backend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── jest.config.js
│   ├── src/
│   │   ├── index.ts
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── controllers/
│   │   ├── websockets/
│   │   │   └── task-events.ts
│   │   ├── auth/
│   │   │   ├── jwt.ts
│   │   │   └── middleware.ts
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── hooks/
│   ├── public/
│   └── Dockerfile
├── shared/                  # Shared types
│   └── types.ts
├── docs/
│   ├── taskflow-prd.md
│   └── taskflow-technical-spec.md
└── start-here.md
```

**Root package.json:**
```json
{
  "name": "taskflow",
  "private": true,
  "workspaces": [
    "backend",
    "frontend"
  ],
  "scripts": {
    "dev": "concurrently \"npm run dev -w backend\" \"npm run dev -w frontend\"",
    "test": "npm run test -w backend && npm run test -w frontend",
    "build": "npm run build -w backend && npm run build -w frontend"
  }
}
```

---

## Example 6: Sprint Planning Integration

### User Request
```
Set up a Python FastAPI project called "inventory-api" and help me plan Sprint 1
to implement basic CRUD operations.
```

### Enhanced Flow

After setup completes, skill asks:

```
Claude: Setup complete! Would you like me to help create an initial Sprint 1 plan now? (yes/no)

User: Yes

Claude: Great! What is the main objective for Sprint 1?

User: Implement CRUD operations for inventory items

Claude: What are the 3-5 key features you want to build first?

User:
1. Create inventory item
2. Get inventory item by ID
3. List all inventory items
4. Update inventory item
5. Delete inventory item
```

**Skill Creates:** `docs/sprint-1-plan.md`

```markdown
# Sprint 1 Plan: Inventory CRUD Operations

**Sprint Objective:** Implement CRUD operations for inventory items

**Duration:** 2 weeks
**Start Date:** 2025-11-23
**End Date:** 2025-12-07

## Tickets

### TICKET-001: Create Inventory Item Endpoint (P0) - 5 points
**Module:** `src/api/inventory/`

**Requirements:**
- POST /api/v1/inventory endpoint
- Request validation (name, quantity, price)
- Database persistence
- Return created item with ID

**High-Risk Files:**
- src/main.py (registration)
- src/shared/validators.py (validation pipeline)

### TICKET-002: Get Inventory Item Endpoint (P0) - 3 points
**Module:** `src/api/inventory/`

**Requirements:**
- GET /api/v1/inventory/:id endpoint
- 404 handling for not found
- Return item details

### TICKET-003: List Inventory Items Endpoint (P0) - 5 points
**Module:** `src/api/inventory/`

**Requirements:**
- GET /api/v1/inventory endpoint
- Pagination support
- Filter by category (optional)
- Return list of items

### TICKET-004: Update Inventory Item Endpoint (P1) - 5 points
**Module:** `src/api/inventory/`

**Requirements:**
- PUT /api/v1/inventory/:id endpoint
- Partial update support
- Validation
- Return updated item

### TICKET-005: Delete Inventory Item Endpoint (P1) - 3 points
**Module:** `src/api/inventory/`

**Requirements:**
- DELETE /api/v1/inventory/:id endpoint
- Soft delete or hard delete (decide)
- Return 204 No Content

**Total Story Points:** 21
```

**Updates start-here.md:**

```markdown
## 📊 Current Work

**Sprint**: Sprint 1 - Inventory CRUD Operations
**Current Ticket**: TICKET-001
**Branch**: feature/TICKET-001-create-inventory-endpoint
**Status**: 🚀 Ready to Start

**Sprint Plan:** [docs/sprint-1-plan.md](docs/sprint-1-plan.md)
```

---

## Common Patterns

### Pattern 1: Minimal Information
```
"Set up a Python project called 'my-app'"
```
Skill will ask for all missing information.

### Pattern 2: Complete Information
```
"Create a Node.js TypeScript REST API called 'user-service' with Express,
PostgreSQL, Jest testing, Docker, and GitHub Actions CI/CD"
```
Skill will confirm and proceed with minimal questions.

### Pattern 3: Iterative Refinement
```
User: "Set up a web app"
Claude: What type of web app? Full-stack, SPA, or backend API?
User: Full-stack with React and Express
Claude: Great! What's the project name?
User: "team-portal"
```

---

## Validation After Setup

After skill completes, always run:

```bash
# Validate setup
./.claude/skills/project-setup/scripts/validate-setup.sh

# Verify dependencies installed
python -m pytest --version  # or npm test
```

---

## Tips for Best Results

1. **Be Specific:** Include project type, tech stack, and key features
2. **Mention Optional Features:** Docker, CI/CD, databases up front
3. **Sprint Planning:** Decide if you want it now or later
4. **Review Generated Docs:** PRD and Tech Spec need refinement
5. **Run Validation:** Use helper scripts to verify setup

---

## Next Steps After Setup

Regardless of project type:

1. ✅ Review `start-here.md`
2. ✅ Refine PRD in `docs/`
3. ✅ Complete Technical Spec
4. ✅ Create/review Sprint 1 plan
5. ✅ Create feature branch: `git checkout -b feature/TICKET-001-description`
6. ✅ Start implementing!

Happy coding! 🚀
