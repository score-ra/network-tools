# Sprint Backlog: Snipe-IT API Integration

**Sprint ID**: SPRINT-02
**Sprint Duration**: 1 week
**Start Date**: 2025-12-06
**Status**: Planning

---

## Sprint Goal

Replace PostgreSQL database integration with Snipe-IT API for device inventory management. Enable network discovery to create and update hardware assets directly in Snipe-IT.

---

## Prerequisites

Before starting implementation, ensure:

- [ ] Snipe-IT instance is running (`http://localhost:8082`)
- [ ] API key is configured in `.env` (`SNIPEIT_API_KEY`)
- [ ] Custom fields exist in Snipe-IT:
  - MAC Address (`_snipeit_mac_address_1`)
  - IP Address (`_snipeit_ip_address_2`)
- [ ] Network category exists (id: 4)
- [ ] Default model created: "Unknown Network Device"

---

## Sprint Backlog

### Phase 0: Cleanup (Remove Database Code)

| ID | Task | Description | Effort | Status |
|----|------|-------------|--------|--------|
| SI-001 | Remove database module | Delete `src/network_tools/db/` directory | XS | To Do |
| SI-002 | Remove database tests | Delete `tests/test_db/` directory | XS | To Do |
| SI-003 | Update dependencies | Remove psycopg from requirements.txt and pyproject.toml | XS | To Do |
| SI-004 | Clean .env.example | Remove DB_* variables, keep SNIPEIT_* | XS | To Do |

### Phase 1: Snipe-IT Client Foundation

| ID | Task | Description | Effort | Status |
|----|------|-------------|--------|--------|
| SI-005 | Create snipeit module structure | Create `src/network_tools/snipeit/` with __init__.py | XS | To Do |
| SI-006 | Implement SnipeITClient class | Base client with auth, requests, error handling | M | To Do |
| SI-007 | Add configuration settings | Add SNIPEIT_* config to config.py | S | To Do |
| SI-008 | Implement asset list/search | GET /hardware with pagination and search | S | To Do |
| SI-009 | Implement asset get by tag | GET /hardware/bytag/{tag} | XS | To Do |
| SI-010 | Implement asset create | POST /hardware with custom fields | M | To Do |
| SI-011 | Implement asset update | PATCH /hardware/{id} | S | To Do |

### Phase 2: Discovery Integration

| ID | Task | Description | Effort | Status |
|----|------|-------------|--------|--------|
| SI-012 | Create asset mapper | Map DiscoveredDevice to Snipe-IT payload | S | To Do |
| SI-013 | Implement asset comparison | Compare discovered vs Snipe-IT inventory | M | To Do |
| SI-014 | Update discover command | Replace DB calls with Snipe-IT API | L | To Do |
| SI-015 | Update status command | Query Snipe-IT for asset counts | S | To Do |

### Phase 3: Testing & Documentation

| ID | Task | Description | Effort | Status |
|----|------|-------------|--------|--------|
| SI-016 | Write client unit tests | Test SnipeITClient with mocked responses | M | To Do |
| SI-017 | Update CLI tests | Mock Snipe-IT API instead of database | M | To Do |
| SI-018 | Update config tests | Test SNIPEIT_* configuration loading | S | To Do |
| SI-019 | Update documentation | Update start-here.md, README | S | To Do |

---

## Task Details

### SI-006: Implement SnipeITClient class

**File**: `src/network_tools/snipeit/client.py`

**Requirements**:
```python
class SnipeITClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """Initialize client with authentication."""

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make authenticated API request with error handling."""

    def list_hardware(self, limit: int = 50, offset: int = 0, search: str = None) -> list:
        """List hardware assets with pagination."""

    def get_hardware_by_tag(self, asset_tag: str) -> dict | None:
        """Get single asset by asset tag."""

    def get_hardware_by_id(self, asset_id: int) -> dict | None:
        """Get single asset by ID."""

    def create_hardware(self, payload: dict) -> dict:
        """Create new hardware asset."""

    def update_hardware(self, asset_id: int, payload: dict) -> dict:
        """Update existing hardware asset."""

    def search_by_mac(self, mac_address: str) -> dict | None:
        """Search for asset by MAC address custom field."""

    def search_by_ip(self, ip_address: str) -> dict | None:
        """Search for asset by IP address custom field."""

    def test_connection(self) -> bool:
        """Test API connectivity and authentication."""
```

