"""Configuration management for network-tools."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Config:
    """Application configuration."""

    # Application
    app_name: str = "network-tools"
    env: str = "development"
    log_level: str = "INFO"

    # Snipe-IT API
    snipeit_base_url: str = "http://localhost:8082/api/v1"
    snipeit_api_key: str = ""
    snipeit_timeout: int = 30
    snipeit_retry_count: int = 3

    # Snipe-IT default IDs
    snipeit_network_category_id: int = 4
    snipeit_default_status_id: int = 2  # Ready to Deploy
    snipeit_default_model_id: int = 0  # Must be configured

    # Network scanning
    default_network: str = "192.168.68.0/22"
    scan_timeout: int = 5
    scan_concurrency: int = 50

    # OUI database
    oui_database_path: str = "./data/oui.txt"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            env=os.getenv("ENV", cls.env),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            # Snipe-IT API
            snipeit_base_url=os.getenv("SNIPEIT_BASE_URL", cls.snipeit_base_url),
            snipeit_api_key=os.getenv("SNIPEIT_API_KEY", cls.snipeit_api_key),
            snipeit_timeout=int(
                os.getenv("SNIPEIT_TIMEOUT", str(cls.snipeit_timeout))
            ),
            snipeit_retry_count=int(
                os.getenv("SNIPEIT_RETRY_COUNT", str(cls.snipeit_retry_count))
            ),
            # Snipe-IT default IDs
            snipeit_network_category_id=int(
                os.getenv(
                    "SNIPEIT_NETWORK_CATEGORY_ID", str(cls.snipeit_network_category_id)
                )
            ),
            snipeit_default_status_id=int(
                os.getenv(
                    "SNIPEIT_DEFAULT_STATUS_ID", str(cls.snipeit_default_status_id)
                )
            ),
            snipeit_default_model_id=int(
                os.getenv(
                    "SNIPEIT_DEFAULT_MODEL_ID", str(cls.snipeit_default_model_id)
                )
            ),
            # Network scanning
            default_network=os.getenv("DEFAULT_NETWORK", cls.default_network),
            scan_timeout=int(os.getenv("SCAN_TIMEOUT", str(cls.scan_timeout))),
            scan_concurrency=int(
                os.getenv("SCAN_CONCURRENCY", str(cls.scan_concurrency))
            ),
            oui_database_path=os.getenv("OUI_DATABASE_PATH", cls.oui_database_path),
        )

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(**data) if data else cls()


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def set_config(config: Config) -> None:
    """Set the global configuration instance (for testing)."""
    global _config
    _config = config
