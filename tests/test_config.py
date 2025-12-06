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
        # Snipe-IT defaults
        assert config.snipeit_base_url == "http://localhost:8082/api/v1"
        assert config.snipeit_api_key == ""
        assert config.snipeit_timeout == 30
        assert config.snipeit_retry_count == 3
        assert config.snipeit_network_category_id == 4
        assert config.snipeit_default_status_id == 2
        assert config.snipeit_default_model_id == 0
        # Network defaults
        assert config.default_network == "192.168.68.0/22"
        assert config.scan_timeout == 5
        assert config.scan_concurrency == 50

    def test_from_env_defaults(self):
        """Test from_env uses defaults when env vars not set."""
        with patch.dict(os.environ, {}, clear=True):
            config = Config.from_env()

            assert config.app_name == "network-tools"
            assert config.snipeit_base_url == "http://localhost:8082/api/v1"

    def test_from_env_with_snipeit_values(self):
        """Test from_env reads Snipe-IT environment variables."""
        env_vars = {
            "APP_NAME": "test-app",
            "ENV": "production",
            "LOG_LEVEL": "DEBUG",
            "SNIPEIT_BASE_URL": "http://snipeit.example.com/api/v1",
            "SNIPEIT_API_KEY": "test_api_key_123",
            "SNIPEIT_TIMEOUT": "60",
            "SNIPEIT_RETRY_COUNT": "5",
            "SNIPEIT_NETWORK_CATEGORY_ID": "10",
            "SNIPEIT_DEFAULT_STATUS_ID": "3",
            "SNIPEIT_DEFAULT_MODEL_ID": "25",
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
            # Snipe-IT config
            assert config.snipeit_base_url == "http://snipeit.example.com/api/v1"
            assert config.snipeit_api_key == "test_api_key_123"
            assert config.snipeit_timeout == 60
            assert config.snipeit_retry_count == 5
            assert config.snipeit_network_category_id == 10
            assert config.snipeit_default_status_id == 3
            assert config.snipeit_default_model_id == 25
            # Network config
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
