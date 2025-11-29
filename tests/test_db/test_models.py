"""Tests for database models."""

from datetime import datetime
from uuid import UUID, uuid4

import pytest

from network_tools.db.models import Device, DiscoveredDevice, Network, Site


class TestSite:
    """Tests for Site model."""

    def test_create_site(self):
        """Test site creation."""
        site_id = uuid4()
        site = Site(
            id=site_id,
            name="Test Site",
            slug="test-site",
            description="A test site",
        )

        assert site.id == site_id
        assert site.name == "Test Site"
        assert site.slug == "test-site"
        assert site.description == "A test site"

    def test_site_optional_fields(self):
        """Test site with minimal fields."""
        site = Site(id=uuid4(), name="Minimal", slug="minimal")

        assert site.description is None
        assert site.created_at is None
        assert site.updated_at is None


class TestNetwork:
    """Tests for Network model."""

    def test_create_network(self):
        """Test network creation."""
        network_id = uuid4()
        site_id = uuid4()

        network = Network(
            id=network_id,
            site_id=site_id,
            name="Main LAN",
            slug="main-lan",
            cidr="192.168.68.0/22",
            network_type="lan",
            gateway_ip="192.168.68.1",
            is_primary=True,
        )

        assert network.id == network_id
        assert network.site_id == site_id
        assert network.cidr == "192.168.68.0/22"
        assert network.is_primary is True

    def test_network_defaults(self):
        """Test network default values."""
        network = Network(
            id=uuid4(),
            site_id=uuid4(),
            name="Test",
            slug="test",
            cidr="10.0.0.0/24",
        )

        assert network.network_type == "lan"
        assert network.is_primary is False
        assert network.vlan_id is None
        assert network.ssid is None


class TestDevice:
    """Tests for Device model."""

    def test_create_device(self):
        """Test device creation with all fields."""
        device = Device(
            id=uuid4(),
            site_id=uuid4(),
            name="Test Device",
            slug="test-device",
            device_type="computer",
            manufacturer="Dell",
            model="XPS 15",
            mac_address="AA:BB:CC:DD:EE:FF",
            ip_address="192.168.68.100",
            hostname="test-pc",
            status="online",
        )

        assert device.name == "Test Device"
        assert device.mac_address == "AA:BB:CC:DD:EE:FF"
        assert device.status == "online"

    def test_device_defaults(self):
        """Test device default values."""
        device = Device()

        assert device.id is None
        assert device.name == ""
        assert device.slug == ""
        assert device.device_type == "unknown"
        assert device.status == "unknown"
        assert device.metadata == {}

    def test_to_insert_dict(self):
        """Test conversion to insert dictionary."""
        site_id = uuid4()
        device = Device(
            site_id=site_id,
            name="Insert Test",
            slug="insert-test",
            device_type="router",
            mac_address="11:22:33:44:55:66",
            ip_address="192.168.1.1",
            status="online",
        )

        result = device.to_insert_dict()

        assert result["site_id"] == site_id
        assert result["name"] == "Insert Test"
        assert result["mac_address"] == "11:22:33:44:55:66"
        assert "id" not in result
        assert "created_at" not in result
        assert "updated_at" not in result

    def test_to_insert_dict_includes_metadata(self):
        """Test metadata is included in insert dict."""
        device = Device(
            name="With Metadata",
            slug="with-metadata",
            metadata={"discovered_via": "arp", "notes": "test"},
        )

        result = device.to_insert_dict()

        assert result["metadata"] == {"discovered_via": "arp", "notes": "test"}


class TestDiscoveredDevice:
    """Tests for DiscoveredDevice model."""

    def test_create_discovered_device(self):
        """Test discovered device creation."""
        device = DiscoveredDevice(
            ip_address="192.168.68.50",
            mac_address="AA:BB:CC:DD:EE:FF",
            hostname="test-host",
            manufacturer="Apple",
            discovery_method="arp",
        )

        assert device.ip_address == "192.168.68.50"
        assert device.mac_address == "AA:BB:CC:DD:EE:FF"
        assert device.status == "unknown"
        assert device.confidence == "low"

    def test_to_device_with_hostname(self):
        """Test conversion to Device uses hostname as name."""
        site_id = uuid4()
        discovered = DiscoveredDevice(
            ip_address="192.168.68.50",
            mac_address="AA:BB:CC:DD:EE:FF",
            hostname="my-laptop",
            manufacturer="Apple",
        )

        device = discovered.to_device(site_id=site_id)

        assert device.name == "my-laptop"
        assert device.slug == "my-laptop"
        assert device.site_id == site_id
        assert device.mac_address == "AA:BB:CC:DD:EE:FF"
        assert device.status == "online"

    def test_to_device_without_hostname(self):
        """Test conversion generates name from IP."""
        site_id = uuid4()
        discovered = DiscoveredDevice(
            ip_address="192.168.68.50",
            mac_address="AA:BB:CC:DD:EE:FF",
        )

        device = discovered.to_device(site_id=site_id)

        assert device.name == "device-192-168-68-50"
        assert device.slug == "device-192-168-68-50"

    def test_to_device_with_custom_name(self):
        """Test conversion with explicit name."""
        site_id = uuid4()
        network_id = uuid4()
        discovered = DiscoveredDevice(
            ip_address="192.168.68.50",
            mac_address="AA:BB:CC:DD:EE:FF",
        )

        device = discovered.to_device(
            site_id=site_id,
            network_id=network_id,
            name="Custom Name",
        )

        assert device.name == "Custom Name"
        assert device.slug == "custom-name"
        assert device.network_id == network_id

    def test_to_device_includes_discovery_metadata(self):
        """Test metadata includes discovery info."""
        discovered = DiscoveredDevice(
            ip_address="192.168.68.50",
            discovery_method="icmp",
            last_seen=datetime(2025, 11, 29, 12, 0, 0),
        )

        device = discovered.to_device(site_id=uuid4())

        assert device.metadata["discovery_method"] == "icmp"
        assert device.metadata["discovered_at"] == "2025-11-29T12:00:00"

    def test_to_device_uses_device_type_guess(self):
        """Test device type from guess."""
        discovered = DiscoveredDevice(
            ip_address="192.168.68.50",
            device_type_guess="speaker",
        )

        device = discovered.to_device(site_id=uuid4())

        assert device.device_type == "speaker"

    def test_to_device_default_device_type(self):
        """Test default device type when no guess."""
        discovered = DiscoveredDevice(ip_address="192.168.68.50")

        device = discovered.to_device(site_id=uuid4())

        assert device.device_type == "unknown"
