"""
This is the init file for the Meraki Home Assistant integration.
It sets up the platform and loads the necessary components.
"""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# from homeassistant.const import Platform

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_RELAXED_TAG_MATCHING,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import (
    MerakiDataUpdateCoordinator,
    MerakiNetworkCoordinator,
)
from .coordinators.ssid_coordinator import MerakiSsidCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""

    _LOGGER.debug(f"Starting async_setup_entry for entry_id: {entry.entry_id}")
    api_key = entry.data[CONF_MERAKI_API_KEY]
    org_id = entry.data[CONF_MERAKI_ORG_ID]
    base_url = "https://api.meraki.com/api/v1"  # Consider moving to const.py

    _LOGGER.debug(f"Entry data: {entry.data}")
    _LOGGER.debug(f"Entry options: {entry.options}")

    scan_interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)

    _LOGGER.debug(
        f"Scan_interval from options: {scan_interval}, type: {type(scan_interval)}"
    )

    scan_interval = int(scan_interval)  # Force integer conversion

    _LOGGER.debug(
        f"Scan_interval after conversion: {scan_interval}, type: {type(scan_interval)}"
    )

    # Log IMMEDIATELY before timedelta
    _LOGGER.debug(
        f"About to create timedelta with: {scan_interval}, type: {type(scan_interval)}"
    )

    interval = timedelta(seconds=scan_interval)  # Create timedelta explicitly

    networks_coordinator = MerakiNetworkCoordinator(
        hass,
        api_key,
        org_id,
        interval,  # Correctly pass the timedelta as scan_interval
        entry.options.get("device_name_format", "prefix"),  # Pass device_name_format
    )
    ssid_coordinator = MerakiSsidCoordinator(
        hass, api_key, org_id, interval, base_url
    )  # Corrected order

    coordinator = MerakiDataUpdateCoordinator(
        hass,
        api_key,
        org_id,
        base_url,
        interval,
        networks_coordinator,
        ssid_coordinator,  # Pass the ssid_coordinator
        entry.options.get(CONF_RELAXED_TAG_MATCHING, False),
        entry,
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator}
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
