"""Meraki HA integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS, DATA_CLIENT, DATA_COORDINATOR
from .coordinator import MerakiCoordinator  # Import your coordinator

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""
    _LOGGER.debug(f"Meraki async_setup_entry called")

    api_key = entry.options["meraki_api_key"]
    org_id = entry.options["meraki_org_id"]

    coordinator = MerakiCoordinator(hass, api_key, org_id) #Create the coordinator object.

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: {"api_key": api_key, "org_id": org_id},
        DATA_COORDINATOR: coordinator,
    }

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug(f"Meraki async_forward_entry_setups called")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok