"""Tests for database queries module."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from network_tools.config import Config, set_config
from network_tools.db.models import Device, Network, Site


class TestSiteQueries:
    """Tests for site query functions."""

    def setup_method(self):
        """Reset config and pool before each test."""
        set_config(Config(db_password="test"))
        import network_tools.db.connection as conn_module
        conn_module._pool = None

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)
        import network_tools.db.connection as conn_module
        if conn_module._pool is not None:
            try:
                conn_module._pool.close()
            except Exception:
                pass
            conn_module._pool = None

    def test_get_site_by_slug_found(self):
        """Test get_site_by_slug returns site when found."""
        site_id = uuid4()
        mock_row = {
            "id": site_id,
            "name": "Test Site",
            "slug": "test-site",
            "description": "A test site",
            "created_at": None,
            "updated_at": None,
        }

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_site_by_slug

            result = get_site_by_slug("test-site")

            assert result is not None
            assert result.id == site_id
            assert result.name == "Test Site"
            assert result.slug == "test-site"

    def test_get_site_by_slug_not_found(self):
        """Test get_site_by_slug returns None when not found."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_site_by_slug

            result = get_site_by_slug("nonexistent")

            assert result is None

    def test_get_site_by_id_found(self):
        """Test get_site_by_id returns site when found."""
        site_id = uuid4()
        mock_row = {
            "id": site_id,
            "name": "Test Site",
            "slug": "test-site",
            "description": None,
            "created_at": None,
            "updated_at": None,
        }

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_site_by_id

            result = get_site_by_id(site_id)

            assert result is not None
            assert result.id == site_id


class TestNetworkQueries:
    """Tests for network query functions."""

    def setup_method(self):
        """Reset config and pool before each test."""
        set_config(Config(db_password="test"))
        import network_tools.db.connection as conn_module
        conn_module._pool = None

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)
        import network_tools.db.connection as conn_module
        if conn_module._pool is not None:
            try:
                conn_module._pool.close()
            except Exception:
                pass
            conn_module._pool = None

    def test_get_networks_by_site(self):
        """Test get_networks_by_site returns list of networks."""
        site_id = uuid4()
        mock_rows = [
            {
                "id": uuid4(),
                "site_id": site_id,
                "name": "Main LAN",
                "slug": "main-lan",
                "cidr": "192.168.68.0/22",
                "network_type": "lan",
                "gateway_ip": "192.168.68.1",
                "vlan_id": None,
                "ssid": None,
                "is_primary": True,
                "created_at": None,
                "updated_at": None,
            }
        ]

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_rows
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_networks_by_site

            result = get_networks_by_site(site_id)

            assert len(result) == 1
            assert result[0].name == "Main LAN"
            assert result[0].is_primary is True

    def test_get_network_by_cidr_found(self):
        """Test get_network_by_cidr returns network when found."""
        site_id = uuid4()
        network_id = uuid4()
        mock_row = {
            "id": network_id,
            "site_id": site_id,
            "name": "Main LAN",
            "slug": "main-lan",
            "cidr": "192.168.68.0/22",
            "network_type": "lan",
            "gateway_ip": None,
            "vlan_id": None,
            "ssid": None,
            "is_primary": False,
            "created_at": None,
            "updated_at": None,
        }

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_network_by_cidr

            result = get_network_by_cidr(site_id, "192.168.68.0/22")

            assert result is not None
            assert result.id == network_id


