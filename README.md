# Network Tools

**Personal networking utilities and diagnostic tools**

A collection of Python scripts and utilities for diagnosing network connectivity issues, particularly focused on troubleshooting unreachable hosts on local networks.

## 🎯 What This Project Provides

- **Network Diagnostics** - Scripts to investigate connectivity issues
- **Organization Management** - Document and track multiple network environments
- **Device Inventory** - Track devices, IPs, and configurations per organization
- **Windows 11 Focus** - Tools optimized for Windows network troubleshooting
- **AI-Assisted Development** - Built using AI-Assisted Agile methodology
- **Modular Design** - Easy to extend with new diagnostic tools

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

### Usage

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term

# Code quality
flake8 src/ tests/
black src/ tests/
mypy src/
```

## 📁 Project Structure

```
network-tools/
├── organizations/          # Network environments
│   ├── sc-office/         # Co-working office network
│   │   ├── README.md      # Organization overview
│   │   └── devices/       # Device specifications
│   └── ra-home-31-nt/     # Home network
│       ├── README.md
│       └── devices/
├── src/                    # Source code
│   ├── shared/            # Shared utilities
│   │   ├── config.py     # Configuration
│   │   └── utils.py      # Utility functions
│   └── __init__.py
├── scripts/                # Utility scripts
│   ├── connect-rdp.ps1   # RDP connection script
│   └── create-shortcut.ps1
├── templates/              # Document templates
│   ├── organization-template.md
│   └── device-template.md
├── tests/                  # Test files
├── docs/                   # Documentation
├── config/                 # Configuration files
├── requirements.txt        # Python dependencies
├── pytest.ini             # Test configuration
├── CLAUDE.md              # Claude Code instructions
└── README.md              # This file
```

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Development guidelines for Claude Code
- **[docs/PROCESS-OVERVIEW.md](docs/PROCESS-OVERVIEW.md)** - Development workflow
- **[docs/network-tools-prd.md](docs/network-tools-prd.md)** - Product Requirements

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
**Last Updated**: 2025-11-25
