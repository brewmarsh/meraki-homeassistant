"""Initializes the Meraki API client package.

This module serves as the entry point for the Meraki API client,
re-exporting key functions and classes from its submodules to provide a
convenient and unified interface for interacting with the Meraki Dashboard API.

The `__all__` list defines the public API of this package, ensuring that
only intended components are exposed when using `from ... import *`.
"""
# /config/custom_components/meraki_ha/meraki_api/__init__.py
from .appliance import get_meraki_device_appliance_uplinks
from .clients import get_meraki_device_clients, update_connected_clients
from .devices import get_meraki_devices
from .exceptions import MerakiApiError
from .wireless import (
    get_meraki_device_wireless_radio_settings,
    get_meraki_network_wireless_rf_profile,
)

__all__ = [
    "get_meraki_devices",
    "get_meraki_device_wireless_radio_settings",
    "get_meraki_network_wireless_rf_profile",
    "get_meraki_device_appliance_uplinks",
    "MerakiApiError",
    "get_meraki_device_clients",  # Ensure this is imported and listed
    "update_connected_clients",
]
