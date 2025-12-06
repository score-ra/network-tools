# Product Requirement Document (PRD)

> **⚠️ SUPERSEDED**: This PRD has been replaced by [snipeit-integration-prd.md](snipeit-integration-prd.md).
> The database integration approach described here was replaced with Snipe-IT API integration in December 2025.
> This document is retained for historical reference only.

**Project Name**: Automated Network Device Discovery
**Version**: 1.2
**Date**: 2025-11-29
**Owner**: personal-ra
**Status**: Superseded

---

## Executive Summary

This PRD defines requirements for automated network device discovery functionality within the network-tools repository. The system will scan networks to detect devices, collect device metadata (MAC address, IP address, hostname, manufacturer), and populate the device inventory database managed by `ra-infrastructure`. This enables maintaining an accurate, up-to-date inventory of all devices across networks without manual data entry.

---

## Business Objectives

### Goals
1. Automatically discover devices on configured networks with minimal manual intervention
2. Collect device metadata including MAC address, IP address, hostname, and inferred manufacturer
3. Correlate discovered devices with existing inventory records to detect new devices vs. updates
4. Provide visibility into network device population and changes over time

### Success Metrics
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Device detection accuracy | N/A | 95%+ of active devices detected | Sprint 1 |
| Discovery scan time (Class C network) | N/A | < 5 minutes | Sprint 1 |
| False positive rate | N/A | < 5% | Sprint 2 |
| Manual data entry reduction | 100% manual | 80% automated | Sprint 2 |

---

## User Stories

### Epic 1: Network Scanning

#### Story 1.1: Scan Local Network for Active Devices
**As a** network administrator
**I want** to scan a network subnet for active devices
**So that** I can discover what devices are connected

**Acceptance Criteria**:
- [ ] Scan a specified CIDR range (e.g., 192.168.1.0/24)
- [ ] Detect active hosts via ICMP ping or ARP scan
- [ ] Collect IP address for each discovered device
- [ ] Report scan progress and completion status
- [ ] Handle scan timeouts gracefully

**Priority**: High
**Estimated Effort**: M

#### Story 1.2: Collect Device MAC Addresses
**As a** network administrator
**I want** to collect MAC addresses for discovered devices
**So that** I can uniquely identify devices across IP changes

**Acceptance Criteria**:
- [ ] Retrieve MAC address from ARP table for discovered IPs
- [ ] Handle cases where MAC is not available (cross-subnet)
- [ ] Validate MAC address format
- [ ] Detect vendor OUI (Organizationally Unique Identifier) prefix

**Priority**: High
**Estimated Effort**: S

#### Story 1.3: Resolve Device Hostnames
**As a** network administrator
**I want** to resolve hostnames for discovered devices
**So that** I can identify devices by name

**Acceptance Criteria**:
- [ ] Perform reverse DNS lookup for each IP
- [ ] Query NetBIOS/LLMNR for Windows devices
- [ ] Query mDNS/Bonjour for Apple/Linux devices
- [ ] Handle resolution failures gracefully (use IP as fallback)

**Priority**: Medium
**Estimated Effort**: M

### Epic 2: Device Identification

#### Story 2.1: Identify Device Manufacturer
**As a** network administrator
**I want** to identify the manufacturer of discovered devices
**So that** I can categorize and understand my device population

**Acceptance Criteria**:
- [ ] Look up manufacturer from MAC OUI database
- [ ] Use local OUI database for offline operation
- [ ] Update OUI database periodically
- [ ] Handle unknown/random MACs gracefully

**Priority**: Medium
**Estimated Effort**: S

#### Story 2.2: Detect Device Type
**As a** network administrator
**I want** to infer device types from discovery data
**So that** I can automatically categorize devices

**Acceptance Criteria**:
- [ ] Infer device type from hostname patterns (e.g., "printer", "iphone")
- [ ] Infer device type from manufacturer (e.g., "Sonos" -> "speaker")
- [ ] Detect common network infrastructure (routers, switches, APs)
- [ ] Flag unknown device types for manual classification

**Priority**: Low
**Estimated Effort**: M

### Epic 3: Inventory Integration

#### Story 3.1: Compare with Existing Inventory
**As a** network administrator
**I want** to compare discovered devices with existing inventory
**So that** I can identify new devices and updates

**Acceptance Criteria**:
- [ ] Query existing devices from ra_inventory database
- [ ] Match devices by MAC address (primary key)
- [ ] Match devices by IP address (secondary)
- [ ] Categorize as: new, updated, missing (previously seen but not now)
- [ ] Generate comparison report

