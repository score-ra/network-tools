"""Tests for main CLI commands."""

import re
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from network_tools.cli.main import cli
from network_tools.config import Config, set_config


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_pattern.sub("", text)


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
        assert "search" in result.output

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

    def test_discover_no_api_key(self):
        """Test discover shows error when API key not configured."""
        # Set config with empty API key
        set_config(Config(snipeit_api_key=""))

        runner = CliRunner()
        result = runner.invoke(cli, ["discover", "--network", "192.168.1.0/24"])
        output = strip_ansi(result.output)

        assert "SNIPEIT_API_KEY not configured" in output

    def test_discover_with_network(self):
        """Test discover with network option shows header."""
        set_config(Config(snipeit_api_key="test_key"))

        runner = CliRunner()

        # Mock the SnipeITClient at the snipeit module level
        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client.test_connection.return_value = True
            mock_client.get_network_assets.return_value = []
            mock_client_class.return_value = mock_client

            with patch("network_tools.scanner.scan_network") as mock_scan:
                mock_scan.return_value = []

                result = runner.invoke(cli, ["discover", "--network", "192.168.1.0/24"])
                output = strip_ansi(result.output)

        assert "Network Discovery" in output
        assert "192.168.1.0/24" in output

    def test_discover_with_yes_flag(self):
        """Test discover with auto-confirm flag."""
        set_config(Config(snipeit_api_key="test_key"))

        runner = CliRunner()

        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client.test_connection.return_value = True
            mock_client.get_network_assets.return_value = []
            mock_client_class.return_value = mock_client

            with patch("network_tools.scanner.scan_network") as mock_scan:
                mock_scan.return_value = []

                result = runner.invoke(
                    cli, ["discover", "-n", "192.168.1.0/24", "-y"]
                )
                output = strip_ansi(result.output)

        assert "Auto-confirm: True" in output


class TestStatusCommand:
    """Tests for status command."""

    def setup_method(self):
        """Reset config before each test."""
        set_config(None)

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)

    def test_status_no_api_key(self):
        """Test status shows error when API key not configured."""
        set_config(Config(snipeit_api_key=""))

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        output = strip_ansi(result.output)

        assert "SNIPEIT_API_KEY not configured" in output

    def test_status_success(self):
        """Test status command with successful connection."""
        set_config(
            Config(
                snipeit_api_key="test_key",
                snipeit_base_url="http://localhost:8082/api/v1",
            )
        )

        runner = CliRunner()

        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client.test_connection.return_value = True
            mock_client.get_asset_counts.return_value = {"total": 50, "network": 20}
            mock_client_class.return_value = mock_client

            result = runner.invoke(cli, ["status"])
            output = strip_ansi(result.output)

        assert "Snipe-IT Status" in output
        assert "OK" in output
        assert "50" in output or "Total" in output

    def test_status_auth_failure(self):
        """Test status command with auth failure."""
        set_config(Config(snipeit_api_key="bad_key"))

        runner = CliRunner()

        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            from network_tools.snipeit.exceptions import SnipeITAuthError

            mock_client = MagicMock()
            mock_client.test_connection.side_effect = SnipeITAuthError("Auth failed")
            mock_client_class.return_value = mock_client

            result = runner.invoke(cli, ["status"])
            output = strip_ansi(result.output)

        assert "FAIL" in output
        assert "Authentication" in output or "auth" in output.lower()

    def test_status_connection_failure(self):
        """Test status command with connection failure."""
        set_config(Config(snipeit_api_key="test_key"))

        runner = CliRunner()

        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            from network_tools.snipeit.exceptions import SnipeITConnectionError

            mock_client = MagicMock()
            mock_client.test_connection.side_effect = SnipeITConnectionError(
                "Connection refused"
            )
            mock_client_class.return_value = mock_client

            result = runner.invoke(cli, ["status"])
            output = strip_ansi(result.output)

        assert "FAIL" in output
        assert "Connection" in output

    def test_status_help(self):
        """Test status help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["status", "--help"])

        assert result.exit_code == 0
        assert "Snipe-IT" in result.output


class TestSearchCommand:
    """Tests for search command."""

    def setup_method(self):
        """Reset config before each test."""
        set_config(None)

    def teardown_method(self):
        """Clean up after each test."""
        set_config(None)

    def test_search_requires_mac_or_ip(self):
        """Test search requires --mac or --ip option."""
        set_config(Config(snipeit_api_key="test_key"))

        runner = CliRunner()
        result = runner.invoke(cli, ["search"])
        output = strip_ansi(result.output)

        assert "Specify --mac or --ip" in output

    def test_search_by_mac_found(self):
        """Test search by MAC finds asset."""
        set_config(Config(snipeit_api_key="test_key"))

        runner = CliRunner()

        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            from network_tools.snipeit.models import Asset

            mock_asset = Asset(
                id=1,
                name="Test Device",
                asset_tag="NET-DDEEFF",
                mac_address="AA:BB:CC:DD:EE:FF",
                ip_address="192.168.1.100",
                category_name="Network",
                status_name="Ready",
            )

            mock_client = MagicMock()
            mock_client.search_by_mac.return_value = mock_asset
            mock_client_class.return_value = mock_client

            result = runner.invoke(cli, ["search", "--mac", "AA:BB:CC:DD:EE:FF"])
            output = strip_ansi(result.output)

        assert "Found asset" in output
        assert "Test Device" in output
        assert "NET-DDEEFF" in output

    def test_search_by_ip_not_found(self):
        """Test search by IP shows not found."""
        set_config(Config(snipeit_api_key="test_key"))

        runner = CliRunner()

        with patch("network_tools.snipeit.SnipeITClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client.search_by_ip.return_value = None
            mock_client_class.return_value = mock_client

            result = runner.invoke(cli, ["search", "--ip", "192.168.1.100"])
            output = strip_ansi(result.output)

        assert "No asset found" in output

    def test_search_help(self):
        """Test search help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["search", "--help"])

        assert result.exit_code == 0
        assert "--mac" in result.output
        assert "--ip" in result.output
