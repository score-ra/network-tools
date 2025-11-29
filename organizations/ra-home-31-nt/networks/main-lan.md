# Network: Main LAN

> **Database Table**: `ra_inventory.networks`
> **Discovered**: 2025-11-28 via ARP scan

---

## Required Fields

| Field | Value | Notes |
|-------|-------|-------|
| **site_id** | `[TBD - assign from ra-infrastructure]` | FK to sites table |
| **name** | `Main LAN` | Primary home network |
| **slug** | `main-lan` | Unique identifier |

## Network Type

| Field | Value | Options |
|-------|-------|---------|
| **network_type** | `ethernet` | Primary wired/wireless combined network |

## IP Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **cidr** | `192.168.68.0/22` | Discovered prefix length: /22 (1022 usable hosts) |
| **gateway_ip** | `192.168.68.1` | Google/Nest WiFi router |
| **vlan_id** | `null` | No VLAN segmentation |

## Wireless Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **ssid** | `[TBD]` | WiFi SSID (to be documented) |

## Flags

| Field | Value | Notes |
|-------|-------|-------|
| **is_primary** | `true` | Primary network for this site |

---

## Discovery Results

### Network Details
- **Scan Date**: 2025-11-28
- **Scan Method**: ARP table query
- **Interface**: Ethernet (Realtek Gaming 2.5GbE)
- **Local IP**: 192.168.68.56
- **Subnet**: /22 (192.168.68.0 - 192.168.71.255)

### Discovered Devices (14 active)

| IP Address | MAC Address | Type | Manufacturer (OUI) |
|------------|-------------|------|-------------------|
| 192.168.68.1 | 54-AF-97-50-C0-F8 | Gateway | Google (Nest WiFi) |
| 192.168.68.57 | 9C-8E-CD-31-54-8D | Device | Apple |
| 192.168.68.58 | A0-60-32-01-38-2B | Device | Apple |
| 192.168.68.60 | 5C-60-BA-5B-62-C3 | Device | HP |
| 192.168.68.62 | 78-E1-03-91-CD-84 | Device | Amazon |
| 192.168.68.64 | 20-BE-B8-8F-F0-FD | Device | Unknown |
| 192.168.68.68 | D4-C9-EF-D5-00-61 | Device | Actions Semiconductor |
| 192.168.68.71 | 64-4B-F0-10-4D-5B | Device | Unknown |
| 192.168.68.74 | 1C-A0-B8-73-71-CD | Desktop | Intel (Windows PC) |
| 192.168.68.80 | 60-83-E7-3D-0E-B0 | Device | Apple |
| 192.168.68.81 | 9C-8E-CD-37-12-F5 | Device | Apple |
| 192.168.68.83 | 9C-8E-CD-37-14-11 | Device | Apple |
| 192.168.68.90 | 9C-8E-CD-31-67-6B | Device | Apple |
| 192.168.68.91 | 60-83-E7-3D-0C-0E | Device | Apple |

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
    '[site_id]'::uuid,           -- Get from sites table
    'Main LAN',
    'main-lan',
    'ethernet',
    '192.168.68.0/22'::cidr,
    '192.168.68.1'::inet,
    null,
    null,                         -- Add SSID when known
    true
);
```

---

## Notes

- Network uses /22 subnet allowing for ~1000 devices
- Gateway is Google/Nest WiFi (OUI: 54-AF-97)
- Heavy Apple device presence (7 devices with 9C-8E-CD or 60-83-E7 OUI)
- One Amazon device (likely Echo/Fire device)
- One HP device (likely printer)
- Windows PC at .74 with Intel NIC

---
**Document Version**: 1.0
**Last Updated**: 2025-11-28
**Discovery Method**: Automated (ARP scan)
