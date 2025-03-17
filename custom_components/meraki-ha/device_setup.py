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

    device_registry = dr.async_get(hass)
    for device in coordinator.data:
        device_registry.async_get_or_create(
            config_entry_id=coordinator.config_entry.entry_id,
            identifiers={(DOMAIN, device["serial"])},
            manufacturer="Cisco Meraki",
            model=device["model"],
            name=device["name"],
            sw_version=device.get("firmware"),
        )
        _LOGGER.debug(f"Device {device['serial']} created/updated")
