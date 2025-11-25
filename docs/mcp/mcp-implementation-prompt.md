# MCP Server Setup Implementation for Symphony Core

I need help implementing Model Context Protocol (MCP) servers for my development workflow. Please create all necessary documentation, configuration files, and scripts for the Symphony Core infrastructure repository.

## My Current Setup

### Technology Stack
- **VS Code Extension:** Cline (Claude Code extension)
- **Primary Projects:**
  - `gohighlevel-data-sync` - Node.js/TypeScript GHL integration
  - `sc-infrastructure` - Docker + PostgreSQL infrastructure
  - `website-testing-automation` - Playwright testing framework
  - `sc-content-conductor` - Python documentation validation
  - `internal-docs` - Docusaurus documentation site
  - `customer-kb` - Docusaurus customer knowledge base

### Infrastructure Details
- **Database:** PostgreSQL 14+
  - Host: `192.168.68.74`
  - Port: `5432`
  - Database: `subaccount_manager`
  - User: `ghl_user`
  - Schema: 33 tables, 10 views
- **GitHub Organization:** `symphonycore-org` (private repos)
- **Development OS:** [Windows/Mac/Linux - specify yours]

### Platforms I Need MCP Access To
1. **GoHighLevel API** - Marketing automation platform (primary)
2. **SearchAtlas** - SEO automation platform
3. **WordPress/Elementor** - Website development
4. **PostgreSQL** - Direct database queries
5. **GitHub** - Repository operations
6. **Local Filesystem** - Project file operations

## Required MCP Servers

Please set up these MCP servers based on priority:

### Priority 1 (Critical - Need First)
1. **Context7** - Documentation access (GoHighLevel, SearchAtlas, WordPress)
2. **PostgreSQL MCP** - Database operations

### Priority 2 (High Value)
3. **Playwright MCP** - Browser automation for testing
4. **Filesystem MCP** - File operations

### Priority 3 (Nice to Have)
5. **GitHub MCP** - Repository management
6. **Git MCP** - Version control operations

## What I Need You to Create

Please generate the following files for my `sc-infrastructure` repository. I want to download each file separately as markdown/script files:

### 1. Documentation Files

**File: `docs/mcp/setup-guide.md`**
- Complete setup instructions for Symphony Core developers
- Prerequisites checklist
- Step-by-step installation for each MCP server
- Configuration instructions for VS Code Cline extension
- Testing procedures
- Include Symphony Core-specific examples using our actual platforms (GHL, SearchAtlas, PostgreSQL)

**File: `docs/mcp/troubleshooting.md`**
- Common issues and solutions
- Connection problems (PostgreSQL, GitHub)
- VS Code extension issues
- NPX/Node.js problems
- MCP server errors
- Include specific fixes for Symphony Core infrastructure

**File: `docs/mcp/recommended-servers.md`**
- Detailed explanation of each MCP server
- Why we use it at Symphony Core
- Use cases with real examples from our projects
- Performance impact
- Alternatives considered

**File: `docs/mcp/account-setup-instructions.md`**
- Step-by-step instructions for creating any required accounts
- GitHub Personal Access Token setup
- PostgreSQL connection testing
- Environment variable setup
- Security best practices

### 2. Configuration Files

**File: `config/mcp/mcp-config.template.json`**
- Complete VS Code Cline MCP configuration
- Include all 6 MCP servers listed above
- Use placeholders for credentials: `${DB_PASSWORD}`, `${GITHUB_TOKEN}`, etc.
- Add comments explaining each section
- Include all required environment variables

**File: `config/mcp/.env.template`**
- Environment variables template
- Clear instructions for each variable
- Security warnings
- Examples with placeholder values

**File: `config/mcp/README.md`**
- How to use the configuration templates
- Steps to customize for individual developers
- Where to place credentials (NOT in git)
- How to test configuration

### 3. Automation Scripts

**File: `scripts/mcp/install-mcp-servers.sh`** (Bash script)
- Automated installation of all MCP servers
- Check prerequisites (Node.js, NPX)
- Install each MCP server with progress indicators
- Success/failure messages
- Next steps instructions
- Make it compatible with Mac/Linux

**File: `scripts/mcp/install-mcp-servers.ps1`** (PowerShell script)
- Same as bash script but for Windows
- Use PowerShell best practices
- Handle Windows paths correctly

**File: `scripts/mcp/validate-mcp-setup.sh`** (Bash script)
- Check Node.js version
- Verify NPX availability
- Test PostgreSQL connection to 192.168.68.74:5432
- Verify VS Code installation
- Check if Cline extension is installed
- Test each MCP server availability
- Output detailed report