**Error Handling**:
- `SnipeITConnectionError` - Network/connection failures
- `SnipeITAuthError` - Authentication failures (401)
- `SnipeITNotFoundError` - Asset not found (404)
- `SnipeITValidationError` - Validation errors from API

---

### SI-007: Add configuration settings

**File**: `src/network_tools/config.py`

**Changes**:
```python
# Remove:
# db_host, db_port, db_name, db_user, db_password, db_dsn

# Add:
@dataclass
class Config:
    # ... existing fields ...

    # Snipe-IT Configuration
    snipeit_base_url: str = "http://localhost:8082/api/v1"
    snipeit_api_key: str = ""
    snipeit_timeout: int = 30
    snipeit_retry_count: int = 3

    # Default IDs (configurable)
    snipeit_network_category_id: int = 4
    snipeit_default_status_id: int = 2  # Ready to Deploy
    snipeit_default_model_id: int = 0   # Must be set

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            snipeit_base_url=os.getenv("SNIPEIT_BASE_URL", "http://localhost:8082/api/v1"),
            snipeit_api_key=os.getenv("SNIPEIT_API_KEY", ""),
            snipeit_timeout=int(os.getenv("SNIPEIT_TIMEOUT", "30")),
            # ... other fields
        )
```

---

### SI-012: Create asset mapper

**File**: `src/network_tools/snipeit/mapper.py`

**Function**:
```python
def discovered_device_to_asset(device: DiscoveredDevice, config: Config) -> dict:
    """
    Map a DiscoveredDevice to Snipe-IT asset creation payload.

    Returns:
        {
            "name": "device-hostname or manufacturer-ip",
            "asset_tag": "NET-{MAC_LAST6}",
            "model_id": config.snipeit_default_model_id,
            "status_id": config.snipeit_default_status_id,
            "_snipeit_mac_address_1": "AA:BB:CC:DD:EE:FF",
            "_snipeit_ip_address_2": "192.168.68.100",
            "notes": "Discovered: 2025-12-06\nManufacturer: Sonos, Inc."
        }
    """
```

---

### SI-014: Update discover command

**File**: `src/network_tools/cli/main.py`

**Changes**:
1. Remove imports from `network_tools.db`
2. Import from `network_tools.snipeit`
3. Replace `get_site_by_slug()` with Snipe-IT category filter
4. Replace `get_device_by_mac()` with `client.search_by_mac()`
5. Replace `insert_device()` with `client.create_hardware()`
6. Replace `close_pool()` cleanup with nothing (no connection pool)

**New Flow**:
```
1. Initialize SnipeITClient from config
2. Test connection (fail fast if unavailable)
3. Scan network (unchanged)
4. Fetch existing Network category assets from Snipe-IT
5. Compare by MAC address
6. Interactive confirmation (unchanged logic)
7. Create/update assets via API
8. Display results
```

---

### SI-015: Update status command

**File**: `src/network_tools/cli/main.py`

**Changes**:
```python
@cli.command()
def status():
    """Check Snipe-IT connection and show inventory summary."""
    config = Config.from_env()
    client = SnipeITClient(config.snipeit_base_url, config.snipeit_api_key)

    # Test connection
    if not client.test_connection():
        console.print("[red]Cannot connect to Snipe-IT[/red]")
        return

    # Get counts
    all_assets = client.list_hardware(limit=1)  # Just get total
    network_assets = client.list_hardware(limit=500, category_id=4)

    console.print(f"Snipe-IT Status: [green]Connected[/green]")
    console.print(f"Total Assets: {all_assets.get('total', 0)}")
    console.print(f"Network Assets: {len(network_assets)}")
```

