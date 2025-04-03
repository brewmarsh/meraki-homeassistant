"""Device Tag Fetch Coordinator for the meraki_ha integration."""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .device_tag_fetcher import DeviceTagFetcher
from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetchCoordinator(DataUpdateCoordinator):
    """
    Coordinator to fetch tags for Meraki devices.

    This coordinator orchestrates the process of fetching device tags from the Meraki API.
    It acts as a middleman between the Home Assistant integration and the `DeviceTagFetcher`,
    handling tasks such as error handling.

    Architecture:
    - This coordinator uses the `DeviceTagFetcher` to make the raw API calls.
    - It separates the API interaction logic from the Home Assistant integration logic.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta,
    ) -> None:
        """
        Initialize the DeviceTagFetchCoordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key.
            scan_interval: Time interval for updates.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Device Tag Fetch",
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.api_fetcher = MerakiApiDataFetcher(
            api_key, None, None, None
        )  # api fetcher used for fetch only
        self.device_tag_fetcher = DeviceTagFetcher(self.api_fetcher)

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """
        Fetch tags for a single device.

        Args:
            serial: Serial number of the device.

        Raises:
            UpdateFailed: If the fetch operation fails.
        """
        try:
            return await self.device_tag_fetcher.get_device_tags(serial)
        except Exception as e:
            _LOGGER.error(f"Error fetching tags for device {serial}: {e}")
            raise UpdateFailed(f"Error fetching tags for device {serial}: {e}")
