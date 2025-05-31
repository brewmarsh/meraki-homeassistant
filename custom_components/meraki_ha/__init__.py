# custom_components/meraki_ha/__init__.py

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
# Ensure CONF_SCAN_INTERVAL is imported if used directly, or rely on its presence in entry.options
from homeassistant.const import CONF_SCAN_INTERVAL

from .coordinators import MerakiDataUpdateCoordinator
from .coordinators.ssid_device_coordinator import SSIDDeviceCoordinator # Import new coordinator
# MerakiAPIClient is likely imported by MerakiDataUpdateCoordinator or entities,
# but explicit import here if we were to instantiate it directly.
# For now, we assume main_coordinator creates/manages it.

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_RELAXED_TAG_MATCHING,
    DEFAULT_SCAN_INTERVAL, # Renamed from CONF_SCAN_INTERVAL to avoid clash with homeassistant.const
    DOMAIN,
    PLATFORMS, # This will now include PLATFORM_TEXT
    DATA_CLIENT, # For storing MerakiAPIClient
    # PLATFORM_TEXT, # No need to explicitly import PLATFORM_TEXT if PLATFORMS is updated correctly
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug(
        "Starting async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )

    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]

    # Use CONF_SCAN_INTERVAL from homeassistant.const for options key
    scan_interval_seconds_option = entry.options.get(
        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
    )
    try:
        # Ensure it's an int, as options can sometimes be strings
        scan_interval_seconds = int(scan_interval_seconds_option)
    except ValueError:
        _LOGGER.error(
            "Invalid scan_interval '%s' in options. Using default: %s seconds.",
            scan_interval_seconds_option,
            DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL

    interval: timedelta = timedelta(seconds=scan_interval_seconds)

    main_coordinator: MerakiDataUpdateCoordinator = MerakiDataUpdateCoordinator(
        hass=hass,
        api_key=api_key,
        org_id=org_id,
        scan_interval=interval,
        relaxed_tag_match=entry.options.get(CONF_RELAXED_TAG_MATCHING, False),
        config_entry=entry,
    )
    # Note: MerakiDataUpdateCoordinator should internally create and store its MerakiAPIClient instance
    # and make it available via a property (e.g., self.meraki_client) AND store it in
    # hass.data[DOMAIN][entry.entry_id][DATA_CLIENT] for entities to use.
    # This is a critical assumption for the rest of the setup.
    await main_coordinator.async_config_entry_first_refresh()

    # Retrieve the client instance that main_coordinator should have created and stored.
    # This relies on main_coordinator's implementation to place the client in hass.data.
    # If it doesn't, this is a structural issue to be fixed in MerakiDataUpdateCoordinator.
    # For now, we assume it does, or at least exposes it via a property.
    meraki_client_instance = getattr(main_coordinator, "meraki_client", None)
    if not meraki_client_instance:
        # This is a fallback logic block if main_coordinator doesn't expose client directly
        # but it should have stored it in hass.data if it created it.
        # Let's check hass.data as a primary source if not on coordinator.
        try:
            meraki_client_instance = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
        except KeyError:
            _LOGGER.error(
                "MerakiAPIClient not found on main_coordinator and not in hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]. "
                "SSID coordinator and its entities may not function correctly if they need to make API calls. "
                "This indicates MerakiDataUpdateCoordinator is not storing the client as expected."
            )
            # Depending on strictness, could return False here.
            # For now, we'll let it proceed, and entities that need the client will fail if it's not there.

    # Initialize SSIDDeviceCoordinator
    ssid_coordinator = SSIDDeviceCoordinator(
        hass=hass,
        config_entry=entry,
        api_data_fetcher=main_coordinator, # main_coordinator's .data should provide "ssids"
        update_interval=interval, # Or a different interval if desired for SSIDs
    )
    await ssid_coordinator.async_config_entry_first_refresh()

    # Store coordinators and client in the structure expected by entities
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": main_coordinator, # Main coordinator (legacy access for some parts)
        DATA_CLIENT: meraki_client_instance, # Central client instance
        "coordinators": {
            "main": main_coordinator,
            "ssid_devices": ssid_coordinator,
        }
    }
    _LOGGER.debug(
        "Stored coordinators and client in hass.data for entry_id: %s. Client instance: %s",
        entry.entry_id,
        "present" if meraki_client_instance else "MISSING",
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug(
        "Completed async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle unloading of a Meraki config entry.

    This function is called by Home Assistant when the integration is being
    unloaded (e.g., due to removal or reconfiguration). It ensures that
    all associated platforms are unloaded and cleans up resources, such as
    the Meraki API client and data coordinators.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry being unloaded.

    Returns:
        True if the unload was successful, False otherwise.
    """
    _LOGGER.debug("Starting async_unload_entry for Meraki integration.")

    # Unload platforms associated with the config entry.
    # PLATFORMS should be the list of platform constants from const.py
    unload_ok: bool = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )

    if unload_ok:
        _LOGGER.debug("Successfully unloaded Meraki platforms.")
        # Retrieve the main coordinator to close its client session
        # This assumes the client is managed by the main coordinator.
        if (
            DOMAIN in hass.data
            and entry.entry_id in hass.data[DOMAIN]
            and "coordinators" in hass.data[DOMAIN][entry.entry_id]
            and "main" in hass.data[DOMAIN][entry.entry_id]["coordinators"]

        ):
            main_coordinator = hass.data[DOMAIN][entry.entry_id]["coordinators"]["main"]
            if hasattr(main_coordinator, "meraki_client") and main_coordinator.meraki_client:
                try:
                    _LOGGER.debug("Closing Meraki API client session.")
                    await main_coordinator.meraki_client.close()
                except Exception as e:
                    _LOGGER.error("Error closing Meraki API client session: %s", e)

            # Clean up hass.data for this entry
            hass.data[DOMAIN].pop(entry.entry_id)
            if not hass.data[DOMAIN]: # If no other entries, remove domain from data
                hass.data.pop(DOMAIN)
            _LOGGER.debug("Cleaned up hass.data for Meraki entry_id: %s", entry.entry_id)
        else:
            _LOGGER.warning(
                "Could not find main coordinator in hass.data to close client session during unload."
            )
    else:
        _LOGGER.error("Failed to unload Meraki platforms for entry_id: %s.", entry.entry_id)

    _LOGGER.debug("Completed async_unload_entry for Meraki integration.")
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki configuration entry.

    This function is called by Home Assistant when the user requests to
    reload the integration, typically after changing configuration options.
    It first unloads the existing setup and then re-initializes it.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry to reload.
    """
    _LOGGER.debug("Reloading Meraki configuration entry: %s", entry.entry_id)
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
    _LOGGER.debug(
        "Finished reloading Meraki configuration entry: %s", entry.entry_id
    )
