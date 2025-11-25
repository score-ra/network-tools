#!/bin/bash

# customize-templates.sh
# Helper script to replace placeholders in template files

set -e

# Check if required arguments are provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <project-name> [description] [tech-stack]"
    echo "Example: $0 my-awesome-app 'A great application' python"
    exit 1
fi

PROJECT_NAME="$1"
DESCRIPTION="${2:-A new project}"
TECH_STACK="${3:-TBD}"
CURRENT_DATE=$(date +%Y-%m-%d)

echo "🎨 Customizing template files..."
echo "  Project: $PROJECT_NAME"
echo "  Description: $DESCRIPTION"
echo "  Tech Stack: $TECH_STACK"
echo "  Date: $CURRENT_DATE"
echo ""

# Function to replace in file
replace_in_file() {
    local file=$1
    local search=$2
    local replace=$3

    if [ -f "$file" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|${search}|${replace}|g" "$file"
        else
            # Linux
            sed -i "s|${search}|${replace}|g" "$file"
        fi
        echo "  ✓ Updated: $file"
    else
        echo "  ⚠ Skipped (not found): $file"
    fi
}

# Customize README.md
if [ -f "README.md" ]; then
    echo "📝 Customizing README.md..."
    replace_in_file "README.md" "\[YOUR_PROJECT_NAME\]" "$PROJECT_NAME"
    replace_in_file "README.md" "your-project" "$PROJECT_NAME"
    replace_in_file "README.md" "A production-ready template.*" "$DESCRIPTION"
fi

# Customize start-here.md if it exists
if [ -f "start-here.md" ]; then
    echo "📝 Customizing start-here.md..."
    replace_in_file "start-here.md" "<project-name>" "$PROJECT_NAME"
    replace_in_file "start-here.md" "<project-description>" "$DESCRIPTION"
    replace_in_file "start-here.md" "<primary-tech-stack>" "$TECH_STACK"
    replace_in_file "start-here.md" "<tech-stack>" "$TECH_STACK"
    replace_in_file "start-here.md" "<current-date>" "$CURRENT_DATE"
fi

# Customize package.json if it exists (Node.js)
if [ -f "package.json" ]; then
    echo "📝 Customizing package.json..."
    replace_in_file "package.json" "<project-name>" "$PROJECT_NAME"
    replace_in_file "package.json" "<project-description>" "$DESCRIPTION"
fi

# Customize .env.example if it exists
if [ -f ".env.example" ]; then
    echo "📝 Customizing .env.example..."
    replace_in_file ".env.example" "<project-name>" "$PROJECT_NAME"
fi

# Update any generated docs
for file in docs/*-prd.md docs/*-technical-spec.md; do
    if [ -f "$file" ]; then
        echo "📝 Customizing $file..."
        replace_in_file "$file" "<project-name>" "$PROJECT_NAME"
        replace_in_file "$file" "<project-description>" "$DESCRIPTION"
        replace_in_file "$file" "<tech-stack>" "$TECH_STACK"
        replace_in_file "$file" "<current-date>" "$CURRENT_DATE"
    fi
done

echo ""
echo "✅ Customization complete!"
echo ""
echo "Files updated:"
echo "  • README.md"
echo "  • start-here.md (if exists)"
echo "  • package.json (if exists)"
echo "  • .env.example (if exists)"
echo "  • Generated documentation"
echo ""
echo "Next steps:"
echo "  1. Review customized files"
echo "  2. Update any remaining placeholders manually"
echo "  3. Commit changes"
