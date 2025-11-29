"""OUI (Organizationally Unique Identifier) lookup for MAC addresses."""

import re
from pathlib import Path
from typing import Optional

from network_tools.config import get_config
from network_tools.logging import get_logger

logger = get_logger("oui.lookup")

# Common manufacturers for quick lookup (most common first)
COMMON_OUIS: dict[str, str] = {
    # Apple
    "00:1C:B3": "Apple",
    "00:23:12": "Apple",
    "00:25:BC": "Apple",
    "28:CF:E9": "Apple",
    "3C:06:30": "Apple",
    "48:D7:05": "Apple",
    "5C:F7:E6": "Apple",
    "70:DE:E2": "Apple",
    "78:7B:8A": "Apple",
    "7C:D1:C3": "Apple",
    "84:FC:FE": "Apple",
    "88:66:A5": "Apple",
    "90:8D:6C": "Apple",
    "A4:D1:8C": "Apple",
    "AC:BC:32": "Apple",
    "B8:E8:56": "Apple",
    "C8:69:CD": "Apple",
    "D0:81:7A": "Apple",
    "DC:A9:04": "Apple",
    "E0:B9:BA": "Apple",
    "F0:18:98": "Apple",
    "F4:5C:89": "Apple",
    # Google/Nest
    "18:D6:C7": "Google",
    "1C:F2:9A": "Google",
    "54:60:09": "Google",
    "94:EB:2C": "Google",
    "F4:F5:D8": "Google",
    "F4:F5:E8": "Google",
    # Amazon
    "00:FC:8B": "Amazon",
    "0C:47:C9": "Amazon",
    "18:74:2E": "Amazon",
    "34:D2:70": "Amazon",
    "40:B4:CD": "Amazon",
    "44:65:0D": "Amazon",
    "50:DC:E7": "Amazon",
    "68:37:E9": "Amazon",
    "74:C2:46": "Amazon",
    "84:D6:D0": "Amazon",
    "A4:08:EA": "Amazon",
    "B0:FC:36": "Amazon",
    "FC:65:DE": "Amazon",
    # Samsung
    "00:07:AB": "Samsung",
    "00:12:47": "Samsung",
    "00:15:B9": "Samsung",
    "00:16:32": "Samsung",
    "00:17:C9": "Samsung",
    "00:18:AF": "Samsung",
    "00:1A:8A": "Samsung",
    "00:1D:25": "Samsung",
    "00:1E:7D": "Samsung",
    "00:21:19": "Samsung",
    "00:21:D1": "Samsung",
    "00:24:54": "Samsung",
    "00:24:91": "Samsung",
    "00:26:37": "Samsung",
    # Intel
    "00:02:B3": "Intel",
    "00:03:47": "Intel",
    "00:04:23": "Intel",
    "00:07:E9": "Intel",
    "00:0C:F1": "Intel",
    "00:0E:0C": "Intel",
    "00:0E:35": "Intel",
    "00:11:11": "Intel",
    "00:12:F0": "Intel",
    "00:13:02": "Intel",
    "00:13:20": "Intel",
    "00:13:CE": "Intel",
    "00:13:E8": "Intel",
    "00:15:00": "Intel",
    "00:15:17": "Intel",
    # Microsoft/Xbox
    "28:18:78": "Microsoft",
    "60:45:BD": "Microsoft",
    "7C:1E:52": "Microsoft",
    "98:5F:D3": "Microsoft",
    "B4:0E:DE": "Microsoft",
    # Dell
    "00:06:5B": "Dell",
    "00:08:74": "Dell",
    "00:0B:DB": "Dell",
    "00:0D:56": "Dell",
    "00:0F:1F": "Dell",
    "00:11:43": "Dell",
    "00:12:3F": "Dell",
    "00:13:72": "Dell",
    "00:14:22": "Dell",
    "00:15:C5": "Dell",
    "00:18:8B": "Dell",
    "00:19:B9": "Dell",
    "00:1A:A0": "Dell",
    "00:1C:23": "Dell",
    "00:1D:09": "Dell",
    "00:1E:4F": "Dell",
    "00:1E:C9": "Dell",
    "00:21:70": "Dell",
    "00:21:9B": "Dell",
    "00:22:19": "Dell",
    "00:24:E8": "Dell",
    "00:25:64": "Dell",
    "00:26:B9": "Dell",
    # Raspberry Pi
    "B8:27:EB": "Raspberry Pi Foundation",
    "DC:A6:32": "Raspberry Pi Trading",
    "E4:5F:01": "Raspberry Pi Trading",
    # TP-Link
    "00:31:92": "TP-Link",
    "14:CC:20": "TP-Link",
    "14:CF:92": "TP-Link",
    "18:A6:F7": "TP-Link",
    "1C:3B:F3": "TP-Link",
    "30:B5:C2": "TP-Link",
    "50:C7:BF": "TP-Link",
    "54:C8:0F": "TP-Link",
    "60:E3:27": "TP-Link",
    "64:66:B3": "TP-Link",
    "64:70:02": "TP-Link",
    "70:4F:57": "TP-Link",
    "78:8C:B5": "TP-Link",
    "98:DA:C4": "TP-Link",
    "AC:84:C6": "TP-Link",
    "B0:4E:26": "TP-Link",
    "C0:4A:00": "TP-Link",
    "C4:E9:84": "TP-Link",
    "D8:07:B6": "TP-Link",
    "EC:08:6B": "TP-Link",
    "F4:EC:38": "TP-Link",
    # Netgear
    "00:09:5B": "Netgear",
    "00:0F:B5": "Netgear",
    "00:14:6C": "Netgear",
    "00:18:4D": "Netgear",
    "00:1B:2F": "Netgear",
    "00:1E:2A": "Netgear",
    "00:1F:33": "Netgear",
    "00:22:3F": "Netgear",
    "00:24:B2": "Netgear",
    "00:26:F2": "Netgear",
    "20:4E:7F": "Netgear",
    "2C:B0:5D": "Netgear",
    "30:46:9A": "Netgear",
    "44:94:FC": "Netgear",
    "6C:B0:CE": "Netgear",
    "84:1B:5E": "Netgear",
    "9C:3D:CF": "Netgear",
    "A4:2B:8C": "Netgear",
    "C0:3F:0E": "Netgear",
    "C4:04:15": "Netgear",
    "E0:91:F5": "Netgear",
    "E4:F4:C6": "Netgear",
    # Cisco/Linksys
    "00:00:0C": "Cisco",
    "00:01:42": "Cisco",
    "00:01:43": "Cisco",
    "00:01:63": "Cisco",
    "00:01:64": "Cisco",
    "00:01:96": "Cisco",
    "00:01:97": "Cisco",
    "00:01:C7": "Cisco",
    "00:01:C9": "Cisco",
    "00:02:16": "Cisco",
    "00:02:17": "Cisco",
    "00:02:3D": "Cisco",
    "00:02:4A": "Cisco",
    "00:02:4B": "Cisco",
    "00:02:7D": "Cisco",
    "00:02:7E": "Cisco",
    "00:02:B9": "Cisco",
    "00:02:BA": "Cisco",
    "00:02:FC": "Cisco",
    "00:02:FD": "Cisco",
    # Asus
    "00:0C:6E": "ASUSTek",
    "00:0E:A6": "ASUSTek",
    "00:11:2F": "ASUSTek",
    "00:11:D8": "ASUSTek",
    "00:13:D4": "ASUSTek",
    "00:15:F2": "ASUSTek",
    "00:17:31": "ASUSTek",
    "00:18:F3": "ASUSTek",
    "00:1A:92": "ASUSTek",
    "00:1B:FC": "ASUSTek",
    "00:1D:60": "ASUSTek",
    "00:1E:8C": "ASUSTek",
    "00:1F:C6": "ASUSTek",
    "00:22:15": "ASUSTek",
    "00:23:54": "ASUSTek",
    "00:24:8C": "ASUSTek",
    "00:25:22": "ASUSTek",
    "00:26:18": "ASUSTek",
    "04:92:26": "ASUSTek",
    "08:60:6E": "ASUSTek",
    "10:BF:48": "ASUSTek",
    "14:DA:E9": "ASUSTek",
    "1C:87:2C": "ASUSTek",
    "20:CF:30": "ASUSTek",
    "2C:4D:54": "ASUSTek",
    "2C:56:DC": "ASUSTek",
    "30:85:A9": "ASUSTek",
    "38:D5:47": "ASUSTek",
    # Sonos
    "00:0E:58": "Sonos",
    "5C:AA:FD": "Sonos",
    "78:28:CA": "Sonos",
    "94:9F:3E": "Sonos",
    "B8:E9:37": "Sonos",
    # Roku
    "00:0D:4B": "Roku",
    "08:05:81": "Roku",
    "10:59:32": "Roku",
    "B0:A7:37": "Roku",
    "B8:3E:59": "Roku",
    "C8:3A:6B": "Roku",
    "D0:4D:2C": "Roku",
    "D8:31:34": "Roku",
    # Espressif (ESP32/ESP8266)
    "24:0A:C4": "Espressif",
    "24:6F:28": "Espressif",
    "30:AE:A4": "Espressif",
    "3C:71:BF": "Espressif",
    "5C:CF:7F": "Espressif",
    "84:0D:8E": "Espressif",
    "84:CC:A8": "Espressif",
    "A4:CF:12": "Espressif",
    "AC:67:B2": "Espressif",
    "B4:E6:2D": "Espressif",
    "BC:DD:C2": "Espressif",
    "C4:4F:33": "Espressif",
    "CC:50:E3": "Espressif",
    "DC:4F:22": "Espressif",
    "EC:FA:BC": "Espressif",
    # HP
    "00:01:E6": "HP",
    "00:01:E7": "HP",
    "00:02:A5": "HP",
    "00:04:EA": "HP",
    "00:08:02": "HP",
    "00:08:83": "HP",
    "00:0A:57": "HP",
    "00:0B:CD": "HP",
    "00:0D:9D": "HP",
    "00:0E:7F": "HP",
    "00:0F:20": "HP",
    "00:0F:61": "HP",
    "00:10:83": "HP",
    "00:11:0A": "HP",
    "00:11:85": "HP",
    "00:12:79": "HP",
    "00:13:21": "HP",
    "00:14:38": "HP",
    "00:14:C2": "HP",
    "00:15:60": "HP",
    "00:16:35": "HP",
    "00:17:08": "HP",
    "00:17:A4": "HP",
    "00:18:71": "HP",
    "00:18:FE": "HP",
    "00:19:BB": "HP",
    "00:1A:4B": "HP",
    "00:1B:78": "HP",
    "00:1C:C4": "HP",
    "00:1E:0B": "HP",
    "00:1F:29": "HP",
    "00:21:5A": "HP",
    "00:22:64": "HP",
    "00:23:7D": "HP",
    "00:24:81": "HP",
    "00:25:B3": "HP",
    "00:26:55": "HP",
    # Lenovo
    "00:09:2D": "Lenovo",
    "00:0B:2E": "Lenovo",
    "00:12:FE": "Lenovo",
    "00:16:D3": "Lenovo",
    "00:19:D1": "Lenovo",
    "00:1C:14": "Lenovo",
    "00:1D:72": "Lenovo",
    "00:1E:4C": "Lenovo",
    "00:1F:16": "Lenovo",
    "00:20:6B": "Lenovo",
    "00:21:86": "Lenovo",
    "00:22:4D": "Lenovo",
    "00:23:15": "Lenovo",
    "00:24:7E": "Lenovo",
    "00:25:4B": "Lenovo",
    "00:26:2D": "Lenovo",
    # Realtek (common in network cards)
    "00:E0:4C": "Realtek",
    "52:54:00": "Realtek",
    # VMware
    "00:0C:29": "VMware",
    "00:50:56": "VMware",
    # Hyper-V
    "00:15:5D": "Microsoft Hyper-V",
    # Ring
    "34:3E:A4": "Ring",
    "48:A4:93": "Ring",
    "5C:47:5E": "Ring",
    # Wyze
    "2C:AA:8E": "Wyze",
    # LG
    "00:1C:62": "LG Electronics",
    "00:1E:75": "LG Electronics",
    "00:1F:6B": "LG Electronics",
    "00:1F:E3": "LG Electronics",
    "00:21:FB": "LG Electronics",
    "00:22:A9": "LG Electronics",
    "00:24:83": "LG Electronics",
    "00:25:E5": "LG Electronics",
    "00:26:E2": "LG Electronics",
    "10:68:3F": "LG Electronics",
    "20:21:A5": "LG Electronics",
    "2C:54:CF": "LG Electronics",
    "34:4D:F7": "LG Electronics",
}

