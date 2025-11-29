"""Tests for database connection module."""

from unittest.mock import MagicMock, patch

import pytest

from network_tools.config import Config, set_config


class TestDatabaseConnection:
    """Tests for database connection functions."""

    def setup_method(self):
        """Reset config and pool before each test."""
        set_config(None)
        # Reset the global pool
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

    def test_get_pool_creates_pool(self):
        """Test get_pool creates connection pool."""
        # Set up test config with mock DSN
        test_config = Config(
            db_host="testhost",
            db_port=5432,
            db_name="testdb",
            db_user="testuser",
            db_password="testpass",
        )
        set_config(test_config)

        with patch("network_tools.db.connection.ConnectionPool") as mock_pool_class:
            mock_pool = MagicMock()
            mock_pool_class.return_value = mock_pool

            from network_tools.db.connection import get_pool

            result = get_pool()

            mock_pool_class.assert_called_once()
            call_kwargs = mock_pool_class.call_args[1]
            assert "postgresql://testuser:testpass@testhost:5432/testdb" in call_kwargs["conninfo"]
            assert call_kwargs["min_size"] == 1
            assert call_kwargs["max_size"] == 10

    def test_get_pool_returns_singleton(self):
        """Test get_pool returns same instance."""
        test_config = Config(db_password="test")
        set_config(test_config)

        with patch("network_tools.db.connection.ConnectionPool") as mock_pool_class:
            mock_pool = MagicMock()
            mock_pool_class.return_value = mock_pool

            from network_tools.db.connection import get_pool

            pool1 = get_pool()
            pool2 = get_pool()

            assert pool1 is pool2
            # Should only create pool once
            assert mock_pool_class.call_count == 1

    def test_close_pool(self):
        """Test close_pool closes and clears pool."""
        test_config = Config(db_password="test")
        set_config(test_config)

        with patch("network_tools.db.connection.ConnectionPool") as mock_pool_class:
            mock_pool = MagicMock()
            mock_pool_class.return_value = mock_pool

            from network_tools.db.connection import get_pool, close_pool
            import network_tools.db.connection as conn_module

            get_pool()
            assert conn_module._pool is not None

            close_pool()

            mock_pool.close.assert_called_once()
            assert conn_module._pool is None

    def test_close_pool_when_none(self):
        """Test close_pool does nothing when no pool."""
        from network_tools.db.connection import close_pool
        import network_tools.db.connection as conn_module

        assert conn_module._pool is None
        close_pool()  # Should not raise
        assert conn_module._pool is None

    def test_get_connection_context_manager(self):
        """Test get_connection as context manager."""
        test_config = Config(db_password="test")
        set_config(test_config)

        mock_conn = MagicMock()
        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.connection import get_connection

            with get_connection() as conn:
                assert conn is mock_conn

    def test_get_transaction_commits_on_success(self):
        """Test get_transaction commits on success."""
        test_config = Config(db_password="test")
        set_config(test_config)

        mock_conn = MagicMock()
        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.connection import get_transaction

            with get_transaction() as conn:
                pass  # Successful execution

            mock_conn.commit.assert_called_once()
            mock_conn.rollback.assert_not_called()

    def test_get_transaction_rollback_on_error(self):
        """Test get_transaction rolls back on error."""
        test_config = Config(db_password="test")
        set_config(test_config)

        mock_conn = MagicMock()
        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.connection import get_transaction

            with pytest.raises(ValueError):
                with get_transaction() as conn:
                    raise ValueError("Test error")

            mock_conn.rollback.assert_called_once()
            mock_conn.commit.assert_not_called()

    def test_test_connection_success(self):
        """Test test_connection returns True on success."""
        test_config = Config(db_password="test")
        set_config(test_config)

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            from network_tools.db.connection import test_connection

            result = test_connection()

            assert result is True
            mock_cursor.execute.assert_called_with("SELECT 1")

    def test_test_connection_failure(self):
        """Test test_connection returns False on error."""
        test_config = Config(db_password="test")
        set_config(test_config)

        with patch("network_tools.db.connection.ConnectionPool") as mock_pool_class:
            mock_pool_class.side_effect = Exception("Connection failed")

            from network_tools.db.connection import test_connection

            result = test_connection()

            assert result is False
