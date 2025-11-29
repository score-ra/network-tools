"""Tests for logging module."""

import logging

import pytest

from network_tools.logging import get_logger, get_audit_logger, setup_logging


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test get_logger returns a logger instance."""
        logger = get_logger("test")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "network_tools.test"

    def test_get_logger_with_prefix(self):
        """Test get_logger includes app prefix."""
        logger = get_logger("module.submodule")

        assert logger.name == "network_tools.module.submodule"

    def test_get_logger_same_name_returns_same_logger(self):
        """Test get_logger returns same logger for same name."""
        logger1 = get_logger("same")
        logger2 = get_logger("same")

        assert logger1 is logger2


class TestGetAuditLogger:
    """Tests for get_audit_logger function."""

    def test_get_audit_logger_returns_logger(self):
        """Test get_audit_logger returns a logger instance."""
        logger = get_audit_logger()

        assert isinstance(logger, logging.Logger)
        assert logger.name == "network_tools.audit"

    def test_get_audit_logger_returns_same_instance(self):
        """Test get_audit_logger returns same logger."""
        logger1 = get_audit_logger()
        logger2 = get_audit_logger()

        assert logger1 is logger2


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_configures_root(self):
        """Test setup_logging configures root logger."""
        setup_logging(level="DEBUG")

        root_logger = logging.getLogger("network_tools")
        assert root_logger.level == logging.DEBUG

    def test_setup_logging_with_info_level(self):
        """Test setup_logging with INFO level."""
        setup_logging(level="INFO")

        root_logger = logging.getLogger("network_tools")
        assert root_logger.level == logging.INFO

    def test_setup_logging_with_warning_level(self):
        """Test setup_logging with WARNING level."""
        setup_logging(level="WARNING")

        root_logger = logging.getLogger("network_tools")
        assert root_logger.level == logging.WARNING
