# Sprint Plan: Network Discovery Implementation

**Date**: 2025-11-29
**Sprint Goal**: Build foundational network discovery tool with interactive CLI
**PRD Reference**: [device-discovery-prd.md](device-discovery-prd.md) v1.2

---

## Sprint Philosophy

**Foundation First**: Build core infrastructure before features. Each layer must be solid before adding the next.

```
Layer 4: Interactive CLI (Feature 5)      ← User-facing
Layer 3: Inventory Comparator (Feature 3) ← Business logic
Layer 2: Device Metadata (Feature 2)      ← Data enrichment
Layer 1: Network Scanner (Feature 1)      ← Core capability
Layer 0: Project Structure & Database     ← Foundation
```

---

## Sprint Backlog (Prioritized)

### Phase 0: Foundation (Must Complete First)

| ID | Task | Description | Effort | Dependencies |
|----|------|-------------|--------|--------------|
| **F-001** | Project structure setup | Create `src/network_tools/` package structure with `__init__.py`, `__main__.py` | XS | None |
| **F-002** | Database connection module | `src/network_tools/db/connection.py` - psycopg3 connection pool, env var config | S | F-001 |
| **F-003** | Database models | `src/network_tools/db/models.py` - Device, Network, Site dataclasses | S | F-002 |
| **F-004** | Database queries | `src/network_tools/db/queries.py` - CRUD operations for devices | M | F-003 |
| **F-005** | Configuration module | `src/network_tools/config.py` - Load from env vars and config file | S | F-001 |
| **F-006** | Logging setup | `src/network_tools/logging.py` - Structured logging for audit | XS | F-001 |

**Acceptance Criteria for Phase 0**:
- [ ] `python -m network_tools --version` works
- [ ] Can connect to ra_inventory database
- [ ] Can query existing devices
- [ ] Can insert new device (manual test)
- [ ] Environment variables documented in `.env.example`

---

### Phase 1: Network Scanner (Core Capability)

| ID | Task | Description | Effort | Dependencies |
|----|------|-------------|--------|--------------|
| **S-001** | ARP scanner module | `src/network_tools/scanner/arp.py` - Windows ARP table query | S | F-001 |
| **S-002** | ICMP ping scanner | `src/network_tools/scanner/ping.py` - Concurrent ping sweep | M | F-001 |
| **S-003** | Scanner interface | `src/network_tools/scanner/base.py` - Abstract scanner protocol | S | S-001 |
| **S-004** | Network scanner CLI | `discover` subcommand with `--network` flag | S | S-001, S-002 |

**Acceptance Criteria for Phase 1**:
- [ ] `python -m network_tools discover --network 192.168.68.0/22` runs scan
- [ ] Discovers active devices with IP and MAC
- [ ] Shows progress during scan
- [ ] Outputs device list to console

---

### Phase 2: Device Metadata (Data Enrichment)

| ID | Task | Description | Effort | Dependencies |
|----|------|-------------|--------|--------------|
| **M-001** | OUI database loader | `src/network_tools/oui/database.py` - Load/cache IEEE OUI file | M | F-001 |
| **M-002** | Manufacturer lookup | `src/network_tools/oui/lookup.py` - MAC prefix → manufacturer | S | M-001 |
| **M-003** | OUI database download | Script to download/update IEEE OUI database | S | M-001 |
| **M-004** | Hostname resolver | `src/network_tools/resolver/hostname.py` - Reverse DNS lookup | S | F-001 |

**Acceptance Criteria for Phase 2**:
- [ ] Can lookup manufacturer from MAC address
- [ ] OUI database cached locally
- [ ] Can resolve hostnames for discovered IPs
- [ ] Scanner output includes manufacturer

---

### Phase 3: Inventory Comparator (Business Logic)

| ID | Task | Description | Effort | Dependencies |
|----|------|-------------|--------|--------------|
| **C-001** | Device comparator | `src/network_tools/comparator.py` - Compare discovered vs DB | M | F-004, S-004 |
| **C-002** | Match by MAC | Primary matching logic using MAC address | S | C-001 |
| **C-003** | Categorize results | New, updated, missing device classification | S | C-002 |
| **C-004** | Comparison report | Console output showing comparison results | S | C-003 |

