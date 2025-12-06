"""Tests for SnipeITClient."""

import pytest
from unittest.mock import Mock, patch

from network_tools.snipeit.client import SnipeITClient
from network_tools.snipeit.exceptions import (
    SnipeITAuthError,
    SnipeITConnectionError,
    SnipeITNotFoundError,
    SnipeITValidationError,
)
from network_tools.snipeit.models import Asset


@pytest.fixture
def client():
    """Create a SnipeITClient instance for testing."""
    return SnipeITClient(
        base_url="http://localhost:8082/api/v1",
        api_key="test_api_key",
        timeout=10,
        retry_count=1,
    )


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.status_code = 200
    return response


class TestSnipeITClientInit:
    """Tests for client initialization."""

    def test_init_strips_trailing_slash(self):
        """Base URL should not have trailing slash."""
        client = SnipeITClient(
            base_url="http://localhost:8082/api/v1/",
            api_key="key",
        )
        assert client.base_url == "http://localhost:8082/api/v1"

    def test_init_sets_auth_header(self):
        """Authorization header should be set."""
        client = SnipeITClient(
            base_url="http://localhost:8082/api/v1",
            api_key="my_secret_key",
        )
        assert "Authorization" in client._session.headers
        assert client._session.headers["Authorization"] == "Bearer my_secret_key"


class TestSnipeITClientRequest:
    """Tests for the _request method."""

    def test_request_returns_json(self, client, mock_response):
        """Successful request should return JSON."""
        mock_response.json.return_value = {"rows": [], "total": 0}

        with patch.object(client._session, "request", return_value=mock_response):
            result = client._request("GET", "/hardware")

        assert result == {"rows": [], "total": 0}

    def test_request_auth_error(self, client, mock_response):
        """401 response should raise SnipeITAuthError."""
        mock_response.status_code = 401

        with patch.object(client._session, "request", return_value=mock_response):
            with pytest.raises(SnipeITAuthError):
                client._request("GET", "/hardware")

    def test_request_not_found_error(self, client, mock_response):
        """404 response should raise SnipeITNotFoundError."""
        mock_response.status_code = 404

        with patch.object(client._session, "request", return_value=mock_response):
            with pytest.raises(SnipeITNotFoundError):
                client._request("GET", "/hardware/999")

    def test_request_connection_error(self, client):
        """Connection error should raise SnipeITConnectionError."""
        import requests

        with patch.object(
            client._session,
            "request",
            side_effect=requests.exceptions.ConnectionError(),
        ):
            with pytest.raises(SnipeITConnectionError):
                client._request("GET", "/hardware")

    def test_request_validation_error(self, client, mock_response):
        """API validation error should raise SnipeITValidationError."""
        mock_response.json.return_value = {
            "status": "error",
            "messages": {"name": ["Name is required"]},
        }

        with patch.object(client._session, "request", return_value=mock_response):
            with pytest.raises(SnipeITValidationError) as exc_info:
                client._request("POST", "/hardware", json={})

        assert "name" in exc_info.value.errors


