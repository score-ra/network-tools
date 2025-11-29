"""Configuration management for network-tools."""

import os
from dataclasses import dataclass, field
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

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "inventory"
    db_user: str = "inventory"
    db_password: str = ""

    # Network scanning
    default_network: str = "192.168.68.0/22"
    scan_timeout: int = 5
    scan_concurrency: int = 50

    # OUI database
    oui_database_path: str = "./data/oui.txt"

    @property
    def db_dsn(self) -> str:
        """Get database connection string."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            env=os.getenv("ENV", cls.env),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            db_host=os.getenv("DB_HOST", cls.db_host),
            db_port=int(os.getenv("DB_PORT", str(cls.db_port))),
            db_name=os.getenv("DB_NAME", cls.db_name),
            db_user=os.getenv("DB_USER", cls.db_user),
            db_password=os.getenv("DB_PASSWORD", cls.db_password),
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
