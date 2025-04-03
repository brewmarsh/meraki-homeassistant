"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers import device_registry as dr
from ..const import DOMAIN
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
        scan_interval: timedelta,  # Expecting timedelta
        device_name_format: str,  # added variable
    ) -> None:
        """Initialize the SSID coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki SSIDs",
            update_interval=scan_interval,  # Using provided timedelta directly
        )
        self.api_key = api_key
        self.session = session
        self.org_id = org_id
        self.networks = []  # Add networks as an instance variable
        self.device_name_format = device_name_format  # added variable
        self.data: Dict[str, Any] = {}  # Initialize data

    async def _async_get_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Fetch SSIDs for a specific network."""
        url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids"
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"Fetching SSIDs for network ID: {network_id}")
        try:
            _LOGGER.debug(f"Making API call to: {url}")  # added log
            async with self.session.get(url, headers=headers) as response:
                _LOGGER.debug(f"Meraki API Response Status: {response.status}")
                if response.status != 200:
                    _LOGGER.error(
                        f"API returned non-200 status: {response.status} for network {network_id}"
                    )  # added log
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
            device_registry = dr.async_get(self.hass)
            for network in self.networks:
                if "wireless" in network.get("productTypes", []):
                    network_id = network["id"]
                    network_name = network["name"]
                    _LOGGER.debug(
                        f"Processing network: {network_id} ({network_name})"
                    )  # Log network name
                    network_ssids = await self._async_get_ssids(network_id)
                    if network_ssids:
                        for ssid in network_ssids:
                            ssid_number = ssid["number"]
                            ssid_name = ssid["name"]
                            ssid_enabled = ssid.get("enabled", True)

                            _LOGGER.debug(
                                f"Device name format: {self.device_name_format}"
                            )  # added log

                            if self.device_name_format == "prefix":
                                device_name = f"[SSID] {ssid_name}"
                            elif self.device_name_format == "suffix":
                                device_name = f"{ssid_name} [SSID]"
                            elif (
                                self.device_name_format == "network_prefix"
                            ):  # New device name format
                                device_name = f"{network_name} - {ssid_name} [SSID]"
                            else:
                                device_name = ssid_name

                            _LOGGER.debug(
                                f"Device name before registry: {device_name}"
                            )  # added log

                            device = device_registry.async_get_or_create(
                                config_entry_id=self.config_entry.entry_id,
                                identifiers={(DOMAIN, f"{network_id}_{ssid_number}")},
                                manufacturer="Cisco Meraki",
                                name=device_name,
                                model="SSID",
                                via_device=(
                                    DOMAIN,
                                    network_id,
                                ),  # link to network device
                            )
                            ssids.append(
                                {
                                    **ssid,
                                    "network_id": network_id,
                                    "device_id": device.id,
                                    "enabled": ssid_enabled,
                                }
                            )  # Store ssid_enabled

                            _LOGGER.debug(
                                f"Created Meraki SSID Device: {device_name} ({network_id}_{ssid_number}) with enabled={ssid_enabled}"
                            )
            self.data = {"ssids": ssids}
            _LOGGER.debug(f"Total SSIDs fetched: {len(ssids)}")  # added log
            return self.data
        except UpdateFailed as err:
            _LOGGER.error(f"Update failed: {err}")
            raise err
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching SSIDs: {err}")
            raise UpdateFailed(f"Unexpected error fetching SSIDs: {err}")
