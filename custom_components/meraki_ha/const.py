"""Constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "meraki_ha"
MANUFACTURER: Final = "Cisco Meraki"
WEBHOOK_ID_FORMAT: Final = "meraki_ha_webhook_{entry_id}"
DATA_CLIENT: Final = "meraki_client"

# Shared Capability Definitions (The "DRY" Approach)
_MX_CAPS = [
    "uplinks",
    "performance",
    "vlans",
    "cellular",
    "appliance_ports",
    "reboot",
    "status",
]

_MR_CAPS = ["ssids", "client_count", "radio_utilization", "reboot", "status"]
_MS_CAPS = ["switch_ports", "poe_usage", "power_supply", "reboot", "status"]
_MV_CAPS = ["camera_stream", "storage_status", "analytics", "reboot", "status"]
_GX_CAPS = ["uplinks", "performance", "vlans", "cellular", "reboot", "status"]

DEVICE_CAPABILITIES: Final = {
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

DEFAULT_CAPS: Final = ["reboot", "status"]
