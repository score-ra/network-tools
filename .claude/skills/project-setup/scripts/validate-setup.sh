#!/bin/bash

# validate-setup.sh
# Validates that the project setup is complete and correct

set -e

echo "🔍 Validating project setup..."
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} Found: $1"
        return 0
    else
        echo -e "${RED}✗${NC} Missing: $1"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Function to check if a directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} Found directory: $1"
        return 0
    else
        echo -e "${RED}✗${NC} Missing directory: $1"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Function to check if a command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        VERSION=$($1 --version 2>&1 | head -n 1 || echo "version unknown")
        echo -e "${GREEN}✓${NC} Found command: $1 ($VERSION)"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} Missing command: $1"
        WARNINGS=$((WARNINGS + 1))
        return 1
    fi
}

# Function to check if string exists in file
check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $1 contains expected content"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1 may need customization"
        WARNINGS=$((WARNINGS + 1))
        return 1
    fi
}

echo "📁 Checking directory structure..."
check_dir "src"
check_dir "tests"
check_dir "docs"
check_dir "templates"
check_dir "config"
echo ""

echo "📄 Checking core template files..."
check_file "README.md"
check_file "CLAUDE.md"
check_file "TEMPLATE-SETUP.md"
check_file ".gitignore"
echo ""

echo "📋 Checking documentation..."
check_file "docs/INDEX.md"
check_file "docs/PROCESS-OVERVIEW.md"
check_file "docs/ai-assisted-agile-process.md"
check_file "docs/parallel-sprint-development-best-practices.md"
echo ""

echo "📝 Checking templates..."
check_file "templates/prd-template.md"
check_file "templates/technical-spec-template.md"
check_file "templates/sprint-planning-template.md"
check_file "templates/pr-template.md"
echo ""

echo "🔧 Checking tech stack configuration..."

# Detect tech stack
if [ -f "requirements.txt" ] && [ -f "pytest.ini" ]; then
    echo "Detected: Python project"
    check_file "requirements.txt"
    check_file "pytest.ini"
    check_command "python3"
    check_command "pip"

    # Check if venv exists
    if [ -d "venv" ]; then
        echo -e "${GREEN}✓${NC} Virtual environment found"
    else
        echo -e "${YELLOW}⚠${NC} Virtual environment not found (create with: python3 -m venv venv)"
        WARNINGS=$((WARNINGS + 1))
    fi

elif [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
    echo "Detected: Node.js/TypeScript project"
    check_file "package.json"
    check_file "tsconfig.json"
    check_command "node"
    check_command "npm"

    # Check if node_modules exists
    if [ -d "node_modules" ]; then
        echo -e "${GREEN}✓${NC} Dependencies installed (node_modules found)"
    else
        echo -e "${YELLOW}⚠${NC} Dependencies not installed (run: npm install)"
        WARNINGS=$((WARNINGS + 1))
    fi

elif [ -f "go.mod" ]; then
    echo "Detected: Go project"
    check_file "go.mod"
    check_command "go"

else
    echo -e "${YELLOW}⚠${NC} Tech stack not yet initialized"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

echo "🎯 Checking session context..."
if check_file "start-here.md"; then
    # Check if it's been customized
    if grep -q "\[YOUR_PROJECT_NAME\]" "start-here.md" || grep -q "<project-name>" "start-here.md"; then
        echo -e "${YELLOW}⚠${NC} start-here.md contains placeholders - needs customization"
        WARNINGS=$((WARNINGS + 1))
    fi
fi
echo ""

echo "📊 Checking for customization..."
if [ -f "README.md" ]; then
    if grep -q "\[YOUR_PROJECT_NAME\]" "README.md"; then
        echo -e "${YELLOW}⚠${NC} README.md still contains [YOUR_PROJECT_NAME] placeholder"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}✓${NC} README.md has been customized"
    fi
fi
echo ""

echo "🔐 Checking git configuration..."
check_command "git"

if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"

    # Check if there are commits
    if git rev-parse HEAD &>/dev/null; then
        COMMIT_COUNT=$(git rev-list --count HEAD)
        echo -e "${GREEN}✓${NC} Repository has $COMMIT_COUNT commit(s)"
    else
        echo -e "${YELLOW}⚠${NC} No commits yet"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Check git config
    if git config user.name &>/dev/null && git config user.email &>/dev/null; then
        echo -e "${GREEN}✓${NC} Git user configured"
    else
        echo -e "${YELLOW}⚠${NC} Git user not configured (set with: git config user.name and user.email)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}✗${NC} Git repository not initialized"
    ERRORS=$((ERRORS + 1))
fi
echo ""

echo "🧪 Checking optional features..."
if [ -f "Dockerfile" ]; then
    echo -e "${GREEN}✓${NC} Docker support configured"
else
    echo -e "${YELLOW}ℹ${NC} Docker not configured (optional)"
fi

if [ -d ".github/workflows" ]; then
    echo -e "${GREEN}✓${NC} GitHub Actions CI/CD configured"
elif [ -d ".gitlab-ci.yml" ]; then
    echo -e "${GREEN}✓${NC} GitLab CI configured"
else
    echo -e "${YELLOW}ℹ${NC} CI/CD not configured (optional)"
fi

if [ -f ".env.example" ]; then
    echo -e "${GREEN}✓${NC} Environment template (.env.example) exists"
    if [ -f ".env" ]; then
        echo -e "${YELLOW}⚠${NC} .env file exists - ensure it's in .gitignore!"
        if ! grep -q "^\.env$" ".gitignore" 2>/dev/null; then
            echo -e "${RED}✗${NC} .env is NOT in .gitignore - SECURITY RISK!"
            ERRORS=$((ERRORS + 1))
        fi
    fi
else
    echo -e "${YELLOW}ℹ${NC} No .env.example (may not be needed)"
fi
echo ""

echo "=========================================="
echo "📊 Validation Summary"
echo "=========================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Perfect! Setup is complete and valid.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Setup mostly complete with $WARNINGS warning(s).${NC}"
    echo "Review warnings above and address as needed."
    exit 0
else
    echo -e "${RED}❌ Setup incomplete: $ERRORS error(s), $WARNINGS warning(s)${NC}"
    echo "Please fix errors above before proceeding."
    exit 1
fi
