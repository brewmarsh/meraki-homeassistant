"""Module to handle Meraki device setup."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN
from .coordinator import MerakiCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_devices(hass: HomeAssistant, coordinator: MerakiCoordinator):
    """Set up Meraki devices in Home Assistant's device registry."""
    _LOGGER.debug("Setting up Meraki devices")
    _LOGGER.debug(f"Coordinator Data: {coordinator.data}")  # added log

    device_registry = dr.async_get(hass)

    devices = coordinator.data.get("devices", [])  # Access the devices list
    if not isinstance(devices, list):
        _LOGGER.error("Devices data is not a list. Skipping device setup.")
        return

    _LOGGER.debug(f"Number of devices to process: {len(devices)}")  # added log

    for device in devices:
        _LOGGER.debug(f"Processing device: {device}")  # added log
        if not isinstance(device, dict):
            _LOGGER.error(f"Device data is not a dictionary: {device}. Skipping.")
            continue
        if "serial" not in device:
            _LOGGER.error(f"Device data missing 'serial' key: {device}. Skipping.")
            continue

        device_registry.async_get_or_create(
            config_entry_id=coordinator.config_entry.entry_id,
            identifiers={(DOMAIN, device["serial"])},
            manufacturer="Cisco Meraki",
            model=device.get("model"),
            name=device.get("name"),
            sw_version=device.get("firmware"),
        )
        _LOGGER.debug(f"Device {device['serial']} created/updated")

    _LOGGER.debug("Finished setting up Meraki devices")  # added log
