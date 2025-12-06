# Sprint Backlog: Network Discovery v1 Test Run

> **📜 HISTORICAL**: This sprint was part of the original database-integrated implementation.
> The system has since been migrated to Snipe-IT API integration.
> See [sprint-backlog-snipeit.md](sprint-backlog-snipeit.md) for current sprint.

**Date**: 2025-11-28
**Test Run**: First automated network discovery
**Status**: Complete (Historical)

---

## Summary

| Metric | Value |
|--------|-------|
| Devices Discovered | 14 |
| Devices in Database (before) | 3 |
| Devices Added | **14** (router + 13 discovered) |
| Devices Missing MAC | 2 (USB controllers - expected) |
| Database Corrections | 2 (CIDR /24 → /22, HomeSeer MAC) |
| **Total Devices Now** | **17** |

---

## Issues Discovered

### Issue 1: Database CIDR Mismatch
**Priority**: P1 - High
**Type**: Data Correction

**Problem**: Database had network CIDR as `192.168.68.0/24` but actual network is `192.168.68.0/22`.

**Impact**:
- Device at 192.168.68.74 (Windows PC) would appear outside network range
- IP allocation queries would be incorrect

**Resolution**: Updated CIDR to `/22` ✅

**Backlog Item**: Add CIDR validation to discovery tool - compare discovered subnet mask with database.

---

### Issue 2: Existing Devices Missing MAC Addresses
**Priority**: P2 - Medium
**Type**: Data Quality

**Problem**: 3 existing devices in database have no MAC address:
- HomeSeer Server (192.168.68.56)
- Z-Wave USB Controller
- Zigbee USB Controller

**Impact**: Cannot correlate discovered devices with existing inventory by MAC.

**Backlog Item**:
1. Update HomeSeer Server with MAC `A0:1E:0B:15:75:B7` (this machine's Ethernet)
2. USB controllers don't have network MACs (expected - they're local USB devices)

---

### Issue 3: 13 Discovered Devices Not in Database
**Priority**: P1 - High
**Type**: Missing Data

**Discovered but not in inventory**:

| IP | MAC | Likely Device | Action |
|----|-----|---------------|--------|
| 192.168.68.57 | 9C:8E:CD:31:54:8D | Apple device | Add |
| 192.168.68.58 | A0:60:32:01:38:2B | Apple device | Add |
| 192.168.68.60 | 5C:60:BA:5B:62:C3 | HP (printer?) | Add |
| 192.168.68.62 | 78:E1:03:91:CD:84 | Amazon Echo | Add |
| 192.168.68.64 | 20:BE:B8:8F:F0:FD | Unknown | Investigate |
| 192.168.68.68 | D4:C9:EF:D5:00:61 | Smart device | Investigate |
| 192.168.68.71 | 64:4B:F0:10:4D:5B | Unknown | Investigate |
| 192.168.68.74 | 1C:A0:B8:73:71:CD | Windows PC (Intel) | Add |
| 192.168.68.80 | 60:83:E7:3D:0E:B0 | Apple device | Add |
| 192.168.68.81 | 9C:8E:CD:37:12:F5 | Apple device | Add |
| 192.168.68.83 | 9C:8E:CD:37:14:11 | Apple device | Add |
| 192.168.68.90 | 9C:8E:CD:31:67:6B | Apple device | Add |
| 192.168.68.91 | 60:83:E7:3D:0C:0E | Apple device | Add |

**Backlog Item**: Bulk import discovered devices with manufacturer lookup.

---

### Issue 4: No OUI Database Integration
**Priority**: P2 - Medium
**Type**: Feature Gap

**Problem**: Manual OUI lookup required. No automated manufacturer identification.

**Backlog Item**: Integrate IEEE OUI database for automatic manufacturer lookup from MAC prefix.

---

### Issue 5: No Hostname Resolution
**Priority**: P3 - Low
**Type**: Feature Gap

