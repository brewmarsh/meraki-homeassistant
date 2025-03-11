"""Meraki HA integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, PLATFORMS, DATA_CLIENT, DATA_COORDINATOR
from .meraki_api import get_meraki_devices, get_meraki_device_appliance_uplinks, get_meraki_device_wireless_radio_settings, get_meraki_network_wireless_rf_profile, MerakiApiError

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""

    api_key = entry.options["meraki_api_key"]
    org_id = entry.options["meraki_org_id"]

    async def async_update_data():
        """Fetch data from Meraki API."""
        try:
            devices = await get_meraki_devices(api_key, org_id)
            for device in devices:
                if device["model"].startswith("MX"):
                    try:
                        uplink_settings = await get_meraki_device_appliance_uplinks(api_key, org_id, device["serial"])
                        device["uplinks"] = uplink_settings["interfaces"]
                    except MerakiApiError as err:
                        _LOGGER.warning(f"Failed to fetch uplink settings for {device['serial']}: {err}")
                        device["uplinks"] = {}
                elif device["model"].startswith("MR"):
                    try:
                        radio_settings = await get_meraki_device_wireless_radio_settings(api_key, org_id, device["serial"])
                        _LOGGER.debug(f"Radio settings for {device['serial']}: {radio_settings}")
                        if radio_settings and radio_settings.get("rfProfileId"):
                            profile_settings = await get_meraki_network_wireless_rf_profile(api_key, device["networkId"], radio_settings["rfProfileId"])
                            _LOGGER.debug(f"RF Profile settings for {device['serial']}: {profile_settings}")
                            device["radio_settings"] = profile_settings
                        else:
                            device["radio_settings"] = radio_settings
                    except MerakiApiError as err:
                        _LOGGER.warning(f"Failed to fetch radio settings for {device['serial']}: {err}")
                        device["radio_settings"] = {}
                else:
                    device["radio_settings"] = {}
            return devices
        except MerakiApiError as err:
            _LOGGER.error("Failed to update Meraki data")
            raise UpdateFailed(f"Error communicating with Meraki API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: {"api_key": api_key, "org_id": org_id},
        DATA_COORDINATOR: coordinator,
    }

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok