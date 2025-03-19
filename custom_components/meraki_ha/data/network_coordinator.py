"""Network data coordinator for the meraki_ha integration."""

import logging
from typing import Any, Dict

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import UpdateFailed

from .base_coordinator import MerakiBaseCoordinator
from ..const import DOMAIN
import aiohttp

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkCoordinator(MerakiBaseCoordinator):
    """Coordinator to fetch network data from Meraki API."""

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

            _LOGGER.debug(f"Making API call to get networks: {url}")  # added log
            async with self.session.get(url, headers=headers) as resp:
                _LOGGER.debug(
                    f"API response status for networks: {resp.status}"
                )  # added log
                if resp.status != 200:
                    raise UpdateFailed("Failed to retrieve Meraki networks.")
                networks = await resp.json()
                _LOGGER.debug(f"Networks retrieved: {networks}")  # added log

            if not networks or len(networks) == 0:
                _LOGGER.warning("Failed to retrieve Meraki networks.")
                return {}

            for network in networks:
                network_id = network["id"]
                network_name = network["name"]

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, network_id)},
                    manufacturer="Cisco Meraki",
                    name=network_name,
                    model="Network",
                )
                _LOGGER.debug(
                    f"Created Meraki Network Device: {network_name} ({network_id})"
                )

            return {"networks": networks}

        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error updating network data: {e}")
            raise UpdateFailed(f"Error updating network data: {e}")
        except Exception as e:
            _LOGGER.error(f"Error updating network data: {e}")
            raise UpdateFailed(f"Error updating network data: {e}")
