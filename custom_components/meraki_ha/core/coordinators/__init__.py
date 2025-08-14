"""Main coordinator for the Meraki integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry

from ..api import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiDataCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Main coordinator for all Meraki data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api_client: MerakiAPIClient,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator.

        Args:
            hass: Home Assistant instance
            config_entry: Config entry containing integration configuration
            api_client: Initialized Meraki API client
            update_interval: How often to update the data
        """
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name="Meraki",
            update_interval=update_interval,
        )
        self.api_client = api_client
        self.config_entry = config_entry

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch all data from the Meraki API.

        Returns:
            Combined dictionary containing all Meraki data

        Raises:
            UpdateFailed: If the update fails
        """
        try:
            return await self.api_client.get_all_data()
        except Exception as err:
            _LOGGER.error("Error updating Meraki data: %s", err)
            raise UpdateFailed(f"Error updating Meraki data: {err}")

    def get_device_by_serial(self, serial: str) -> Optional[Dict[str, Any]]:
        """Get device data by serial number."""
        if self.data:
            for device in self.data.get("devices", []):
                if device.get("serial") == serial:
                    return device
        return None

    def get_network_by_id(self, network_id: str) -> Optional[Dict[str, Any]]:
        """Get network data by network ID."""
        if self.data:
            for network in self.data.get("networks", []):
                if network.get("id") == network_id:
                    return network
        return None
