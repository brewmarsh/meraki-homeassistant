"""
Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, default values, and platform types.
"""

from __future__ import annotations

from typing import Final

# Re-export constants from sub-modules
from .const_conf import *  # noqa: F403
from .const_platform import *  # noqa: F403

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

# Sensor types (examples, expand as needed)
SENSOR_CLIENT_COUNT: Final = "client_count"
"""Sensor type for client count."""
SENSOR_SIGNAL_STRENGTH: Final = "signal_strength"
"""Sensor type for signal strength."""
SENSOR_DATA_USAGE: Final = "data_usage"
"""Sensor type for data usage."""
SENSOR_SSID_AVAILABILITY: Final = "ssid_availability"
"""Sensor type for SSID availability."""
SENSOR_SSID_CHANNEL: Final = "ssid_channel"
"""Sensor type for SSID channel."""

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

WEBHOOK_ID_FORMAT: Final = "meraki_ha_{entry_id}"

MERAKI_CONTENT_FILTERING_CATEGORIES: Final[list[dict[str, str]]] = [
    {
        "id": "meraki:contentFiltering/category/1",
        "name": "Adult and Pornography",
        "description": "Sites featuring sexual content, nudity, or pornography.",
    },
    {
        "id": "meraki:contentFiltering/category/2",
        "name": "Illegal",
        "description": "Sites promoting illegal activities.",
    },
    {
        "id": "meraki:contentFiltering/category/3",
        "name": "Gambling",
        "description": "Online gambling sites.",
    },
    {
        "id": "meraki:contentFiltering/category/4",
        "name": "Hate and Racism",
        "description": "Sites promoting hatred or discrimination.",
    },
    {
        "id": "meraki:contentFiltering/category/5",
        "name": "Weapons",
        "description": "Sites related to the sale or promotion of weapons.",
    },
    {
        "id": "meraki:contentFiltering/category/6",
        "name": "Violence",
        "description": "Sites with graphic or gratuitous violence.",
    },
    {
        "id": "meraki:contentFiltering/category/7",
        "name": "Peer-to-peer",
        "description": "Peer-to-peer file sharing sites and applications.",
    },
    {
        "id": "meraki:contentFiltering/category/8",
        "name": "Malware sites",
        "description": "Sites known to host or distribute malware.",
    },
    {
        "id": "meraki:contentFiltering/category/9",
        "name": "Phishing and other frauds",
        "description": "Sites engaged in phishing, scams, or other frauds.",
    },
    {
        "id": "meraki:contentFiltering/category/10",
        "name": "Key loggers and monitoring",
        "description": "Sites for keyloggers, spyware, and monitoring tools.",
    },
    {
        "id": "meraki:contentFiltering/category/11",
        "name": "Botnets",
        "description": "Sites associated with botnet command and control servers.",
    },
    {
        "id": "meraki:contentFiltering/category/12",
        "name": "Spam URLs",
        "description": "URLs frequently found in unsolicited email (spam).",
    },
    {
        "id": "meraki:contentFiltering/category/13",
        "name": "Auctions",
        "description": "Online auction sites.",
    },
    {
        "id": "meraki:contentFiltering/category/14",
        "name": "Games",
        "description": "Online gaming sites.",
    },
    {
        "id": "meraki:contentFiltering/category/15",
        "name": "Social Networking",
        "description": "Social networking sites and applications.",
    },
    {
        "id": "meraki:contentFiltering/category/16",
        "name": "Web-based email",
        "description": "Web-based email services.",
    },
    {
        "id": "meraki:contentFiltering/category/17",
        "name": "Internet communications",
        "description": "Chat, instant messaging, and other communication platforms.",
    },
    {
        "id": "meraki:contentFiltering/category/18",
        "name": "Shareware and freeware",
        "description": "Sites for downloading shareware and freeware.",
    },
    {
        "id": "meraki:contentFiltering/category/19",
        "name": "Web advertisements",
        "description": "Sites primarily serving advertisements.",
    },
    {
        "id": "meraki:contentFiltering/category/20",
        "name": "Nudity",
        "description": "Sites with non-pornographic nudity.",
    },
]
