"""ARP-based network scanner for device discovery."""

import subprocess
import re
import ipaddress
from dataclasses import dataclass
from typing import Optional

from network_tools.logging import get_logger

logger = get_logger("scanner.arp")


@dataclass
class ARPEntry:
    """Represents an ARP table entry."""

    ip_address: str
    mac_address: str
    interface: Optional[str] = None


def normalize_mac(mac: str) -> str:
    """Normalize MAC address to uppercase colon-separated format.

    Args:
        mac: MAC address in any format.

    Returns:
        Normalized MAC (e.g., 'AA:BB:CC:DD:EE:FF').
    """
    # Remove all separators and convert to uppercase
    cleaned = mac.upper().replace(":", "").replace("-", "").replace(".", "")

    # Pad if needed (some systems show shortened MACs)
    cleaned = cleaned.zfill(12)

    # Insert colons
    return ":".join(cleaned[i : i + 2] for i in range(0, 12, 2))


def get_arp_table() -> list[ARPEntry]:
    """Get current ARP table entries from the system.

    Returns:
        List of ARP entries.
    """
    entries = []

    try:
        # Run arp -a command (works on Windows)
        result = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            logger.warning(f"ARP command failed: {result.stderr}")
            return entries

        # Parse Windows ARP output
        # Format: "  192.168.68.1         aa-bb-cc-dd-ee-ff     dynamic"
        # Or: "Interface: 192.168.68.x --- 0xNN"
        pattern = r"^\s*(\d+\.\d+\.\d+\.\d+)\s+([\da-fA-F-]{17})\s+(\w+)"

        for line in result.stdout.splitlines():
            match = re.match(pattern, line)
            if match:
                ip_addr = match.group(1)
                mac_addr = normalize_mac(match.group(2))

                # Skip broadcast and multicast MACs
                if mac_addr.startswith("FF:FF:FF") or mac_addr.startswith("01:00:5E"):
                    continue

                entries.append(ARPEntry(ip_address=ip_addr, mac_address=mac_addr))

        logger.info(f"Found {len(entries)} ARP entries")

    except subprocess.TimeoutExpired:
        logger.error("ARP command timed out")
    except Exception as e:
        logger.error(f"Failed to get ARP table: {e}")

    return entries


def ping_sweep(network: str, timeout: int = 1) -> list[str]:
    """Ping sweep a network to populate ARP table.

    Args:
        network: Network CIDR (e.g., '192.168.68.0/24').
        timeout: Ping timeout in seconds.

    Returns:
        List of responding IP addresses.
    """
    responding = []

    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError as e:
        logger.error(f"Invalid network CIDR: {e}")
        return responding

    # For large networks, limit the scan
    hosts = list(net.hosts())
    if len(hosts) > 1024:
        logger.warning(f"Network has {len(hosts)} hosts, limiting to first 1024")
        hosts = hosts[:1024]

    logger.info(f"Starting ping sweep of {len(hosts)} hosts in {network}")

    for i, host in enumerate(hosts):
        ip = str(host)

        try:
            # Windows ping: -n 1 (count), -w (timeout in ms)
            result = subprocess.run(
                ["ping", "-n", "1", "-w", str(timeout * 1000), ip],
                capture_output=True,
                text=True,
                timeout=timeout + 2,
            )

            if result.returncode == 0:
                responding.append(ip)
                logger.debug(f"Host {ip} responded")

        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            logger.debug(f"Ping failed for {ip}: {e}")

        # Progress logging every 50 hosts
        if (i + 1) % 50 == 0:
            logger.info(f"Progress: {i + 1}/{len(hosts)} hosts scanned")

    logger.info(f"Ping sweep complete: {len(responding)} hosts responded")
    return responding


def scan_network(network: str, use_ping: bool = True) -> list[ARPEntry]:
    """Scan a network for devices using ARP.

    Args:
        network: Network CIDR to scan.
        use_ping: Whether to ping sweep first to populate ARP table.

    Returns:
        List of discovered ARP entries.
    """
    if use_ping:
        ping_sweep(network, timeout=1)

    # Get ARP table after ping sweep
    entries = get_arp_table()

    # Filter to only include IPs in the target network
    try:
        net = ipaddress.ip_network(network, strict=False)
        entries = [e for e in entries if ipaddress.ip_address(e.ip_address) in net]
    except ValueError:
        pass

    logger.info(f"Found {len(entries)} devices in {network}")
    return entries
