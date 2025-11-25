# How to Use the MCP Implementation Prompt

## Quick Start

1. **Download the prompt file:**
   - File: `mcp-implementation-prompt.md`
   - Location: Available above for download

2. **Open Claude.ai:**
   - Go to https://claude.ai
   - Start a new conversation

3. **Copy and paste the entire prompt:**
   - Open `mcp-implementation-prompt.md`
   - Copy everything
   - Paste into Claude web chat
   - Press Enter

4. **Follow the conversation:**
   - Claude will generate files one at a time
   - After each file, download it using the download button in Claude's response
   - Tell Claude to continue to the next file
   - Repeat until all 13 files are generated

## Expected Workflow

### Step 1: Account Setup (15 minutes)
Claude will first generate `docs/mcp/account-setup-instructions.md`
- Follow this guide to set up required accounts
- Create GitHub token
- Verify PostgreSQL access
- Install prerequisites

### Step 2: Core Configuration (10 minutes)
Claude generates configuration templates:
- `config/mcp/mcp-config.template.json`
- `config/mcp/.env.template`

### Step 3: Documentation (20 minutes)
Claude generates setup and reference docs:
- `docs/mcp/setup-guide.md`
- `docs/mcp/troubleshooting.md`
- `docs/mcp/recommended-servers.md`
- `docs/mcp/quick-reference.md`

### Step 4: Automation Scripts (15 minutes)
Claude generates installation and validation scripts:
- Bash scripts (Mac/Linux)
- PowerShell scripts (Windows)

### Step 5: Repository Integration (5 minutes)
- `sc-infrastructure-README-update.md`
- Copy into your existing README

## Downloading Files from Claude Web

When Claude generates a file:

1. **Look for the code block** with the full file content
2. **Click the copy button** in the top-right of the code block
3. **Save to local file:**
   - Windows: Notepad → Paste → Save As → Change "Save as type" to "All Files"
   - Mac: TextEdit → Paste → Format → Make Plain Text → Save
   - Linux: gedit/nano → Paste → Save

4. **Name the file** exactly as Claude specifies:
   - Example: `setup-guide.md`
   - Keep the extension (.md, .sh, .ps1, .json)

## Organizing Downloaded Files

Create this structure on your desktop first:

```
MCP-Setup/
├── docs/
│   └── mcp/
│       ├── setup-guide.md
│       ├── troubleshooting.md
│       ├── recommended-servers.md
│       ├── quick-reference.md
│       └── account-setup-instructions.md
├── config/
│   └── mcp/
│       ├── mcp-config.template.json
│       ├── .env.template
│       └── README.md
├── scripts/
│   └── mcp/
│       ├── install-mcp-servers.sh
│       ├── install-mcp-servers.ps1
│       ├── validate-mcp-setup.sh
│       └── validate-mcp-setup.ps1
└── sc-infrastructure-README-update.md
```

Then copy all files into your `sc-infrastructure` repository.

## After Generating All Files

### Step 1: Copy to Repository
```bash
# Navigate to sc-infrastructure
cd ~/projects/symphonycore-org/sc-infrastructure

# Copy all MCP files
cp -r ~/Desktop/MCP-Setup/* .

# Make scripts executable (Mac/Linux)
chmod +x scripts/mcp/*.sh

# Review changes
git status
```

### Step 2: Follow Setup Guide
```bash
# Read the main setup guide
cat docs/mcp/setup-guide.md

# Or open in your preferred editor
code docs/mcp/setup-guide.md
```

### Step 3: Run Installation
```bash
# Mac/Linux
./scripts/mcp/install-mcp-servers.sh

# Windows PowerShell
.\scripts\mcp\install-mcp-servers.ps1
```

### Step 4: Validate Setup
```bash
# Mac/Linux
./scripts/mcp/validate-mcp-setup.sh

# Windows PowerShell
.\scripts\mcp\validate-mcp-setup.ps1
```

## Tips for Using Claude Web

### Keep Context Focused
If Claude gets confused:
- Start a new conversation
- Paste the prompt again
- Specify which file you need: "Please generate file #5: scripts/mcp/install-mcp-servers.sh"

### Request Modifications
You can ask Claude to adjust files:
- "Make the installation script more verbose"
- "Add more examples to the troubleshooting guide"
- "Include Windows-specific instructions in setup guide"

### Batch Download
- Let Claude generate 2-3 files before downloading
- Then download all at once
- This is faster for documentation files

### Verify Content
Before saving each file:
- Quickly scan for placeholder text
- Check file is complete (not cut off)
- Verify it matches expected file name

## Common Issues

### Claude Stops Mid-File
**Solution:** Type "continue" or "please continue generating that file"

### File Too Long (Cut Off)
**Solution:** Ask "Please provide the rest of [filename]"

### Wrong File Format
**Solution:** Specify "Please provide as downloadable code block"

### Need to Regenerate
**Solution:** "Please regenerate [filename] with [specific change]"

## Timeline Estimate

| Task | Time | Details |
|------|------|---------|
| Copy prompt to Claude | 1 min | Simple copy-paste |
| Generate all files | 15-20 min | Claude generates sequentially |
| Download files | 10 min | Save each file locally |
| Copy to repository | 5 min | Organize in correct structure |
| **Total** | **30-35 min** | Complete file generation |

Then add:
- Account setup: 15 min
- Installation: 10 min
- Testing: 10 min

**Total implementation: ~1 hour**

## What to Do If You Get Stuck

1. **Review this guide** - Reread relevant section
2. **Check generated docs** - Answer might be in `troubleshooting.md`
3. **Ask Claude for clarification** - "How do I [specific task]?"
4. **Verify prerequisites** - Node.js, VS Code, Cline extension
5. **Test incrementally** - Don't try to set up everything at once

## Next Steps After File Generation

1. ✅ All files generated and downloaded
2. ✅ Files organized in MCP-Setup directory
3. ✅ Copied to sc-infrastructure repository
4. 📝 Follow `docs/mcp/account-setup-instructions.md`
5. 📝 Follow `docs/mcp/setup-guide.md`
6. 🚀 Start using MCPs in development

## Success Indicators

You'll know setup is complete when:
- ✅ All 13 files generated and saved
- ✅ Files in sc-infrastructure repository
- ✅ Scripts are executable
- ✅ No credential placeholders remain (in your personal copies)
- ✅ VS Code settings.json updated
- ✅ Test prompt works: "Use context7 to show GoHighLevel API docs"

## Support

If something doesn't work:
1. Check `docs/mcp/troubleshooting.md`
2. Run validation script: `./scripts/mcp/validate-mcp-setup.sh`
3. Review Claude's responses for any warnings
4. Ensure all prerequisites installed

---

**Remember:** This is a one-time setup. Once complete, MCPs will be available in all your VS Code projects automatically.
