"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
import aiohttp

from .data.device_coordinator import MerakiDeviceCoordinator
from .data.ssid_coordinator import MerakiSsidCoordinator
from .data.network_coordinator import MerakiNetworkCoordinator
from .meraki_api.devices import (
    get_device_tags,
    update_device_tags,
)  #  Import get_device_tags and update_device_tags
from .const import (
    ERASE_TAGS_WARNING,
)  #  Import constants for tag erasing

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Meraki API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,  #  add device_name_format
        erase_tags: bool,  #  New: Option to erase tags
        relaxed_tag_match: bool,  # New: Option for relaxed tag matching
    ) -> None:
        """Initialize the Meraki data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=scan_interval,
        )
        self.session = session
        self.api_key = api_key
        self.org_id = org_id
        self.data = {}  #  Initialize self.data
        self.device_coordinator = MerakiDeviceCoordinator(
            hass, session, api_key, org_id, scan_interval, device_name_format
        )
        self.ssid_coordinator = MerakiSsidCoordinator(
            hass, api_key, session, org_id, scan_interval, device_name_format
        )
        self.network_coordinator = MerakiNetworkCoordinator(
            hass,
            session,
            api_key,
            org_id,
            scan_interval,
            device_name_format,
        )
        self.erase_tags = erase_tags  #  Store the erase_tags option
        self.relaxed_tag_match = (
            relaxed_tag_match  # Store the relaxed tag matching option
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Meraki API endpoint."""
        _LOGGER.debug("Starting Meraki data update")
        try:
            #  First, update devices and networks
            device_data = await self.device_coordinator._async_update_data()
            _LOGGER.debug(f"Device data retrieved: {device_data}")
            network_data = await self.network_coordinator._async_update_data()
            _LOGGER.debug(f"Network data retrieved: {network_data}")

            #  Fetch device tags and determine SSID status
            devices: List[Dict[str, Any]] = device_data.get("devices", [])
            device_tags: Dict[str, List[str]] = {}  #  Store device tags
            for device in devices:
                serial = device["serial"]
                tags = await get_device_tags(
                    self.session, self.api_key, serial
                )  #  Fetch tags
                device_tags[serial] = tags if tags else []  #  Store tags
                device["tags"] = device_tags[
                    serial
                ]  #  Attach tags to device data for tag erasing

            if self.ssid_coordinator and self.ssid_coordinator.data:  # add check here.
                ssids: List[Dict[str, Any]] = self.ssid_coordinator.data.get(
                    "ssids", []
                )
            else:
                _LOGGER.warning("ssid_coordinator data is not available")
                ssids: List[Dict[str, Any]] = []

            for ssid in ssids:
                ssid_name = ssid["name"]
                ssid["enabled"] = False  #  Default to disabled

                for device in devices:
                    device_tags_list = device_tags.get(device["serial"], [])
                    if self.relaxed_tag_match:
                        # Relaxed matching: Check if any tag contains the ssid name
                        if any(ssid_name in tag for tag in device_tags_list):
                            ssid["enabled"] = True
                            break  # SSID enabled if found on any device
                    else:
                        # Strict matching: Check for exact tag match
                        if f"ssid_{ssid_name}_enabled" in device_tags_list:
                            ssid["enabled"] = True
                            break  # SSID enabled if found on any device

            #  Populate self.data
            self.data = {
                "devices": devices,
                "networks": network_data.get("networks", []),
                "ssids": ssids,
            }

            #  Update ssid_coordinator only if network data is available
            if network_data and network_data.get("networks"):
                _LOGGER.debug("Network data available, proceeding with SSID update")
                self.ssid_coordinator.networks = network_data.get(
                    "networks", []
                )  #  provide network data
                ssid_data = await self.ssid_coordinator._async_update_data()
                _LOGGER.debug(f"SSID data retrieved: {ssid_data}")
            else:
                _LOGGER.warning("Network data not available, skipping SSID update")
                ssid_data = {
                    "ssids": []
                }  #  Provide empty SSID data if network data is missing

            #  Combine data from sub-coordinators
            combined_data = {
                "devices": devices,
                "ssids": ssids,
                "networks": network_data.get("networks", []),
            }
            _LOGGER.debug(f"Meraki data update completed: {combined_data}")
            self.data = combined_data
            _LOGGER.debug(f"Coordinator data: {self.data}")

            #  Handle tag erasing (if enabled)
            if self.erase_tags:
                _LOGGER.warning(ERASE_TAGS_WARNING)
                for device in devices:
                    await self.async_erase_device_tags(device["serial"])

            return combined_data
        except UpdateFailed as update_error:
            _LOGGER.error(f"Update failed: {update_error}")
            raise update_error
        except Exception as error:
            _LOGGER.exception(f"Unexpected error: {error}")
            raise UpdateFailed(f"Unexpected error: {error}")

    async def _async_shutdown(self):
        """Close the aiohttp session on shutdown."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of a config entry."""
        try:
            await super().async_config_entry_first_refresh()
        finally:
            self.hass.bus.async_listen_once("homeassistant_stop", self._async_shutdown)

    async def async_erase_device_tags(self, serial: str) -> None:
        """Erase tags for a single device."""
        from .meraki_api.devices import (
            erase_device_tags,
        )  #  Import here to avoid circular import

        try:
            await erase_device_tags(self.session, self.api_key, serial)
            _LOGGER.info(f"Tags erased for device: {serial}")
        except Exception as e:
            _LOGGER.error(f"Error erasing tags for device {serial}: {e}")
            #  We do not raise an exception here.
            #  Tag erasing should not block the integration from working.

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Update tags for a single device."""
        try:
            await update_device_tags(self.session, self.api_key, serial, tags)
            _LOGGER.info(f"Tags updated for device: {serial} with tags: {tags}")
            # Optionally, you might want to request a data refresh here to update the state in Home Assistant
            await self.async_request_refresh()
        except Exception as e:
            _LOGGER.error(f"Error updating tags for device {serial}: {e}")
            raise UpdateFailed(f"Error updating tags for device {serial}: {e}")
