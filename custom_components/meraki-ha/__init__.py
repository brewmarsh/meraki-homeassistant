"""Meraki HA integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, PLATFORMS, DATA_CLIENT, DATA_COORDINATOR
from .meraki_api import get_meraki_devices, MerakiApiError

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""
    _LOGGER.debug("Meraki HA: async_setup_entry in __init__.py called")
    _LOGGER.debug(f"Config Entry: {entry.as_dict()}")

    api_key = entry.options["meraki_api_key"]
    org_id = entry.options["meraki_org_id"]

    async def async_update_data():
        """Fetch data from Meraki API."""
        try:
            return await get_meraki_devices(api_key, org_id)
        except MerakiApiError as err:
            _LOGGER.error("Failed to update Meraki data")
            raise UpdateFailed(f"Error communicating with Meraki API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: {"api_key": api_key, "org_id": org_id},
        DATA_COORDINATOR: coordinator,
    }

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading meraki_ha config entry")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok