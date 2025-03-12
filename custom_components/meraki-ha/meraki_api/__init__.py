# /config/custom_components/meraki_ha/meraki_api/__init__.py
from .appliance import get_meraki_device_appliance_uplinks
from .authentication import validate_meraki_credentials
from .clients import get_clients, update_connected_clients  # Modified Line
from .devices import get_meraki_devices
from .exceptions import MerakiApiError
from .wireless import (
    get_meraki_device_wireless_radio_settings,
    get_meraki_network_wireless_rf_profile,
)

__all__ = [
    "validate_meraki_credentials",
    "get_meraki_devices",
    "get_meraki_device_wireless_radio_settings",
    "get_meraki_network_wireless_rf_profile",
    "get_meraki_device_appliance_uplinks",
    "MerakiApiError",
    "get_clients",  # Modified Line
    "update_connected_clients",  # Modified Line
]
