# Required Accounts & Services for MCP Setup

## Summary: What You'll Need

Good news: **You already have most of what's needed!** Here's the complete list:

| Service | Status | Cost | Setup Time | Required For |
|---------|--------|------|------------|--------------|
| **Node.js 18+** | ✅ Likely have | Free | 5 min | Running MCP servers |
| **VS Code** | ✅ Have | Free | Already installed | Development environment |
| **Cline Extension** | ⚠️ Verify | Free | 2 min | MCP integration |
| **PostgreSQL** | ✅ Have | Free | Already running | Database MCP |
| **GitHub Account** | ✅ Have | Free | Already have | GitHub MCP |
| **GitHub Token** | ⚠️ Need to create | Free | 3 min | GitHub MCP access |
| **GoHighLevel** | ✅ Have | Existing plan | Already have | Documentation via Context7 |
| **SearchAtlas** | ✅ Have | Existing plan | Already have | Documentation via Context7 |

**Total New Accounts Needed:** 0 ✅  
**Total New Tokens Needed:** 1 (GitHub)  
**Total Cost:** $0  
**Total Setup Time:** ~10 minutes  

---

## Detailed Setup Instructions

### 1. Verify Node.js Installation (5 minutes)

**Check if already installed:**
```bash
# Open terminal/command prompt
node --version
npm --version
npx --version
```

**Expected output:**
```
v18.0.0 or higher
9.0.0 or higher
9.0.0 or higher
```

**If not installed or version too old:**

#### Windows
1. Go to https://nodejs.org/
2. Download "LTS" version (recommended)
3. Run installer with default settings
4. Restart terminal/VS Code
5. Verify: `node --version`

#### Mac
```bash
# Using Homebrew (recommended)
brew install node

# Verify
node --version
```

#### Linux (Ubuntu/Debian)
```bash
# Using NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
```

---

### 2. Verify VS Code Cline Extension (2 minutes)

**Check installation:**
1. Open VS Code
2. Click Extensions icon (Ctrl/Cmd + Shift + X)
3. Search for "Cline"
4. Look for "Cline" by Saoud Rizwan

**If not installed:**
1. Click "Install" button
2. Wait for installation to complete
3. Reload VS Code if prompted
4. Verify: Look for Cline icon in sidebar

