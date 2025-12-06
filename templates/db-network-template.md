# Network Entry Template

> **⚠️ OBSOLETE**: This template was for the ra_inventory PostgreSQL database.
> network-tools now uses Snipe-IT API integration instead.

> **Purpose**: Template for adding a network to the `ra_inventory.networks` table.
> **Schema Owner**: ra-infrastructure repository
> **Reference**: [DATABASE.md](file:///C:/Users/ranand/workspace/personal/software/ra-infrastructure/docs/DATABASE.md)

---

## Required Fields

| Field | Value | Notes |
|-------|-------|-------|
| **site_id** | `[UUID]` | FK to sites table (required) |
| **name** | `[Display Name]` | Human-readable name (max 255 chars) |
| **slug** | `[url-friendly-slug]` | Unique within site (max 100 chars, lowercase, hyphens) |

## Network Type

| Field | Value | Options |
|-------|-------|---------|
| **network_type** | `[type]` | `ethernet`, `wifi`, `zwave`, `zigbee`, `bluetooth`, `thread`, `matter`, `other` |

## IP Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **cidr** | `[192.168.1.0/24]` | Network CIDR notation |
| **gateway_ip** | `[192.168.1.1]` | Gateway IP address |
| **vlan_id** | `[null or 1-4094]` | VLAN ID (optional) |

## Wireless Configuration (if network_type = wifi)

| Field | Value | Notes |
|-------|-------|-------|
| **ssid** | `[NetworkName]` | WiFi SSID (max 100 chars, optional) |

## Flags

| Field | Value | Notes |
|-------|-------|-------|
| **is_primary** | `[true/false]` | Primary network for this site |

---

## Example Entry

```yaml
# Main LAN Network
site_id: "550e8400-e29b-41d4-a716-446655440000"
name: "Main LAN"
slug: "main-lan"
network_type: "ethernet"
cidr: "192.168.1.0/24"
gateway_ip: "192.168.1.1"
vlan_id: null
ssid: null
is_primary: true
```

```yaml
# Guest WiFi Network
site_id: "550e8400-e29b-41d4-a716-446655440000"
name: "Guest WiFi"
slug: "guest-wifi"
network_type: "wifi"
cidr: "192.168.10.0/24"
gateway_ip: "192.168.10.1"
vlan_id: 10
ssid: "GuestNetwork"
is_primary: false
```

---

## SQL Insert Statement

```sql
INSERT INTO networks (
    site_id,
    name,
    slug,
    network_type,
    cidr,
    gateway_ip,
    vlan_id,
    ssid,
    is_primary
) VALUES (
    '[site_id]'::uuid,
    '[name]',
    '[slug]',
    '[network_type]',
    '[cidr]'::cidr,
    '[gateway_ip]'::inet,
    [vlan_id],          -- null or integer
    '[ssid]',           -- null or string
    [is_primary]        -- true or false
);
```

---

## Validation Rules

- `slug` must be unique within the site
- `vlan_id` must be between 1-4094 if provided
- `cidr` must be valid CIDR notation
- `gateway_ip` should be within the `cidr` range
- `ssid` typically only populated when `network_type` = 'wifi'

---

## Related Tables

- **sites**: Parent table (site_id FK)
- **devices**: Devices can reference this network (network_id)
- **ip_allocations**: IP assignments within this network

---
**Template Version**: 1.0
**Last Updated**: 2025-11-28
