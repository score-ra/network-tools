"""Logging configuration for network-tools."""

import logging
import sys
from typing import Optional

from network_tools.config import get_config


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """Configure and return the application logger.

    Args:
        level: Log level override. If None, uses config value.

    Returns:
        Configured logger instance.
    """
    config = get_config()
    log_level = level or config.log_level

    # Create logger
    logger = logging.getLogger("network_tools")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Format: timestamp - level - module - message
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "network_tools") -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (will be prefixed with 'network_tools.')

    Returns:
        Logger instance.
    """
    if not name.startswith("network_tools"):
        name = f"network_tools.{name}"
    return logging.getLogger(name)


# Audit logger for tracking database operations
def get_audit_logger() -> logging.Logger:
    """Get the audit logger for database operations.

    Returns:
        Audit logger instance.
    """
    return get_logger("audit")