class TestDeviceQueries:
    """Tests for device query functions."""

    def setup_method(self):
        """Reset config and pool before each test."""
        set_config(Config(db_password="test"))
        import network_tools.db.connection as conn_module
        conn_module._pool = None

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)
        import network_tools.db.connection as conn_module
        if conn_module._pool is not None:
            try:
                conn_module._pool.close()
            except Exception:
                pass
            conn_module._pool = None

    def _make_device_row(self, **kwargs):
        """Create a mock device row."""
        defaults = {
            "id": uuid4(),
            "site_id": uuid4(),
            "zone_id": None,
            "network_id": None,
            "category_id": None,
            "name": "Test Device",
            "slug": "test-device",
            "device_type": "computer",
            "manufacturer": None,
            "model": None,
            "serial_number": None,
            "firmware_version": None,
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "ip_address": "192.168.68.100",
            "hostname": None,
            "status": "online",
            "metadata": {},
            "created_at": None,
            "updated_at": None,
        }
        defaults.update(kwargs)
        return defaults

    def test_get_devices_by_site(self):
        """Test get_devices_by_site returns list of devices."""
        site_id = uuid4()
        mock_rows = [self._make_device_row(site_id=site_id)]

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_rows
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_devices_by_site

            result = get_devices_by_site(site_id)

            assert len(result) == 1
            assert result[0].name == "Test Device"

    def test_get_device_by_mac_found(self):
        """Test get_device_by_mac returns device when found."""
        mock_row = self._make_device_row()

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_device_by_mac

            result = get_device_by_mac("AA:BB:CC:DD:EE:FF")

            assert result is not None
            assert result.mac_address == "AA:BB:CC:DD:EE:FF"

    def test_get_device_by_mac_normalizes_format(self):
        """Test get_device_by_mac normalizes MAC address format."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_device_by_mac

            # Test with dashes instead of colons
            get_device_by_mac("aa-bb-cc-dd-ee-ff")

            # Verify normalized MAC was used in query
            call_args = mock_cursor.execute.call_args
            assert "AABBCCDDEEFF" in call_args[0][1]

    def test_get_device_by_ip_with_site(self):
        """Test get_device_by_ip with site filter."""
        site_id = uuid4()
        mock_row = self._make_device_row(site_id=site_id)

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_device_by_ip

            result = get_device_by_ip("192.168.68.100", site_id=site_id)

            assert result is not None
            # Verify site_id was included in query
            call_args = mock_cursor.execute.call_args
            assert site_id in call_args[0][1]

    def test_get_device_by_ip_without_site(self):
        """Test get_device_by_ip without site filter."""
        mock_row = self._make_device_row()

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import get_device_by_ip

            result = get_device_by_ip("192.168.68.100")

            assert result is not None

    def test_insert_device(self):
        """Test insert_device creates new device."""
        device_id = uuid4()
        device = Device(
            site_id=uuid4(),
            name="New Device",
            slug="new-device",
            mac_address="11:22:33:44:55:66",
            ip_address="192.168.68.50",
        )

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (device_id,)
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import insert_device

            result = insert_device(device)

            assert result == device_id
            mock_conn.commit.assert_called_once()

    def test_insert_device_with_connection(self):
        """Test insert_device uses provided connection."""
        device_id = uuid4()
        device = Device(
            site_id=uuid4(),
            name="New Device",
            slug="new-device",
        )

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (device_id,)
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        from network_tools.db.queries import insert_device

        result = insert_device(device, conn=mock_conn)

        assert result == device_id
        # Should not commit when using provided connection
        mock_conn.commit.assert_not_called()

    def test_update_device_ip(self):
        """Test update_device_ip updates IP address."""
        device_id = uuid4()

        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import update_device_ip

            result = update_device_ip(device_id, "192.168.68.200")

            assert result is True
            mock_conn.commit.assert_called_once()

    def test_update_device_status(self):
        """Test update_device_status updates status."""
        device_id = uuid4()

        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import update_device_status

            result = update_device_status(device_id, "offline")

            assert result is True

    def test_batch_insert_devices(self):
        """Test batch_insert_devices inserts multiple devices."""
        device_ids = [uuid4(), uuid4()]
        devices = [
            Device(site_id=uuid4(), name="Device 1", slug="device-1"),
            Device(site_id=uuid4(), name="Device 2", slug="device-2"),
        ]

        call_count = [0]

        def mock_fetchone():
            result = (device_ids[call_count[0]],)
            call_count[0] += 1
            return result

        mock_cursor = MagicMock()
        mock_cursor.fetchone = mock_fetchone
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.queries import batch_insert_devices

            result = batch_insert_devices(devices)

            assert len(result) == 2
            assert result == device_ids
            mock_conn.commit.assert_called_once()
