"""Network data coordinator for the meraki_ha integration."""

import logging
from typing import Any, Dict
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ..const import DOMAIN
import aiohttp

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch network data from Meraki API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,  # Expecting timedelta
        device_name_format: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Networks",
            update_interval=scan_interval,  # Using provided timedelta directly
        )
        self.session = session
        self.api_key = api_key
        self.org_id = org_id
        self.device_name_format = device_name_format

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch and process network data from Meraki API."""
        device_registry = dr.async_get(self.hass)
        try:
            api_key = self.api_key
            org_id = self.org_id

            headers = {
                "X-Cisco-Meraki-API-Key": api_key,
                "Content-Type": "application/json",
            }
            url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"

            _LOGGER.debug(f"Making API call to get networks: {url}")
            async with self.session.get(url, headers=headers) as resp:
                _LOGGER.debug(f"API response status for networks: {resp.status}")
                if resp.status != 200:
                    raise UpdateFailed("Failed to retrieve Meraki networks.")
                networks = await resp.json()
                _LOGGER.debug(f"Networks retrieved: {networks}")

            if not networks or len(networks) == 0:
                _LOGGER.warning("Failed to retrieve Meraki networks.")
                return {}

            for network in networks:
                network_id = network["id"]
                network_name = network["name"]

                _LOGGER.debug(
                    f"Device name format: {self.device_name_format}"
                )  # Added log
                if self.device_name_format == "prefix":
                    device_name = f"[Network] {network_name}"
                elif self.device_name_format == "suffix":
                    device_name = f"{network_name} [Network]"
                else:
                    device_name = network_name
                _LOGGER.debug(
                    f"Device name before registry: {device_name}"
                )  # Added log

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, network_id)},
                    manufacturer="Cisco Meraki",
                    name=device_name,
                    model="Network",
                )
                _LOGGER.debug(
                    f"Created Meraki Network Device: {device_name} ({network_id})"
                )

            return {"networks": networks}

        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error updating network data: {e}")
            raise UpdateFailed(f"Error updating network data: {e}")
        except Exception as e:
            _LOGGER.error(f"Error updating network data: {e}")
            raise UpdateFailed(f"Error updating network data: {e}")
