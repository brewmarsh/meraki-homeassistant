"""Initializes the Meraki Home Assistant integration.

This module sets up the core components of the Meraki integration, primarily
by initializing and configuring the `MerakiDataUpdateCoordinator`. This
coordinator is responsible for fetching and managing all data from the
Meraki Dashboard API, which is then used by various platforms (sensor, switch, etc.).
"""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_RELAXED_TAG_MATCHING,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS, # List of platforms (e.g., ["sensor", "switch"])
)
from .coordinators.base_coordinator import MerakiDataUpdateCoordinator
# Obsolete imports for MerakiNetworkCoordinator and MerakiSsidCoordinator are removed.

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki Home Assistant integration from a configuration entry.

    This function initializes the `MerakiDataUpdateCoordinator`, which handles
    all API interactions and data management. It then forwards the setup to
    the relevant Home Assistant platforms (like sensor, switch).

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry containing user-provided settings
               (API key, Organization ID, options).

    Returns:
        True if the setup was successful, False otherwise.
    """
    _LOGGER.debug("Starting async_setup_entry for Meraki integration (entry_id: %s)", entry.entry_id)

    # Retrieve API key and organization ID from the configuration entry.
    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]
    # The base_url is handled by the MerakiAPIClient within the coordinator/SDK.
    # No longer needed here: base_url: str = "https://api.meraki.com/api/v1"

    _LOGGER.debug("Meraki entry data: %s", entry.data)
    _LOGGER.debug("Meraki entry options: %s", entry.options)

    # Get scan interval from entry options, with a default value.
    scan_interval_seconds: int = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)

    # Ensure scan_interval_seconds is an integer.
    try:
        scan_interval_seconds = int(scan_interval_seconds)
    except ValueError:
        _LOGGER.error(
            "Invalid scan_interval '%s' in options. Using default: %s seconds.",
            scan_interval_seconds, DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL
    
    _LOGGER.debug("Using scan interval of %d seconds for Meraki coordinator.", scan_interval_seconds)
    interval: timedelta = timedelta(seconds=scan_interval_seconds)

    # Initialization of separate MerakiNetworkCoordinator and MerakiSsidCoordinator removed,
    # as their functionalities are now integrated within or made obsolete by changes to
    # MerakiDataUpdateCoordinator and MerakiApiDataFetcher.

    # Initialize the main data update coordinator.
    # This coordinator now manages all data fetching and sub-coordination internally.
    coordinator: MerakiDataUpdateCoordinator = MerakiDataUpdateCoordinator(
        hass=hass,
        api_key=api_key,
        org_id=org_id,
        scan_interval=interval,
        relaxed_tag_match=entry.options.get(CONF_RELAXED_TAG_MATCHING, False),
        config_entry=entry,
    )

    # Perform the initial data fetch. This is crucial to ensure that data is
    # available before Home Assistant attempts to set up entities on various platforms.
    await coordinator.async_config_entry_first_refresh()

    # Store the initialized coordinator in `hass.data` for access by platforms.
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator}
    _LOGGER.debug(
        "Stored MerakiDataUpdateCoordinator in hass.data for entry_id: %s", entry.entry_id
    )

    # Forward the setup to all defined platforms (e.g., sensor, switch).
    # These platforms will use the coordinator stored in `hass.data`.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up a listener to reload the entry if the configuration options change.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug("Completed async_setup_entry for Meraki integration (entry_id: %s)", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki configuration entry.

    This function is called when the integration is being removed or reloaded.
    It handles unloading platforms, closing API client sessions, and cleaning
    up data stored in `hass.data`.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry to unload.

    Returns:
        True if the unload process was successful, False otherwise.
    """
    _LOGGER.debug("Unloading Meraki integration for entry_id: %s", entry.entry_id)
    # Unload platforms (sensor, switch, etc.) associated with this config entry.
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # If platforms unloaded successfully, clean up coordinator and API client.
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            domain_entry_data = hass.data[DOMAIN].pop(entry.entry_id) # Remove and get entry's data.
            coordinator: Optional[MerakiDataUpdateCoordinator] = domain_entry_data.get("coordinator")
            
            # Gracefully close the Meraki API client session if the coordinator and client exist.
            if coordinator and hasattr(coordinator, 'meraki_client') and coordinator.meraki_client:
                if hasattr(coordinator.meraki_client, 'close'):
                    _LOGGER.info("Closing Meraki API client session for entry %s.", entry.entry_id)
                    try:
                        await coordinator.meraki_client.close()
                    except Exception as e:
                        _LOGGER.error("Error closing Meraki API client session for entry %s: %s", entry.entry_id, e)
                else:
                    _LOGGER.warning("Meraki API client for entry %s does not have a 'close' method.", entry.entry_id)
            else:
                _LOGGER.warning("Meraki API client or coordinator not found for entry %s during unload.", entry.entry_id)
            
            _LOGGER.info("Successfully unloaded Meraki integration and associated data for entry: %s", entry.entry_id)
        else:
            _LOGGER.info("No data found in hass.data[DOMAIN] for entry %s to remove during unload.", entry.entry_id)
    else:
        _LOGGER.error("Failed to unload Meraki platforms for entry: %s", entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a Meraki configuration entry upon option changes.

    This function is triggered when the user modifies the integration's options.
    It ensures changes are applied by unloading and then setting up the
    integration again with the new configuration, avoiding a full Home Assistant restart.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry that has been updated.
    """
    _LOGGER.info("Reloading Meraki integration due to option changes for entry: %s", entry.entry_id)
    await async_unload_entry(hass, entry) # Unload the current setup.
    await async_setup_entry(hass, entry)  # Set up again with new options.
    _LOGGER.info("Finished reloading Meraki integration for entry: %s", entry.entry_id)