"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import aiohttp

from .data.device_coordinator import MerakiDeviceCoordinator
from .data.ssid_coordinator import MerakiSsidCoordinator
from .data.network_coordinator import MerakiNetworkCoordinator

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
        device_name_format: str,  # add device_name_format
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
        self.data = {}  # Initialize self.data
        self.device_coordinator = MerakiDeviceCoordinator(
            hass, session, api_key, org_id, scan_interval
        )
        self.ssid_coordinator = MerakiSsidCoordinator(
            hass, api_key, session, org_id, scan_interval
        )
        self.network_coordinator = MerakiNetworkCoordinator(
            hass,
            session,
            api_key,
            org_id,
            scan_interval,
            device_name_format,  # add device_name_format
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Meraki API endpoint."""
        _LOGGER.debug("Starting Meraki data update")
        try:
            # First, update devices and networks
            device_data = await self.device_coordinator._async_update_data()
            _LOGGER.debug(f"Device data retrieved: {device_data}")
            network_data = await self.network_coordinator._async_update_data()
            _LOGGER.debug(f"Network data retrieved: {network_data}")

            # Populate self.data before ssid_coordinator is called.
            self.data = {
                "devices": device_data.get("devices", []),
                "networks": network_data.get("networks", []),
            }

            # Update ssid_coordinator only if network data is available
            if network_data and network_data.get("networks"):
                _LOGGER.debug("Network data available, proceeding with SSID update")
                self.ssid_coordinator.networks = network_data.get(
                    "networks", []
                )  # provide network data
                ssid_data = await self.ssid_coordinator._async_update_data()
                _LOGGER.debug(f"SSID data retrieved: {ssid_data}")
            else:
                _LOGGER.warning("Network data not available, skipping SSID update")
                ssid_data = {
                    "ssids": []
                }  # Provide empty SSID data if network data is missing

            # Combine data from sub-coordinators
            combined_data = {
                "devices": device_data.get("devices", []),
                "ssids": ssid_data.get("ssids", []),
                "networks": network_data.get("networks", []),
            }
            _LOGGER.debug(f"Meraki data update completed: {combined_data}")
            self.data = combined_data
            _LOGGER.debug(f"Coordinator data: {self.data}")
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
