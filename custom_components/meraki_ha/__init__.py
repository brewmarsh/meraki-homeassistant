"""The Meraki Home Assistant integration.

This component provides integration with the Cisco Meraki cloud-managed
networking platform. It allows users to monitor and potentially control
aspects of their Meraki networks and devices within Home Assistant.

Key responsibilities of this `__init__.py` file:
- Setting up the integration from a configuration entry (`async_setup_entry`).
- Unloading the integration (`async_unload_entry`).
- Reloading the integration, typically when options change (`async_reload_entry`).
- Initializing and coordinating data update coordinators.
- Registering the Meraki organization as a device in Home Assistant.
- Forwarding the setup to various platforms (sensor, switch, etc.).
"""

import logging
from datetime import timedelta

import voluptuous as vol # Added import
import homeassistant.helpers.config_validation as cv # Added import
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.helpers.service import async_register_admin_service # Not used, standard register is used
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError # Added imports

from .coordinators import MerakiDataUpdateCoordinator
from .coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

# Ensure MerakiAPIClient and specific exceptions are available
from .meraki_api import MerakiAPIClient, MerakiApiError, MerakiApiAuthError, MerakiApiNotFoundError, MerakiApiConnectionError # Added import

# MerakiAPIClient might not be directly needed in __init__ if main_coordinator creates and stores it.
# from .meraki_api import MerakiAPIClient

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    # CONF_RELAXED_TAG_MATCHING, # Removed as feature was removed
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    DATA_CLIENT,
    # PLATFORM_TEXT, # Already part of PLATFORMS from const.py
)

_LOGGER = logging.getLogger(__name__)

SERVICE_SET_DEVICE_TAGS_SCHEMA = vol.Schema(
    {
        vol.Required("serial"): cv.string,
        vol.Required("tags"): cv.string,
    }
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry.

    This function initializes the Meraki integration by setting up
    data update coordinators, performing an initial data refresh,
    registering devices, and forwarding the setup to relevant platforms.

    Args:
        hass: The Home Assistant instance, used for storing shared data (e.g., API client, coordinators)
              and for setting up platforms.
        entry: The ConfigEntry object representing this integration instance,
               containing user configuration (API key, Org ID) and options (scan interval).

    Returns:
        True if setup is successful, False otherwise.
    """
    _LOGGER.debug(
        "Starting async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )

    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]

    scan_interval_seconds_option = entry.options.get(
        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
    )
    try:
        scan_interval_seconds = int(
            scan_interval_seconds_option
        )
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
        config_entry=entry,
    )
    await main_coordinator.async_config_entry_first_refresh()

    if hasattr(main_coordinator, "async_register_organization_device"):
        _LOGGER.debug("Attempting to register Meraki Organization as a device.")
        await main_coordinator.async_register_organization_device(hass)
    else:
        _LOGGER.warning("main_coordinator does not have async_register_organization_device method.")

    meraki_client_instance = getattr(main_coordinator, "meraki_client", None)
    if not meraki_client_instance:
        _LOGGER.error(
            "MerakiAPIClient not available from main_coordinator. Integration setup failed for entry %s.",
            entry.entry_id,
        )
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: meraki_client_instance,
        "coordinator": main_coordinator,
        "coordinators": {
            "main": main_coordinator,
        },
    }
    _LOGGER.debug(
        "Stored MerakiAPIClient and main_coordinator in hass.data for entry_id: %s",
        entry.entry_id,
    )

    ssid_coordinator = SSIDDeviceCoordinator(
        hass=hass,
        config_entry=entry,
        api_data_fetcher=main_coordinator,
        update_interval=interval,
    )
    await ssid_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id]["coordinators"]["ssid_devices"] = ssid_coordinator
    _LOGGER.debug(
        "Added ssid_devices_coordinator to hass.data for entry_id: %s",
        entry.entry_id,
    )

    platform_setup_success = await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    if not platform_setup_success:
        _LOGGER.error("One or more Meraki platforms failed to set up for entry %s. Integration setup failed.", entry.entry_id)
        return False

    # Defines the service handler for meraki_ha.set_device_tags
    # This is an inner function to capture `hass` and `entry` from the outer scope.
    async def _async_set_device_tags_service_handler(call):
        # Handles the service call meraki_ha.set_device_tags
        serial = call.data.get("serial") # Get device serial
        tags_str = call.data.get("tags")

        if not serial: # 8 spaces
            # raise ServiceValidationError("Serial number is required.")
            _LOGGER.debug("DIAGNOSTIC: Service call set_device_tags was made without a serial number.")

        if tags_str == "": # 8 spaces
            tag_list = [] # 12 spaces
        else: # 8 spaces
            tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()] # 12 spaces

        current_entry_data = hass.data[DOMAIN].get(entry.entry_id) # 8 spaces
        if not current_entry_data: # 8 spaces
            _LOGGER.error(f"Configuration for entry {entry.entry_id} not found in hass.data.") # 12 spaces
            raise HomeAssistantError("Meraki integration configuration not found.") # 12 spaces

        meraki_client: MerakiAPIClient = current_entry_data.get(DATA_CLIENT) # 8 spaces
        main_coordinator: MerakiDataUpdateCoordinator = current_entry_data.get("coordinators", {}).get("main") # 8 spaces

        if not meraki_client: # 8 spaces
            _LOGGER.error(f"Meraki API client not found for entry {entry.entry_id}. Cannot set device tags.") # 12 spaces
            raise HomeAssistantError("Meraki API client unavailable for this configuration entry.") # 12 spaces

        # Only proceed if serial was provided
        if serial:
            _LOGGER.info(f"Service meraki_ha.set_device_tags called for serial {serial} (entry {entry.entry_id}) with tags: {tag_list}") # 8 spaces

            try: # 8 spaces
                await meraki_client.async_update_device_tags(serial=serial, tags=tag_list) # 12 spaces
                _LOGGER.info(f"Successfully updated tags for device {serial}. Requesting coordinator refresh.") # 12 spaces
                if main_coordinator: # 12 spaces
                    await main_coordinator.async_request_refresh() # 16 spaces
            except MerakiApiAuthError as e: # 8 spaces
                _LOGGER.error(f"Authentication error updating tags for {serial}: {e}") # 12 spaces
                raise HomeAssistantError(f"Meraki API authentication error for {serial}: {e}") from e # 12 spaces
            except MerakiApiNotFoundError as e: # 8 spaces
                _LOGGER.error(f"Device {serial} not found when updating tags: {e}") # 12 spaces
                raise HomeAssistantError(f"Meraki device {serial} not found: {e}") from e # 12 spaces
            except MerakiApiConnectionError as e: # 8 spaces
                _LOGGER.error(f"Connection error updating tags for {serial}: {e}") # 12 spaces
                raise HomeAssistantError(f"Meraki API connection error for {serial}: {e}") from e # 12 spaces
            except MerakiApiError as e: # 8 spaces
                _LOGGER.error(f"Meraki API error updating tags for {serial}: {e}") # 12 spaces
                raise HomeAssistantError(f"Meraki API error for {serial}: {e}") from e # 12 spaces
            except Exception as e: # 8 spaces
                _LOGGER.exception(f"Unexpected error updating tags for {serial}: {e}") # 12 spaces
                raise HomeAssistantError(f"Unexpected error updating tags for {serial}: {e}") from e # 12 spaces
        # Removed redundant 'elif not serial: pass' block


    hass.services.async_register(
        DOMAIN,
        "set_device_tags",
        _async_set_device_tags_service_handler,
        schema=SERVICE_SET_DEVICE_TAGS_SCHEMA,
    )

    _LOGGER.debug(
        "Completed async_setup_entry for Meraki integration (entry_id: %s) successfully, all platforms loaded.",
        entry.entry_id,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry.

    This function is called when Home Assistant is removing the integration setup.
    It unloads the platforms, closes the API client session, and cleans up
    data stored in `hass.data`.

    Args:
        hass: The Home Assistant instance, used to access integration data for cleanup
              and to unload platforms.
        entry: The ConfigEntry object for this integration instance, used to identify
               the data and platforms to unload.

    Returns:
        True if all unload operations are successful, False otherwise.
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
        hass: The Home Assistant instance, passed to unload and setup functions.
        entry: The ConfigEntry object being reloaded, passed to unload and setup functions.
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
