"""Data models for Snipe-IT entities and discovery."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Asset:
    """Snipe-IT hardware asset."""

    id: int
    name: str
    asset_tag: str
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    status_id: Optional[int] = None
    status_name: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    manufacturer_name: Optional[str] = None
    location_id: Optional[int] = None
    location_name: Optional[str] = None
    serial: Optional[str] = None
    notes: Optional[str] = None

    # Custom fields
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None

    # Timestamps
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Asset":
        """Create Asset from Snipe-IT API response.

        Args:
            data: API response dictionary for a single asset.

        Returns:
            Asset instance.
        """
        # Extract nested values safely
        model = data.get("model") or {}
        status = data.get("status_label") or {}
        category = data.get("category") or {}
        manufacturer = data.get("manufacturer") or {}
        location = data.get("location") or {}
        custom_fields = data.get("custom_fields") or {}

        # Extract custom field values
        mac_field = custom_fields.get("MAC Address") or {}
        ip_field = custom_fields.get("IP Address") or {}

        return cls(
            id=data.get("id", 0),
            name=data.get("name", ""),
            asset_tag=data.get("asset_tag", ""),
            model_id=model.get("id"),
            model_name=model.get("name"),
            status_id=status.get("id"),
            status_name=status.get("name"),
            category_id=category.get("id"),
            category_name=category.get("name"),
            manufacturer_name=manufacturer.get("name"),
            location_id=location.get("id") if location else None,
            location_name=location.get("name") if location else None,
            serial=data.get("serial"),
            notes=data.get("notes"),
            mac_address=mac_field.get("value"),
            ip_address=ip_field.get("value"),
            created_at=data.get("created_at", {}).get("datetime")
            if isinstance(data.get("created_at"), dict)
            else data.get("created_at"),
            updated_at=data.get("updated_at", {}).get("datetime")
            if isinstance(data.get("updated_at"), dict)
            else data.get("updated_at"),
        )


@dataclass
class DiscoveredDevice:
    """Device discovered during network scan."""

    ip_address: str
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    manufacturer: Optional[str] = None
    device_type_guess: Optional[str] = None
    response_time_ms: Optional[int] = None
    discovery_method: str = "arp"
    last_seen: Optional[datetime] = None

    # Comparison status (set after Snipe-IT comparison)
    status: str = "unknown"  # new, existing, updated, missing
    matched_asset: Optional[Asset] = None
    confidence: str = "low"  # low, medium, high

    def to_snipeit_payload(
        self,
        model_id: int,
        status_id: int,
        name: Optional[str] = None,
        location_id: Optional[int] = None,
    ) -> dict[str, Any]:
        """Convert to Snipe-IT asset creation payload.

        Args:
            model_id: Snipe-IT model ID for the asset.
            status_id: Snipe-IT status ID (e.g., Ready to Deploy).
            name: Optional device name (defaults to hostname or generated).
            location_id: Optional Snipe-IT location ID.

        Returns:
            Dictionary payload for POST /hardware.
        """
        # Generate name if not provided
        if name is None:
            if self.hostname:
                name = self.hostname
            elif self.manufacturer:
                ip_suffix = self.ip_address.split(".")[-1]
                name = f"{self.manufacturer}-{ip_suffix}"
            else:
                name = f"device-{self.ip_address.replace('.', '-')}"

        # Generate asset tag from MAC (last 6 chars) or IP
        if self.mac_address:
            mac_clean = self.mac_address.replace(":", "").replace("-", "").upper()
            asset_tag = f"NET-{mac_clean[-6:]}"
        else:
            ip_clean = self.ip_address.replace(".", "")
            asset_tag = f"NET-{ip_clean[-6:]}"

        # Build notes
        notes_parts = []
        if self.manufacturer:
            notes_parts.append(f"Manufacturer: {self.manufacturer}")
        if self.last_seen:
            notes_parts.append(f"Discovered: {self.last_seen.isoformat()}")
        notes_parts.append(f"Discovery method: {self.discovery_method}")

        payload: dict[str, Any] = {
            "name": name,
            "asset_tag": asset_tag,
            "model_id": model_id,
            "status_id": status_id,
            "notes": "\n".join(notes_parts),
        }

        # Add custom fields
        if self.mac_address:
            payload["_snipeit_mac_address_1"] = self.mac_address.upper()
        if self.ip_address:
            payload["_snipeit_ip_address_2"] = self.ip_address

        # Add location if provided
        if location_id:
            payload["rtd_location_id"] = location_id

        return payload

    def generate_asset_tag(self) -> str:
        """Generate unique asset tag from MAC or IP.

        Returns:
            Asset tag string (e.g., NET-DDEEFF).
        """
        if self.mac_address:
            mac_clean = self.mac_address.replace(":", "").replace("-", "").upper()
            return f"NET-{mac_clean[-6:]}"
        else:
            ip_clean = self.ip_address.replace(".", "")
            return f"NET-{ip_clean[-6:]}"
