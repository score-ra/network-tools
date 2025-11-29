"""OUI (MAC vendor) lookup module."""

from network_tools.oui.lookup import (
    COMMON_OUIS,
    guess_device_type,
    lookup_manufacturer,
)

__all__ = [
    "COMMON_OUIS",
    "guess_device_type",
    "lookup_manufacturer",
]