**Alternative extensions (if Cline doesn't work):**
- "Continue" - Similar functionality
- Check which extension you actually have installed

---

### 3. Create GitHub Personal Access Token (3 minutes)

**Why needed:** GitHub MCP needs authentication to access your repositories.

**Step-by-step:**

1. **Go to GitHub Settings:**
   - Navigate to https://github.com/settings/tokens
   - Or: GitHub.com → Your Profile (top right) → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Create new token:**
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: `Symphony Core MCP - VS Code`
   - Expiration: Select `90 days` or `No expiration` (less secure but convenient)

3. **Select scopes:**
   Check these boxes:
   ```
   ✅ repo (Full control of private repositories)
      ✅ repo:status
      ✅ repo_deployment
      ✅ public_repo
      ✅ repo:invite
      ✅ security_events
   
   ✅ read:org (Read org and team membership, read org projects)
   ```

4. **Generate token:**
   - Scroll to bottom
   - Click "Generate token"
   - **IMPORTANT:** Copy token immediately (you won't see it again!)

5. **Store token securely:**
   ```
   # Save to a secure note app or password manager
   # Format: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
   Example:
   GitHub Token for MCP: ghp_abc123def456ghi789jkl012mno345pqr678stu
   Created: 2025-11-22
   Expires: 2026-02-20
   ```

**Security notes:**
- Never commit token to git
- Never share token publicly
- Rotate every 90 days
- Use in environment variables only

---

### 4. Verify PostgreSQL Access (3 minutes)

**You already have PostgreSQL running.** Just verify connection:

**Test connection:**

#### Using psql (command line)
```bash
# Mac/Linux
psql -h 192.168.68.74 -p 5432 -U ghl_user -d subaccount_manager

# Windows (if psql installed)
psql -h 192.168.68.74 -p 5432 -U ghl_user -d subaccount_manager

# Enter password when prompted
# Should see: subaccount_manager=>
```

**If psql not installed:**
- Don't worry! The MCP server will connect directly
- You just need the connection details:
  ```
  Host: 192.168.68.74
  Port: 5432
  Database: subaccount_manager
  User: ghl_user
  Password: [your existing password]
  ```

**Where to find password:**
- Check your `.env.shared` file in gohighlevel-data-sync project
- Look for `DB_PASSWORD=` line
- This is what you'll use for PostgreSQL MCP

---

### 5. Verify GoHighLevel Access (1 minute)

**You already have this!** No setup needed.

**What you need:**
- ✅ Access to GoHighLevel dashboard
- ✅ Agency account credentials

**For MCP:**
- Context7 MCP will fetch GHL documentation automatically
- No API key needed for documentation access
- Your existing GHL account is sufficient

---

### 6. Verify SearchAtlas Access (1 minute)

**You already have this!** No setup needed.

**What you need:**
- ✅ Access to SearchAtlas dashboard
- ✅ SearchAtlas login credentials

**For MCP:**
- Context7 MCP will fetch SearchAtlas documentation automatically
- No API key needed for documentation access
- Your existing account is sufficient

---

## Environment Variables to Collect

Before running the MCP setup, gather these values:

### From Your Existing Setup:

| Variable | Where to Find | Example | Your Value |
|----------|---------------|---------|------------|
| `DB_PASSWORD` | `gohighlevel-data-sync/.env.shared` | `mysecretpass123` | _____________ |
| `GITHUB_TOKEN` | Created in step 3 above | `ghp_abc123...` | _____________ |
| `PROJECTS_PATH` | Your local path | `/Users/rohit/projects` | _____________ |

### PostgreSQL Connection Details:

You already have these - just document them:

```
Host: 192.168.68.74
Port: 5432
Database: subaccount_manager
User: ghl_user
Password: [from DB_PASSWORD above]
```

### Full PostgreSQL URL:

Format:
```
postgresql://ghl_user:${DB_PASSWORD}@192.168.68.74:5432/subaccount_manager
```

Example (with your password):
```
postgresql://ghl_user:mysecretpass123@192.168.68.74:5432/subaccount_manager
```

---

## Pre-Setup Checklist

Before running MCP installation, verify:

- [ ] **Node.js 18+** - Run `node --version`
- [ ] **NPX available** - Run `npx --version`
- [ ] **VS Code installed** - Open VS Code successfully
- [ ] **Cline extension** - See Cline icon in VS Code sidebar
- [ ] **GitHub token created** - Saved securely
- [ ] **PostgreSQL password** - Located in .env.shared
- [ ] **Database accessible** - Can connect to 192.168.68.74:5432
- [ ] **Projects path known** - Full path to symphonycore-org directory

**All checked?** ✅ You're ready for MCP installation!

---

## Security Best Practices

### DO ✅
- Store tokens in environment variables
- Use `.env` files (not committed to git)
- Add `.env` to `.gitignore`
- Rotate tokens every 90 days
- Use minimal token permissions
- Keep passwords in password manager

### DON'T ❌
- Commit credentials to git repositories
- Share tokens publicly
- Use tokens in code comments
- Store passwords in plain text files
- Give tokens unlimited expiration
- Use admin tokens when viewer access sufficient

---

## What Gets Installed

**MCP Servers** (via NPX):
- Stored in: `~/.npm/_npx/`
- Total size: ~200-300MB
- Installation: Automatic on first use
- Updates: Automatic (or manual via update script)

**No cloud services:**
- Everything runs locally
- No data sent to third parties
- No monthly subscriptions
- No usage limits

---

## Cost Breakdown (Final)

| Item | Monthly Cost | One-Time Cost | Notes |
|------|--------------|---------------|-------|
| Node.js | $0 | $0 | Free and open source |
| VS Code | $0 | $0 | Free from Microsoft |
| Cline Extension | $0 | $0 | Free extension |
| MCP Servers | $0 | $0 | Open source, run locally |
| GitHub Account | $0 | $0 | Free tier sufficient |
| PostgreSQL | $0 | $0 | Self-hosted (existing) |
| **TOTAL** | **$0** | **$0** | **No new costs** |

**Existing subscriptions** (unchanged):
- Claude Pro: $20/month (you already have)
- GoHighLevel: [existing plan]
- SearchAtlas: [existing plan]

---

## Timeline Summary

| Task | Time | When |
|------|------|------|
| **Prerequisites** | **15 min** | **Before MCP setup** |
| - Verify Node.js | 2 min | Now |
| - Verify Cline | 2 min | Now |
| - Create GitHub token | 3 min | Now |
| - Collect credentials | 5 min | Now |
| - Verify PostgreSQL | 3 min | Now |
| **MCP Setup** | **45 min** | **After prerequisites** |
| - Generate files with Claude | 20 min | Using prompt |
| - Download/organize files | 10 min | Manual |
| - Run installation script | 5 min | Automated |
| - Configure VS Code | 5 min | Manual |
| - Test setup | 5 min | Validation script |
| **TOTAL** | **~1 hour** | **Start to finish** |

---

## Next Steps

1. **Complete this checklist** ✅
2. **Open Claude.ai** → Use the MCP implementation prompt
3. **Generate all files** → Download each one
4. **Follow setup guide** → Generated file will have detailed steps
5. **Start coding** → MCPs active in VS Code!

---

## Getting Help

**If you get stuck on accounts/prerequisites:**
- Node.js: https://nodejs.org/en/download/
- VS Code: https://code.visualstudio.com/download
- Cline: Search "Cline" in VS Code extensions
- GitHub: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

**After setup:**
- Check generated `docs/mcp/troubleshooting.md`
- Run validation script
- Test with simple prompt: "Use context7 to show GoHighLevel API docs"

---

**Ready to proceed?** You have everything you need! Move on to using the MCP implementation prompt in Claude.ai.