---

## Environment Configuration

### .env.example (Updated)

```ini
# Application
APP_NAME=network-tools
ENV=development
LOG_LEVEL=INFO

# Snipe-IT API
SNIPEIT_BASE_URL=http://localhost:8082/api/v1
SNIPEIT_API_KEY=your_api_key_here
SNIPEIT_TIMEOUT=30

# Snipe-IT Default IDs
SNIPEIT_NETWORK_CATEGORY_ID=4
SNIPEIT_DEFAULT_STATUS_ID=2
SNIPEIT_DEFAULT_MODEL_ID=0

# Network Settings
DEFAULT_NETWORK=192.168.68.0/22
SCAN_TIMEOUT=5
SCAN_CONCURRENCY=50

# OUI Database
OUI_DATABASE_PATH=./data/oui.txt
```

---

## Dependencies Update

### requirements.txt

**Remove**:
```
psycopg[binary]>=3.1
```

**Add**:
```
requests>=2.31.0
```

### pyproject.toml

**Remove from dependencies**:
```
"psycopg[binary]>=3.1",
"psycopg-pool>=3.1",
```

**Add to dependencies**:
```
"requests>=2.31.0",
```

---

## File Changes Summary

### Files to DELETE
| Path | Reason |
|------|--------|
| `src/network_tools/db/connection.py` | PostgreSQL-specific |
| `src/network_tools/db/queries.py` | SQL queries |
| `src/network_tools/db/__init__.py` | DB module exports |
| `tests/test_db/test_connection.py` | DB connection tests |
| `tests/test_db/test_queries.py` | DB query tests |
| `tests/test_db/__init__.py` | Test module |

### Files to CREATE
| Path | Purpose |
|------|---------|
| `src/network_tools/snipeit/__init__.py` | Module exports |
| `src/network_tools/snipeit/client.py` | API client |
| `src/network_tools/snipeit/models.py` | Response dataclasses |
| `src/network_tools/snipeit/mapper.py` | Device to asset mapping |
| `src/network_tools/snipeit/exceptions.py` | Custom exceptions |
| `tests/test_snipeit/__init__.py` | Test module |
| `tests/test_snipeit/test_client.py` | Client unit tests |

### Files to MODIFY
| Path | Changes |
|------|---------|
| `src/network_tools/config.py` | Remove DB, add Snipe-IT config |
| `src/network_tools/cli/main.py` | Use Snipe-IT instead of DB |
| `src/network_tools/db/models.py` | Move to snipeit/models.py or keep for scanner |
| `.env.example` | Remove DB vars, document Snipe-IT vars |
| `requirements.txt` | Swap psycopg for requests |
| `pyproject.toml` | Update dependencies |
| `tests/test_cli/test_main.py` | Mock Snipe-IT API |
| `tests/test_config.py` | Test Snipe-IT config |
| `start-here.md` | Update sprint context |
| `README.md` | Update setup instructions |

---

## Definition of Done

A task is complete when:
- [ ] Code implemented and tested locally
- [ ] Unit tests written with ≥80% coverage
- [ ] No linter errors (`flake8`)
- [ ] Code formatted (`black`)
- [ ] Manual testing against real Snipe-IT instance
- [ ] Documentation updated if applicable

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Snipe-IT not running during dev | High | Use mock responses for unit tests |
| API key permissions insufficient | Medium | Document required permissions |
| Custom field IDs change | Low | Make configurable, validate on startup |
| Breaking existing scanner | High | Keep scanner module unchanged |

---

## Sprint Summary

| Category | Count | Effort |
|----------|-------|--------|
| Phase 0 (Cleanup) | 4 tasks | XS |
| Phase 1 (Client) | 7 tasks | M-L |
| Phase 2 (Integration) | 4 tasks | M-L |
| Phase 3 (Testing) | 4 tasks | M |
| **Total** | **19 tasks** | |

---

**Document Version**: 1.0
**Created**: 2025-12-06
**Author**: Claude Code
