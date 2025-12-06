# Product Requirement Document (PRD)

**Project Name**: Snipe-IT API Integration for Network Device Discovery
**Version**: 1.0
**Date**: 2025-12-06
**Owner**: personal-ra
**Status**: Draft

---

## Executive Summary

This PRD defines requirements for integrating the network-tools device discovery system with Snipe-IT asset management. The system will scan networks to detect devices, collect device metadata (MAC address, IP address, hostname, manufacturer), and sync discovered devices with Snipe-IT via its REST API. This replaces the previous direct PostgreSQL database approach with a standardized asset management integration.

---

## Business Objectives

### Goals
1. Integrate network discovery with Snipe-IT for centralized asset management
2. Automatically create and update hardware assets in Snipe-IT from discovered devices
3. Leverage Snipe-IT's existing asset tracking features (locations, categories, custom fields)
4. Enable unified inventory view across network devices and other IT assets

### Success Metrics
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| API integration reliability | N/A | 99%+ successful API calls | Sprint 1 |
| Discovery-to-asset sync time | N/A | < 30 seconds per device | Sprint 1 |
| Asset deduplication accuracy | N/A | 100% (by MAC address) | Sprint 1 |
| Manual data entry reduction | 50% manual | 90% automated | Sprint 2 |

---

## User Stories

### Epic 1: Snipe-IT API Client

#### Story 1.1: Connect to Snipe-IT API
**As a** network administrator
**I want** to connect to my Snipe-IT instance via API
**So that** I can programmatically manage network device assets

**Acceptance Criteria**:
- [ ] Configure API base URL via environment variable
- [ ] Authenticate using Bearer token from SNIPEIT_API_KEY
- [ ] Handle API rate limiting gracefully
- [ ] Provide clear error messages for authentication failures
- [ ] Support both localhost and network-accessible URLs

**Priority**: High
**Estimated Effort**: S

#### Story 1.2: Query Existing Hardware Assets
**As a** network administrator
**I want** to query existing assets in Snipe-IT
**So that** I can compare with discovered devices

**Acceptance Criteria**:
- [ ] List all hardware assets with pagination
- [ ] Search assets by name, asset tag, or serial
- [ ] Get asset by specific asset tag
- [ ] Filter assets by category (e.g., "Network")
- [ ] Retrieve custom field values (MAC, IP addresses)

**Priority**: High
**Estimated Effort**: M

#### Story 1.3: Create Hardware Assets
**As a** network administrator
**I want** to create new assets in Snipe-IT from discovered devices
**So that** my asset inventory stays current

**Acceptance Criteria**:
- [ ] Create asset with required fields (name, asset_tag, model_id, status_id)
- [ ] Set custom fields for MAC address and IP address
- [ ] Auto-generate unique asset tags for new devices
- [ ] Set appropriate category (Network) for discovered devices
- [ ] Handle validation errors from Snipe-IT API

**Priority**: High
**Estimated Effort**: M

#### Story 1.4: Update Existing Assets
**As a** network administrator
**I want** to update existing assets when device info changes
**So that** IP address and other metadata stays current

**Acceptance Criteria**:
- [ ] Update asset by ID using PATCH endpoint
- [ ] Update IP address custom field when device IP changes
- [ ] Update notes field with discovery metadata
- [ ] Preserve existing asset data not related to discovery
- [ ] Log all updates for audit trail

**Priority**: Medium
**Estimated Effort**: S

### Epic 2: Device Discovery Integration

#### Story 2.1: Map Discovered Devices to Snipe-IT Assets
**As a** network administrator
**I want** discovered devices mapped to Snipe-IT asset format
**So that** they can be imported correctly

**Acceptance Criteria**:
- [ ] Map MAC address to `_snipeit_mac_address_1` custom field
- [ ] Map IP address to `_snipeit_ip_address_2` custom field
- [ ] Generate device name from hostname or manufacturer + IP
- [ ] Generate unique asset tag (e.g., "NET-{MAC_SUFFIX}")
- [ ] Set default model_id for "Unknown Network Device"
- [ ] Set default status_id to "Ready to Deploy" (id: 2)

**Priority**: High
**Estimated Effort**: S

