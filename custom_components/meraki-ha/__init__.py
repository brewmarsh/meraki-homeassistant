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

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_SCAN_INTERVAL
# from homeassistant.helpers.service import async_register_admin_service # Not used for set_device_tags
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError

from .coordinators import MerakiDataUpdateCoordinator
from .coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from .meraki_api import MerakiAPIClient, MerakiApiError, MerakiApiAuthError, MerakiApiNotFoundError, MerakiApiConnectionError

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    DATA_CLIENT,
)

_LOGGER = logging.getLogger(DOMAIN)

# SERVICE_SET_DEVICE_TAGS_SCHEMA = vol.Schema(
#     {
#         vol.Required("serial"): cv.string,
#         vol.Required("tags"): cv.string,
#     }
# )

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
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
        scan_interval_seconds = int(scan_interval_seconds_option)
    except ValueError:
        _LOGGER.error(
            "Invalid scan_interval '%s' in options. Using default: %s seconds.",
            scan_interval_seconds_option,
            DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL

    interval: timedelta = timedelta(seconds=scan_interval_seconds)

    main_coordinator = MerakiDataUpdateCoordinator(
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
        "coordinator": main_coordinator, # Legacy key
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

    _LOGGER.debug("PLATFORMS constant before forwarding: %s (type: %s, length: %s)", PLATFORMS, type(PLATFORMS), len(PLATFORMS) if isinstance(PLATFORMS, list) else 'N/A')
    platform_setup_success = await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("Result of async_forward_entry_setups (platform_setup_success): %s (type: %s)", platform_setup_success, type(platform_setup_success))

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    if not platform_setup_success:
        _LOGGER.error("One or more Meraki platforms failed to set up for entry %s. Integration setup failed.", entry.entry_id)
        return False

    # Defines the service handler for meraki-ha.set_device_tags
    # This is an inner function to capture `hass` and `entry` from the outer scope.
    # async def _async_set_device_tags_service_handler(call):
    #     # Handles the service call meraki-ha.set_device_tags
    #     serial = call.data.get("serial") # Get device serial
    #     tags_str = call.data.get("tags")

    #     if not serial: # 8 spaces
    #         # raise ServiceValidationError("Serial number is required.")
    #         _LOGGER.debug("DIAGNOSTIC: Service call set_device_tags was made without a serial number.")

    #     if tags_str == "": # 8 spaces
    #         tag_list = [] # 12 spaces
    #     else: # 8 spaces
    #         tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()] # 12 spaces

    #     current_entry_data = hass.data[DOMAIN].get(entry.entry_id) # 8 spaces
    #     if not current_entry_data: # 8 spaces
    #         _LOGGER.error(f"Configuration for entry {entry.entry_id} not found in hass.data.") # 12 spaces
    #         raise HomeAssistantError("Meraki integration configuration not found.") # 12 spaces

    #     meraki_client: MerakiAPIClient = current_entry_data.get(DATA_CLIENT) # 8 spaces
    #     main_coordinator_ref: MerakiDataUpdateCoordinator = current_entry_data.get("coordinators", {}).get("main") # 8 spaces

    #     if not meraki_client: # 8 spaces
    #         _LOGGER.error(f"Meraki API client not found for entry {entry.entry_id}. Cannot set device tags.") # 12 spaces
    #         raise HomeAssistantError("Meraki API client unavailable for this configuration entry.") # 12 spaces

    #     # Only proceed if serial was provided
    #     if serial:
    #         _LOGGER.info(f"Service meraki-ha.set_device_tags called for serial {serial} (entry {entry.entry_id}) with tags: {tag_list}") # 8 spaces

    #         try: # 8 spaces
    #             await meraki_client.async_update_device_tags(serial=serial, tags=tag_list) # 12 spaces
    #             _LOGGER.info(f"Successfully updated tags for device {serial}. Requesting coordinator refresh.") # 12 spaces
    #             if main_coordinator_ref: # 12 spaces
    #                 await main_coordinator_ref.async_request_refresh() # 16 spaces
    #         except MerakiApiAuthError as e: # 8 spaces
    #             _LOGGER.error(f"Authentication error updating tags for {serial}: {e}") # 12 spaces
    #             raise HomeAssistantError(f"Meraki API authentication error for {serial}: {e}") from e # 12 spaces
    #         except MerakiApiNotFoundError as e: # 8 spaces
    #             _LOGGER.error(f"Device {serial} not found when updating tags: {e}") # 12 spaces
    #             raise HomeAssistantError(f"Meraki device {serial} not found: {e}") from e # 12 spaces
    #         except MerakiApiConnectionError as e: # 8 spaces
    #             _LOGGER.error(f"Connection error updating tags for {serial}: {e}") # 12 spaces
    #             raise HomeAssistantError(f"Meraki API connection error for {serial}: {e}") from e # 12 spaces
    #         except MerakiApiError as e: # 8 spaces
    #             _LOGGER.error(f"Meraki API error updating tags for {serial}: {e}") # 12 spaces
    #             raise HomeAssistantError(f"Meraki API error for {serial}: {e}") from e # 12 spaces
    #         except Exception as e: # 8 spaces
    #             _LOGGER.exception(f"Unexpected error updating tags for {serial}: {e}") # 12 spaces
    #             raise HomeAssistantError(f"Unexpected error updating tags for {serial}: {e}") from e # 12 spaces

    # hass.services.async_register(
    #     DOMAIN,
    #     "set_device_tags",
    #     _async_set_device_tags_service_handler,
    #     schema=SERVICE_SET_DEVICE_TAGS_SCHEMA,
    # )

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
    )
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            domain_entry_data = hass.data[DOMAIN].pop(entry.entry_id)
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
                coordinator = domain_entry_data.get("coordinator")
                if (
                    coordinator
                    and hasattr(coordinator, "meraki_client")
                    and coordinator.meraki_client
                    and hasattr(coordinator.meraki_client, "close")
                ):
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
                        "Meraki API client not found at expected paths for entry %s during unload. Client session may not be closed.",
                        entry.entry_id,
                    )

            if not hass.data[DOMAIN]:
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
    """Reload Meraki config entry."""
    _LOGGER.info(
        "Reloading Meraki integration due to option changes for entry: %s",
        entry.entry_id,
    )
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
    _LOGGER.info("Finished reloading Meraki integration for entry: %s", entry.entry_id)
