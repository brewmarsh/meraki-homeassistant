# custom_components/meraki_ha/__init__.py

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_SCAN_INTERVAL

from .coordinators import MerakiDataUpdateCoordinator
from .coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

# MerakiAPIClient might not be directly needed in __init__ if main_coordinator creates and stores it.
# from .meraki_api import MerakiAPIClient

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_RELAXED_TAG_MATCHING,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    DATA_CLIENT,
    # PLATFORM_TEXT, # Already part of PLATFORMS from const.py
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry.

    Args:
        hass: Home Assistant instance.
        entry: Config entry.

    Returns:
        True if successful, False otherwise.
    """
    _LOGGER.debug(
        "Starting async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )

    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]

    scan_interval_seconds_option = entry.options.get(  # Corrected variable name
        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
    )
    try:
        scan_interval_seconds = int(
            scan_interval_seconds_option
        )  # Use corrected var name
    except ValueError:
        _LOGGER.error(
            "Invalid scan_interval '%s' in options. Using default: %s seconds.",
            scan_interval_seconds_option,  # Use corrected var name
            DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL

    interval: timedelta = timedelta(seconds=scan_interval_seconds)

    # 1. Initialize Main Coordinator
    # This coordinator is responsible for fetching primary data like devices, networks, etc.
    # It serves as the main source of truth for physical device information.
    main_coordinator: MerakiDataUpdateCoordinator = MerakiDataUpdateCoordinator(
        hass=hass,
        api_key=api_key,
        org_id=org_id,
        scan_interval=interval,
        relaxed_tag_match=entry.options.get(CONF_RELAXED_TAG_MATCHING, False),
        config_entry=entry,
    )
    # 2. Perform its first refresh
    # This initial refresh populates the coordinator with data before entities are set up.
    await main_coordinator.async_config_entry_first_refresh()

    # Register the Meraki Organization itself as a device in Home Assistant.
    # This call is placed after the first refresh to ensure that the
    # coordinator has fetched necessary data, like the organization name,
    # which is used in the device registration process.
    if hasattr(main_coordinator, "async_register_organization_device"):
        _LOGGER.debug("Attempting to register Meraki Organization as a device.")
        await main_coordinator.async_register_organization_device(hass)
    else:
        _LOGGER.warning("main_coordinator does not have async_register_organization_device method.")

    # 3. Populate hass.data with the client from main_coordinator and the main_coordinator itself
    # hass.data is the central store in Home Assistant for sharing data between components and platforms.
    # We store the MerakiAPIClient instance for direct API access if needed by other parts
    # of the integration (e.g., services) and the coordinators themselves.
    # This assumes main_coordinator has a 'meraki_client' attribute holding the MerakiAPIClient instance.
    meraki_client_instance = getattr(main_coordinator, "meraki_client", None)
    if not meraki_client_instance:
        _LOGGER.error(
            "MerakiAPIClient not available from main_coordinator. Integration setup failed for entry %s.",
            entry.entry_id,
        )
        return False  # Critical failure if the client isn't initialized.

    hass.data.setdefault(DOMAIN, {})
    # Store data per config entry to support multiple Meraki organizations.
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: meraki_client_instance,  # The shared Meraki API client.
        "coordinator": main_coordinator,  # Main coordinator (legacy key, might be phased out).
        "coordinators": {  # Dictionary to hold all coordinators for this config entry.
            "main": main_coordinator,  # Store the main coordinator.
        },
    }
    _LOGGER.debug(
        "Stored MerakiAPIClient and main_coordinator in hass.data for entry_id: %s",
        entry.entry_id,
    )

    # 4. Initialize SSIDDeviceCoordinator
    # This coordinator specifically handles SSID "devices" (logical representations of SSIDs).
    # It relies on the main_coordinator for the list of SSIDs fetched from the API.
    # It can now access DATA_CLIENT (the MerakiAPIClient) from hass.data during its first refresh if needed for detailed calls.
    ssid_coordinator = SSIDDeviceCoordinator(
        hass=hass,
        config_entry=entry,
        api_data_fetcher=main_coordinator,  # main_coordinator acts as the source of the raw SSID list.
        update_interval=interval,  # Use the same update interval.
    )
    # 5. Perform its first refresh
    # This populates the SSID coordinator with its specific data (e.g., enabled SSIDs and their details).
    await ssid_coordinator.async_config_entry_first_refresh()

    # 6. Add ssid_coordinator to the coordinators dictionary in hass.data
    # This makes the SSID coordinator accessible to platforms that need it (e.g., sensor, switch for SSIDs).
    hass.data[DOMAIN][entry.entry_id]["coordinators"]["ssid_devices"] = ssid_coordinator
    _LOGGER.debug(
        "Added ssid_devices_coordinator to hass.data for entry_id: %s",
        entry.entry_id,
    )

    # Forward the setup to configured platforms (sensor, switch, etc.).
    # Each platform will look up its relevant coordinator(s) from hass.data.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up a listener for options updates. If options change (e.g., scan interval),
    # the entry will be reloaded.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug(
        "Completed async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry.

    Args:
        hass: Home Assistant instance.
        entry: Config entry.

    Returns:
        True if successful, False otherwise.
    """
    _LOGGER.info(
        "Unloading Meraki integration for entry_id: %s", entry.entry_id
    )  # Changed to info
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            # Remove this entry's data from the central hass.data store.
            domain_entry_data = hass.data[DOMAIN].pop(entry.entry_id)

            # Close the MerakiAPIClient session to release resources.
            meraki_client_instance = domain_entry_data.get(DATA_CLIENT)
            if meraki_client_instance and hasattr(meraki_client_instance, "close"):
                _LOGGER.info(
                    "Closing Meraki API client session for entry %s.", entry.entry_id
                )
                try:
                    await meraki_client_instance.close()
                except Exception as e:
                    _LOGGER.error(
                        "Error closing Meraki API client session for entry %s: %s",
                        entry.entry_id,
                        e,
                        exc_info=True,
                    )
            elif meraki_client_instance:
                _LOGGER.warning(
                    "Meraki API client for entry %s does not have a 'close' method.",
                    entry.entry_id,
                )
            else:
                # Fallback for safety, though DATA_CLIENT should be the primary path now.
                # This handles older structures or if DATA_CLIENT was somehow not populated.
                coordinator = domain_entry_data.get(
                    "coordinator"
                )  # Legacy path to main coordinator
                if (
                    coordinator
                    and hasattr(coordinator, "meraki_client")
                    and coordinator.meraki_client
                ):
                    if hasattr(coordinator.meraki_client, "close"):
                        _LOGGER.info(
                            "Closing Meraki API client session (via legacy coordinator attribute) for entry %s.",
                            entry.entry_id,
                        )
                        try:
                            await coordinator.meraki_client.close()
                        except Exception as e:
                            _LOGGER.error(
                                "Error closing Meraki API client session (via legacy coordinator attribute) for entry %s: %s",
                                entry.entry_id,
                                e,
                                exc_info=True,
                            )
                    else:
                        _LOGGER.warning(
                            "Meraki API client (via legacy coordinator attribute) for entry %s does not have a 'close' method.",
                            entry.entry_id,
                        )
                else:
                    _LOGGER.warning(
                        "Meraki API client not found at expected paths for entry %s during unload. Client session may not be closed.",
                        entry.entry_id,
                    )

            # If this was the last Meraki config entry, remove the domain itself from hass.data.
            if not hass.data[DOMAIN]:  # If no other entries, remove domain from data
                hass.data.pop(DOMAIN)
            _LOGGER.info(
                "Successfully unloaded Meraki integration and associated data for entry: %s",
                entry.entry_id,
            )
        else:
            _LOGGER.info(
                "No data found in hass.data[DOMAIN] for entry %s to remove during unload.",
                entry.entry_id,
            )
    else:
        _LOGGER.error("Failed to unload Meraki platforms for entry: %s", entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry.

    This is typically called when integration options are changed.
    It ensures that the integration is re-initialized with the new options.

    Args:
        hass: Home Assistant instance.
        entry: Config entry.
    """
    _LOGGER.info(
        "Reloading Meraki integration due to option changes for entry: %s",
        entry.entry_id,
    )
    # Unload the existing setup.
    await async_unload_entry(hass, entry)
    # Set up the integration again with the new options.
    await async_setup_entry(hass, entry)
    _LOGGER.info("Finished reloading Meraki integration for entry: %s", entry.entry_id)
