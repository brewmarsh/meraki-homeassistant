"""Device Tag Fetch Coordinator for the meraki_ha integration."""

import logging
from typing import List, Optional
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetchCoordinator(DataUpdateCoordinator):
    """
    Coordinator to fetch tags for Meraki devices.

    This coordinator orchestrates the process of fetching device tags from the Meraki API.
    It acts as a middleman between the Home Assistant integration and the `MerakiApiDataFetcher`,
    handling tasks such as error handling.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta,
        main_coordinator,  # Receive the MerakiDataUpdateCoordinator instance
    ) -> None:
        """
        Initialize the DeviceTagFetchCoordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key.
            scan_interval: Time interval for updates.
            main_coordinator: Instance of MerakiDataUpdateCoordinator.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Device Tag Fetch",
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = main_coordinator.org_id
        self.main_coordinator = main_coordinator
        self.api_fetcher = MerakiApiDataFetcher(
            api_key,
            self.org_id,
            None,
            None,
        )  # api fetcher used for fetch only

    async def _async_update_data(self):
        """Fetch all device tags (this might not be efficient for large networks)."""
        # Consider fetching tags on demand instead of all at once
        return {}

    async def async_get_device_tags(self, serial: str) -> Optional[List[str]]:
        """
        Fetch tags for a single device.

        Args:
            serial: Serial number of the device.

        Raises:
            UpdateFailed: If the fetch operation fails.
        """
        try:
            return await self.api_fetcher.async_get_device_tags(serial)
        except Exception as e:
            _LOGGER.error(f"Error fetching tags for device {serial}: {e}")
            raise UpdateFailed(f"Error fetching tags for device {serial}: {e}")
