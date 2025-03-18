"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import aiohttp

_LOGGER = logging.getLogger(__name__)


class MerakiSsidCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch SSIDs from Meraki API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        session: aiohttp.ClientSession,
        org_id: str,
        scan_interval: timedelta,
    ) -> None:
        """Initialize the SSID coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki SSIDs",
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.session = session
        self.org_id = org_id
        self.networks = []  # Add networks as an instance variable

    async def _async_get_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Fetch SSIDs for a specific network."""
        url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids"
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"Fetching SSIDs for network ID: {network_id}")
        try:
            async with self.session.get(url, headers=headers) as response:
                _LOGGER.debug(f"Meraki API Response Status: {response.status}")
                response.raise_for_status()
                json_data = await response.json()
                _LOGGER.debug(f"Meraki API Response JSON: {json_data}")
                return json_data
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Error fetching SSIDs: {err}")
            raise UpdateFailed(f"Error fetching SSIDs: {err}")
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching SSIDs: {err}")
            raise UpdateFailed(f"Unexpected error fetching SSIDs: {err}")

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch all SSIDs."""
        _LOGGER.debug(f"Networks in ssid_coordinator: {self.networks}")

        if not self.networks:
            _LOGGER.error("Networks data is None. Cannot fetch SSIDs.")
            raise UpdateFailed("Networks data not available.")

        ssids = []
        try:
            for network in self.networks:
                if "wireless" in network.get("productTypes", []):
                    network_id = network["id"]
                    _LOGGER.debug(f"Processing network: {network_id}")
                    network_ssids = await self._async_get_ssids(network_id)
                    if network_ssids:
                        ssids.extend(network_ssids)
            return {"ssids": ssids}
        except UpdateFailed as err:
            _LOGGER.error(f"Update failed: {err}")
            raise err
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching SSIDs: {err}")
            raise UpdateFailed(f"Unexpected error fetching SSIDs: {err}")
