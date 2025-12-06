# Network-Tools Architecture

**Version**: 2.0
**Last Updated**: 2025-12-06
**Status**: Active

---

## Overview

Network-tools is a Python-based utility for automated network device discovery and inventory management. It scans local networks to discover devices, identifies manufacturers via MAC address lookup, and integrates discovered devices with Snipe-IT asset management via REST API.

**Key Value Proposition**: Automate the tedious process of manually tracking network devices by combining network scanning with an interactive confirmation workflow and Snipe-IT integration.

---

## Capabilities

| Capability | Description |
|------------|-------------|
| Network Scanning | ARP-based discovery and ICMP ping sweep |
| Device Discovery | Identify active hosts on network segments |
| OUI Lookup | MAC-to-manufacturer mapping using built-in database |
| Device Type Inference | Guess device type based on manufacturer patterns |
| Inventory Comparison | Compare discovered devices against Snipe-IT inventory |
| Interactive CLI | Confirm/skip/edit devices before adding to inventory |
| Snipe-IT Integration | Query, create, and update assets via REST API |
| Asset Search | Find assets by MAC or IP address |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    network-tools (Python)                    │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Network Scanner │  │ Interactive CLI │                   │
│  │ (ARP/ICMP)      │─►│ Confirm Devices │                   │
│  └─────────────────┘  └────────┬────────┘                   │
│           │                    │                             │
│           ▼                    │                             │
│  ┌─────────────────┐           │                             │
│  │  OUI Lookup     │           │                             │
│  │  (Manufacturer) │           │                             │
│  └─────────────────┘           │                             │
│                                ▼                             │
│                       ┌─────────────────┐                    │
│                       │ Snipe-IT Client │                    │
│                       │ (REST API)      │                    │
│                       └────────┬────────┘                    │
│                                │ HTTPS                       │
└────────────────────────────────┼────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────┐
│                    Snipe-IT Asset Management                   │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │  REST API       │  │  Web Dashboard  │                     │
│  │  /api/v1/*      │  │  localhost:8082 │                     │
│  └─────────────────┘  └─────────────────┘                     │
└───────────────────────────────────────────────────────────────┘
```

---

## Component Responsibilities

| Component | Owner | Responsibilities |
|-----------|-------|------------------|
| Network Scanner | network-tools | ARP/ICMP scanning, host discovery |
| OUI Lookup | network-tools | MAC-to-manufacturer mapping |
| Interactive CLI | network-tools | User confirmation workflow |
| Snipe-IT Client | network-tools | REST API client for asset operations |
| Snipe-IT | External | Asset management, storage, web UI |

---

## Snipe-IT Integration

### API Connection

- **Protocol**: HTTPS REST API
- **Authentication**: Bearer token (API key)
- **Base URL**: Configurable via `SNIPEIT_BASE_URL`
- **Timeout**: Configurable via `SNIPEIT_TIMEOUT`

### Key Endpoints Used

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Test connection | `/hardware?limit=1` | GET |
| List assets | `/hardware` | GET |
| Get by asset tag | `/hardware/bytag/{tag}` | GET |
| Create asset | `/hardware` | POST |
| Update asset | `/hardware/{id}` | PATCH |
| Get categories | `/categories` | GET |

### Custom Fields

Network devices use custom fields for MAC and IP addresses:

| Field Name | Field ID | Purpose |
|------------|----------|---------|
| MAC Address | `_snipeit_mac_address_1` | Device MAC address |
| IP Address | `_snipeit_ip_address_2` | Device IP address |

### Asset Mapping

Discovered devices are mapped to Snipe-IT assets:

| Discovery Field | Snipe-IT Field | Notes |
|-----------------|----------------|-------|
| MAC Address | Custom field | Primary device identifier |
| IP Address | Custom field | Current IP |
| Hostname | `name` | Falls back to manufacturer + IP |
| Manufacturer | `notes` | Included in notes |
| - | `asset_tag` | Generated from MAC: `NET-DDEEFF` |
| - | `model_id` | Configurable default |
| - | `status_id` | Configurable default |

---

## CLI Commands

| Command | Purpose |
|---------|---------|
| `network-tools status` | Show Snipe-IT connection status and asset counts |
| `network-tools discover` | Scan network and sync devices to Snipe-IT |
| `network-tools search` | Search for asset by MAC or IP address |

### Discovery Options

| Option | Description |
|--------|-------------|
| `--network <CIDR>` | Network to scan (e.g., 192.168.1.0/24) |
| `--yes` | Auto-confirm all new devices |
| `--no-ping` | Skip ICMP ping sweep (ARP only) |

### Search Options

| Option | Description |
|--------|-------------|
| `--mac <address>` | Search by MAC address |
| `--ip <address>` | Search by IP address |

---

## Environment Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `SNIPEIT_BASE_URL` | Snipe-IT API base URL | `http://localhost:8082/api/v1` |
| `SNIPEIT_API_KEY` | API key for authentication | (required) |
| `SNIPEIT_TIMEOUT` | Request timeout in seconds | `30` |
| `SNIPEIT_RETRY_COUNT` | Number of retries | `3` |
| `SNIPEIT_NETWORK_CATEGORY_ID` | Category ID for network assets | `4` |
| `SNIPEIT_DEFAULT_STATUS_ID` | Default status for new assets | `2` |
| `SNIPEIT_DEFAULT_MODEL_ID` | Default model for new assets | `0` |
| `DEFAULT_NETWORK` | Default scan CIDR | `192.168.68.0/22` |

---

## Module Structure

```
src/network_tools/
├── __init__.py          # Package exports, version
├── config.py            # Configuration from environment
├── logging.py           # Logging setup
├── cli/
│   ├── __init__.py
│   └── main.py          # Click CLI commands
├── snipeit/
│   ├── __init__.py      # Module exports
│   ├── client.py        # SnipeITClient class
│   ├── models.py        # Asset, DiscoveredDevice dataclasses
│   └── exceptions.py    # Custom exceptions
├── scanner/
│   ├── __init__.py
│   └── scanner.py       # Network scanning (ARP/ICMP)
└── oui/
    ├── __init__.py
    └── lookup.py        # MAC-to-manufacturer lookup
```

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [Snipe-IT Integration PRD](snipeit-integration-prd.md) | Detailed product requirements |
| [Sprint Backlog](sprint-backlog-snipeit.md) | Implementation tasks |
| [README](../README.md) | User guide and quick start |

---

## Historical Note

**Prior to v2.0** (December 2025), this tool integrated with a PostgreSQL database (`ra_inventory`) managed by the ra-infrastructure repository. This was replaced with Snipe-IT API integration to leverage existing asset management infrastructure and web UI.

The following documents are now historical/superseded:
- `device-discovery-prd.md` - Original PRD with database integration
- `NETWORK-TOOLS-DECISIONS-2025-11-29.md` - Database architecture decisions