**Problem**: Reverse DNS lookups returned no results. NetBIOS/mDNS not queried.

**Backlog Item**: Implement multi-protocol hostname resolution (DNS, NetBIOS, mDNS).

---

## Insights

### Insight 1: Heavy Apple Device Presence
- 7 of 14 devices (50%) have Apple OUI prefixes
- OUI prefixes: `9C:8E:CD` (Apple), `60:83:E7` (Apple)
- Suggests iPhones, iPads, Macs, Apple TVs

### Insight 2: Network Uses /22 Subnet
- Larger than typical home /24
- Allows for ~1000 devices
- Google/Nest WiFi default configuration

### Insight 3: Mixed Network Infrastructure
- Google Nest WiFi as gateway
- Existing HomeSeer home automation
- Z-Wave and Zigbee controllers present
- Smart home ecosystem in place

### Insight 4: Current Machine is HomeSeer Server
- Discovery machine IP: 192.168.68.56
- Matches HomeSeer Server in database
- MAC: A0:1E:0B:15:75:B7 (Realtek NIC)

---

## Sprint Backlog Items

### P0 - Critical (This Sprint) - ✅ COMPLETE

| ID | Story | Acceptance Criteria | Effort | Status |
|----|-------|---------------------|--------|--------|
| ND-001 | Bulk import discovered devices | Import 13 missing devices with MAC, IP, manufacturer | S | ✅ Done |
| ND-002 | Update HomeSeer Server MAC | Add MAC A0:1E:0B:15:75:B7 to existing record | XS | ✅ Done |

### P1 - High (Next Sprint)

| ID | Story | Acceptance Criteria | Effort |
|----|-------|---------------------|--------|
| ND-003 | OUI database integration | Lookup manufacturer from MAC prefix automatically | M |
| ND-004 | Discovery comparison report | Show new/updated/missing devices vs database | M |
| ND-005 | CIDR validation | Detect and warn on subnet mask mismatches | S |

### P2 - Medium (Backlog)

| ID | Story | Acceptance Criteria | Effort |
|----|-------|---------------------|--------|
| ND-006 | Multi-protocol hostname resolution | Query DNS, NetBIOS, mDNS for hostnames | L |
| ND-007 | Device type inference | Infer type from manufacturer/hostname patterns | M |
| ND-008 | Discovery scan CLI | `python -m network_tools discover --network 192.168.68.0/22` | M |

### P3 - Low (Future)

| ID | Story | Acceptance Criteria | Effort |
|----|-------|---------------------|--------|
| ND-009 | Scheduled discovery scans | Configure periodic auto-discovery | L |
| ND-010 | Discovery history tracking | Track device first_seen/last_seen over time | M |

---

## Database Operations Completed

```sql
-- 1. Updated network CIDR
UPDATE networks SET cidr = '192.168.68.0/22' WHERE slug = 'main-lan';

-- 2. Inserted Nest WiFi Router
INSERT INTO devices (site_id, network_id, name, slug, device_type, status,
                     manufacturer, model, mac_address, ip_address, metadata)
VALUES ('b0000000-...', 'd0000000-...', 'Nest WiFi Router', 'nest-wifi-router',
        'router', 'online', 'Google', 'Nest WiFi', '54:AF:97:50:C0:F8',
        '192.168.68.1', '{"role": "gateway", ...}');
```

---

## Next Steps

1. ~~**Immediate**: Run ND-001 and ND-002 to complete device inventory~~ ✅ DONE
2. **This Week**: Build OUI lookup (ND-003) for automated manufacturer ID
3. **Next Sprint**: Build discovery CLI tool (ND-008) with comparison report (ND-004)
4. **Manual Task**: Identify 7 Apple devices and 3 unknown devices

---
**Document Version**: 1.1
**Created**: 2025-11-28
**Updated**: 2025-11-28
**Author**: Claude Code (automated discovery test)
