"""Database queries for ra_inventory CRUD operations."""

from typing import Optional
from uuid import UUID

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row

from network_tools.db.connection import get_connection, get_transaction
from network_tools.db.models import Device, Network, Site
from network_tools.logging import get_audit_logger, get_logger

logger = get_logger("db.queries")
audit = get_audit_logger()


# =============================================================================
# Site Queries
# =============================================================================


def get_site_by_slug(slug: str) -> Optional[Site]:
    """Get site by slug.

    Args:
        slug: Site slug (e.g., 'ra-home-31-nt').

    Returns:
        Site or None if not found.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, name, slug, description, created_at, updated_at "
                "FROM sites WHERE slug = %s",
                (slug,),
            )
            row = cur.fetchone()

            if row:
                return Site(**row)
            return None


def get_site_by_id(site_id: UUID) -> Optional[Site]:
    """Get site by ID."""
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, name, slug, description, created_at, updated_at "
                "FROM sites WHERE id = %s",
                (site_id,),
            )
            row = cur.fetchone()

            if row:
                return Site(**row)
            return None


# =============================================================================
# Network Queries
# =============================================================================


def get_networks_by_site(site_id: UUID) -> list[Network]:
    """Get all networks for a site.

    Args:
        site_id: Site UUID.

    Returns:
        List of networks.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, site_id, name, slug, cidr, network_type, "
                "gateway_ip, vlan_id, ssid, is_primary, created_at, updated_at "
                "FROM networks WHERE site_id = %s ORDER BY is_primary DESC, name",
                (site_id,),
            )
            rows = cur.fetchall()
            return [Network(**row) for row in rows]


def get_network_by_cidr(site_id: UUID, cidr: str) -> Optional[Network]:
    """Get network by CIDR.

    Args:
        site_id: Site UUID.
        cidr: Network CIDR (e.g., '192.168.68.0/22').

    Returns:
        Network or None.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, site_id, name, slug, cidr, network_type, "
                "gateway_ip, vlan_id, ssid, is_primary, created_at, updated_at "
                "FROM networks WHERE site_id = %s AND cidr = %s",
                (site_id, cidr),
            )
            row = cur.fetchone()

            if row:
                return Network(**row)
            return None


# =============================================================================
# Device Queries
# =============================================================================


def get_devices_by_site(site_id: UUID) -> list[Device]:
    """Get all devices for a site.

    Args:
        site_id: Site UUID.

    Returns:
        List of devices.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, site_id, zone_id, network_id, category_id, "
                "name, slug, device_type, manufacturer, model, serial_number, "
                "firmware_version, mac_address, ip_address, hostname, status, "
                "metadata, created_at, updated_at "
                "FROM devices WHERE site_id = %s ORDER BY name",
                (site_id,),
            )
            rows = cur.fetchall()
            return [Device(**row) for row in rows]


def get_device_by_mac(mac_address: str) -> Optional[Device]:
    """Get device by MAC address.

    Args:
        mac_address: MAC address (any format).

    Returns:
        Device or None.
    """
    # Normalize MAC address (remove separators for comparison)
    normalized = mac_address.upper().replace(":", "").replace("-", "")

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Use REPLACE to normalize in SQL for comparison
            cur.execute(
                "SELECT id, site_id, zone_id, network_id, category_id, "
                "name, slug, device_type, manufacturer, model, serial_number, "
                "firmware_version, mac_address, ip_address, hostname, status, "
                "metadata, created_at, updated_at "
                "FROM devices "
                "WHERE UPPER(REPLACE(REPLACE(mac_address, ':', ''), '-', '')) = %s",
                (normalized,),
            )
            row = cur.fetchone()

            if row:
                return Device(**row)
            return None


def get_device_by_ip(ip_address: str, site_id: Optional[UUID] = None) -> Optional[Device]:
    """Get device by IP address.

    Args:
        ip_address: IP address.
        site_id: Optional site filter.

    Returns:
        Device or None.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            if site_id:
                cur.execute(
                    "SELECT id, site_id, zone_id, network_id, category_id, "
                    "name, slug, device_type, manufacturer, model, serial_number, "
                    "firmware_version, mac_address, ip_address, hostname, status, "
                    "metadata, created_at, updated_at "
                    "FROM devices WHERE ip_address = %s AND site_id = %s",
                    (ip_address, site_id),
                )
            else:
                cur.execute(
                    "SELECT id, site_id, zone_id, network_id, category_id, "
                    "name, slug, device_type, manufacturer, model, serial_number, "
                    "firmware_version, mac_address, ip_address, hostname, status, "
                    "metadata, created_at, updated_at "
                    "FROM devices WHERE ip_address = %s",
                    (ip_address,),
                )
            row = cur.fetchone()

            if row:
                return Device(**row)
            return None


def insert_device(device: Device, conn: Optional[Connection] = None) -> UUID:
    """Insert a new device.

    Args:
        device: Device to insert.
        conn: Optional existing connection (for transaction batching).

    Returns:
        New device UUID.
    """
    def _insert(c: Connection) -> UUID:
        with c.cursor() as cur:
            cur.execute(
                """
                INSERT INTO devices (
                    site_id, zone_id, network_id, category_id,
                    name, slug, device_type, manufacturer, model,
                    serial_number, firmware_version, mac_address,
                    ip_address, hostname, status, metadata
                ) VALUES (
                    %(site_id)s, %(zone_id)s, %(network_id)s, %(category_id)s,
                    %(name)s, %(slug)s, %(device_type)s, %(manufacturer)s, %(model)s,
                    %(serial_number)s, %(firmware_version)s, %(mac_address)s,
                    %(ip_address)s, %(hostname)s, %(status)s, %(metadata)s
                ) RETURNING id
                """,
                device.to_insert_dict(),
            )
            result = cur.fetchone()
            device_id = result[0]

            audit.info(
                f"INSERT device: id={device_id}, name={device.name}, "
                f"mac={device.mac_address}, ip={device.ip_address}"
            )
            return device_id

    if conn:
        return _insert(conn)
    else:
        with get_transaction() as c:
            return _insert(c)


def update_device_ip(device_id: UUID, ip_address: str) -> bool:
    """Update device IP address.

    Args:
        device_id: Device UUID.
        ip_address: New IP address.

    Returns:
        True if updated.
    """
    with get_transaction() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE devices SET ip_address = %s, updated_at = NOW() WHERE id = %s",
                (ip_address, device_id),
            )
            updated = cur.rowcount > 0

            if updated:
                audit.info(f"UPDATE device ip: id={device_id}, ip={ip_address}")

            return updated


def update_device_status(device_id: UUID, status: str) -> bool:
    """Update device status.

    Args:
        device_id: Device UUID.
        status: New status (online, offline, unknown, maintenance).

    Returns:
        True if updated.
    """
    with get_transaction() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE devices SET status = %s, updated_at = NOW() WHERE id = %s",
                (status, device_id),
            )
            updated = cur.rowcount > 0

            if updated:
                audit.info(f"UPDATE device status: id={device_id}, status={status}")

            return updated


def batch_insert_devices(devices: list[Device]) -> list[UUID]:
    """Insert multiple devices in a single transaction.

    Args:
        devices: List of devices to insert.

    Returns:
        List of new device UUIDs.
    """
    device_ids = []

    with get_transaction() as conn:
        for device in devices:
            device_id = insert_device(device, conn=conn)
            device_ids.append(device_id)

        audit.info(f"BATCH INSERT: {len(devices)} devices inserted")

    return device_ids
