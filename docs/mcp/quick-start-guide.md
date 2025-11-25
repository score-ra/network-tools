# MCP Setup Quick Start Guide

## 🚀 Complete Setup in 1 Hour

This guide walks you through the complete MCP setup for Symphony Core from start to finish.

---

## Overview: What You're Setting Up

**Model Context Protocol (MCP) servers** give Claude Code direct access to:
- 📚 Documentation (GoHighLevel, SearchAtlas, WordPress)
- 🗄️ Your PostgreSQL database
- 🌐 Browser automation (Playwright)
- 📁 File system operations
- 🔧 GitHub repositories

**Result:** Faster development, better code quality, less manual documentation lookup.

---

## Phase 1: Prerequisites (15 minutes)

### Step 1: Verify Node.js
```bash
node --version
# Need: v18.0.0 or higher
# Don't have it? Download from: https://nodejs.org/
```

### Step 2: Verify VS Code + Cline
```bash
# Open VS Code
code .

# Check Extensions (Ctrl/Cmd + Shift + X)
# Search: "Cline"
# Install if not present
```

### Step 3: Create GitHub Token
1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token (classic)"
3. Name: `Symphony Core MCP`
4. Select scopes: `repo` + `read:org`
5. Generate and **copy token immediately**
6. Save token securely (you'll need it later)

### Step 4: Collect Database Credentials
```bash
# Find your PostgreSQL password
cat gohighlevel-data-sync/.env.shared | grep DB_PASSWORD

# Note this password - you'll need it for MCP configuration
```

### ✅ Prerequisites Checklist
- [ ] Node.js 18+ installed
- [ ] VS Code with Cline extension
- [ ] GitHub token created and saved
- [ ] PostgreSQL password located

---

## Phase 2: Generate Configuration Files (20 minutes)

### Step 1: Open Claude.ai
- Go to: https://claude.ai
- Start a new conversation

### Step 2: Use the Implementation Prompt
- Open file: `mcp-implementation-prompt.md` (downloaded earlier)
- Copy entire contents
- Paste into Claude.ai
- Press Enter

### Step 3: Download Generated Files

Claude will generate 13 files one by one. After each file:

1. **Identify the file** - Claude will say "Ready to download: [filename]"
2. **Copy the content** - Click copy button on code block
3. **Save locally** - Create file in correct directory structure
4. **Ask for next** - Type "continue" or "next file please"

**Recommended:** Create this structure first on your Desktop:
```
MCP-Setup/
├── docs/mcp/
├── config/mcp/
└── scripts/mcp/
```

### File Generation Order

Claude will generate in this order:
1. account-setup-instructions.md
2. mcp-config.template.json
3. .env.template
4. setup-guide.md
5. install-mcp-servers.sh
6. install-mcp-servers.ps1
7. validate-mcp-setup.sh
8. validate-mcp-setup.ps1
9. troubleshooting.md
10. recommended-servers.md
11. quick-reference.md
12. README.md
13. sc-infrastructure-README-update.md

**Time estimate:** 15-20 minutes to generate + download all files

---

## Phase 3: Install in Repository (10 minutes)

### Step 1: Copy Files to sc-infrastructure

```bash
# Navigate to your sc-infrastructure repo
cd ~/projects/symphonycore-org/sc-infrastructure

# Copy all MCP files
cp -r ~/Desktop/MCP-Setup/* .

# Make scripts executable (Mac/Linux)
chmod +x scripts/mcp/*.sh

# Verify structure
ls -la docs/mcp/
ls -la config/mcp/
ls -la scripts/mcp/
```

### Step 2: Update .gitignore

Add to your `sc-infrastructure/.gitignore`:
```gitignore
# MCP credentials (never commit these)
config/mcp/.env
*.env
```

### Step 3: Commit Documentation (Not Credentials)

```bash
# Stage all MCP documentation and scripts
git add docs/mcp/
git add config/mcp/*.template*
git add config/mcp/README.md
git add scripts/mcp/
git add README.md

# Commit
git commit -m "Add MCP server documentation and setup automation

- Add comprehensive MCP setup guide
- Create configuration templates
- Add automated installation scripts
- Document troubleshooting steps

MCP servers provide direct access to:
- Documentation (GHL, SearchAtlas, WordPress)
- PostgreSQL database
- Browser automation (Playwright)
- GitHub repositories"

# Push to GitHub
git push origin main
```

---

## Phase 4: Run Installation (5 minutes)

### Step 1: Run Installation Script

**Mac/Linux:**
```bash
cd sc-infrastructure
./scripts/mcp/install-mcp-servers.sh
```

**Windows PowerShell:**
```powershell
cd sc-infrastructure
.\scripts\mcp\install-mcp-servers.ps1
```

**Expected output:**
```
Installing MCP servers for Symphony Core development...
Installing Context7 (Documentation)... ✅
Installing PostgreSQL MCP (Database)... ✅
Installing Playwright MCP (Browser Automation)... ✅
Installing Filesystem MCP... ✅
Installing GitHub MCP... ✅
✅ MCP servers installed successfully!
```

---

## Phase 5: Configure VS Code (10 minutes)

### Step 1: Create Your Personal Configuration

```bash
# Copy the template
cp config/mcp/mcp-config.template.json ~/Desktop/my-mcp-config.json

# Edit with your credentials
code ~/Desktop/my-mcp-config.json
```

### Step 2: Replace Placeholders

Replace these in your personal config file:

```json
{
  "cline.mcpServers": {
    "postgres": {
      "env": {
        // REPLACE THIS:
        "POSTGRES_URL": "postgresql://ghl_user:${DB_PASSWORD}@192.168.68.74:5432/subaccount_manager"
        
        // WITH YOUR ACTUAL PASSWORD:
        "POSTGRES_URL": "postgresql://ghl_user:YOUR_ACTUAL_PASSWORD@192.168.68.74:5432/subaccount_manager"
      }
    },
    "github": {
      "env": {
        // REPLACE THIS:
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
        
        // WITH YOUR TOKEN:
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_actual_token_here"
      }
    },
    "filesystem": {
      "env": {
        // REPLACE THIS:
        "ALLOWED_DIRECTORIES": "${YOUR_PROJECTS_PATH}/symphonycore-org"
        
        // WITH YOUR PATH:
        "ALLOWED_DIRECTORIES": "/Users/rohit/projects/symphonycore-org"
      }
    }
  }
}
```

### Step 3: Add to VS Code Settings

**Option A: Via UI (Easier)**
1. Open VS Code
2. Press `Ctrl/Cmd + ,` (Settings)
3. Search: "Cline MCP"
4. Click "Edit in settings.json"
5. Paste your configuration
6. Save file

**Option B: Direct Edit**
1. Open file:
   - Mac: `~/Library/Application Support/Code/User/settings.json`
   - Windows: `%APPDATA%\Code\User\settings.json`
   - Linux: `~/.config/Code/User/settings.json`
2. Add your MCP configuration
3. Save file

### Step 4: Reload VS Code

```
Press: Ctrl/Cmd + Shift + P
Type: "Reload Window"
Press: Enter
```

---

## Phase 6: Test Setup (5 minutes)

### Step 1: Run Validation Script

**Mac/Linux:**
```bash
./scripts/mcp/validate-mcp-setup.sh
```

**Windows PowerShell:**
```powershell
.\scripts\mcp\validate-mcp-setup.ps1
```

**Expected output:**
```
Validating MCP setup...
✅ Node.js v20.10.0
✅ NPX available
✅ VS Code CLI available
✅ PostgreSQL connection successful
Setup validation complete!
```

### Step 2: Test in VS Code

1. **Open any project** in VS Code
2. **Open Cline chat** (icon in sidebar)
3. **Test Context7:**
   ```
   Use context7 to show me the latest GoHighLevel API documentation for custom values
   ```
   
4. **Test PostgreSQL:**
   ```
   Query the PostgreSQL database and show me the schema for the custom_values table
   ```

5. **Test Filesystem:**
   ```
   List all TypeScript files in the src/ directory
   ```

**If all three work:** ✅ Setup complete!

---

## Phase 7: Start Using MCPs (Immediately!)

### Example Use Cases

#### Working on gohighlevel-data-sync:
```
"Use context7 for GoHighLevel API v2 documentation. I need to implement 
bulk import functionality for custom values. Show me the required parameters 
and example request."
```

#### Testing a WordPress site:
```
"Use Playwright MCP to navigate to https://clientname.com and:
1. Test the contact form submission
2. Check for any console errors
3. Verify Google Analytics tracking fires
4. Take screenshots if any issues found"
```

#### Querying client data:
```
"Query the PostgreSQL database to show me all clients where 
lifecycle_stage = 'at_risk' and last_stage_update > 30 days ago"
```

#### Checking repository status:
```
"Use GitHub MCP to show me:
1. All open issues in gohighlevel-data-sync
2. Recent commits in the last week
3. Any pull requests waiting for review"
```

---

## Troubleshooting

### Issue: "MCP server not found"

**Solution:**
```bash
# Reinstall the specific MCP
npx -y @uptime-technology/context7
```

### Issue: "Cannot connect to PostgreSQL"

**Solution:**
1. Verify PostgreSQL is running:
   ```bash
   pg_isready -h 192.168.68.74 -p 5432
   ```
2. Check password in configuration
3. Test connection manually:
   ```bash
   psql -h 192.168.68.74 -U ghl_user -d subaccount_manager
   ```

### Issue: "GitHub token invalid"

**Solution:**
1. Verify token in settings.json
2. Check token hasn't expired: https://github.com/settings/tokens
3. Regenerate token if needed
4. Update in VS Code settings

### More Help:

Check generated documentation:
- `docs/mcp/troubleshooting.md` - Common issues
- `docs/mcp/setup-guide.md` - Detailed setup
- `docs/mcp/quick-reference.md` - Command examples

---

## Success Checklist

- [ ] All 13 files generated and downloaded
- [ ] Files copied to sc-infrastructure repository
- [ ] Documentation committed to git (credentials NOT committed)
- [ ] Installation script executed successfully
- [ ] VS Code settings.json updated with personal credentials
- [ ] VS Code reloaded
- [ ] Validation script passed
- [ ] Test prompts work in Cline
- [ ] Can query database via MCP
- [ ] Can access documentation via Context7

**All checked?** 🎉 **You're done! Start using MCPs in your development.**

---

## Time Investment vs. ROI

| Investment | Return |
|------------|--------|
| **1 hour setup** | **5-10 hours saved per week** |
| Documentation lookup: 15 min → 30 sec | 90% faster |
| Database queries: 5 min → 1 min | 80% faster |
| Browser testing: 20 min → 5 min | 75% faster |
| API reference: 10 min → 30 sec | 95% faster |

**Payback period:** ~1 week of development

---

## What's Next?

### Week 1: Learn the Basics
- Use Context7 daily for documentation
- Practice PostgreSQL queries via MCP
- Test Playwright for website debugging

### Week 2: Build Workflows
- Create custom commands for common tasks
- Document your most-used prompts
- Share learnings with team

### Week 3: Optimize
- Refine MCP usage based on experience
- Add project-specific configurations
- Measure time savings

### Ongoing
- Keep MCP servers updated
- Rotate GitHub token every 90 days
- Share tips in team documentation

---

## Support Resources

**Generated Documentation:**
- Setup Guide: `docs/mcp/setup-guide.md`
- Troubleshooting: `docs/mcp/troubleshooting.md`
- Quick Reference: `docs/mcp/quick-reference.md`
- Server Details: `docs/mcp/recommended-servers.md`

**External Resources:**
- Context7: https://github.com/uptime-technology/context7
- MCP Directory: https://github.com/wong2/mcp-directory
- Claude MCP Docs: https://docs.anthropic.com/en/docs/build-with-claude/mcp

**Symphony Core:**
- Repository: https://github.com/symphonycore-org/sc-infrastructure
- Team Docs: https://team.symphonycore.com (internal-docs)

---

## Final Notes

- **Cost:** $0 - Everything is free
- **Time:** ~1 hour for complete setup
- **ROI:** 5-10 hours saved per week
- **Maintenance:** Minimal (token rotation every 90 days)
- **Team Ready:** Documentation in git for team onboarding

**You're now ready to code faster with AI assistance!** 🚀

Start with a simple test:
```
"Use context7 to show me GoHighLevel API documentation for webhooks"
```

If that works, you're all set! Happy coding! 💻✨