**File: `scripts/mcp/validate-mcp-setup.ps1`** (PowerShell script)
- Same validation but for Windows

### 4. Repository Documentation

**File: `sc-infrastructure-README-update.md`**
- Section to add to the main sc-infrastructure README.md
- Overview of MCP setup
- Quick start instructions
- Links to detailed documentation
- Make it concise but informative

### 5. Quick Reference

**File: `docs/mcp/quick-reference.md`**
- Cheat sheet for common MCP commands
- Example prompts for each MCP server
- Symphony Core-specific use cases:
  - Querying GHL custom values from database
  - Accessing GoHighLevel API documentation
  - Testing WordPress sites with Playwright
  - Searching SearchAtlas docs
- Keyboard shortcuts
- Troubleshooting one-liners

## Specific Configuration Requirements

### PostgreSQL MCP Configuration
```
Host: 192.168.68.74
Port: 5432
Database: subaccount_manager
User: ghl_user
Password: [use placeholder ${DB_PASSWORD}]
```

### Filesystem MCP Configuration
- Allow access to: `${PROJECTS_PATH}/symphonycore-org/*`
- Restrict to project directories only
- No system directories

### GitHub MCP Configuration
- Organization: `symphonycore-org`
- Access: Private repositories
- Token scope: repo, read:org

## Example Use Cases to Include

For each MCP server, include these Symphony Core-specific examples in the documentation:

### Context7 Examples
```
"Use context7 to show me GoHighLevel API v2 documentation for custom values endpoints"
"Use context7 for SearchAtlas API authentication methods"
"Use context7 for Elementor widget development best practices"
```

### PostgreSQL Examples
```
"Query PostgreSQL to show all custom_values for client 'upscalelegal-2025'"
"Query the database to find OAuth tokens expiring in the next 7 days"
"Show me the schema for the business_rules table"
```

### Playwright Examples
```
"Use Playwright to test the contact form on upscalelegal.com"
"Navigate to the staging site and check for console errors"
"Screenshot the mobile view of the homepage"
```

## Output Format

Please create each file as a separate, complete, ready-to-use document. For each file:

1. Include full file path as a header
2. Add appropriate frontmatter (if markdown)
3. Include all necessary content
4. Add comments explaining complex sections
5. Use Symphony Core branding and terminology
6. Make it professional and production-ready

After creating each file, say "Ready to download: [filename]" so I know to save it.

## Additional Requirements

- Use clear, concise language
- Include code blocks with syntax highlighting
- Add warning/info boxes where appropriate
- Use tables for comparison information
- Include command examples with expected output
- Add security warnings where credentials are involved
- Make scripts executable with clear usage instructions
- Include success/failure checks in scripts
- Add troubleshooting for each major step

## File Generation Order

Please generate files in this order so I can implement incrementally:

1. `docs/mcp/account-setup-instructions.md` (I'll need this first)
2. `config/mcp/mcp-config.template.json` (Core configuration)
3. `config/mcp/.env.template` (Credentials template)
4. `docs/mcp/setup-guide.md` (Main documentation)
5. `scripts/mcp/install-mcp-servers.sh` (Automation for Mac/Linux)
6. `scripts/mcp/install-mcp-servers.ps1` (Automation for Windows)
7. `scripts/mcp/validate-mcp-setup.sh` (Testing for Mac/Linux)
8. `scripts/mcp/validate-mcp-setup.ps1` (Testing for Windows)
9. `docs/mcp/troubleshooting.md` (Problem solving)
10. `docs/mcp/recommended-servers.md` (Deep dive)
11. `docs/mcp/quick-reference.md` (Cheat sheet)
12. `config/mcp/README.md` (Configuration guide)
13. `sc-infrastructure-README-update.md` (Repository update)

## Security Notes to Include

In all documentation, emphasize:
- Never commit credentials to git
- Use environment variables or VS Code settings (not in repo)
- Add `config/mcp/.env` to `.gitignore`
- Use minimal permissions for tokens
- Rotate credentials regularly
- Document what to do if credentials are exposed

## Testing Checklist to Include

Each file should help developers verify:
- Installation successful
- Configuration correct
- MCP servers responding
- Database connection working
- Credentials properly secured
- VS Code integration functional

## Start Generation

Please begin generating the files in the order specified above. After each file, pause and ask if I want to proceed to the next one. This allows me to download and review each file before continuing.

For the first file (`docs/mcp/account-setup-instructions.md`), please include:
- GitHub Personal Access Token creation (step-by-step with screenshots description)
- PostgreSQL connection verification steps
- VS Code Cline extension installation
- Node.js/NPX installation verification
- Any other accounts or prerequisites needed

Ready to begin?
