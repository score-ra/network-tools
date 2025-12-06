"""Custom exceptions for Snipe-IT API client."""


class SnipeITError(Exception):
    """Base exception for Snipe-IT API errors."""

    pass


class SnipeITConnectionError(SnipeITError):
    """Raised when connection to Snipe-IT fails."""

    pass


class SnipeITAuthError(SnipeITError):
    """Raised when authentication fails (401)."""

    pass


class SnipeITNotFoundError(SnipeITError):
    """Raised when resource is not found (404)."""

    pass


class SnipeITValidationError(SnipeITError):
    """Raised when API returns validation errors."""

    def __init__(self, message: str, errors: dict | None = None):
        super().__init__(message)
        self.errors = errors or {}
