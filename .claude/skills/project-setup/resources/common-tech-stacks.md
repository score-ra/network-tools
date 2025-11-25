# Common Tech Stack Configurations

Quick reference for popular tech stack combinations.

## Python Stacks

### Python + FastAPI + PostgreSQL
**Use Case:** Modern REST APIs, microservices, data-driven apps

**Dependencies (requirements.txt):**
```
# Core
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
python-dotenv>=1.0.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
alembic>=1.12.0

# Testing
pytest>=7.4
pytest-cov>=4.1
pytest-asyncio>=0.21.0
httpx>=0.25.0

# Code quality
black>=23.0
flake8>=6.0
mypy>=1.5
```

**Commands:**
```bash
# Test
pytest --cov=src

# Lint
flake8 src/ tests/

# Format
black src/ tests/

# Type check
mypy src/

# Run dev server
uvicorn src.main:app --reload
```

---

### Python + Flask + SQLite
**Use Case:** Simple web apps, prototypes, small tools

**Dependencies:**
```
# Core
flask>=3.0.0
flask-sqlalchemy>=3.1.0
python-dotenv>=1.0.0

# Testing
pytest>=7.4
pytest-cov>=4.1
pytest-flask>=1.3.0

# Code quality
black>=23.0
flake8>=6.0
```

**Commands:**
```bash
# Test
pytest --cov=src

# Lint
flake8 src/

# Format
black src/

# Run dev server
flask run --debug
```

---

### Python + Click (CLI)
**Use Case:** Command-line tools, automation scripts

**Dependencies:**
```
# Core
click>=8.1.0
rich>=13.6.0
pyyaml>=6.0

# Testing
pytest>=7.4
pytest-cov>=4.1

# Code quality
black>=23.0
flake8>=6.0
```

**Commands:**
```bash
# Test
pytest --cov=src

# Lint
flake8 src/

# Format
black src/

# Run CLI
python -m src.cli
```

---

### Python + Pandas (Data Pipeline)
**Use Case:** Data processing, ETL, analytics

**Dependencies:**
```
# Core
pandas>=2.1.0
numpy>=1.26.0
sqlalchemy>=2.0.0

# Optional
pyarrow>=14.0.0
openpyxl>=3.1.0

# Testing
pytest>=7.4
pytest-cov>=4.1

# Code quality
black>=23.0
flake8>=6.0
```

---

## Node.js/TypeScript Stacks

### Node.js + Express + TypeScript + PostgreSQL
**Use Case:** REST APIs, web backends, microservices

**package.json:**
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "pg": "^8.11.0",
    "dotenv": "^16.3.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.20",
    "@types/node": "^20.9.0",
    "@types/pg": "^8.10.0",
    "typescript": "^5.2.0",
    "ts-node": "^10.9.0",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.0",
    "ts-jest": "^29.1.0",
    "eslint": "^8.53.0",
    "@typescript-eslint/parser": "^6.11.0",
    "@typescript-eslint/eslint-plugin": "^6.11.0",
    "prettier": "^3.1.0"
  }
}
```

**Commands:**
```bash
# Test
npm test

# Lint
npm run lint

# Format
npm run format

# Build
npm run build

# Run dev
npm run dev
```

---

### Node.js + NestJS + TypeScript
**Use Case:** Enterprise applications, microservices, scalable APIs

**Installation:**
```bash
npm i -g @nestjs/cli
nest new project-name
```

**Key Dependencies:**
```bash
npm install @nestjs/core @nestjs/common rxjs reflect-metadata
npm install --save-dev @nestjs/testing jest
```

---

### Node.js + Commander (CLI)
**Use Case:** CLI tools, automation, developer tools

**package.json:**
```json
{
  "dependencies": {
    "commander": "^11.1.0",
    "chalk": "^5.3.0",
    "inquirer": "^9.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.9.0",
    "typescript": "^5.2.0",
    "jest": "^29.7.0"
  }
}
```

---

## Go Stacks

### Go + Gin + PostgreSQL
**Use Case:** High-performance APIs, microservices

**go.mod (after init):**
```bash
go get -u github.com/gin-gonic/gin
go get -u gorm.io/gorm
go get -u gorm.io/driver/postgres
go get -u github.com/joho/godotenv
go get -u github.com/stretchr/testify
```

**Project Structure:**
```
cmd/
  app/
    main.go
internal/
  app/
    handlers/
    models/
    services/
pkg/
  database/
  middleware/
```

**Commands:**
```bash
# Test
go test ./...

# Build
go build -o bin/app cmd/app/main.go

# Run
./bin/app

# Test with coverage
go test -cover ./...
```

---

### Go + Cobra (CLI)
**Use Case:** CLI tools, system utilities

**Installation:**
```bash
go get -u github.com/spf13/cobra/cobra
cobra init
cobra add command-name
```

**Commands:**
```bash
# Test
go test ./...

# Build
go build -o bin/app

# Run
./bin/app
```

---

## Full-Stack Stacks

### React + Node.js + PostgreSQL
**Backend (Express + TypeScript):**
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "pg": "^8.11.0",
    "cors": "^2.8.5"
  }
}
```

**Frontend (React + TypeScript):**
```bash
npx create-react-app frontend --template typescript
```

**Monorepo Structure:**
```
project/
├── backend/
│   ├── src/
│   ├── tests/
│   └── package.json
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── package.json (root)
```

---

### Python + FastAPI + React
**Backend:**
```
FastAPI + SQLAlchemy + Alembic
```

**Frontend:**
```bash
npx create-react-app frontend --template typescript
```

**Directory Structure:**
```
project/
├── backend/
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── docker-compose.yml
```

---

## Testing Framework Choices

### Python
- **pytest** (recommended) - Most popular, plugin ecosystem
- **unittest** - Built-in, Java-like syntax
- **nose2** - Extends unittest

### Node.js
- **Jest** (recommended) - All-in-one, great DX
- **Mocha** - Flexible, requires more setup
- **Vitest** - Modern, fast, Vite integration

### Go
- **testing** (built-in) - Standard library
- **testify** - Assertions and mocking
- **Ginkgo** - BDD-style

---

## Code Quality Tools

### Python
```bash
# Linting
flake8 src/

# Formatting
black src/

# Type checking
mypy src/

# Import sorting
isort src/
```

### Node.js/TypeScript
```bash
# Linting
eslint src/

# Formatting
prettier --write src/

# Type checking
tsc --noEmit
```

### Go
```bash
# Formatting
go fmt ./...

# Linting
golangci-lint run

# Vetting
go vet ./...
```

---

## Environment Variables

### Python (.env.example)
```bash
# Application
ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# Server
HOST=0.0.0.0
PORT=8000
```

### Node.js (.env.example)
```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API
API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_here

# CORS
CORS_ORIGIN=http://localhost:3000
```

### Go (.env.example)
```bash
# Application
ENV=development
PORT=8080
LOG_LEVEL=info

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=dbname

# API
API_KEY=your_api_key_here
```
