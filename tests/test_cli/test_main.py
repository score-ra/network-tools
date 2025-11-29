"""Tests for main CLI commands."""

import re
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from network_tools.cli.main import cli
from network_tools.config import set_config


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_pattern.sub('', text)


class TestCli:
    """Tests for CLI group."""

    def setup_method(self):
        """Reset config before each test."""
        set_config(None)

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)

    def test_cli_help(self):
        """Test CLI shows help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Network Tools" in result.output
        assert "discover" in result.output
        assert "status" in result.output

    def test_cli_version(self):
        """Test CLI shows version."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "network-tools" in result.output

    def test_verbose_flag(self):
        """Test verbose flag sets context object."""
        runner = CliRunner()
        # Test that verbose flag is accepted
        result = runner.invoke(cli, ["-v", "--help"])
        assert result.exit_code == 0


class TestDiscoverCommand:
    """Tests for discover command."""

    def setup_method(self):
        """Reset config before each test."""
        set_config(None)

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)

    def test_discover_requires_network(self):
        """Test discover requires --network option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["discover"])

        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()

    def test_discover_with_network(self):
        """Test discover with network option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["discover", "--network", "192.168.1.0/24"])
        output = strip_ansi(result.output)

        assert result.exit_code == 0
        assert "Network Discovery" in output
        assert "192.168.1.0/24" in output

    def test_discover_with_site(self):
        """Test discover with site option."""
        runner = CliRunner()
        result = runner.invoke(
            cli, ["discover", "-n", "10.0.0.0/8", "--site", "test-site"]
        )

        assert result.exit_code == 0
        assert "test-site" in result.output

    def test_discover_with_yes_flag(self):
        """Test discover with auto-confirm flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["discover", "-n", "192.168.1.0/24", "-y"])
        output = strip_ansi(result.output)

        assert result.exit_code == 0
        assert "Auto-confirm: True" in output

    def test_discover_shows_not_implemented(self):
        """Test discover shows not implemented message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["discover", "-n", "192.168.1.0/24"])

        assert result.exit_code == 0
        assert "not yet implemented" in result.output.lower()


class TestStatusCommand:
    """Tests for status command."""

    def setup_method(self):
        """Reset config before each test."""
        set_config(None)

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)
        # Ensure pool is closed
        try:
            from network_tools.db.connection import close_pool
            close_pool()
        except Exception:
            pass

    def test_status_success(self):
        """Test status command with successful connection."""
        runner = CliRunner()

        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [(5,), (2,), (10,)]  # devices, sites, networks
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_pool = MagicMock()
        mock_pool.connection.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_pool.connection.return_value.__exit__ = MagicMock(return_value=False)

        with patch("network_tools.db.connection.ConnectionPool", return_value=mock_pool):
            result = runner.invoke(cli, ["status"])

        assert result.exit_code == 0
        assert "Database Status" in result.output
        assert "OK" in result.output

    def test_status_connection_failure(self):
        """Test status command with connection failure."""
        runner = CliRunner()

        with patch(
            "network_tools.db.connection.ConnectionPool",
            side_effect=Exception("Connection refused"),
        ):
            result = runner.invoke(cli, ["status"])

        assert result.exit_code == 0  # Command completes but shows error
        assert "FAIL" in result.output
        assert "Connection refused" in result.output or "failed" in result.output.lower()

    def test_status_help(self):
        """Test status help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["status", "--help"])

        assert result.exit_code == 0
        assert "database connection status" in result.output.lower()
