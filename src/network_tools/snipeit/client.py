"""Snipe-IT API client."""

import logging
from typing import Any, Optional

import requests

from .exceptions import (
    SnipeITAuthError,
    SnipeITConnectionError,
    SnipeITError,
    SnipeITNotFoundError,
    SnipeITValidationError,
)
from .models import Asset

logger = logging.getLogger(__name__)


class SnipeITClient:
    """Client for interacting with Snipe-IT REST API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        retry_count: int = 3,
    ):
        """Initialize Snipe-IT API client.

        Args:
            base_url: Base URL for API (e.g., http://localhost:8082/api/v1).
            api_key: Bearer token for authentication.
            timeout: Request timeout in seconds.
            retry_count: Number of retries for transient failures.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.retry_count = retry_count

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Make authenticated API request.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE).
            endpoint: API endpoint (e.g., /hardware).
            params: Query parameters.
            json: JSON body for POST/PATCH.

        Returns:
            API response as dictionary.

        Raises:
            SnipeITConnectionError: Connection failed.
            SnipeITAuthError: Authentication failed.
            SnipeITNotFoundError: Resource not found.
            SnipeITValidationError: Validation errors from API.
            SnipeITError: Other API errors.
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.retry_count):
            try:
                logger.debug(f"API {method} {url} (attempt {attempt + 1})")

                response = self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    timeout=self.timeout,
                )

                # Handle HTTP errors
                if response.status_code == 401:
                    raise SnipeITAuthError("Authentication failed. Check API key.")

                if response.status_code == 404:
                    raise SnipeITNotFoundError(f"Resource not found: {endpoint}")

                if response.status_code == 429:
                    # Rate limited - retry
                    logger.warning("Rate limited, retrying...")
                    continue

                # Parse response
                data = response.json()

                # Check for API-level errors (Snipe-IT returns 200 with status field)
                if isinstance(data, dict) and data.get("status") == "error":
                    messages = data.get("messages", {})
                    if isinstance(messages, dict):
                        raise SnipeITValidationError(
                            f"Validation error: {messages}",
                            errors=messages,
                        )
                    else:
                        raise SnipeITError(f"API error: {messages}")

                return data

            except requests.exceptions.ConnectionError as e:
                logger.error(f"Connection error: {e}")
                if attempt == self.retry_count - 1:
                    raise SnipeITConnectionError(
                        f"Failed to connect to Snipe-IT at {self.base_url}"
                    ) from e

            except requests.exceptions.Timeout as e:
                logger.error(f"Request timeout: {e}")
                if attempt == self.retry_count - 1:
                    raise SnipeITConnectionError(
                        f"Request timed out after {self.timeout}s"
                    ) from e

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                raise SnipeITError(f"Request failed: {e}") from e

        raise SnipeITError("Max retries exceeded")

    def test_connection(self) -> bool:
        """Test API connectivity and authentication.

        Returns:
            True if connection successful.

        Raises:
            SnipeITConnectionError: Connection failed.
            SnipeITAuthError: Authentication failed.
        """
        try:
            # Simple request to verify auth
            self._request("GET", "/hardware", params={"limit": 1})
            return True
        except (SnipeITConnectionError, SnipeITAuthError):
            raise
        except SnipeITError:
            return False

    def list_hardware(
        self,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> tuple[list[Asset], int]:
        """List hardware assets with pagination.

        Args:
            limit: Maximum results to return (max 500).
            offset: Starting offset for pagination.
            search: Search query string.
            category_id: Filter by category ID.
            sort: Field to sort by.
            order: Sort order (asc/desc).

        Returns:
            Tuple of (list of Assets, total count).
        """
        params: dict[str, Any] = {
            "limit": min(limit, 500),
            "offset": offset,
            "sort": sort,
            "order": order,
        }

        if search:
            params["search"] = search

        if category_id:
            params["category_id"] = category_id

        data = self._request("GET", "/hardware", params=params)

        assets = [Asset.from_api_response(row) for row in data.get("rows", [])]
        total = data.get("total", len(assets))

        return assets, total

    def get_hardware_by_id(self, asset_id: int) -> Asset:
        """Get single asset by ID.

        Args:
            asset_id: Snipe-IT asset ID.

        Returns:
            Asset instance.

        Raises:
            SnipeITNotFoundError: Asset not found.
        """
        data = self._request("GET", f"/hardware/{asset_id}")
        return Asset.from_api_response(data)

    def get_hardware_by_tag(self, asset_tag: str) -> Optional[Asset]:
        """Get single asset by asset tag.

        Args:
            asset_tag: Asset tag string.

        Returns:
            Asset instance or None if not found.
        """
        try:
            data = self._request("GET", f"/hardware/bytag/{asset_tag}")
            return Asset.from_api_response(data)
        except SnipeITNotFoundError:
            return None

    def create_hardware(self, payload: dict[str, Any]) -> Asset:
        """Create new hardware asset.

        Args:
            payload: Asset data including name, asset_tag, model_id, status_id.

        Returns:
            Created Asset instance.

        Raises:
            SnipeITValidationError: Validation errors.
        """
        data = self._request("POST", "/hardware", json=payload)

        # Snipe-IT returns the created asset in 'payload' field
        asset_data = data.get("payload", data)
        return Asset.from_api_response(asset_data)

    def update_hardware(self, asset_id: int, payload: dict[str, Any]) -> Asset:
        """Update existing hardware asset.

        Args:
            asset_id: Snipe-IT asset ID.
            payload: Fields to update.

        Returns:
            Updated Asset instance.

        Raises:
            SnipeITNotFoundError: Asset not found.
            SnipeITValidationError: Validation errors.
        """
        data = self._request("PATCH", f"/hardware/{asset_id}", json=payload)

        # Get updated asset
        asset_data = data.get("payload", data)
        return Asset.from_api_response(asset_data)

    def search_by_mac(self, mac_address: str) -> Optional[Asset]:
        """Search for asset by MAC address custom field.

        Args:
            mac_address: MAC address to search for.

        Returns:
            Asset instance or None if not found.
        """
        # Normalize MAC format for search
        mac_normalized = mac_address.upper().replace("-", ":")

        # Search using the MAC address
        assets, _ = self.list_hardware(search=mac_normalized, limit=10)

        # Filter to exact MAC match
        for asset in assets:
            if asset.mac_address:
                asset_mac = asset.mac_address.upper().replace("-", ":")
                if asset_mac == mac_normalized:
                    return asset

        return None

    def search_by_ip(self, ip_address: str) -> Optional[Asset]:
        """Search for asset by IP address custom field.

        Args:
            ip_address: IP address to search for.

        Returns:
            Asset instance or None if not found.
        """
        assets, _ = self.list_hardware(search=ip_address, limit=10)

        # Filter to exact IP match
        for asset in assets:
            if asset.ip_address == ip_address:
                return asset

        return None

    def get_network_assets(self, category_id: int = 4) -> list[Asset]:
        """Get all assets in Network category.

        Args:
            category_id: Network category ID (default 4).

        Returns:
            List of network Assets.
        """
        all_assets: list[Asset] = []
        offset = 0
        limit = 100

        while True:
            assets, total = self.list_hardware(
                limit=limit,
                offset=offset,
                category_id=category_id,
            )

            all_assets.extend(assets)

            if len(all_assets) >= total or len(assets) == 0:
                break

            offset += limit

        return all_assets

    def get_asset_counts(self) -> dict[str, int]:
        """Get summary counts for dashboard.

        Returns:
            Dictionary with total, network, and other counts.
        """
        # Get total count
        _, total = self.list_hardware(limit=1)

        # Get network category count
        network_assets = self.get_network_assets()

        return {
            "total": total,
            "network": len(network_assets),
        }