**Acceptance Criteria for Phase 3**:
- [ ] Compares discovered devices with database
- [ ] Identifies new devices (not in DB)
- [ ] Identifies updated devices (IP changed)
- [ ] Identifies missing devices (in DB, not discovered)
- [ ] Shows comparison summary

---

### Phase 4: Interactive CLI (User-Facing)

| ID | Task | Description | Effort | Dependencies |
|----|------|-------------|--------|--------------|
| **I-001** | Device display formatter | Pretty-print device details | S | C-004 |
| **I-002** | Confirmation prompts | [C]onfirm/[S]kip/[E]dit/[A]ll/[Q]uit workflow | M | I-001 |
| **I-003** | Device editor | Edit name, device_type before confirmation | S | I-002 |
| **I-004** | Database writer | Write confirmed devices to ra_inventory | M | F-004, I-002 |
| **I-005** | Write results display | Show success/failure with device IDs | S | I-004 |
| **I-006** | --yes flag | Non-interactive bulk approval mode | S | I-002 |

**Acceptance Criteria for Phase 4**:
- [ ] Interactive review of each new device
- [ ] Can edit device name and type
- [ ] Can confirm/skip individual devices
- [ ] Can bulk approve remaining devices
- [ ] Confirmed devices written to database
- [ ] Shows database IDs after write

---

## Effort Estimates

| Size | Time Estimate |
|------|---------------|
| XS | < 30 min |
| S | 30 min - 2 hours |
| M | 2 - 4 hours |
| L | 4 - 8 hours |

---

## Total Sprint Estimate

| Phase | Tasks | Effort |
|-------|-------|--------|
| Phase 0: Foundation | 6 | ~6 hours |
| Phase 1: Scanner | 4 | ~5 hours |
| Phase 2: Metadata | 4 | ~5 hours |
| Phase 3: Comparator | 4 | ~4 hours |
| Phase 4: Interactive | 6 | ~8 hours |
| **Total** | **24 tasks** | **~28 hours** |

---

## Definition of Done

For each phase:
- [ ] All tasks completed
- [ ] Unit tests written (≥80% coverage for new code)
- [ ] Manual testing passed
- [ ] Code follows project standards (black, flake8, mypy)
- [ ] Documentation updated

---

## Project Structure (Target)

```
src/network_tools/
├── __init__.py
├── __main__.py           # CLI entry point
├── cli/
│   ├── __init__.py
│   ├── main.py           # Click CLI app
│   └── discover.py       # discover subcommand
├── config.py             # Configuration
├── logging.py            # Logging setup
├── db/
│   ├── __init__.py
│   ├── connection.py     # Database connection
│   ├── models.py         # Data models
│   └── queries.py        # CRUD operations
├── scanner/
│   ├── __init__.py
│   ├── base.py           # Scanner interface
│   ├── arp.py            # ARP scanner
│   └── ping.py           # ICMP scanner
├── oui/
│   ├── __init__.py
│   ├── database.py       # OUI database loader
│   └── lookup.py         # Manufacturer lookup
├── resolver/
│   ├── __init__.py
│   └── hostname.py       # Hostname resolution
└── comparator.py         # Device comparison logic

tests/
├── __init__.py
├── test_db/
├── test_scanner/
├── test_oui/
└── test_comparator.py
```

---

## Environment Variables Required

```bash
# Database connection (ra_inventory)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ra_inventory
DB_USER=inventory
DB_PASSWORD=<from-secrets>

# Optional
OUI_DATABASE_PATH=./data/oui.txt
LOG_LEVEL=INFO
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| ARP requires admin privileges | Fallback to ICMP ping; document requirements |
| Database connection fails | Retry logic; offline mode with export |
| OUI database outdated | Auto-download script; monthly refresh |
| Large network slow scan | Concurrent scanning; progress indication |

---

## Success Criteria

Sprint is complete when:
1. `python -m network_tools discover --network 192.168.68.0/22` runs end-to-end
2. User can interactively confirm new devices
3. Confirmed devices are written to ra_inventory database
4. All tests pass with ≥80% coverage

---

**Document Version**: 1.0
**Created**: 2025-11-29
**Author**: Claude Code
