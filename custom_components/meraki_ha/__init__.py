"""
This is the init file for the Meraki Home Assistant integration.

It sets up the platform and loads the necessary components.
"""
import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_RELAXED_TAG_MATCHING,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
)
from .coordinators.base_coordinator import MerakiDataUpdateCoordinator
from .coordinators.network_coordinator import MerakiNetworkCoordinator
from .coordinators.ssid_coordinator import MerakiSsidCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki Home Assistant from a config entry.

    This function initializes the Meraki integration by setting up coordinators
    for data fetching and processing, and then forwards the setup to the
    relevant platforms (e.g., sensor, switch).

    Args:
        hass: The Home Assistant instance.
        entry: The config entry containing user configuration.

    Returns:
        True if the setup was successful, False otherwise.
    """
    _LOGGER.debug(f"Starting async_setup_entry for entry_id: {entry.entry_id}")
    # Retrieve API key and organization ID from the configuration entry data
    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]
    # Define the base URL for Meraki API v1.
    # This could be moved to const.py for better maintainability.
    base_url: str = "https://api.meraki.com/api/v1"

    _LOGGER.debug(f"Entry data: {entry.data}")
    _LOGGER.debug(f"Entry options: {entry.options}")

    # Get scan interval from entry options, defaulting to
    # DEFAULT_SCAN_INTERVAL if not set
    scan_interval_seconds: int = entry.options.get(
        "scan_interval", DEFAULT_SCAN_INTERVAL
    )

    _LOGGER.debug(
        "Scan_interval from options: %s, type: %s",
        scan_interval_seconds,
        type(scan_interval_seconds),
    )

    # Ensure scan_interval_seconds is an int before creating timedelta
    # This handles cases where the option might be stored as a string.
    try:
        scan_interval_seconds = int(scan_interval_seconds)
    except ValueError:
        _LOGGER.error(
            "Invalid scan_interval: %s. Using default: %s",
            scan_interval_seconds,
            DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL


    _LOGGER.debug(
        "Scan_interval after conversion: %s, type: %s",
        scan_interval_seconds,
        type(scan_interval_seconds),
    )

    # Convert scan interval to a timedelta object for use with coordinators
    interval: timedelta = timedelta(seconds=scan_interval_seconds)

    # Initialize the coordinator for fetching network-specific data
    networks_coordinator: MerakiNetworkCoordinator = MerakiNetworkCoordinator(
        hass,
        api_key,
        org_id,
        interval,  # Use the calculated timedelta interval
        entry.options.get(
            "device_name_format", "prefix"
        ),  # Pass device name formatting option
    )
    # Initialize the coordinator for fetching SSID-specific data
    ssid_coordinator: MerakiSsidCoordinator = MerakiSsidCoordinator(
        hass,
        api_key,
        org_id,
        interval,
        base_url,  # Pass necessary config and interval
    )

    # Initialize the main data update coordinator for the Meraki integration
    # This coordinator orchestrates data fetching using sub-coordinators.
    coordinator: MerakiDataUpdateCoordinator = MerakiDataUpdateCoordinator(
        hass,
        api_key,
        org_id,
        base_url,
        interval,  # Use the calculated timedelta interval
        networks_coordinator,  # Pass the networks_coordinator instance
        ssid_coordinator,  # Pass the ssid_coordinator instance
        entry.options.get(
            CONF_RELAXED_TAG_MATCHING, False
        ),  # Get relaxed tag matching option
        entry,  # Pass the full config entry for context
    )
    # Perform the initial data fetch for the coordinator.
    # This ensures data is available before entities are set up.
    await coordinator.async_config_entry_first_refresh()

    # Store the initialized coordinator in hass.data for access by platforms
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator}
    _LOGGER.debug(
        "Meraki: Stored coordinator data in hass.data for entry_id: %s",
        entry.entry_id,
    )

    # Forward the setup of the config entry to all defined platforms
    # (sensor, switch, etc.)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Add an update listener to reload the entry when options change
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug("Completed async_setup_entry")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry.

    This function unloads the Meraki integration by removing listeners and
    cleaning up resources associated with the config entry. This is called
    when the integration is being removed or reloaded.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry to unload.

    Returns:
        True if the unload was successful, False otherwise.
    """
    # Unload platforms associated with this config entry
    unload_ok: bool = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    # If platform unloading was successful, remove coordinator data from hass.data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info(
            "Successfully unloaded Meraki integration for entry: %s",
            entry.entry_id,
        )
    else:
        _LOGGER.error(
            "Failed to unload Meraki platforms for entry: %s", entry.entry_id
        )
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a Meraki config entry.

    This function handles reloading the Meraki integration when the config entry
    (e.g., options) is updated. It first unloads the existing setup and then
    sets up the integration again with the new configuration. This ensures
    changes are applied without needing a full HA restart.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry to reload.
    """
    _LOGGER.info(
        "Reloading Meraki integration for entry: %s", entry.entry_id
    )
    # Unload the current setup
    await async_unload_entry(hass, entry)
    # Set up the integration again with the (potentially updated) entry
    # data/options
    await async_setup_entry(hass, entry)
    _LOGGER.info(
        "Finished reloading Meraki integration for entry: %s", entry.entry_id
    )
