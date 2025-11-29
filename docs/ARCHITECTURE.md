# Network-Tools Architecture

**Version**: 1.0
**Last Updated**: 2025-11-29
**Status**: Active

---

## Overview

Network-tools is a Python-based utility for automated network device discovery and inventory management. It scans local networks to discover devices, identifies manufacturers via MAC address lookup, and integrates discovered devices directly into the ra_inventory database.

**Key Value Proposition**: Automate the tedious process of manually tracking network devices by combining network scanning with an interactive confirmation workflow and direct database integration.

---

## Capabilities

| Capability | Description |
|------------|-------------|
| Network Scanning | ARP-based discovery and ICMP ping sweep |
| Device Discovery | Identify active hosts on network segments |
| OUI Lookup | MAC-to-manufacturer mapping using built-in database |
| Device Type Inference | Guess device type based on manufacturer patterns |
| Inventory Comparison | Compare discovered devices against existing inventory |
| Interactive CLI | Confirm/skip/edit devices before adding to inventory |
| Direct Database Integration | Read/write to ra_inventory PostgreSQL database |

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

## Component Responsibilities

| Component | Owner | Responsibilities |
|-----------|-------|------------------|
| Network Scanner | network-tools | ARP/ICMP scanning, host discovery |
| OUI Lookup | network-tools | MAC-to-manufacturer mapping |
| Interactive CLI | network-tools | User confirmation workflow |
| Database Layer | network-tools | Read/write to inventory DB |
| PostgreSQL DB | ra-infrastructure | Schema, migrations, data storage |
| inv CLI | ra-infrastructure | Manual device management |

---

## Integration with ra-infrastructure

### Database Integration

- **Connection**: psycopg3 with connection pooling
- **Access Level**: Direct READ/WRITE to inventory database
- **Authentication**: Credentials via environment variables

### Schema Ownership

- ra-infrastructure owns all schema definitions and migrations
- network-tools reads/writes data but cannot modify schema
- Schema change requests should be submitted to ra-infrastructure team

### Key Tables Used

| Table | Purpose |
|-------|---------|
| `sites` | Site/location information |
| `devices` | Device inventory records |
| `networks` | Network segment definitions |

---

## For Database Integrators

Services wanting to integrate with ra_inventory (like network-tools) should follow these guidelines:

### Connection Requirements

1. **Request database credentials** from ra-infrastructure team
2. **Use connection pooling** for production workloads (psycopg3 pool recommended)
3. **Support transactions** for atomic operations

### Data Model Guidelines

- **Primary Identifier**: Use MAC address as the primary device identifier
- **Normalization**: Store MAC addresses in lowercase, colon-separated format (e.g., `aa:bb:cc:dd:ee:ff`)

### PostgreSQL Data Types

| Field Type | PostgreSQL Type | Notes |
|------------|-----------------|-------|
| MAC Address | `macaddr` | Native PostgreSQL type |
| IP Address | `inet` | Supports IPv4 and IPv6 |
| Metadata | `jsonb` | Flexible key-value storage |
| Identifiers | `uuid` | Primary keys and foreign keys |

---

## For Network Scanning Consumers

Services wanting to use network-tools scanning capabilities:

### CLI Commands

| Command | Purpose |
|---------|---------|
| `network-tools discover` | Scan network and discover devices |
| `network-tools status` | Show database connection and inventory summary |

### Discovery Options

| Option | Description |
|--------|-------------|
| `--network <CIDR>` | Network to scan (e.g., 192.168.1.0/24) |
| `--site <slug>` | Site slug for device assignment |
| `--yes` | Auto-confirm all new devices |
| `--no-ping` | Skip ICMP ping sweep (ARP only) |

### Scanning Features

- **ARP-based discovery**: Fast, uses system ARP table
- **ICMP ping sweep**: Thorough, populates ARP table before reading
- **MAC normalization**: Consistent format for comparison
- **Manufacturer identification**: Via built-in OUI database

### Discovery Output

The discover command identifies devices in three categories:

| Category | Description |
|----------|-------------|
| New Devices | Not found in inventory (by MAC) |
| Existing Devices | Already in inventory (matched by MAC) |
| IP Changed | Known device with different IP address |

---

## Environment Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | localhost |
| `DB_PORT` | PostgreSQL port | 5432 |
| `DB_NAME` | Database name | inventory |
| `DB_USER` | Database user | inventory |
| `DB_PASSWORD` | Database password | (required) |
| `DEFAULT_NETWORK` | Default scan CIDR | 192.168.68.0/22 |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [Device Discovery PRD](device-discovery-prd.md) | Detailed product requirements |
| [Architecture Decisions](NETWORK-TOOLS-DECISIONS-2025-11-29.md) | Decision log and rationale |
| [Sprint Plan](sprint-plan-discovery-implementation.md) | Implementation phases |
