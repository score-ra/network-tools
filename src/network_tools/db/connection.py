"""Database connection management for ra_inventory."""

from contextlib import contextmanager
from typing import Generator, Optional

import psycopg
from psycopg import Connection
from psycopg_pool import ConnectionPool

from network_tools.config import get_config
from network_tools.logging import get_logger

logger = get_logger("db.connection")

# Global connection pool
_pool: Optional[ConnectionPool] = None


def get_pool() -> ConnectionPool:
    """Get or create the global connection pool.

    Returns:
        ConnectionPool instance.
    """
    global _pool

    if _pool is None:
        config = get_config()
        logger.info(f"Creating connection pool for {config.db_name}@{config.db_host}")

        _pool = ConnectionPool(
            conninfo=config.db_dsn,
            min_size=1,
            max_size=10,
            open=True,
        )

    return _pool


def close_pool() -> None:
    """Close the global connection pool."""
    global _pool

    if _pool is not None:
        logger.info("Closing connection pool")
        _pool.close()
        _pool = None


@contextmanager
def get_connection() -> Generator[Connection, None, None]:
    """Get a database connection from the pool.

    Yields:
        Database connection.

    Example:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM devices")
    """
    pool = get_pool()

    with pool.connection() as conn:
        yield conn


@contextmanager
def get_transaction() -> Generator[Connection, None, None]:
    """Get a database connection with transaction management.

    The transaction is automatically committed on success or rolled back on error.

    Yields:
        Database connection within a transaction.

    Example:
        with get_transaction() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO devices ...")
    """
    with get_connection() as conn:
        try:
            yield conn
            conn.commit()
            logger.debug("Transaction committed")
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction rolled back: {e}")
            raise


def test_connection() -> bool:
    """Test database connectivity.

    Returns:
        True if connection successful, False otherwise.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                return result is not None and result[0] == 1
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
