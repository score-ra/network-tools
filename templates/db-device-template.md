# Device Entry Template

> **⚠️ OBSOLETE**: This template was for the ra_inventory PostgreSQL database.
> network-tools now uses Snipe-IT API integration instead.
> For adding devices, use the `network-tools discover` CLI command.

> **Purpose**: Template for adding a device to the `ra_inventory.devices` table.
> **Schema Owner**: ra-infrastructure repository
> **Reference**: [DATABASE.md](file:///C:/Users/ranand/workspace/personal/software/ra-infrastructure/docs/DATABASE.md)

---

## Required Fields

| Field | Value | Notes |
|-------|-------|-------|
| **site_id** | `[UUID]` | FK to sites table (required) |
| **name** | `[Display Name]` | Human-readable name (max 255 chars) |
| **slug** | `[url-friendly-slug]` | Unique within site (max 100 chars, lowercase, hyphens) |

## Optional Foreign Keys

| Field | Value | Notes |
|-------|-------|-------|
| **zone_id** | `[UUID or null]` | FK to zones table (room/location) |
| **network_id** | `[UUID or null]` | FK to networks table |
| **category_id** | `[UUID or null]` | FK to device_categories table |

## Device Identification

| Field | Value | Notes |
|-------|-------|-------|
| **device_type** | `[type string]` | Free-form type (max 100 chars) |
| **manufacturer** | `[Manufacturer Name]` | e.g., "Apple", "Dell", "Sonos" (max 255 chars) |
| **model** | `[Model Name]` | e.g., "MacBook Pro 16" (max 255 chars) |
| **serial_number** | `[Serial]` | Manufacturer serial (max 255 chars) |
| **firmware_version** | `[Version]` | Current firmware (max 100 chars) |

## Network Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **mac_address** | `[XX:XX:XX:XX:XX:XX]` | MAC address (MACADDR type) |
| **ip_address** | `[192.168.1.x]` | IP address (INET type) |
| **hostname** | `[hostname.local]` | DNS hostname (max 255 chars) |

## Status

| Field | Value | Options |
|-------|-------|---------|
| **status** | `[status]` | `online`, `offline`, `unknown`, `maintenance` |
| **is_active** | `[true/false]` | Soft delete flag (default: true) |

## Flexible Metadata (JSONB)

| Field | Value | Notes |
|-------|-------|-------|
| **metadata** | `{}` | Any additional attributes as JSON |

---

## Example Entry

```yaml
# Desktop Computer
site_id: "550e8400-e29b-41d4-a716-446655440000"
zone_id: "660e8400-e29b-41d4-a716-446655440001"
network_id: "770e8400-e29b-41d4-a716-446655440002"
category_id: null
name: "Office Desktop"
slug: "office-desktop"
device_type: "desktop"
status: "online"
manufacturer: "Dell"
model: "OptiPlex 7090"
serial_number: "ABC123XYZ"
mac_address: "00:1A:2B:3C:4D:5E"
ip_address: "192.168.1.50"
hostname: "office-desktop.local"
firmware_version: null
is_active: true
metadata:
  purchase_date: "2023-06-15"
  warranty_expires: "2026-06-15"
  os: "Windows 11 Pro"
```

```yaml
# Smart Speaker
site_id: "550e8400-e29b-41d4-a716-446655440000"
zone_id: "660e8400-e29b-41d4-a716-446655440003"
network_id: "880e8400-e29b-41d4-a716-446655440004"
category_id: null
name: "Living Room Sonos"
slug: "living-room-sonos"
device_type: "speaker"
status: "online"
manufacturer: "Sonos"
model: "One SL"
serial_number: "SONOS-12345"
mac_address: "94:9F:3E:12:34:56"
ip_address: "192.168.1.120"
hostname: "sonos-living.local"
firmware_version: "15.6"
is_active: true
metadata:
  room: "Living Room"
  paired_with: "sonos-kitchen"
```

---

## SQL Insert Statement

```sql
INSERT INTO devices (
    site_id,
    zone_id,
    network_id,
    category_id,
    name,
    slug,
    device_type,
    status,
    manufacturer,
    model,
    serial_number,
    mac_address,
    ip_address,
    hostname,
    firmware_version,
    is_active,
    metadata
) VALUES (
    '[site_id]'::uuid,
    [zone_id],              -- null or 'uuid'::uuid
    [network_id],           -- null or 'uuid'::uuid
    [category_id],          -- null or 'uuid'::uuid
    '[name]',
    '[slug]',
    '[device_type]',
    '[status]',
    '[manufacturer]',
    '[model]',
    '[serial_number]',
    '[mac_address]'::macaddr,
    '[ip_address]'::inet,
    '[hostname]',
    '[firmware_version]',
    [is_active],            -- true or false
    '[metadata]'::jsonb     -- '{}' or '{"key": "value"}'
);
```

---

## Validation Rules

- `slug` must be unique within the site
- `mac_address` must be valid MAC format (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)
- `ip_address` must be valid IPv4 or IPv6
- `status` must be one of: `online`, `offline`, `unknown`, `maintenance`
- `metadata` must be valid JSON

---

## Common Device Types

| device_type | Description |
|-------------|-------------|
| `desktop` | Desktop computer |
| `laptop` | Laptop computer |
| `server` | Server |
| `router` | Network router |
| `switch` | Network switch |
| `access-point` | Wireless access point |
| `printer` | Printer/MFP |
| `nas` | Network attached storage |
| `camera` | Security/IP camera |
| `speaker` | Smart speaker |
| `tv` | Smart TV |
| `streaming-device` | Roku, Apple TV, etc. |
| `thermostat` | Smart thermostat |
| `phone` | Smartphone |
| `tablet` | Tablet |
| `game-console` | Gaming console |
| `iot-sensor` | IoT sensor device |

---

## Related Tables

- **sites**: Parent table (site_id FK) - required
- **zones**: Location within site (zone_id FK) - optional
- **networks**: Network assignment (network_id FK) - optional
- **device_categories**: Category classification (category_id FK) - optional
- **device_attributes**: Extended attributes for this device
- **ip_allocations**: IP assignments for this device

---
**Template Version**: 1.0
**Last Updated**: 2025-11-28
