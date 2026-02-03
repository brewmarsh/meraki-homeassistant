"""
Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, default values, and platform types.
"""

from __future__ import annotations

from typing import Final

# Re-export constants from sub-modules
from .const_api import *  # noqa: F403
from .const_conf import *  # noqa: F403
from .const_device import *  # noqa: F403
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

WEBHOOK_ID_FORMAT: Final = "meraki_ha_{entry_id}"
