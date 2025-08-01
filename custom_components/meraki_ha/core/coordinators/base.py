"""Base coordinator for the Meraki integration."""

from datetime import timedelta
import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..api import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class BaseMerakiCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Base coordinator for Meraki data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        name: str,
        update_interval: timedelta,
        options: Dict[str, Any],
    ) -> None:
        """Initialize the coordinator.

        Args:
            hass: Home Assistant instance
            api_client: Initialized Meraki API client
            name: Name of the coordinator for logging
            update_interval: How often to update the data
            options: Config entry options
        """
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=name,
            update_interval=update_interval,
        )
        self.api_client = api_client
        self.options = options

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from API endpoint.

        This method should be implemented by child classes to do the actual data
        fetching and processing.

        Returns:
            Dict containing the fetched and processed data

        Raises:
            UpdateFailed: If update fails
        """
        raise NotImplementedError("Data update method not implemented")
