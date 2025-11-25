# Project Types Guide

This guide helps determine the right configuration for different project types.

## 1. Web Application (Full-Stack)

**Characteristics:**
- Frontend + Backend + Database
- User interface required
- API endpoints
- Data persistence

**Recommended Stack:**
- **Python**: FastAPI/Flask + React/Vue + PostgreSQL
- **Node.js**: Express/NestJS + React/Vue + PostgreSQL
- **Go**: Gin/Echo + React/Vue + PostgreSQL

**Initial Features:**
- User authentication
- CRUD operations
- API documentation
- Database migrations

**Directory Structure:**
```
src/
├── api/           # API routes and handlers
├── models/        # Data models
├── services/      # Business logic
├── middleware/    # Auth, logging, etc.
└── frontend/      # UI components (if monorepo)
```

## 2. REST API Service

**Characteristics:**
- Backend only
- Exposes REST endpoints
- Data processing
- Integration with other services

**Recommended Stack:**
- **Python**: FastAPI (recommended), Flask, Django REST
- **Node.js**: Express, NestJS, Fastify
- **Go**: Gin, Echo, Chi

**Initial Features:**
- API routing
- Request validation
- Error handling
- API documentation (OpenAPI/Swagger)
- Authentication/Authorization

**Directory Structure:**
```
src/
├── api/
│   ├── routes/       # Route definitions
│   ├── handlers/     # Request handlers
│   └── middleware/   # Middleware
├── models/           # Data models
├── services/         # Business logic
├── repositories/     # Data access layer
└── utils/           # Utilities
```

## 3. CLI Tool

**Characteristics:**
- Command-line interface
- Terminal-based interaction
- Automation scripts
- System operations

**Recommended Stack:**
- **Python**: Click, Typer, argparse
- **Node.js**: Commander.js, yargs, oclif
- **Go**: Cobra, urfave/cli

**Initial Features:**
- Command parsing
- Subcommands
- Help documentation
- Configuration file support
- Output formatting

**Directory Structure:**
```
src/
├── commands/      # Command implementations
├── cli/           # CLI framework setup
├── core/          # Core functionality
├── utils/         # Utilities
└── config/        # Configuration
```

## 4. Data Pipeline

**Characteristics:**
- Data ingestion
- Data transformation (ETL/ELT)
- Data storage
- Scheduled jobs

**Recommended Stack:**
- **Python**: Pandas, Apache Airflow, Luigi
- **Node.js**: Bull, Agenda, node-cron
- **Go**: Temporal, Asynq

**Initial Features:**
- Data extraction
- Data validation
- Transformation logic
- Error handling and retry
- Monitoring and logging

**Directory Structure:**
```
src/
├── extractors/    # Data sources
├── transformers/  # Transformation logic
├── loaders/       # Data sinks
├── validators/    # Data validation
├── pipelines/     # Pipeline orchestration
└── utils/        # Utilities
```

## 5. Library/Package

**Characteristics:**
- Reusable code
- Published to package registry (PyPI, npm, etc.)
- API for other developers
- Documentation-heavy

**Recommended Stack:**
- **Python**: setuptools, poetry
- **Node.js**: npm, TypeScript
- **Go**: Go modules

**Initial Features:**
- Core API
- Example usage
- API documentation
- Tests with high coverage
- Version management

**Directory Structure:**
```
src/
├── core/          # Core functionality
├── utils/         # Utilities
├── types/         # Type definitions
└── __init__.py    # Package exports
examples/          # Usage examples
docs/             # API documentation
```

## 6. Mobile App Backend

**Characteristics:**
- API for mobile apps (iOS/Android)
- Real-time features
- Push notifications
- Authentication

**Recommended Stack:**
- **Python**: FastAPI + WebSockets
- **Node.js**: Express + Socket.io
- **Go**: Gin + WebSockets

**Initial Features:**
- User authentication (JWT)
- RESTful endpoints
- Real-time messaging (WebSockets)
- File uploads
- Push notification service

**Directory Structure:**
```
src/
├── api/           # REST endpoints
├── websockets/    # Real-time features
├── auth/          # Authentication
├── notifications/ # Push notifications
├── models/        # Data models
└── services/      # Business logic
```

## 7. Microservice

**Characteristics:**
- Single responsibility
- Part of larger system
- Service-to-service communication
- Containerized deployment

**Recommended Stack:**
- **Python**: FastAPI, Flask
- **Node.js**: Express, NestJS
- **Go**: Gin, Echo (ideal for microservices)

**Initial Features:**
- Service API
- Health checks
- Metrics endpoint
- Service discovery
- Circuit breaker

**Directory Structure:**
```
src/
├── api/           # Service endpoints
├── models/        # Data models
├── services/      # Business logic
├── clients/       # External service clients
├── health/        # Health checks
└── metrics/       # Monitoring
```

## Mapping to Tech Stack

### Python Projects
**Best For:**
- Data pipelines
- ML/AI applications
- REST APIs
- CLI tools
- Backend services

**Key Dependencies:**
- FastAPI (APIs)
- Click/Typer (CLI)
- Pandas (data processing)
- SQLAlchemy (database)
- Pydantic (validation)

### Node.js/TypeScript Projects
**Best For:**
- Full-stack web apps
- REST APIs
- Real-time applications
- Microservices
- CLI tools

**Key Dependencies:**
- Express/NestJS (APIs)
- Prisma/TypeORM (database)
- Socket.io (real-time)
- Commander (CLI)
- Jest (testing)

### Go Projects
**Best For:**
- High-performance APIs
- Microservices
- CLI tools
- System tools
- Distributed systems

**Key Dependencies:**
- Gin/Echo (APIs)
- GORM (database)
- Cobra (CLI)
- Testify (testing)

## Decision Matrix

| Requirement | Python | Node.js | Go |
|-------------|--------|---------|-----|
| High performance | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Quick development | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Data processing | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Real-time features | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Microservices | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ML/AI | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Full-stack web | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| CLI tools | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Questions to Help Decide

1. **What is the primary function?**
   - Serve API → REST API Service or Mobile Backend
   - Process data → Data Pipeline
   - User interface → Web Application
   - Terminal commands → CLI Tool
   - Reusable code → Library/Package

2. **What are the performance requirements?**
   - Very high → Go
   - Moderate to high → Node.js or Go
   - Standard → Python, Node.js, or Go

3. **What's the team's expertise?**
   - Python developers → Python
   - JavaScript developers → Node.js
   - Systems programming → Go

4. **What are the scaling needs?**
   - Massive scale → Go or Node.js
   - Moderate scale → Any
   - Small scale → Any

5. **Is real-time communication needed?**
   - Yes → Node.js (Socket.io) or Go (WebSockets)
   - No → Any

6. **Does it involve ML/AI?**
   - Yes → Python
   - No → Any
