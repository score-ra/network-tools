# Organization: sc-office

## Overview

| Field | Value |
|-------|-------|
| Organization ID | `sc-office` |
| Location | Co-working facility |
| Network Type | Co-working (Shared Wi-Fi) |
| Created | 2025-11-25 |
| Last Updated | 2025-11-25 |

## Network Configuration

### WAN Details

| Field | Value |
|-------|-------|
| ISP | Spectrum (via co-working facility) |
| WAN IP | Shared / Dynamic |
| Connection Type | Cable/Fiber (facility managed) |
| Speed (Down/Up) | TBD |

### LAN Details

| Field | Value |
|-------|-------|
| Network Subnet | 192.168.1.0/24 |
| Gateway | 192.168.1.1 |
| DHCP Range | Auto (facility managed) |
| DNS Servers | 192.168.1.1 (Auto) |

### Wireless Networks

| SSID | Security | Band | Notes |
|------|----------|------|-------|
| SpectrumSetup-40EF | WPA2-PSK(AES) | 2.4GHz (802.11b/g/n) | Shared co-working network |

## Devices

| Device Name | Type | IP Address | Status |
|-------------|------|------------|--------|
| SYMPHONY-CORE (Epson WF-7840) | Printer | 192.168.1.8 | Active |

See individual device specs in `devices/` subdirectory.

## Notes

- This is a co-working facility with shared network infrastructure
- No control over router/gateway configuration
- Personal devices connect to shared Wi-Fi
- Printer is personally owned, connected to shared network
