"""Device and sensor constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

# Re-export for backward compatibility
from .sensor import (  # noqa: F401
    SENSOR_CLIENT_COUNT,
    SENSOR_DATA_USAGE,
    SENSOR_SIGNAL_STRENGTH,
    SENSOR_SSID_AVAILABILITY,
    SENSOR_SSID_CHANNEL,
)

# Device Attributes (examples, expand as needed)
ATTR_CONNECTED_CLIENTS: Final = "connected_clients"
"""Device attribute for connected clients."""
ATTR_SSIDS: Final = "ssids"
"""Device attribute for SSIDs."""

TAG_HA_DISABLED: Final = "ha-disabled"
"""Tag used to indirectly disable an SSID on an access point."""

ERASE_TAGS_WARNING: Final = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
"""Warning message for the tag erasing feature."""

# Shared Capability Definitions
_MX_CAPS = [
    "uplinks",
    "performance",
    "vlans",
    "cellular",
    "appliance_ports",
    "reboot",
    "status",
    "physical_sensors",
    "led_control",
    "wireless",
]

_MR_CAPS = [
    "ssids",
    "radio_utilization",
    "reboot",
    "status",
    "physical_sensors",
    "led_control",
    "wireless",
]
_MS_CAPS = [
    "switch_ports",
    "poe_usage",
    "power_supply",
    "reboot",
    "status",
    "physical_sensors",
]
_MV_CAPS = [
    "camera_stream",
    "storage_status",
    "camera_analytics",
    "reboot",
    "status",
    "physical_sensors",
]
_GX_CAPS = [
    "uplinks",
    "performance",
    "vlans",
    "cellular",
    "reboot",
    "status",
    "physical_sensors",
]

DEVICE_CAPABILITIES: Final[dict[str, list[str]]] = {
    "MT10": ["temperature", "humidity", "battery", "signal_strength"],
    "MT11": ["temperature", "humidity", "battery", "signal_strength"],
    "MT12": ["temperature", "humidity", "battery", "signal_strength", "water"],
    "MT14": [
        "pm25",
        "tvoc",
        "temperature",
        "humidity",
        "noise",
        "battery",
        "signal_strength",
    ],
    "MT15": [
        "co2",
        "tvoc",
        "pm25",
        "temperature",
        "humidity",
        "noise",
        "signal_strength",
        "mt15_refresh",
        "reboot",
        "status",
        "physical_sensors",
    ],  # No Battery
    "MT20": ["temperature", "humidity", "battery", "signal_strength", "door"],
    "MT30": ["button_press", "battery", "signal_strength"],
    "MT40": ["power_monitor", "remote_switch", "signal_strength"],
    # MX Family
    "MX64": _MX_CAPS,
    "MX65": _MX_CAPS,
    "MX67": _MX_CAPS,
    "MX68": _MX_CAPS,
    "MX75": _MX_CAPS,
    "MX85": _MX_CAPS,
    # MR Family
    "MR36": _MR_CAPS,
    "MR44": _MR_CAPS,
    "MR56": _MR_CAPS,
    # MS Family
    "MS120": _MS_CAPS,
    "MS225": _MS_CAPS,
    "MS250": _MS_CAPS,
    # MV Family
    "MV12": _MV_CAPS,
    "MV22": _MV_CAPS,
    "MV72": _MV_CAPS,
    # GX Family
    "GX20": _GX_CAPS,
    "GX50": _GX_CAPS,
}

DEFAULT_CAPS: Final = ["reboot", "status", "physical_sensors"]


def get_ssid_identifier(network_id: str, ssid_number: int | str) -> str:
    """Return a unified SSID identifier."""
    return f"{network_id}ssid{ssid_number}"
