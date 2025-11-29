# Network-Tools Architectural Decisions

**Date**: 2025-11-29
**Context**: Repo consolidation review (ra-infrastructure, network-tools, ra-home-automation)
**Status**: Approved - Ready for PRD/Sprint Plan Updates

---

## Summary

This document captures architectural decisions made during the consolidation review that impact the network-tools PRD (`docs/device-discovery-prd.md`) and sprint planning.

---

## Decision 1: Direct Database Access (Not SQL File Generation)

### Previous Approach (PRD v1.1)
- network-tools generates SQL import files
- ra-infrastructure imports via `psql -f` or CLI command
- network-tools has READ-ONLY database access

### New Decision
- **network-tools has direct READ/WRITE access to ra_inventory database**
- No SQL file generation needed
- network-tools owns the full device discovery workflow end-to-end

### Rationale
- Simpler architecture with fewer moving parts
- network-tools needs control over database logical layer operations
- Eliminates handoff step between repos
- Interactive confirmation can write directly after user approval

### PRD Sections to Update
- Remove Story 3.5 (Generate Import Artifacts) or repurpose for backup/audit
- Remove Feature 5 requirement for SQL generation
- Update "Integration Requirements" section - remove ra-infrastructure import process
- Update "Database Integration" - change from READ-ONLY to READ/WRITE
- Remove ImportArtifact data entity (or repurpose for audit logs)

---

## Decision 2: Language Confirmed - Python 3.11+

### Decision
- Rewrite/implement scanners in Python (not keep PowerShell from ra-home-automation)

### Rationale
- PRD already specifies Python 3.11+
- Interactive confirmation CLI needs Python anyway
- Single language = better maintainability
- Python networking libraries (scapy, python-nmap) are mature
- Consistent with ra-infrastructure CLI (also Python)

### PRD Impact
- No change needed - PRD already specifies Python

---

## Decision 3: Scope Boundaries

### network-tools owns:
- Network scanning (ARP/ICMP/mDNS)
- Device metadata collection
- MAC vendor lookup (OUI database)
- Change detection
- Interactive confirmation CLI
- **Direct database writes** (new)

### ra-infrastructure provides:
- PostgreSQL database (ra_inventory)
- Database schema and migrations
- Python CLI for manual device management (`inv device ...`)
- Connection credentials via environment variables

### ra-home-automation keeps:
- HomeSeer integration
- BlueIris integration
- Windows setup scripts
- Property-specific documentation

---

## Updated Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    network-tools (Python)                    │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Network Scanner │  │ Interactive CLI │                   │
│  │ (ARP/ICMP/mDNS) │─►│ Confirm Devices │                   │
│  └─────────────────┘  └────────┬────────┘                   │
│                                │                             │
│                                ▼                             │
│                       ┌─────────────────┐                    │
│                       │ Database Layer  │                    │
│                       │ (psycopg3)      │                    │
│                       └────────┬────────┘                    │
│                                │ READ/WRITE                  │
└────────────────────────────────┼────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────┐
│                    ra-infrastructure                           │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │  PostgreSQL DB  │  │  Python CLI     │                     │
│  │  (ra_inventory) │  │  (inv command)  │                     │
│  └─────────────────┘  └─────────────────┘                     │
└───────────────────────────────────────────────────────────────┘
```

---

## Action Items for network-tools

### PRD Updates Required
1. [ ] Update Story 3.5 - Remove SQL file generation, or repurpose for audit/backup
2. [ ] Update Feature 5 - Remove SQL generation requirements
3. [ ] Update "Database Integration" section - READ/WRITE access
4. [ ] Update "Integration Requirements" - Remove ra-infrastructure import process
5. [ ] Update "Out of Scope" - Remove "Direct database writes" (now in scope)
6. [ ] Review ImportArtifact entity - Remove or repurpose

### Sprint Plan Updates
1. [ ] Remove tasks related to SQL file generation
2. [ ] Add tasks for database write layer implementation
3. [ ] Ensure psycopg3 connection pooling is planned

---

## Questions Resolved

| Question | Answer |
|----------|--------|
| Keep PowerShell or rewrite in Python? | Rewrite in Python |
| SQL file generation or direct DB access? | Direct DB access |
| Who owns device import? | network-tools (end-to-end) |
| Git history recovery needed? | No |

---

*Move this file to network-tools repo: `docs/DECISIONS-2025-11-29.md`*