# Global cache for OUI database
_oui_db: Optional[dict[str, str]] = None


def _load_oui_database() -> dict[str, str]:
    """Load OUI database from file.

    Returns:
        Dictionary mapping OUI prefix to manufacturer name.
    """
    global _oui_db

    if _oui_db is not None:
        return _oui_db

    # Start with common OUIs
    _oui_db = COMMON_OUIS.copy()

    config = get_config()
    oui_path = Path(config.oui_database_path)

    if not oui_path.exists():
        logger.warning(f"OUI database not found at {oui_path}, using built-in list")
        return _oui_db

    try:
        # Parse IEEE OUI file format
        # Format: "AA-BB-CC   (hex)    Company Name"
        pattern = re.compile(r"^([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})\s+\(hex\)\s+(.+)$")

        with open(oui_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = pattern.match(line.strip())
                if match:
                    oui = match.group(1).replace("-", ":")
                    manufacturer = match.group(2).strip()
                    _oui_db[oui] = manufacturer

        logger.info(f"Loaded {len(_oui_db)} OUI entries from {oui_path}")

    except Exception as e:
        logger.error(f"Failed to load OUI database: {e}")

    return _oui_db


def lookup_manufacturer(mac_address: str) -> Optional[str]:
    """Look up manufacturer from MAC address.

    Args:
        mac_address: MAC address in any format.

    Returns:
        Manufacturer name or None if not found.
    """
    # Normalize MAC address
    cleaned = mac_address.upper().replace(":", "").replace("-", "").replace(".", "")
    if len(cleaned) < 6:
        return None

    # Get OUI prefix (first 3 bytes)
    oui = f"{cleaned[0:2]}:{cleaned[2:4]}:{cleaned[4:6]}"

    db = _load_oui_database()
    return db.get(oui)


def guess_device_type(manufacturer: Optional[str], hostname: Optional[str] = None) -> str:
    """Guess device type from manufacturer and hostname.

    Args:
        manufacturer: Manufacturer name.
        hostname: Optional hostname.

    Returns:
        Guessed device type.
    """
    if not manufacturer and not hostname:
        return "unknown"

    manufacturer_lower = (manufacturer or "").lower()
    hostname_lower = (hostname or "").lower()

    # Check hostname patterns first
    if hostname_lower:
        if any(x in hostname_lower for x in ["iphone", "ipad", "macbook", "imac"]):
            return "mobile" if "iphone" in hostname_lower or "ipad" in hostname_lower else "computer"
        if any(x in hostname_lower for x in ["android", "galaxy", "pixel"]):
            return "mobile"
        if any(x in hostname_lower for x in ["tv", "roku", "fire", "chromecast"]):
            return "media_player"
        if any(x in hostname_lower for x in ["echo", "alexa", "google-home", "homepod"]):
            return "speaker"
        if any(x in hostname_lower for x in ["printer", "officejet", "laserjet"]):
            return "printer"
        if any(x in hostname_lower for x in ["router", "gateway", "ap-", "wap"]):
            return "router"
        if any(x in hostname_lower for x in ["switch", "hub"]):
            return "switch"
        if any(x in hostname_lower for x in ["cam", "camera", "ring", "nest"]):
            return "camera"

    # Check manufacturer
    if manufacturer_lower:
        if "apple" in manufacturer_lower:
            return "computer"  # Could be mobile, but safer default
        if any(x in manufacturer_lower for x in ["samsung", "lg electronics"]):
            return "media_player"  # Often TVs
        if any(x in manufacturer_lower for x in ["amazon", "ring"]):
            return "iot"
        if any(x in manufacturer_lower for x in ["google", "nest"]):
            return "iot"
        if any(x in manufacturer_lower for x in ["sonos", "roku"]):
            return "media_player"
        if any(x in manufacturer_lower for x in ["espressif"]):
            return "iot"
        if any(x in manufacturer_lower for x in ["raspberry"]):
            return "computer"
        if any(x in manufacturer_lower for x in ["tp-link", "netgear", "cisco", "asus", "linksys"]):
            return "router"
        if any(x in manufacturer_lower for x in ["hp", "brother", "canon", "epson"]):
            return "printer"
        if any(x in manufacturer_lower for x in ["dell", "lenovo", "intel", "microsoft"]):
            return "computer"
        if "vmware" in manufacturer_lower or "hyper-v" in manufacturer_lower:
            return "virtual_machine"

    return "unknown"
