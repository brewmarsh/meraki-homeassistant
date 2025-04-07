"""The meraki_ha integration."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_MERAKI_ORG_ID,
    CONF_MERAKI_API_KEY,
    DEFAULT_SCAN_INTERVAL,
    DATA_COORDINATOR,
)
from .coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""
    _LOGGER.debug("Starting async_setup_entry")
    api_key = entry.data[CONF_MERAKI_API_KEY]
    org_id = entry.data[CONF_MERAKI_ORG_ID]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    device_name_format = entry.options.get("device_name_format", "omitted")
    erase_tags = entry.options.get("erase_tags", False)
    relaxed_tag_match = entry.options.get("relaxed_tag_match", False)

    coordinator = MerakiDataUpdateCoordinator(
        hass,
        api_key,
        org_id,
        timedelta(seconds=scan_interval),
        device_name_format,
        erase_tags,
        relaxed_tag_match,
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {DATA_COORDINATOR: coordinator}
    _LOGGER.debug(
        "Meraki: Stored coordinator data in hass.data:"
        f" {hass.data[DOMAIN][entry.entry_id]}"
    )

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
