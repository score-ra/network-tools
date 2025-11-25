#!/bin/bash

# detect-tech-stack.sh
# Detects the current tech stack or helps determine what to use

set -e

echo "🔍 Detecting project tech stack..."
echo ""

DETECTED=""

# Check for Python
if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    DETECTED="python"
    echo "✓ Python project detected"

    if command -v python3 &> /dev/null; then
        VERSION=$(python3 --version)
        echo "  Python version: $VERSION"
    else
        echo "  ⚠ Python not installed"
    fi

    if [ -f "requirements.txt" ]; then
        COUNT=$(wc -l < requirements.txt | tr -d ' ')
        echo "  Dependencies: $COUNT packages in requirements.txt"
    fi

    if [ -f "pytest.ini" ] || grep -q "pytest" requirements.txt 2>/dev/null; then
        echo "  Testing: pytest"
    fi

    if [ -d "venv" ] || [ -d ".venv" ] || [ -d "env" ]; then
        echo "  Virtual environment: present"
    else
        echo "  Virtual environment: not found"
    fi
fi

# Check for Node.js
if [ -f "package.json" ]; then
    DETECTED="nodejs"
    echo "✓ Node.js project detected"

    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo "  Node version: $NODE_VERSION"
    else
        echo "  ⚠ Node.js not installed"
    fi

    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        echo "  npm version: $NPM_VERSION"
    fi

    if [ -f "tsconfig.json" ]; then
        echo "  Language: TypeScript"
    else
        echo "  Language: JavaScript"
    fi

    if [ -f "jest.config.js" ] || [ -f "jest.config.ts" ]; then
        echo "  Testing: Jest"
    fi

    if [ -d "node_modules" ]; then
        echo "  Dependencies: installed"
    else
        echo "  Dependencies: not installed (run: npm install)"
    fi
fi

# Check for Go
if [ -f "go.mod" ]; then
    DETECTED="go"
    echo "✓ Go project detected"

    if command -v go &> /dev/null; then
        GO_VERSION=$(go version)
        echo "  Go version: $GO_VERSION"
    else
        echo "  ⚠ Go not installed"
    fi

    if [ -f "go.mod" ]; then
        MODULE=$(grep '^module' go.mod | awk '{print $2}')
        echo "  Module: $MODULE"
    fi
fi

# Check for Java
if [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
    DETECTED="java"
    echo "✓ Java project detected"

    if [ -f "pom.xml" ]; then
        echo "  Build tool: Maven"
    elif [ -f "build.gradle" ]; then
        echo "  Build tool: Gradle"
    fi

    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n 1)
        echo "  Java version: $JAVA_VERSION"
    else
        echo "  ⚠ Java not installed"
    fi
fi

# Check for Ruby
if [ -f "Gemfile" ]; then
    DETECTED="ruby"
    echo "✓ Ruby project detected"

    if command -v ruby &> /dev/null; then
        RUBY_VERSION=$(ruby --version)
        echo "  Ruby version: $RUBY_VERSION"
    else
        echo "  ⚠ Ruby not installed"
    fi
fi

# Check for Rust
if [ -f "Cargo.toml" ]; then
    DETECTED="rust"
    echo "✓ Rust project detected"

    if command -v cargo &> /dev/null; then
        CARGO_VERSION=$(cargo --version)
        echo "  Cargo version: $CARGO_VERSION"
    else
        echo "  ⚠ Cargo not installed"
    fi
fi

# No tech stack detected
if [ -z "$DETECTED" ]; then
    echo "ℹ No tech stack detected yet"
    echo ""
    echo "This appears to be a fresh project template."
    echo "Common tech stacks:"
    echo "  • Python (pytest, black, mypy)"
    echo "  • Node.js/TypeScript (Jest, ESLint, Prettier)"
    echo "  • Go (built-in testing)"
    echo "  • Java (JUnit, Maven/Gradle)"
fi

echo ""
echo "Tech stack: ${DETECTED:-none}"
exit 0
