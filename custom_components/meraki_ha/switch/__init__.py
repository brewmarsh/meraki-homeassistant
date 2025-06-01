# custom_components/meraki_ha/switch/__init__.py
"""Switch platform for Meraki to control SSID devices."""

# Forward the async_setup_entry from the new meraki_ssid_device_switch module.
# This makes meraki_ssid_device_switch.py responsible for setting up
# the switch entities for this platform.
from .meraki_ssid_device_switch import async_setup_entry

__all__ = ["async_setup_entry"]
