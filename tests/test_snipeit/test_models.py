"""Tests for Snipe-IT models."""

import pytest
from datetime import datetime

from network_tools.snipeit.models import Asset, DiscoveredDevice


class TestAsset:
    """Tests for Asset model."""

    def test_from_api_response_minimal(self):
        """Asset should be created from minimal API response."""
        data = {
            "id": 1,
            "name": "Test Device",
            "asset_tag": "NET-123456",
        }

        asset = Asset.from_api_response(data)

        assert asset.id == 1
        assert asset.name == "Test Device"
        assert asset.asset_tag == "NET-123456"
        assert asset.mac_address is None
        assert asset.ip_address is None

    def test_from_api_response_full(self):
        """Asset should be created from full API response."""
        data = {
            "id": 42,
            "name": "Router",
            "asset_tag": "NET-AABBCC",
            "serial": "SN12345",
            "notes": "Main router",
            "model": {"id": 5, "name": "AC1200"},
            "status_label": {"id": 2, "name": "Ready to Deploy"},
            "category": {"id": 4, "name": "Network"},
            "manufacturer": {"id": 3, "name": "TP-Link"},
            "location": {"id": 15, "name": "Server Closet"},
            "custom_fields": {
                "MAC Address": {"value": "AA:BB:CC:DD:EE:FF", "field_format": "MAC"},
                "IP Address": {"value": "192.168.1.1", "field_format": "IP"},
            },
            "created_at": {"datetime": "2025-01-15 10:30:00"},
            "updated_at": {"datetime": "2025-01-20 14:45:00"},
        }

        asset = Asset.from_api_response(data)

        assert asset.id == 42
        assert asset.name == "Router"
        assert asset.asset_tag == "NET-AABBCC"
        assert asset.serial == "SN12345"
        assert asset.notes == "Main router"
        assert asset.model_id == 5
        assert asset.model_name == "AC1200"
        assert asset.status_id == 2
        assert asset.status_name == "Ready to Deploy"
        assert asset.category_id == 4
        assert asset.category_name == "Network"
        assert asset.manufacturer_name == "TP-Link"
        assert asset.location_id == 15
        assert asset.location_name == "Server Closet"
        assert asset.mac_address == "AA:BB:CC:DD:EE:FF"
        assert asset.ip_address == "192.168.1.1"

    def test_from_api_response_empty_custom_fields(self):
        """Asset should handle empty custom fields."""
        data = {
            "id": 1,
            "name": "Test",
            "asset_tag": "NET-000000",
            "custom_fields": {},
        }

        asset = Asset.from_api_response(data)

        assert asset.mac_address is None
        assert asset.ip_address is None

    def test_from_api_response_null_nested(self):
        """Asset should handle null nested objects."""
        data = {
            "id": 1,
            "name": "Test",
            "asset_tag": "NET-000000",
            "model": None,
            "status_label": None,
            "category": None,
            "manufacturer": None,
            "location": None,
            "custom_fields": None,
        }

        asset = Asset.from_api_response(data)

        assert asset.model_id is None
        assert asset.status_id is None
        assert asset.category_id is None
        assert asset.manufacturer_name is None
        assert asset.location_id is None


class TestDiscoveredDevice:
    """Tests for DiscoveredDevice model."""

    def test_init_defaults(self):
        """DiscoveredDevice should have sensible defaults."""
        device = DiscoveredDevice(ip_address="192.168.1.100")

        assert device.ip_address == "192.168.1.100"
        assert device.mac_address is None
        assert device.hostname is None
        assert device.manufacturer is None
        assert device.device_type_guess is None
        assert device.discovery_method == "arp"
        assert device.status == "unknown"
        assert device.confidence == "low"

    def test_to_snipeit_payload_minimal(self):
        """Payload should include required fields."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
        )

        payload = device.to_snipeit_payload(model_id=1, status_id=2)

        assert payload["model_id"] == 1
        assert payload["status_id"] == 2
        assert payload["asset_tag"] == "NET-DDEEFF"
        assert payload["_snipeit_mac_address_1"] == "AA:BB:CC:DD:EE:FF"
        assert payload["_snipeit_ip_address_2"] == "192.168.1.100"
        assert "name" in payload
        assert "notes" in payload

    def test_to_snipeit_payload_with_hostname(self):
        """Payload should use hostname as name if available."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
            hostname="my-router",
        )

        payload = device.to_snipeit_payload(model_id=1, status_id=2)

        assert payload["name"] == "my-router"

    def test_to_snipeit_payload_with_manufacturer(self):
        """Payload should use manufacturer in name if no hostname."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
            manufacturer="Cisco",
        )

        payload = device.to_snipeit_payload(model_id=1, status_id=2)

        assert "Cisco" in payload["name"]
        assert "Manufacturer: Cisco" in payload["notes"]

    def test_to_snipeit_payload_custom_name(self):
        """Payload should use provided name."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
            hostname="auto-name",
        )

        payload = device.to_snipeit_payload(model_id=1, status_id=2, name="Custom Name")

        assert payload["name"] == "Custom Name"

    def test_to_snipeit_payload_with_location(self):
        """Payload should include location if provided."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
        )

        payload = device.to_snipeit_payload(model_id=1, status_id=2, location_id=15)

        assert payload["rtd_location_id"] == 15

    def test_to_snipeit_payload_no_mac(self):
        """Payload should generate asset tag from IP if no MAC."""
        device = DiscoveredDevice(ip_address="192.168.1.100")

        payload = device.to_snipeit_payload(model_id=1, status_id=2)

        # Last 6 chars of "1921681100" = "81100" (padded/truncated)
        assert payload["asset_tag"].startswith("NET-")
        assert "_snipeit_mac_address_1" not in payload

    def test_generate_asset_tag_from_mac(self):
        """Asset tag should be generated from MAC address."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
        )

        tag = device.generate_asset_tag()

        assert tag == "NET-DDEEFF"

    def test_generate_asset_tag_from_mac_with_dashes(self):
        """Asset tag should normalize MAC with dashes."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="aa-bb-cc-dd-ee-ff",
        )

        tag = device.generate_asset_tag()

        assert tag == "NET-DDEEFF"

    def test_generate_asset_tag_from_ip(self):
        """Asset tag should be generated from IP if no MAC."""
        device = DiscoveredDevice(ip_address="192.168.68.100")

        tag = device.generate_asset_tag()

        assert tag.startswith("NET-")
        # Last 6 chars of "19216868100" = "868100"
        assert tag == "NET-868100"

    def test_to_snipeit_payload_with_last_seen(self):
        """Payload notes should include discovery timestamp."""
        device = DiscoveredDevice(
            ip_address="192.168.1.100",
            mac_address="AA:BB:CC:DD:EE:FF",
            last_seen=datetime(2025, 1, 15, 10, 30, 0),
        )

        payload = device.to_snipeit_payload(model_id=1, status_id=2)

        assert "Discovered: 2025-01-15" in payload["notes"]
