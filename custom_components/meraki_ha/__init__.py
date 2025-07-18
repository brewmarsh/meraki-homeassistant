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
from .api.meraki_api import MerakiAPIClient, MerakiApiError, MerakiApiAuthError, MerakiApiNotFoundError, MerakiApiConnectionError

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    DATA_CLIENT,
)

_LOGGER = logging.getLogger(DOMAIN)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
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
    # Check if coordinators have already been set up for this entry
    if "coordinators" in hass.data[DOMAIN].get(entry.entry_id, {}):
        return True

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: meraki_client_instance,
        "coordinator": main_coordinator,  # Legacy key
        "coordinators": {
            "main": main_coordinator,
        },
    }

    ssid_coordinator = SSIDDeviceCoordinator(
        hass=hass,
        config_entry=entry,
        api_data_fetcher=main_coordinator,
        update_interval=interval,
    )
    await ssid_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id]["coordinators"]["ssid_devices"] = ssid_coordinator

    unique_platforms = list(set(PLATFORMS))

    await hass.config_entries.async_forward_entry_setups(entry, unique_platforms)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

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
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            domain_entry_data = hass.data[DOMAIN].pop(entry.entry_id)
            meraki_client_instance = domain_entry_data.get(DATA_CLIENT)
            if meraki_client_instance and hasattr(meraki_client_instance, "close"):
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
    else:
        _LOGGER.error("Failed to unload Meraki platforms for entry: %s", entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
