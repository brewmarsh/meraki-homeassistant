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
    _LOGGER.debug(
        "Starting async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )

    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]

    scan_interval_seconds_option = entry.options.get( # Corrected variable name
        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
    )
    try:
        scan_interval_seconds = int(scan_interval_seconds_option) # Use corrected var name
    except ValueError:
        _LOGGER.error(
            "Invalid scan_interval '%s' in options. Using default: %s seconds.",
            scan_interval_seconds_option, # Use corrected var name
            DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL

    interval: timedelta = timedelta(seconds=scan_interval_seconds)

    # 1. Initialize Main Coordinator
    main_coordinator: MerakiDataUpdateCoordinator = MerakiDataUpdateCoordinator(
        hass=hass,
        api_key=api_key,
        org_id=org_id,
        scan_interval=interval,
        relaxed_tag_match=entry.options.get(CONF_RELAXED_TAG_MATCHING, False),
        config_entry=entry,
    )
    # 2. Perform its first refresh
    await main_coordinator.async_config_entry_first_refresh()

    # 3. Populate hass.data with the client from main_coordinator and the main_coordinator itself
    # This assumes main_coordinator has a 'meraki_client' attribute holding the MerakiAPIClient instance.
    meraki_client_instance = getattr(main_coordinator, "meraki_client", None)
    if not meraki_client_instance:
        _LOGGER.error("MerakiAPIClient not available from main_coordinator. Integration setup failed for entry %s.", entry.entry_id)
        return False # Critical failure

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: meraki_client_instance,
        "coordinator": main_coordinator, # Main coordinator (legacy key)
        "coordinators": { # Prepare coordinators dictionary
            "main": main_coordinator,
        }
    }
    _LOGGER.debug(
        "Stored MerakiAPIClient and main_coordinator in hass.data for entry_id: %s",
        entry.entry_id,
    )

    # 4. Initialize SSIDDeviceCoordinator
    # It can now access DATA_CLIENT from hass.data during its first refresh.
    # It still needs main_coordinator's data.
    ssid_coordinator = SSIDDeviceCoordinator(
        hass=hass,
        config_entry=entry,
        api_data_fetcher=main_coordinator, # main_coordinator acts as the source of SSID list
        update_interval=interval,
    )
    # 5. Perform its first refresh
    await ssid_coordinator.async_config_entry_first_refresh()

    # 6. Add ssid_coordinator to the coordinators dictionary in hass.data
    hass.data[DOMAIN][entry.entry_id]["coordinators"]["ssid_devices"] = ssid_coordinator
    _LOGGER.debug(
        "Added ssid_devices_coordinator to hass.data for entry_id: %s",
        entry.entry_id,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.debug(
        "Completed async_setup_entry for Meraki integration (entry_id: %s)",
        entry.entry_id,
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Unloading Meraki integration for entry_id: %s", entry.entry_id) # Changed to info
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            domain_entry_data = hass.data[DOMAIN].pop(entry.entry_id)

            meraki_client_instance = domain_entry_data.get(DATA_CLIENT)
            if meraki_client_instance and hasattr(meraki_client_instance, "close"):
                _LOGGER.info("Closing Meraki API client session for entry %s.", entry.entry_id)
                try:
                    await meraki_client_instance.close()
                except Exception as e:
                    _LOGGER.error("Error closing Meraki API client session for entry %s: %s", entry.entry_id, e, exc_info=True)
            elif meraki_client_instance:
                 _LOGGER.warning("Meraki API client for entry %s does not have a 'close' method.", entry.entry_id)
            else:
                # Fallback for safety, though DATA_CLIENT should be the primary path now
                coordinator = domain_entry_data.get("coordinator")
                if coordinator and hasattr(coordinator, "meraki_client") and coordinator.meraki_client:
                    if hasattr(coordinator.meraki_client, "close"):
                        _LOGGER.info("Closing Meraki API client session (via legacy coordinator attribute) for entry %s.", entry.entry_id)
                        try:
                            await coordinator.meraki_client.close()
                        except Exception as e:
                            _LOGGER.error("Error closing Meraki API client session (via legacy coordinator attribute) for entry %s: %s", entry.entry_id, e, exc_info=True)
                    else:
                        _LOGGER.warning("Meraki API client (via legacy coordinator attribute) for entry %s does not have a 'close' method.", entry.entry_id)
                else:
                    _LOGGER.warning("Meraki API client not found at expected paths for entry %s during unload. Client session may not be closed.", entry.entry_id)

            if not hass.data[DOMAIN]: # If no other entries, remove domain from data
                hass.data.pop(DOMAIN)
            _LOGGER.info("Successfully unloaded Meraki integration and associated data for entry: %s", entry.entry_id)
        else:
            _LOGGER.info("No data found in hass.data[DOMAIN] for entry %s to remove during unload.", entry.entry_id)
    else:
        _LOGGER.error("Failed to unload Meraki platforms for entry: %s", entry.entry_id)

    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    _LOGGER.info("Reloading Meraki integration due to option changes for entry: %s", entry.entry_id)
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
    _LOGGER.info("Finished reloading Meraki integration for entry: %s", entry.entry_id)