class TestSnipeITClientHardware:
    """Tests for hardware CRUD operations."""

    def test_list_hardware_empty(self, client, mock_response):
        """List hardware should return empty list when no assets."""
        mock_response.json.return_value = {"rows": [], "total": 0}

        with patch.object(client._session, "request", return_value=mock_response):
            assets, total = client.list_hardware()

        assert assets == []
        assert total == 0

    def test_list_hardware_with_assets(self, client, mock_response):
        """List hardware should return Asset objects."""
        mock_response.json.return_value = {
            "rows": [
                {
                    "id": 1,
                    "name": "Test Device",
                    "asset_tag": "NET-123456",
                    "model": {"id": 1, "name": "Test Model"},
                    "status_label": {"id": 2, "name": "Ready"},
                    "category": {"id": 4, "name": "Network"},
                    "custom_fields": {
                        "MAC Address": {"value": "AA:BB:CC:DD:EE:FF"},
                        "IP Address": {"value": "192.168.1.100"},
                    },
                }
            ],
            "total": 1,
        }

        with patch.object(client._session, "request", return_value=mock_response):
            assets, total = client.list_hardware()

        assert len(assets) == 1
        assert total == 1
        assert isinstance(assets[0], Asset)
        assert assets[0].name == "Test Device"
        assert assets[0].mac_address == "AA:BB:CC:DD:EE:FF"

    def test_list_hardware_with_search(self, client, mock_response):
        """List hardware should pass search parameter."""
        mock_response.json.return_value = {"rows": [], "total": 0}

        with patch.object(client._session, "request", return_value=mock_response) as mock:
            client.list_hardware(search="router")

        call_args = mock.call_args
        assert call_args.kwargs["params"]["search"] == "router"

    def test_get_hardware_by_tag_found(self, client, mock_response):
        """Get by tag should return Asset when found."""
        mock_response.json.return_value = {
            "id": 1,
            "name": "Test Device",
            "asset_tag": "NET-123456",
            "custom_fields": {},
        }

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.get_hardware_by_tag("NET-123456")

        assert asset is not None
        assert asset.asset_tag == "NET-123456"

    def test_get_hardware_by_tag_not_found(self, client, mock_response):
        """Get by tag should return None when not found."""
        mock_response.status_code = 404

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.get_hardware_by_tag("NET-NOTFOUND")

        assert asset is None

    def test_create_hardware(self, client, mock_response):
        """Create hardware should return new Asset."""
        mock_response.json.return_value = {
            "status": "success",
            "payload": {
                "id": 99,
                "name": "New Device",
                "asset_tag": "NET-AABBCC",
                "custom_fields": {},
            },
        }

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.create_hardware(
                {
                    "name": "New Device",
                    "asset_tag": "NET-AABBCC",
                    "model_id": 1,
                    "status_id": 2,
                }
            )

        assert asset.id == 99
        assert asset.name == "New Device"

    def test_update_hardware(self, client, mock_response):
        """Update hardware should return updated Asset."""
        mock_response.json.return_value = {
            "status": "success",
            "payload": {
                "id": 1,
                "name": "Updated Device",
                "asset_tag": "NET-123456",
                "custom_fields": {},
            },
        }

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.update_hardware(1, {"name": "Updated Device"})

        assert asset.name == "Updated Device"


class TestSnipeITClientSearch:
    """Tests for search methods."""

    def test_search_by_mac_found(self, client, mock_response):
        """Search by MAC should return Asset when found."""
        mock_response.json.return_value = {
            "rows": [
                {
                    "id": 1,
                    "name": "Test Device",
                    "asset_tag": "NET-DDEEFF",
                    "custom_fields": {
                        "MAC Address": {"value": "AA:BB:CC:DD:EE:FF"},
                    },
                }
            ],
            "total": 1,
        }

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.search_by_mac("AA:BB:CC:DD:EE:FF")

        assert asset is not None
        assert asset.mac_address == "AA:BB:CC:DD:EE:FF"

    def test_search_by_mac_normalizes_format(self, client, mock_response):
        """Search by MAC should normalize MAC format."""
        mock_response.json.return_value = {
            "rows": [
                {
                    "id": 1,
                    "name": "Test Device",
                    "asset_tag": "NET-DDEEFF",
                    "custom_fields": {
                        "MAC Address": {"value": "AA:BB:CC:DD:EE:FF"},
                    },
                }
            ],
            "total": 1,
        }

        with patch.object(client._session, "request", return_value=mock_response):
            # Search with dashes instead of colons
            asset = client.search_by_mac("aa-bb-cc-dd-ee-ff")

        assert asset is not None

    def test_search_by_mac_not_found(self, client, mock_response):
        """Search by MAC should return None when not found."""
        mock_response.json.return_value = {"rows": [], "total": 0}

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.search_by_mac("00:00:00:00:00:00")

        assert asset is None

    def test_search_by_ip_found(self, client, mock_response):
        """Search by IP should return Asset when found."""
        mock_response.json.return_value = {
            "rows": [
                {
                    "id": 1,
                    "name": "Test Device",
                    "asset_tag": "NET-123456",
                    "custom_fields": {
                        "IP Address": {"value": "192.168.1.100"},
                    },
                }
            ],
            "total": 1,
        }

        with patch.object(client._session, "request", return_value=mock_response):
            asset = client.search_by_ip("192.168.1.100")

        assert asset is not None
        assert asset.ip_address == "192.168.1.100"


class TestSnipeITClientConnection:
    """Tests for connection testing."""

    def test_test_connection_success(self, client, mock_response):
        """Test connection should return True on success."""
        mock_response.json.return_value = {"rows": [], "total": 0}

        with patch.object(client._session, "request", return_value=mock_response):
            result = client.test_connection()

        assert result is True

    def test_test_connection_auth_failure(self, client, mock_response):
        """Test connection should raise on auth failure."""
        mock_response.status_code = 401

        with patch.object(client._session, "request", return_value=mock_response):
            with pytest.raises(SnipeITAuthError):
                client.test_connection()
