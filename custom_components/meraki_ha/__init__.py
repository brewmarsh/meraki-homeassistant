"""The meraki_ha integration."""

import logging
import aiohttp
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_MERAKI_ORG_ID,
    CONF_MERAKI_API_KEY,
    DEFAULT_SCAN_INTERVAL,
)
from .coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.DEVICE_TRACKER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""
    _LOGGER.debug("Starting async_setup_entry")
    api_key = entry.options[CONF_MERAKI_API_KEY]
    org_id = entry.options[CONF_MERAKI_ORG_ID]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    session = aiohttp.ClientSession()

    coordinator = MerakiDataUpdateCoordinator(
        hass, session, api_key, org_id, timedelta(seconds=scan_interval)
    )
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug("Completed async_setup_entry")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