**Priority**: High
**Estimated Effort**: M

#### Story 3.2: Propose Inventory Updates
**As a** network administrator
**I want** to see proposed changes before committing
**So that** I can review and approve updates

**Acceptance Criteria**:
- [ ] Display new devices to be added
- [ ] Display existing devices with updated info (IP changed, etc.)
- [ ] Display devices not seen (possibly offline)
- [ ] Show confidence level for each proposal
- [ ] Allow filtering by change type

**Priority**: Medium
**Estimated Effort**: S

#### Story 3.3: Export Discovery Results
**As a** network administrator
**I want** to export discovery results to standard formats
**So that** I can process them externally or keep records

**Acceptance Criteria**:
- [ ] Export to JSON format
- [ ] Export to CSV format
- [ ] Include all collected metadata
- [ ] Include timestamps and scan metadata

**Priority**: Medium
**Estimated Effort**: S

#### Story 3.4: Interactive Device Confirmation
**As a** network administrator
**I want** to interactively review and confirm new devices before adding them
**So that** I can verify accuracy and prevent unwanted entries

**Acceptance Criteria**:
- [ ] Display each new device with collected metadata (IP, MAC, hostname, manufacturer)
- [ ] Show confidence level for device identification
- [ ] Allow user to confirm (c), skip (s), or edit (e) each device
- [ ] Allow bulk confirm/skip for multiple devices (a = all remaining)
- [ ] Support non-interactive mode with --yes flag for automation
- [ ] Provide summary of confirmed vs skipped devices

**Priority**: High
**Estimated Effort**: M

#### Story 3.5: Write Confirmed Devices to Database
**As a** network administrator
**I want** confirmed devices to be written directly to the inventory database
**So that** my inventory is immediately updated without manual import steps

**Acceptance Criteria**:
- [ ] Write confirmed devices directly to ra_inventory database
- [ ] Use database transactions for atomic operations
- [ ] Handle duplicate MAC addresses gracefully (update vs insert)
- [ ] Log all database write operations for audit
- [ ] Provide rollback capability on error
- [ ] Show success/failure status for each device write

**Priority**: High
**Estimated Effort**: M

### Epic 4: Scheduled Discovery

#### Story 4.1: Configure Scheduled Scans
**As a** network administrator
**I want** to schedule automatic discovery scans
**So that** inventory stays current without manual intervention

**Acceptance Criteria**:
- [ ] Configure scan schedule (hourly, daily, weekly)
- [ ] Configure target networks per schedule
- [ ] Enable/disable scheduled scans
- [ ] Configure quiet hours (no scanning)

**Priority**: Low (Phase 2)
**Estimated Effort**: L

---

## Functional Requirements

### Feature 1: Network Scanner
**Description**: Core network scanning engine to detect active devices on a network.

**Requirements**:
1. The system shall support ARP scanning for local network segments
2. The system shall support ICMP ping scanning for remote/routed networks
3. The system shall support concurrent scanning for performance
4. The system shall respect configurable rate limits to avoid network disruption
5. The system shall timeout unresponsive hosts after configurable duration
6. The system shall support scanning multiple networks in a single run

**User Flows**:
```
1. User specifies target network(s) via CLI or config
2. System validates network CIDR format
3. System begins scanning with progress indication
4. System collects responses and builds device list
5. User receives scan results summary
```

### Feature 2: Device Metadata Collector
**Description**: Collects additional metadata about discovered devices.

**Requirements**:
1. The system shall query local ARP cache for MAC addresses
2. The system shall perform reverse DNS lookups for hostnames
3. The system shall query NetBIOS name service (port 137) for Windows devices
4. The system shall query mDNS (port 5353) for Apple/Linux devices
5. The system shall look up manufacturer from OUI database
6. The system shall store collected metadata in structured format

### Feature 3: Inventory Comparator
**Description**: Compares discovery results with existing inventory database.

**Requirements**:
1. The system shall connect to ra_inventory PostgreSQL database
2. The system shall query existing devices for comparison
3. The system shall match devices using MAC address as primary identifier
4. The system shall detect and report new devices
5. The system shall detect and report changed device attributes
6. The system shall detect devices in inventory but not discovered

### Feature 4: Results Reporter
**Description**: Generates reports from discovery scans.

**Requirements**:
1. The system shall output human-readable summary to console
2. The system shall export detailed results to JSON
3. The system shall export detailed results to CSV
4. The system shall include scan metadata (timestamp, duration, networks)
5. The system shall support filtering results by status/type

### Feature 5: Interactive Confirmation CLI
**Description**: Interactive command-line workflow for reviewing and confirming discovered devices before writing to database.

**Requirements**:
1. The system shall display new devices in a formatted table (IP, MAC, Hostname, Manufacturer, Confidence)
2. The system shall prompt user for confirmation per device or in bulk
3. The system shall support editing device metadata before confirmation (name, device type)
4. The system shall write confirmed devices directly to ra_inventory database
5. The system shall use database transactions for atomicity
6. The system shall support --yes flag for non-interactive bulk approval
7. The system shall provide clear summary of actions taken
8. The system shall display database write results with device IDs

**User Flow**:
```
1. User runs: python -m network_tools discover --network 192.168.68.0/22
2. System scans network and compares with database
3. System displays: "Found 3 new devices, 2 updated, 1 missing"
4. System prompts: "Review 3 new devices? [Y/n]"
5. For each new device:
   - Display device details (IP, MAC, hostname, manufacturer, confidence)
   - Prompt: "[C]onfirm, [S]kip, [E]dit, [A]ll remaining, [Q]uit?"
6. System writes confirmed devices to database
7. System displays: "Added 2 devices to inventory"
8. System displays device IDs and confirmation
```

**Example CLI Output**:
```
$ python -m network_tools discover --network 192.168.68.0/22

Scanning 192.168.68.0/22... ████████████████████ 100% (254/254 hosts)
Scan completed in 2m 34s

Comparing with inventory database...

Summary:
  New devices:     3
  Updated devices: 2
  Missing devices: 1

═══════════════════════════════════════════════════════════════
NEW DEVICES (3)
═══════════════════════════════════════════════════════════════

[1/3] New Device
  IP Address:   192.168.68.145
  MAC Address:  AA:BB:CC:DD:EE:FF
  Hostname:     living-room-speaker
  Manufacturer: Sonos, Inc.
  Confidence:   High (MAC + hostname match)

  Action? [C]onfirm [S]kip [E]dit [A]ll [Q]uit: c
  ✓ Confirmed

[2/3] New Device
  IP Address:   192.168.68.201
  MAC Address:  11:22:33:44:55:66
  Hostname:     (unknown)
  Manufacturer: Unknown (randomized MAC)
  Confidence:   Low

  Action? [C]onfirm [S]kip [E]dit [A]ll [Q]uit: e

  Edit device metadata:
  Name [device-192-168-68-201]: guest-phone
  Device Type [unknown]: mobile
  ✓ Updated and confirmed

═══════════════════════════════════════════════════════════════
WRITE COMPLETE
═══════════════════════════════════════════════════════════════

Confirmed: 2 devices
Skipped:   1 device

Database writes:
  ✓ living-room-speaker (ID: 42) - Added
  ✓ guest-phone (ID: 43) - Added

Inventory updated successfully.
```

---

## Non-Functional Requirements

### Performance
- Scan a /24 network (254 hosts) in under 5 minutes
- Support concurrent scanning of up to 50 hosts
- Memory usage under 100MB during scan

### Security
- Database credentials via environment variables (never in code)
- Database access requires explicit user confirmation before writes
- No scanning of networks without explicit configuration
- Log all scan and write activities for audit

### Reliability
- Graceful handling of network errors and timeouts
- Resumable scans after interruption
- Retry logic for transient failures

### Compatibility
- Windows 11 primary platform (also support Linux/macOS)
- Python 3.11+
- PostgreSQL 15+ (ra_inventory database)

---

## User Personas

### Persona 1: Home Network Administrator
- **Role**: Personal user managing home network
- **Goals**: Know all devices on home network, detect unknown devices
- **Pain Points**: Manual tracking is tedious, devices change IPs
- **Tech Savviness**: Medium-High

### Persona 2: Small Business IT
- **Role**: IT administrator for small business
- **Goals**: Asset inventory, security monitoring, compliance
- **Pain Points**: Shadow IT, unauthorized devices, inventory drift
- **Tech Savviness**: High

---

## Data Requirements

### Data Entities (Discovery Output)

1. **DiscoveredDevice**
   - ip_address: INET, Required
   - mac_address: MACADDR, Optional (not available cross-subnet)
   - hostname: VARCHAR(255), Optional
   - manufacturer: VARCHAR(255), Optional
   - device_type_guess: VARCHAR(100), Optional
   - last_seen: TIMESTAMPTZ, Required
   - response_time_ms: INTEGER, Optional
   - discovery_method: VARCHAR(50), Required (arp/icmp/tcp)

2. **DiscoveryScan**
   - scan_id: UUID, Required
   - started_at: TIMESTAMPTZ, Required
   - completed_at: TIMESTAMPTZ, Optional
   - networks_scanned: CIDR[], Required
   - devices_found: INTEGER, Required
   - status: VARCHAR(50), Required (running/completed/failed)

### Database Integration
- **Target Database**: ra_inventory (managed by ra-infrastructure)
- **Access Mode**: READ/WRITE (read for comparison, write for confirmed devices)
- **Transaction Support**: Required for atomic device writes
- **Connection Pooling**: Recommended via psycopg3 connection pool
- **Schema Changes**: Submit change requests to ra-infrastructure per policy
- **Connection**: Via psycopg3

---

## Integration Requirements

### External Systems

1. **ra-infrastructure Database (ra_inventory)**
   - Purpose: Compare discovered devices with existing inventory; write confirmed devices
   - Integration type: PostgreSQL direct connection
   - Authentication: Username/password via environment variables
   - Data exchanged: Query and write to devices, sites, networks tables
   - Access: READ/WRITE

2. **IEEE OUI Database**
   - Purpose: MAC address to manufacturer lookup
   - Integration type: Local file (downloaded/cached)
   - Update frequency: Monthly
   - Source: IEEE public OUI registry

### APIs Required
- None for MVP (CLI-based tool)
- Future: REST API for integration with other tools

---

## Constraints & Assumptions

### Constraints
- **Schema**: Cannot modify ra_inventory database schema (owned by ra-infrastructure)
- **Technology**: Python 3.11+, must work on Windows 11
- **Permissions**: May require elevated privileges for ARP scanning
- **Network**: Must be on same network segment for ARP scans

### Assumptions
- User has network connectivity to target subnets
- User has credentials for ra_inventory database (read/write access)
- Target devices respond to ICMP or ARP
- Network allows discovery traffic (not blocked by firewall)

---

## Out of Scope

Explicitly not included in this release:
- Database schema modifications (owned by ra-infrastructure)
- Port scanning / service detection
- Vulnerability scanning
- SNMP-based discovery
- Agent-based discovery
- Web UI / dashboard
- Alerting / notifications
- Historical trending

---

## Dependencies

### Internal Dependencies
- Depends on: ra-infrastructure database being available
- Depends on: Network configuration being defined (which networks to scan)

### External Dependencies
- IEEE OUI database for manufacturer lookup
- Python networking libraries (scapy, python-nmap, or similar)
- psycopg3 for PostgreSQL connectivity

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Network scanning blocked by firewall | High | Medium | Support multiple scan methods; document requirements |
| Elevated privileges required | Medium | High | Document requirements; provide non-privileged fallback |
| Database connection issues | Medium | Low | Connection pooling; retry logic; clear error messages |
| Incomplete device detection | Medium | Medium | Multiple discovery methods; manual entry fallback |
| MAC address randomization | Medium | Medium | Secondary matching by hostname/IP pattern |

---

## Glossary

- **ARP**: Address Resolution Protocol - maps IP addresses to MAC addresses
- **CIDR**: Classless Inter-Domain Routing - network addressing notation (e.g., 192.168.1.0/24)
- **MAC**: Media Access Control address - unique hardware identifier
- **OUI**: Organizationally Unique Identifier - first 3 bytes of MAC identifying manufacturer
- **mDNS**: Multicast DNS - used for local network name resolution (Bonjour)
- **NetBIOS**: Network Basic Input/Output System - Windows network naming

---

## References

- [ra-infrastructure DATABASE.md](file:///C:/Users/ranand/workspace/personal/software/ra-infrastructure/docs/DATABASE.md) - Database schema reference
- [IEEE OUI Registry](https://standards-oui.ieee.org/) - MAC address vendor lookup

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | Claude Code | Initial draft |
| 1.1 | 2025-11-29 | Claude Code | Added Story 3.4 (Interactive Device Confirmation), Story 3.5 (Generate Import Artifacts), Feature 5 (Interactive CLI Workflow), ImportArtifact data entity, ra-infrastructure import process integration. Updated Out of Scope to clarify import file generation vs direct DB writes. |
| 1.2 | 2025-11-29 | Claude Code | Aligned with NETWORK-TOOLS-DECISIONS-2025-11-29: Changed to direct database READ/WRITE access, removed SQL file generation, updated Story 3.5 and Feature 5 for direct writes, removed ImportArtifact entity and ra-infrastructure import process. |
