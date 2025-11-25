# Device: SYMPHONY-CORE (Epson WF-7840)

## Overview

| Field | Value |
|-------|-------|
| Device ID | `epson-wf7840` |
| Organization | sc-office |
| Manufacturer | EPSON |
| Model | Microsoft IPP Class Driver |
| Model Number | WF-7840 Series |
| Serial Number | DCCD2F7AB1BC |
| Category | Printer, Multi Function Printer, Scanner |
| Status | Active |

## Network Configuration

### Basic Settings (from Web UI)

| Field | Value |
|-------|-------|
| Device Name | SYMPHONY-CORE |
| Location | (not set) |

### IP Configuration

| Field | Value |
|-------|-------|
| Obtain IP Address | **Manual** (Static) |
| IP Address | 192.168.1.8 |
| Subnet Mask | 255.255.255.0 |
| Default Gateway | 192.168.1.1 |
| Set using BOOTP | Disable |
| Set using APIPA | Enable (grayed out) |

### DNS Settings

| Field | Value |
|-------|-------|
| DNS Server Setting | Manual |
| Primary DNS Server | (not set - not required for printing) |
| Secondary DNS Server | (not set) |
| DNS Host Name Setting | Manual |
| DNS Host Name | SYMPHONY-CORE |
| DNS Domain Name Setting | Auto |
| DNS Domain Name | lan |
| Register to DNS | Disable |

### Proxy Settings

| Field | Value |
|-------|-------|
| Proxy Server Setting | Do Not Use |
| Proxy Server | (not set) |
| Proxy Server Port Number | (not set) |
| Proxy Server User Name | (not set) |
| Proxy Server Password | (not set) |

### IPv6 Settings

| Field | Value |
|-------|-------|
| IPv6 Setting | Disable |
| IPv6 Privacy Extension | Disable |
| IPv6 DHCP Server Setting | Do Not Use |
| IPv6 Address | (not set) |
| IPv6 Address Default Gateway | (not set) |
| IPv6 Link-Local Address | (not set) |
| IPv6 Stateful Address | (not set) |
| IPv6 Stateless Address 1-3 | (not set) |
| IPv6 Primary DNS Server | (not set) |
| IPv6 Secondary DNS Server | (not set) |

### Wireless Configuration

| Field | Value |
|-------|-------|
| Connection Type | Wi-Fi |
| SSID | SpectrumSetup-40EF |
| Security | WPA2-PSK(AES) |
| Wi-Fi Mode | IEEE 802.11b/g/n |
| Channel | 6 |
| Signal Strength | Excellent |
| Wi-Fi Setup | Manual |
| MAC Address | DC:CD:2F:7A:B1:BC |

## Services & Ports

| Service | Port | Protocol | Status |
|---------|------|----------|--------|
| HTTP (Web Interface) | 80 | TCP | Open |
| IPP (Internet Printing) | 631 | TCP | Open |
| Web Services | - | - | Enabled |

## Web Interface

| Field | Value |
|-------|-------|
| URL | http://192.168.1.8:80/PRESENTATION/ |
| Authentication | TBD |
| Default Credentials | TBD |

## Unique Identifiers

| Field | Value |
|-------|-------|
| UUID | urn:uuid:cfe92100-67c4-11d4-a45f-dccd2f7ab1bc |
| Transport | Web Services |
| Connection | Standard |

## Known Issues

| Issue | Workaround | Status |
|-------|------------|--------|
| Printer unreachable after power on | Static IP configured | **Resolved** |

## Troubleshooting History

### Issue: Printer Unreachable After Power On

**Root Cause:** Printer was using DHCP with APIPA fallback. When powered on, it would sometimes get a different IP or fall back to 169.254.x.x (not routable).

**Resolution (2025-11-25):** Configured static IP via printer web UI:
- Changed "Obtain IP Address" from Auto to **Manual**
- Set static IP: 192.168.1.8
- Set Subnet Mask: 255.255.255.0
- Set Default Gateway: 192.168.1.1

**Access Web UI:** http://192.168.1.8/PRESENTATION/ → Network Settings → Basic

---
**Last Updated**: 2025-11-25
