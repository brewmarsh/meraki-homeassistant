"""
Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, default values, and platform types.
"""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "meraki_ha"
"""Domain for the component."""

MANUFACTURER: Final = "Cisco Meraki"
"""Manufacturer for all Meraki devices."""

DATA_CLIENT: Final = "client"
"""Key for storing the Meraki API client in Home Assistant's data."""

DATA_COORDINATOR: Final = "coordinator"
"""Key for storing the Meraki data coordinator in Home Assistant's data."""

DATA_COORDINATORS: Final = "coordinators"
"""Key for storing the dictionary of all coordinators."""

DATA_SSID_DEVICES_COORDINATOR: Final = "ssid_devices"
"""Key for the SSID devices coordinator."""

MERAKI_API_CLIENT: Final = "meraki_api_client"
"""Key for storing the MerakiAPIClient instance in hass.data."""

WEBHOOK_ID_FORMAT: Final = "meraki_ha_{entry_id}"

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
    ],
    "MT20": ["temperature", "humidity", "battery", "signal_strength", "door"],
    "MT30": ["button_press", "battery", "signal_strength"],
    "MT40": ["power_monitor", "remote_switch", "signal_strength"],
    "MX64": [
        "uplinks",
        "performance",
        "vlans",
        "cellular",
        "appliance_ports",
        "reboot",
        "status",
    ],
    "MX65": [
        "uplinks",
        "performance",
        "vlans",
        "cellular",
        "appliance_ports",
        "reboot",
        "status",
    ],
    "MX67": [
        "uplinks",
        "performance",
        "vlans",
        "cellular",
        "appliance_ports",
        "reboot",
        "status",
    ],
    "MX68": [
        "uplinks",
        "performance",
        "vlans",
        "cellular",
        "appliance_ports",
        "reboot",
        "status",
    ],
    "MX75": [
        "uplinks",
        "performance",
        "vlans",
        "cellular",
        "appliance_ports",
        "reboot",
        "status",
    ],
    "MX85": [
        "uplinks",
        "performance",
        "vlans",
        "cellular",
        "appliance_ports",
        "reboot",
        "status",
    ],
    "MR36": ["ssids", "client_count", "radio_utilization", "reboot", "status"],
    "MR44": ["ssids", "client_count", "radio_utilization", "reboot", "status"],
    "MR56": ["ssids", "client_count", "radio_utilization", "reboot", "status"],
    "MS120": ["switch_ports", "poe_usage", "power_supply", "reboot", "status"],
    "MS225": ["switch_ports", "poe_usage", "power_supply", "reboot", "status"],
    "MS250": ["switch_ports", "poe_usage", "power_supply", "reboot", "status"],
    "MV12": ["camera_stream", "storage_status", "analytics", "reboot", "status"],
    "MV22": ["camera_stream", "storage_status", "analytics", "reboot", "status"],
    "MV72": ["camera_stream", "storage_status", "analytics", "reboot", "status"],
    "GX20": ["uplinks", "performance", "vlans", "cellular", "reboot", "status"],
    "GX50": ["uplinks", "performance", "vlans", "cellular", "reboot", "status"],
}

DEFAULT_CAPS: Final = ["reboot", "status"]