#### Story 2.2: Compare Discovered Devices with Snipe-IT Inventory
**As a** network administrator
**I want** to compare discovered devices with existing Snipe-IT assets
**So that** I can identify new, updated, and missing devices

**Acceptance Criteria**:
- [ ] Query all Network category assets from Snipe-IT
- [ ] Match devices by MAC address (primary identifier)
- [ ] Match devices by IP address (secondary identifier)
- [ ] Categorize as: new, updated (IP changed), existing (unchanged)
- [ ] Identify assets in Snipe-IT not seen on network (missing)
- [ ] Generate comparison summary report

**Priority**: High
**Estimated Effort**: M

#### Story 2.3: Interactive Confirmation Workflow
**As a** network administrator
**I want** to interactively review and confirm new devices
**So that** I can verify accuracy before adding to Snipe-IT

**Acceptance Criteria**:
- [ ] Display each new device with collected metadata
- [ ] Show confidence level for device identification
- [ ] Allow user to [C]onfirm, [S]kip, [E]dit, [A]ll, [Q]uit
- [ ] Support --yes flag for non-interactive automation
- [ ] Provide summary of confirmed vs skipped devices

**Priority**: High
**Estimated Effort**: M

#### Story 2.4: Sync Confirmed Devices to Snipe-IT
**As a** network administrator
**I want** confirmed devices written to Snipe-IT
**So that** my asset inventory is immediately updated

**Acceptance Criteria**:
- [ ] Create new assets in Snipe-IT for confirmed devices
- [ ] Update existing assets if device info changed
- [ ] Handle API errors gracefully with retry logic
- [ ] Display success/failure status for each device
- [ ] Show Snipe-IT asset IDs for newly created assets

**Priority**: High
**Estimated Effort**: M

### Epic 3: Asset Lookup Utilities

#### Story 3.1: Search Assets by MAC Address
**As a** network administrator
**I want** to find Snipe-IT assets by MAC address
**So that** I can quickly look up device information

**Acceptance Criteria**:
- [ ] Search using MAC address custom field
- [ ] Support various MAC format inputs (colons, dashes, no separator)
- [ ] Return matching asset details including location
- [ ] Handle no results gracefully

**Priority**: Medium
**Estimated Effort**: S

#### Story 3.2: Search Assets by IP Address
**As a** network administrator
**I want** to find Snipe-IT assets by IP address
**So that** I can identify which device has a specific IP

