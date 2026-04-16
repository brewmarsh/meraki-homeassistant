"""Device constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

# Device Attributes
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
    "connectivity",
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
    "connectivity",
    "ssids",
    "radio_utilization",
    "reboot",
    "status",
    "physical_sensors",
    "led_control",
    "wireless",
]

_MS_CAPS = [
    "connectivity",
    "switch_ports",
    "poe_usage",
    "power_supply",
    "reboot",
    "status",
    "physical_sensors",
]

_MV_CAPS = [
    "connectivity",
    "camera_stream",
    "storage_status",
    "camera_analytics",
    "reboot",
    "status",
    "physical_sensors",
]

_GX_CAPS = [
    "connectivity",
    "uplinks",
    "performance",
    "vlans",
    "cellular",
    "appliance_ports",
    "reboot",
    "status",
    "physical_sensors",
]

# Strict Hardware Capability Matrix based on Meraki Datasheets
DEVICE_CAPABILITIES: Final[dict[str, list[str]]] = {
    "MT10": ["connectivity", "temperature", "humidity", "battery", "signal_strength"],
    "MT11": ["connectivity", "temperature", "battery", "signal_strength"],
    "MT12": ["connectivity", "water", "battery", "signal_strength"],
    "MT14": [
        "connectivity",
        "pm25",
        "tvoc",
        "temperature",
        "humidity",
        "noise",
        "battery",
        "signal_strength",
    ],
    "MT15": [
        "connectivity",
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
    ],  # Note: MT15 uses AC power/USB, typically no battery sensor
    "MT20": ["connectivity", "door", "battery", "signal_strength"],
    "MT30": ["connectivity", "button_press", "battery", "signal_strength"],
    "MT40": [
        "connectivity",
        "power_monitor",
        "remote_switch",
        "signal_strength",
    ],
    # MX Family
    "MX6": _MX_CAPS,
    "MX7": _MX_CAPS,
    "MX8": _MX_CAPS,
    "MX9": _MX_CAPS,
    "MX1": _MX_CAPS,
    "Z3": _MX_CAPS,
    "Z4": _MX_CAPS,
    # MR Family
    "MR36": _MR_CAPS,
    "MR44": _MR_CAPS,
    "MR56": _MR_CAPS,
    # MS Family
    "MS120": _MS_CAPS,
    "MS225": _MS_CAPS,
    "MS250": _MS_CAPS,
    "GS": _MS_CAPS,
    # MV Family
    "MV12": _MV_CAPS,
    "MV22": _MV_CAPS,
    "MV72": _MV_CAPS,
    # GX Family
    "GX20": _GX_CAPS,
    "GX50": _GX_CAPS,
}

DEFAULT_CAPS: Final = ["connectivity", "reboot", "status", "physical_sensors"]


def get_ssid_identifier(network_id: str, ssid_number: int | str) -> str:
    """Return a unified SSID identifier."""
    return f"{network_id}ssid{ssid_number}"
