"""Main coordinator for the Meraki integration."""

import logging
from datetime import timedelta
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.config_entries import ConfigEntry

from ..api import MerakiAPIClient
from .base import BaseMerakiCoordinator
from .device import MerakiDeviceCoordinator
from .network import MerakiNetworkCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataCoordinator(BaseMerakiCoordinator):
    """Main coordinator for all Meraki data.

    This coordinator aggregates data from both device and network coordinators
    to provide a complete view of the Meraki organization.
    """

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
            api_client=api_client,
            name="Meraki",
            update_interval=update_interval,
        )

        self.config_entry = config_entry
        self.device_coordinator = MerakiDeviceCoordinator(
            hass=hass,
            api_client=api_client,
            name="Meraki Devices",
            update_interval=update_interval,
        )
        self.network_coordinator = MerakiNetworkCoordinator(
            hass=hass,
            api_client=api_client,
            name="Meraki Networks",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from all coordinators.

        Returns:
            Combined dictionary containing all Meraki data

        Raises:
            UpdateFailed: If any coordinator update fails
        """
        try:
            device_data = await self.device_coordinator._async_update_data()
            network_data = await self.network_coordinator._async_update_data()

            return {
                **device_data,
                **network_data,
                "org_id": self.api_client.org_id,
            }

        except Exception as err:
            _LOGGER.error("Error updating Meraki data: %s", err)
            raise UpdateFailed(f"Error updating Meraki data: {err}")

    def get_device_by_serial(self, serial: str) -> Dict[str, Any]:
        """Get device data by serial number."""
        return self.device_coordinator.get_device_by_serial(serial)

    def get_network_by_id(self, network_id: str) -> Dict[str, Any]:
        """Get network data by network ID."""
        return self.network_coordinator.get_network_by_id(network_id)
