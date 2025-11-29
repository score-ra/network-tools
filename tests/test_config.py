"""Tests for configuration module."""

import os
from unittest.mock import patch

import pytest

from network_tools.config import Config, get_config, set_config


class TestConfig:
    """Tests for Config dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = Config()

        assert config.app_name == "network-tools"
        assert config.env == "development"
        assert config.log_level == "INFO"
        assert config.db_host == "localhost"
        assert config.db_port == 5432
        assert config.db_name == "inventory"
        assert config.db_user == "inventory"
        assert config.db_password == ""
        assert config.default_network == "192.168.68.0/22"
        assert config.scan_timeout == 5
        assert config.scan_concurrency == 50

    def test_db_dsn_property(self):
        """Test database DSN generation."""
        config = Config(
            db_host="testhost",
            db_port=5433,
            db_name="testdb",
            db_user="testuser",
            db_password="testpass",
        )

        expected = "postgresql://testuser:testpass@testhost:5433/testdb"
        assert config.db_dsn == expected

    def test_db_dsn_empty_password(self):
        """Test DSN with empty password."""
        config = Config(db_password="")

        assert "@localhost:5432/inventory" in config.db_dsn

    def test_from_env_defaults(self):
        """Test from_env uses defaults when env vars not set."""
        with patch.dict(os.environ, {}, clear=True):
            config = Config.from_env()

            assert config.app_name == "network-tools"
            assert config.db_host == "localhost"

    def test_from_env_with_values(self):
        """Test from_env reads environment variables."""
        env_vars = {
            "APP_NAME": "test-app",
            "ENV": "production",
            "LOG_LEVEL": "DEBUG",
            "DB_HOST": "db.example.com",
            "DB_PORT": "5433",
            "DB_NAME": "prod_inventory",
            "DB_USER": "prod_user",
            "DB_PASSWORD": "secret123",
            "DEFAULT_NETWORK": "10.0.0.0/8",
            "SCAN_TIMEOUT": "10",
            "SCAN_CONCURRENCY": "100",
            "OUI_DATABASE_PATH": "/opt/oui.txt",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = Config.from_env()

            assert config.app_name == "test-app"
            assert config.env == "production"
            assert config.log_level == "DEBUG"
            assert config.db_host == "db.example.com"
            assert config.db_port == 5433
            assert config.db_name == "prod_inventory"
            assert config.db_user == "prod_user"
            assert config.db_password == "secret123"
            assert config.default_network == "10.0.0.0/8"
            assert config.scan_timeout == 10
            assert config.scan_concurrency == 100
            assert config.oui_database_path == "/opt/oui.txt"


class TestConfigSingleton:
    """Tests for global config instance."""

    def setup_method(self):
        """Reset global config before each test."""
        set_config(None)

    def teardown_method(self):
        """Reset global config after each test."""
        set_config(None)

    def test_get_config_creates_instance(self):
        """Test get_config creates config on first call."""
        config = get_config()

        assert config is not None
        assert isinstance(config, Config)

    def test_get_config_returns_same_instance(self):
        """Test get_config returns singleton."""
        config1 = get_config()
        config2 = get_config()

        assert config1 is config2

    def test_set_config_overrides(self):
        """Test set_config allows override."""
        custom = Config(app_name="custom-app")
        set_config(custom)

        result = get_config()

        assert result.app_name == "custom-app"
        assert result is custom
