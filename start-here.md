# Start Here - Session Context

> **New to this project?** Read [PROCESS-OVERVIEW.md](docs/PROCESS-OVERVIEW.md) first!
> **Claude Code?** Read [CLAUDE.md](CLAUDE.md) for development guidelines!

---

## Project Overview

**Project**: network-tools
**Description**: Network device discovery with Snipe-IT asset management integration
**Tech Stack**: Python 3.11+, Snipe-IT API, Click CLI
**Organization**: personal-ra
**Status**: Active - Snipe-IT Integration Complete

---

## Current State

**Branch**: `master`
**Status**: Stable
**Last Sprint**: Sprint 2 - Snipe-IT API Integration (Complete)

---

## Sprint 2 Completed (2025-12-06)

### All Tasks Complete ✓
1. ✓ Created Snipe-IT Integration PRD (`docs/snipeit-integration-prd.md`)
2. ✓ Created Sprint Backlog (`docs/sprint-backlog-snipeit.md`)
3. ✓ Removed database module (`src/network_tools/db/`)
4. ✓ Created Snipe-IT API client module (`src/network_tools/snipeit/`)
5. ✓ Updated config.py for Snipe-IT settings
6. ✓ Updated CLI commands (`discover`, `status`, new `search`)
7. ✓ Wrote tests for Snipe-IT client (65 tests passing)
8. ✓ Updated dependencies (replaced psycopg with requests)

### Key Files Created
- `src/network_tools/snipeit/client.py` - API client
- `src/network_tools/snipeit/models.py` - Asset, DiscoveredDevice models
- `src/network_tools/snipeit/exceptions.py` - Custom exceptions
- `tests/test_snipeit/` - Client and model tests

---

## Sprint 1 Completed (Archive)

### Device Discovery (2025-11-28)
- Created Device Discovery PRD
- Ran first network discovery via ARP scan
- Discovered 14 active devices on network

---

## Key Documentation

- **Process**: [AI-Assisted Agile Process](docs/ai-assisted-agile-process.md)
- **Claude Instructions**: [CLAUDE.md](CLAUDE.md)
- **Snipe-IT PRD**: [docs/snipeit-integration-prd.md](docs/snipeit-integration-prd.md)
- **Sprint Backlog**: [docs/sprint-backlog-snipeit.md](docs/sprint-backlog-snipeit.md)
- **Snipe-IT API Guide**: [snipeit-asset-management API Guide](../snipeit-asset-management/docs/snipeit-api-integration-guide.md)

---

## CLI Commands

```bash
# Check Snipe-IT connection status
python -m network_tools status

# Discover devices on network and sync to Snipe-IT
python -m network_tools discover --network 192.168.68.0/24

# Auto-confirm all new devices (non-interactive)
python -m network_tools discover -n 192.168.68.0/24 -y

# Search for asset by MAC or IP
python -m network_tools search --mac AA:BB:CC:DD:EE:FF
python -m network_tools search --ip 192.168.68.100

# Show version
python -m network_tools --version
```

---

## Testing

```bash
pytest                              # Run all tests
pytest --cov=src --cov-report=term  # Run with coverage
```

---

## Environment Setup

Copy `.env.example` to `.env` and configure:
```ini
SNIPEIT_BASE_URL=http://localhost:8082/api/v1
SNIPEIT_API_KEY=your_api_key_here
SNIPEIT_TIMEOUT=30
SNIPEIT_NETWORK_CATEGORY_ID=4
SNIPEIT_DEFAULT_STATUS_ID=2
SNIPEIT_DEFAULT_MODEL_ID=25
```

**Note**: Set `SNIPEIT_DEFAULT_MODEL_ID` to a valid model ID in your Snipe-IT instance.

---

**Last Updated**: 2025-12-06
**Updated By**: Claude Code
