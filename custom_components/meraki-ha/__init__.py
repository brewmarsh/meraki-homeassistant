"""Meraki HA integration."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from .coordinator import MerakiCoordinator

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha: Starting __init__.py import")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""
    _LOGGER.debug(
        f"Meraki async_setup_entry called. Entry options: {entry.options}"
    )  # changed to options

    try:
        api_key = entry.options[CONF_MERAKI_API_KEY]  # changed to options
        org_id = entry.options[CONF_MERAKI_ORG_ID]  # changed to options
        scan_interval = entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )  # changed to options
        scan_interval_timedelta = timedelta(minutes=scan_interval)

        coordinator = MerakiCoordinator(hass, api_key, org_id, scan_interval_timedelta)

        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = {
            DATA_CLIENT: {"api_key": api_key, "org_id": org_id},
            DATA_COORDINATOR: coordinator,
        }

        await coordinator.async_config_entry_first_refresh()

        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        _LOGGER.debug("Meraki async_forward_entry_setups called")
        return True

    except KeyError as e:
        _LOGGER.error(
            f"KeyError during setup: {e}. Entry options: {entry.options}"
        )  # changed to options
        return False
    except Exception as e:
        _LOGGER.error(
            f"Unexpected error during setup: {e}. Entry options: {entry.options}"
        )  # changed to options
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
