# Device: Nest WiFi Router

> **Database Table**: `ra_inventory.devices`
> **Discovered**: 2025-11-28 via ARP scan

---

## Required Fields

| Field | Value | Notes |
|-------|-------|-------|
| **site_id** | `[TBD - assign from ra-infrastructure]` | FK to sites table |
| **name** | `Nest WiFi Router` | Primary network gateway |
| **slug** | `nest-wifi-router` | Unique identifier |

## Optional Foreign Keys

| Field | Value | Notes |
|-------|-------|-------|
| **zone_id** | `null` | TBD - assign to room/location |
| **network_id** | `[main-lan UUID]` | FK to main-lan network |
| **category_id** | `null` | TBD - router/network-infrastructure |

## Device Identification

| Field | Value | Notes |
|-------|-------|-------|
| **device_type** | `router` | Network gateway device |
| **manufacturer** | `Google` | OUI lookup: 54-AF-97 = Google |
| **model** | `Nest WiFi` | Inferred from OUI |
| **serial_number** | `[TBD]` | Check device label |
| **firmware_version** | `[TBD]` | Check Google Home app |

## Network Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **mac_address** | `54:AF:97:50:C0:F8` | Discovered via ARP |
| **ip_address** | `192.168.68.1` | Gateway IP (static) |
| **hostname** | `null` | No reverse DNS record |

## Status

| Field | Value | Options |
|-------|-------|---------|
| **status** | `online` | Responding to ARP |
| **is_active** | `true` | Active device |

## Flexible Metadata (JSONB)

```json
{
  "role": "gateway",
  "discovery_method": "arp",
  "discovery_date": "2025-11-28",
  "oui": "54-AF-97",
  "oui_vendor": "Google, Inc.",
  "is_dhcp_server": true,
  "is_dns_server": true,
  "management_url": "https://home.google.com"
}
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
    null,                                    -- zone_id TBD
    '[network_id]'::uuid,                    -- main-lan network
    null,                                    -- category_id TBD
    'Nest WiFi Router',
    'nest-wifi-router',
    'router',
    'online',
    'Google',
    'Nest WiFi',
    null,                                    -- serial_number TBD
    '54:AF:97:50:C0:F8'::macaddr,
    '192.168.68.1'::inet,
    null,
    null,                                    -- firmware TBD
    true,
    '{
        "role": "gateway",
        "discovery_method": "arp",
        "discovery_date": "2025-11-28",
        "oui": "54-AF-97",
        "oui_vendor": "Google, Inc.",
        "is_dhcp_server": true,
        "is_dns_server": true,
        "management_url": "https://home.google.com"
    }'::jsonb
);
```

---

## Discovery Details

| Field | Value |
|-------|-------|
| **Discovery Date** | 2025-11-28 |
| **Discovery Method** | ARP table query |
| **ARP Entry Type** | dynamic |
| **Responding Interface** | 192.168.68.56 (Ethernet) |

## OUI Lookup

| Field | Value |
|-------|-------|
| **OUI Prefix** | 54-AF-97 |
| **Vendor** | Google, Inc. |
| **Address** | 1600 Amphitheatre Parkway, Mountain View CA 94043 |

---

## Device Capabilities

| Capability | Status | Notes |
|------------|--------|-------|
| Router/Gateway | Yes | Primary network gateway |
| DHCP Server | Yes | Assigns IPs to network devices |
| DNS Server | Yes | Local DNS resolver (192.168.68.1) |
| WiFi Access Point | Yes | Provides wireless connectivity |
| Mesh Support | Likely | Nest WiFi supports mesh networking |

## Management

| Method | Access | Notes |
|--------|--------|-------|
| Web Interface | No | Google Nest uses app-only management |
| Google Home App | Yes | Primary management interface |
| SSH | No | Not available on consumer devices |

---

## Notes

- This is the primary gateway/router for the home network
- Google Nest WiFi devices are managed via the Google Home mobile app
- No local web interface available (unlike traditional routers)
- Acts as DHCP and DNS server for the network
- MAC OUI confirms this is an authentic Google device

---
**Document Version**: 1.0
**Last Updated**: 2025-11-28
**Discovery Method**: Automated (ARP scan)
