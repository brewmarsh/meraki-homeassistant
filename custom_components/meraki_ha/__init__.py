"""Initializes the meraki_ha integration.

This file sets up the Meraki integration for Home Assistant, coordinating
the data flow and platform setup. It handles the creation and management
of the MerakiDataUpdateCoordinator, which is responsible for fetching
data from the Meraki API. It also manages the setup and teardown of
associated platforms (sensor, device_tracker, switch).
"""

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
    """Set up Meraki integration from a config entry.

    This function initializes the Meraki integration by:
    1. Retrieving API key, organization ID, and other settings from the config entry.
    2. Creating and configuring the MerakiDataUpdateCoordinator.
    3. Performing an initial data refresh.
    4. Storing the coordinator in `hass.data`.
    5. Forwarding the setup to relevant platforms (sensor, device_tracker, switch).
    6. Setting up an update listener for reloading the entry on changes.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry containing integration settings.

    Returns:
        True if the setup was successful, False otherwise.
    """
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

    # Store the coordinator in hass.data for access by platforms
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {DATA_COORDINATOR: coordinator}
    _LOGGER.debug(
        "Meraki: Stored coordinator data in hass.data:"
        f" {hass.data[DOMAIN][entry.entry_id]}"
    )

    # Forward the setup to the defined platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up a listener to reload the entry when its options change
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug("Completed async_setup_entry")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry.

    This function is called when a config entry is to be removed. It unloads
    the platforms associated with the integration and removes the coordinator
    from `hass.data`.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry to unload.

    Returns:
        True if the unload was successful, False otherwise.
    """
    # Unload platforms associated with the integration
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # Remove the coordinator from hass.data
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a Meraki config entry.

    This function is called when a config entry's options have been updated.
    It first unloads the existing entry and then sets it up again with the
    new configuration.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry to reload.
    """
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
