# Network Tools

**Personal networking utilities and diagnostic tools**

A collection of Python scripts and utilities for diagnosing network connectivity issues, particularly focused on troubleshooting unreachable hosts on local networks.

## 🎯 What This Project Provides

- **Network Discovery** - Automated scanning to find devices on your network
- **Inventory Integration** - Direct read/write to ra_inventory PostgreSQL database
- **OUI Lookup** - Automatic manufacturer identification from MAC addresses
- **Interactive CLI** - Confirm, skip, or edit devices before adding to inventory
- **Organization Management** - Document and track multiple network environments
- **Windows 11 Focus** - Tools optimized for Windows network troubleshooting

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Windows 11 (primary target)
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

The tool connects to the ra_inventory PostgreSQL database. Set these environment variables:

```bash
# Required
set DB_PASSWORD=your_database_password

# Optional (defaults shown)
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=inventory
set DB_USER=inventory
set DEFAULT_NETWORK=192.168.68.0/22
```

Or create a `.env` file (see `.env.example`).

## 📡 Network Discovery

### Check Database Connection

```bash
python -m network_tools status
```

Example output:
```
Database Status
───────────────
Connection: ✓ Connected
Host: localhost:5432
Database: inventory

Inventory Summary
─────────────────
Sites: 1
Networks: 5
Devices: 17
```

### Discover Devices on Network

```bash
# Basic scan (interactive mode)
python -m network_tools discover --network 192.168.68.0/24

# Scan with site association
python -m network_tools discover --network 192.168.68.0/24 --site ra-home-31-nt

# Auto-confirm all new devices (non-interactive)
python -m network_tools discover --network 192.168.68.0/24 --site ra-home-31-nt --yes

# Use existing ARP table only (faster, no ping sweep)
python -m network_tools discover --network 192.168.68.0/24 --no-ping
```

### Discovery Options

| Option | Description |
|--------|-------------|
| `-n, --network` | Network CIDR to scan (required) |
| `-s, --site` | Site slug for inventory association |
| `-y, --yes` | Auto-confirm all new devices |
| `--no-ping` | Skip ping sweep, use existing ARP table |

### What Happens During Discovery

1. **Scan** - ARP scan (and optional ping sweep) finds active hosts
2. **Identify** - MAC addresses are looked up for manufacturer info
3. **Compare** - Discovered devices are compared against inventory
4. **Categorize** - Devices are marked as New, Existing, or IP Changed
5. **Confirm** - Interactive prompt to confirm/skip/edit each new device
6. **Insert** - Confirmed devices are added to the database

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
│       ├── db/             # Database connection, models, queries
│       ├── scanner/        # ARP/ICMP network scanning
│       ├── oui/            # MAC address manufacturer lookup
│       ├── resolver/       # Hostname resolution
│       └── config.py       # Configuration management
├── organizations/          # Network environment documentation
│   ├── sc-office/         # Co-working office network
│   └── ra-home-31-nt/     # Home network
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── templates/              # Document templates
├── data/                   # OUI database files
└── requirements.txt        # Python dependencies
```

## 🗄️ Database Dependency

This tool integrates with the **ra_inventory** PostgreSQL database managed by the [ra-infrastructure](../ra-infrastructure) repository.

- **Schema ownership**: ra-infrastructure (this repo cannot modify schema)
- **Access level**: Direct READ/WRITE to device inventory
- **Key tables**: `sites`, `networks`, `devices`

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for integration details.

## 📚 Documentation

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and integration
- **[docs/device-discovery-prd.md](docs/device-discovery-prd.md)** - Discovery feature requirements
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
pytest tests/test_module.py
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
**Tech Stack**: Python 3.11+
**Last Updated**: 2025-11-30