**Acceptance Criteria**:
- [ ] Search using IP address custom field
- [ ] Return matching asset with full details
- [ ] Handle multiple assets with same IP (shouldn't happen, but warn)

**Priority**: Medium
**Estimated Effort**: S

#### Story 3.3: List Network Category Assets
**As a** network administrator
**I want** to list all network devices from Snipe-IT
**So that** I can see the complete network inventory

**Acceptance Criteria**:
- [ ] Filter assets by Network category (id: 4)
- [ ] Display in formatted table with key fields
- [ ] Support output as JSON for scripting
- [ ] Include pagination for large inventories

**Priority**: Low
**Estimated Effort**: S

---

## Functional Requirements

### Feature 1: Snipe-IT API Client
**Description**: Python client for interacting with Snipe-IT REST API.

**Requirements**:
1. The system shall authenticate using Bearer token from environment variable
2. The system shall support configurable base URL for API endpoint
3. The system shall handle HTTP errors with appropriate retries
4. The system shall respect rate limiting (429 responses)
5. The system shall validate responses and parse JSON correctly
6. The system shall log all API requests for debugging

**Configuration**:
```python
SNIPEIT_BASE_URL = "http://localhost:8082/api/v1"
SNIPEIT_API_KEY = "<bearer_token>"
SNIPEIT_TIMEOUT = 30  # seconds
SNIPEIT_RETRY_COUNT = 3
```

### Feature 2: Asset CRUD Operations
**Description**: Create, read, update operations for hardware assets.

**Requirements**:
1. The system shall list hardware assets with pagination (limit/offset)
2. The system shall search assets by query string
3. The system shall get single asset by ID or asset tag
4. The system shall create assets with required and custom fields
5. The system shall update assets using PATCH method
6. The system shall handle custom field formats correctly

**API Endpoints Used**:
| Operation | Method | Endpoint |
|-----------|--------|----------|
| List assets | GET | `/hardware?limit=100&offset=0` |
| Search | GET | `/hardware?search={query}` |
| Get by tag | GET | `/hardware/bytag/{tag}` |
| Get by ID | GET | `/hardware/{id}` |
| Create | POST | `/hardware` |
| Update | PATCH | `/hardware/{id}` |

### Feature 3: Discovery-to-Asset Mapping
**Description**: Maps discovered device data to Snipe-IT asset format.

**Requirements**:
1. The system shall map DiscoveredDevice to Snipe-IT asset payload
2. The system shall generate unique asset tags from MAC address
3. The system shall use default model_id for unknown devices
4. The system shall set custom fields for MAC and IP addresses
5. The system shall include discovery metadata in notes field

**Mapping Table**:
| Discovered Field | Snipe-IT Field | Notes |
|------------------|----------------|-------|
| mac_address | `_snipeit_mac_address_1` | Custom field |
| ip_address | `_snipeit_ip_address_2` | Custom field |
| hostname | `name` | Falls back to manufacturer + IP |
| manufacturer | Notes or model lookup | Informational |
| last_seen | `notes` | Appended to notes |
| - | `asset_tag` | Generated: NET-{MAC_LAST6} |
| - | `model_id` | Default: "Unknown Network Device" |
| - | `status_id` | Default: 2 (Ready to Deploy) |

### Feature 4: Interactive CLI Workflow
**Description**: CLI commands for discovery and Snipe-IT sync.

**Commands**:
```bash
# Discover devices and sync to Snipe-IT
python -m network_tools discover --network 192.168.68.0/22

# Check Snipe-IT connection and asset counts
python -m network_tools status

# Search for asset by MAC
python -m network_tools search --mac AA:BB:CC:DD:EE:FF

# Search for asset by IP
python -m network_tools search --ip 192.168.68.100
```

**Example Output**:
```
$ python -m network_tools discover --network 192.168.68.0/22

Scanning 192.168.68.0/22... [████████████████████] 100%
Scan completed in 2m 34s

Comparing with Snipe-IT inventory...

Summary:
  New devices:     3
  Updated devices: 2
  Unchanged:       12

═══════════════════════════════════════════════════════════════
NEW DEVICES (3)
═══════════════════════════════════════════════════════════════

[1/3] New Device
  IP Address:   192.168.68.145
  MAC Address:  AA:BB:CC:DD:EE:FF
  Hostname:     living-room-speaker
  Manufacturer: Sonos, Inc.

  Action? [C]onfirm [S]kip [E]dit [A]ll [Q]uit: c
  ✓ Confirmed

═══════════════════════════════════════════════════════════════
SYNC COMPLETE
═══════════════════════════════════════════════════════════════

Synced to Snipe-IT:
  ✓ living-room-speaker (Asset Tag: NET-DDEEFF) - Created
  ✓ guest-phone (Asset Tag: NET-445566) - Created

2 assets added to Snipe-IT inventory.
```

---

## Non-Functional Requirements

### Performance
- API response handling: < 5 seconds per request
- Bulk asset creation: 50+ assets without timeout
- Memory usage: < 100MB during sync operations

### Security
- API key stored in environment variable (never in code)
- HTTPS supported for production deployments
- No sensitive data logged (API key masked in logs)
- Input validation for all user-provided data

### Reliability
- Automatic retry on transient API failures (3 attempts)
- Graceful degradation when Snipe-IT unavailable
- Clear error messages for API failures
- No data loss on interrupted sync operations

### Compatibility
- Python 3.11+
- Snipe-IT v6.x API
- Windows 11 primary platform (also Linux/macOS)
- Works with both HTTP (local) and HTTPS (production)

---

## Data Requirements

### Snipe-IT Custom Fields Used

| Field Name | DB Column | Format | Purpose |
|------------|-----------|--------|---------|
| MAC Address | `_snipeit_mac_address_1` | MAC | Device identification |
| IP Address | `_snipeit_ip_address_2` | IP | Network location |

### Snipe-IT Reference Data

| Entity | ID | Name | Usage |
|--------|----|----- |-------|
| Category | 4 | Network | All discovered devices |
| Status | 2 | Ready to Deploy | Default for new devices |
| Status | 4 | Deployed | For active devices |
| Location | 18 | Unknown Location | Default when unknown |

### Asset Tag Generation
- Format: `NET-{MAC_LAST_6_CHARS}`
- Example: MAC `AA:BB:CC:DD:EE:FF` -> `NET-DDEEFF`
- Ensures uniqueness via MAC address

---

## Integration Requirements

### External Systems

1. **Snipe-IT Asset Management**
   - Purpose: Central asset inventory management
   - Integration type: REST API (JSON)
   - Authentication: Bearer token
   - Data exchanged: Hardware assets (create, read, update)
   - Base URL: Configurable (default: `http://localhost:8082/api/v1`)

2. **IEEE OUI Database**
   - Purpose: MAC address to manufacturer lookup
   - Integration type: Local file (unchanged from previous)
   - Usage: Populate manufacturer info for device identification

### APIs Required
- Snipe-IT API v1: Hardware, Categories, Models, Status Labels
- Reference: https://snipe-it.readme.io/reference/api-overview

---

## Constraints & Assumptions

### Constraints
- **Schema**: Must use existing Snipe-IT custom fields (MAC Address, IP Address)
- **Model**: Need a default model in Snipe-IT for "Unknown Network Device"
- **Rate Limits**: Snipe-IT may have rate limiting; must handle gracefully
- **Network**: Requires network access to Snipe-IT instance

### Assumptions
- Snipe-IT instance is running and accessible
- API key has permissions for hardware CRUD operations
- MAC Address and IP Address custom fields are configured
- Network category (id: 4) exists in Snipe-IT

---

## Out of Scope

Explicitly not included in this release:
- Direct database access (removed - using API only)
- Creating new categories/models/manufacturers in Snipe-IT
- Snipe-IT user management
- Asset checkout/checkin operations
- Maintenance/audit log operations
- File/image uploads to Snipe-IT
- Webhook integrations

---

## Dependencies

### Internal Dependencies
- Network scanner module (existing)
- OUI lookup module (existing)
- Configuration module (needs update)

### External Dependencies
- Snipe-IT v6.x instance
- `requests` or `httpx` library for HTTP
- Snipe-IT API key with appropriate permissions

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Snipe-IT API unavailable | High | Low | Graceful error handling; offline mode for scanning |
| API rate limiting | Medium | Medium | Implement backoff and retry logic |
| Custom fields not configured | High | Low | Document prerequisites; validate on startup |
| Model/category IDs change | Medium | Low | Make IDs configurable; validate on startup |
| Duplicate asset tags | Medium | Low | MAC-based generation ensures uniqueness |

---

## Migration Notes

### Removed Components (from previous PostgreSQL approach)
- `src/network_tools/db/connection.py` - PostgreSQL connection pool
- `src/network_tools/db/queries.py` - SQL queries
- `tests/test_db/` - Database tests
- `psycopg[binary]` dependency
- `psycopg-pool` dependency
- `DB_*` environment variables

### New Components
- `src/network_tools/snipeit/client.py` - API client
- `src/network_tools/snipeit/models.py` - Response models
- `tests/test_snipeit/` - API client tests
- `requests` or `httpx` dependency
- `SNIPEIT_*` environment variables

---

## Glossary

- **Snipe-IT**: Open-source IT asset management software
- **Bearer Token**: API authentication method using Authorization header
- **Asset Tag**: Unique identifier for assets in Snipe-IT
- **Custom Field**: User-defined fields in Snipe-IT for extended attributes
- **Hardware**: Snipe-IT entity type for physical assets

---

## References

- [Snipe-IT API Integration Guide](../../../snipeit-asset-management/docs/snipeit-api-integration-guide.md)
- [Snipe-IT API Reference](https://snipe-it.readme.io/reference/api-overview)
- [Previous Device Discovery PRD](device-discovery-prd.md)

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-06 | Claude Code | Initial draft - Snipe-IT API integration replacing PostgreSQL |
