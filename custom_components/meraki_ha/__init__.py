"""Meraki Home Assistant integration."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DATA_COORDINATOR, DEFAULT_SCAN_INTERVAL, PLATFORMS
from .coordinator import MerakiCoordinator
from .device_setup import async_setup_devices
from .network_setup import async_setup_networks

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki integration from a config entry."""
    _LOGGER.debug("Setting up Meraki integration")

    scan_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

    coordinator = MerakiCoordinator(hass, scan_interval, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        DATA_COORDINATOR: coordinator,
    }

    # Setup devices and networks
    await async_setup_devices(hass, coordinator)
    await async_setup_networks(hass, coordinator)

    _LOGGER.debug(f"Platforms to be set up: {PLATFORMS}")

    # Use async_forward_entry_setups
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Meraki integration")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
