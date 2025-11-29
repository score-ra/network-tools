"""Data models for ra_inventory entities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import UUID


@dataclass
class Site:
    """Site/organization entity."""

    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Network:
    """Network entity."""

    id: UUID
    site_id: UUID
    name: str
    slug: str
    cidr: str
    network_type: str = "lan"
    gateway_ip: Optional[str] = None
    vlan_id: Optional[int] = None
    ssid: Optional[str] = None
    is_primary: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Device:
    """Device entity matching ra_inventory schema."""

    id: Optional[UUID] = None
    site_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    network_id: Optional[UUID] = None
    category_id: Optional[int] = None

    # Core identification
    name: str = ""
    slug: str = ""
    device_type: str = "unknown"
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None

    # Network information
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    hostname: Optional[str] = None

    # Status
    status: str = "unknown"  # online, offline, unknown, maintenance

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: tuple, columns: list[str]) -> "Device":
        """Create Device from database row.

        Args:
            row: Database row tuple.
            columns: Column names.

        Returns:
            Device instance.
        """
        data = dict(zip(columns, row))
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})

    def to_insert_dict(self) -> dict[str, Any]:
        """Get dictionary for INSERT operation (excludes id, timestamps)."""
        return {
            "site_id": self.site_id,
            "zone_id": self.zone_id,
            "network_id": self.network_id,
            "category_id": self.category_id,
            "name": self.name,
            "slug": self.slug,
            "device_type": self.device_type,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial_number": self.serial_number,
            "firmware_version": self.firmware_version,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
            "hostname": self.hostname,
            "status": self.status,
            "metadata": self.metadata,
        }


@dataclass
class DiscoveredDevice:
    """Device discovered during network scan (before DB correlation)."""

    ip_address: str
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    manufacturer: Optional[str] = None
    device_type_guess: Optional[str] = None
    response_time_ms: Optional[int] = None
    discovery_method: str = "arp"  # arp, icmp, tcp
    last_seen: Optional[datetime] = None

    # Comparison status (set after DB comparison)
    status: str = "unknown"  # new, existing, updated, missing
    matched_device: Optional[Device] = None
    confidence: str = "low"  # low, medium, high

    def to_device(
        self,
        site_id: UUID,
        network_id: Optional[UUID] = None,
        name: Optional[str] = None,
    ) -> Device:
        """Convert to Device for database insertion.

        Args:
            site_id: Site UUID.
            network_id: Network UUID (optional).
            name: Device name (defaults to hostname or IP-based name).

        Returns:
            Device instance ready for insertion.
        """
        # Generate name if not provided
        if name is None:
            if self.hostname:
                name = self.hostname
            else:
                name = f"device-{self.ip_address.replace('.', '-')}"

        # Generate slug from name
        slug = name.lower().replace(" ", "-").replace("_", "-")

        return Device(
            site_id=site_id,
            network_id=network_id,
            name=name,
            slug=slug,
            device_type=self.device_type_guess or "unknown",
            manufacturer=self.manufacturer,
            mac_address=self.mac_address,
            ip_address=self.ip_address,
            hostname=self.hostname,
            status="online",
            metadata={
                "discovery_method": self.discovery_method,
                "discovered_at": (
                    self.last_seen.isoformat() if self.last_seen else None
                ),
            },
        )
