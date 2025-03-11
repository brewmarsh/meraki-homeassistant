# /config/custom_components/meraki_ha/coordinator.py
import logging
from datetime import timedelta

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
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, api_key, org_id) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Meraki Data",
            # Polling interval. Consider using CONFIG_ENTRY_POLL_INTERVAL.
            update_interval=timedelta(seconds=60),
        )
        self.api_key = api_key
        self.org_id = org_id

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the DataUpdateCoordinator base class.
            devices = await get_meraki_devices(self.api_key, self.org_id)
            if devices is None:
                raise UpdateFailed(f"Error communicating with Meraki API")

            for device in devices:
                model = device["model"].strip()
                _LOGGER.debug(f"Raw Model: {repr(model)}")  # added line.
                if model.startswith("MR") or model.startswith("GR"):
                    _LOGGER.debug(f"Fetching clients for {device['serial']}")
                    try:
                        clients = await get_clients(self.api_key, device["networkId"], device["serial"]) #added device serial to get_clients call.
                        device["connected_clients"] = clients #Changed to save the clients object.
                    except Exception as client_err:
                        _LOGGER.warning(f"Failed to fetch clients for {device['serial']}: {client_err}")
                        device["connected_clients"] = [] #changed to empty list.
                else:
                    device["connected_clients"] = [] #changed to empty list.

            return devices
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")