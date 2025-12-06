# Network Tools

**Personal networking utilities and diagnostic tools**

A collection of Python scripts and utilities for network device discovery and asset management integration with Snipe-IT.

## 🎯 What This Project Provides

- **Network Discovery** - Automated scanning to find devices on your network
- **Snipe-IT Integration** - Sync discovered devices with Snipe-IT asset management
- **OUI Lookup** - Automatic manufacturer identification from MAC addresses
- **Interactive CLI** - Confirm, skip, or edit devices before adding to inventory
- **Asset Search** - Find assets by MAC or IP address
- **Windows 11 Focus** - Tools optimized for Windows network troubleshooting

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Windows 11 (primary target)
- Snipe-IT instance with API access
- Network access to target hosts

### Installation

```bash
# Clone the repository
git clone <repo-url> network-tools
cd network-tools

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Configure Snipe-IT API access. Copy `.env.example` to `.env`:

```bash
# Required
SNIPEIT_API_KEY=your_api_key_here

# Optional (defaults shown)
SNIPEIT_BASE_URL=http://localhost:8082/api/v1
SNIPEIT_TIMEOUT=30
SNIPEIT_NETWORK_CATEGORY_ID=4
SNIPEIT_DEFAULT_STATUS_ID=2
SNIPEIT_DEFAULT_MODEL_ID=25
DEFAULT_NETWORK=192.168.68.0/22
```

**Note**: Set `SNIPEIT_DEFAULT_MODEL_ID` to a valid model ID in your Snipe-IT instance (e.g., "Unknown Network Device" model).

## 📡 CLI Commands

### Check Snipe-IT Connection

```bash
python -m network_tools status
```

Example output:
```
Snipe-IT Status

OK Connected to http://localhost:8082/api/v1

Asset Summary
┏━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Category       ┃ Count ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Total Assets   │    50 │
│ Network Assets │    20 │
└────────────────┴───────┘
```

### Discover Devices on Network

```bash
# Basic scan (interactive mode)
python -m network_tools discover --network 192.168.68.0/24

# Auto-confirm all new devices (non-interactive)
python -m network_tools discover --network 192.168.68.0/24 --yes

# Use existing ARP table only (faster, no ping sweep)
python -m network_tools discover --network 192.168.68.0/24 --no-ping
```

### Search for Assets

```bash
# Search by MAC address
python -m network_tools search --mac AA:BB:CC:DD:EE:FF

# Search by IP address
python -m network_tools search --ip 192.168.68.100
```

### Discovery Options

| Option | Description |
|--------|-------------|
| `-n, --network` | Network CIDR to scan (required) |
| `-y, --yes` | Auto-confirm all new devices |
| `--no-ping` | Skip ping sweep, use existing ARP table |

### What Happens During Discovery

1. **Connect** - Verify Snipe-IT API connectivity
2. **Scan** - ARP scan (and optional ping sweep) finds active hosts
3. **Identify** - MAC addresses are looked up for manufacturer info
4. **Compare** - Discovered devices are compared against Snipe-IT inventory
5. **Categorize** - Devices are marked as New, Existing, or IP Changed
6. **Confirm** - Interactive prompt to confirm/skip each new device
7. **Sync** - Confirmed devices are added to Snipe-IT via API

### Discovery Output Categories

| Category | Description |
|----------|-------------|
| **New** | Device not in inventory (by MAC address) |
| **Existing** | Device already in inventory |
| **IP Changed** | Known device with different IP address |

## 📁 Project Structure

```
network-tools/
├── src/
│   └── network_tools/      # Main package
│       ├── cli/            # Click CLI commands
│       ├── snipeit/        # Snipe-IT API client
│       ├── scanner/        # ARP/ICMP network scanning
│       ├── oui/            # MAC address manufacturer lookup
│       └── config.py       # Configuration management
├── organizations/          # Network environment documentation
├── tests/                  # Test files
├── docs/                   # Documentation
├── templates/              # Document templates
├── data/                   # OUI database files
└── requirements.txt        # Python dependencies
```

## 🔗 Snipe-IT Integration

This tool integrates with **Snipe-IT** asset management via REST API.

- **Connection**: HTTPS REST API with Bearer token authentication
- **Operations**: Query, create, and update hardware assets
- **Custom Fields**: Uses MAC Address and IP Address custom fields
- **Categories**: Discovers devices in the "Network" category

See [docs/snipeit-integration-prd.md](docs/snipeit-integration-prd.md) for detailed requirements.

## 📚 Documentation

- **[docs/snipeit-integration-prd.md](docs/snipeit-integration-prd.md)** - Snipe-IT integration requirements
- **[docs/sprint-backlog-snipeit.md](docs/sprint-backlog-snipeit.md)** - Sprint backlog
- **[CLAUDE.md](CLAUDE.md)** - Development guidelines for Claude Code

## 🏢 Organizations

| Organization | Type | Subnet | Description |
|--------------|------|--------|-------------|
| [sc-office](organizations/sc-office/) | Co-working | 192.168.1.0/24 | Office at co-working facility |
| [ra-home-31-nt](organizations/ra-home-31-nt/) | Home | 192.168.68.0/24 | Home network |

## 🔧 Scripts

| Script | Description |
|--------|-------------|
| [connect-rdp.ps1](scripts/connect-rdp.ps1) | Connect to remote PC via RDP (single display) |
| [create-shortcut.ps1](scripts/create-shortcut.ps1) | Create desktop shortcut for RDP |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_snipeit/test_client.py
```

## ✅ Development Standards

- Test coverage ≥80%
- Code formatted with `black`
- Linted with `flake8`
- Type hints checked with `mypy`

## 📄 License

Personal project - All rights reserved

---

**Organization**: personal-ra
**Tech Stack**: Python 3.11+, Snipe-IT API, Click
**Last Updated**: 2025-12-06
