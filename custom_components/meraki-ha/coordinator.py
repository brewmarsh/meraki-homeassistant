"""DataUpdateCoordinator for the meraki_ha integration."""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .meraki_api.devices import get_meraki_devices
from .meraki_api.clients import get_clients
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class MerakiCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Meraki API."""

    def __init__(self, hass: HomeAssistant, api_key: str, org_id: str) -> None:
        """Initialize the Meraki data coordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key.
            org_id: Meraki organization ID.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=timedelta(seconds=60),
        )
        self.api_key = api_key
        self.org_id = org_id

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from Meraki API endpoint.

        Returns:
            A list of dictionaries representing Meraki devices with client data.

        Raises:
            UpdateFailed: If there's an error communicating with the Meraki API.
        """
        try:
            devices: List[Dict[str, Any]] = await get_meraki_devices(self.api_key, self.org_id)
            if devices is None:
                raise UpdateFailed("Error communicating with Meraki API")

            for device in devices:
                model: str = device["model"].strip()
                _LOGGER.debug(f"Raw Model: {repr(model)}")
                if model.startswith("MR") or model.startswith("GR"):
                    _LOGGER.debug(f"Fetching clients for {device['serial']}")
                    try:
                        clients: List[Dict[str, Any]] = await get_clients(self.api_key, device["networkId"], device["serial"])
                        device["connected_clients"] = clients
                    except Exception as client_err:
                        _LOGGER.warning(f"Failed to fetch clients for {device['serial']}: {client_err}")
                        device["connected_clients"] = []
                else:
                    device["connected_clients"] = []

            return devices
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")