"""Provides the DeviceTagFetchCoordinator for the Meraki Home Assistant integration.

This module defines `DeviceTagFetchCoordinator`, a Home Assistant
`DataUpdateCoordinator` that, despite its name and structure, primarily
acts as a direct pass-through to `DeviceTagFetcher` for retrieving device tags.
It doesn't currently implement the typical periodic update pattern of a
DataUpdateCoordinator via `_async_update_data`.
"""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .device_tag_fetcher import DeviceTagFetcher
from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetchCoordinator(DataUpdateCoordinator[List[str]]):
    """Coordinates the fetching of tags for Meraki devices.

    Although structured as a `DataUpdateCoordinator`, this class currently
    functions more as a service to directly fetch device tags on demand via
    the `async_get_device_tags` method. It does not implement the
    `_async_update_data` method, so it won't perform periodic background
    updates of tag data for all devices.

    It utilizes `DeviceTagFetcher` for the actual API interaction.

    Attributes:
        api_key (str): The Meraki API key.
        api_fetcher (MerakiApiDataFetcher): An instance of `MerakiApiDataFetcher`
            used by the `DeviceTagFetcher`.
        device_tag_fetcher (DeviceTagFetcher): An instance of `DeviceTagFetcher`
            that handles the API calls to get device tags.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta,
    ) -> None:
        """Initializes the DeviceTagFetchCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): The Meraki API key for authentication.
            scan_interval (timedelta): The desired time interval for updates.
                Note: This interval is passed to the parent `DataUpdateCoordinator`
                but is not actively used by this coordinator for periodic updates
                as `_async_update_data` is not implemented.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Device Tag Fetch", # Name for logging and diagnostics
            update_interval=scan_interval,
        )
        self.api_key = api_key
        # Initialize MerakiApiDataFetcher; it's used by DeviceTagFetcher.
        # Passing None for unused coordinator dependencies of MerakiApiDataFetcher.
        self.api_fetcher = MerakiApiDataFetcher(self.api_key, None, None, None)
        self.device_tag_fetcher = DeviceTagFetcher(self.api_fetcher)

    # This coordinator currently does not implement _async_update_data,
    # so it won't perform scheduled background updates for all device tags.
    # async def _async_update_data(self) -> List[str]:
    #     """
    #     (Not Implemented) Fetches tags for all relevant devices.
    #     If this were to be implemented, it would typically iterate through known
    #     devices and fetch their tags, then store them in self.data.
    #     """
    #     _LOGGER.debug("DeviceTagFetchCoordinator._async_update_data called, but not implemented for periodic updates.")
    #     # Example: return await self.device_tag_fetcher.get_all_device_tags(list_of_serials)
    #     return [] # Or appropriate data structure

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """Fetches tags for a single specified Meraki device.

        This method directly calls the `DeviceTagFetcher` to retrieve tags
        for the given device serial number.

        Args:
            serial (str): The serial number of the Meraki device for which
                to fetch tags.

        Returns:
            List[str]: A list of tags associated with the device. Returns an
                empty list if no tags are found or in case of certain errors
                handled by `DeviceTagFetcher`.

        Raises:
            UpdateFailed: If an unrecoverable error occurs during the tag
                fetching process (e.g., unexpected API error not handled
                by `DeviceTagFetcher` returning a default value).
        """
        _LOGGER.debug("Fetching tags for device serial: %s", serial)
        try:
            # Delegate the actual fetching to the DeviceTagFetcher instance.
            tags = await self.device_tag_fetcher.get_device_tags(serial)
            _LOGGER.debug("Successfully fetched tags for device %s: %s", serial, tags)
            return tags
        except Exception as e:
            # Catch any exception from the fetcher and wrap it in UpdateFailed.
            _LOGGER.error("Error fetching tags for device %s: %s", serial, e)
            raise UpdateFailed(
                f"Error fetching tags for device {serial}: {e}"
            ) from e
