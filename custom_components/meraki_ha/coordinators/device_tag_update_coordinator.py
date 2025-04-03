"""Device Tag Update Coordinator for the meraki_ha integration."""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed
from datetime import timedelta

from .device_tag_updater import DeviceTagUpdater
from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class DeviceTagUpdateCoordinator(DataUpdateCoordinator):
    """
    Coordinator to update tags for Meraki devices.

    This coordinator orchestrates the process of updating device tags in the Meraki API.
    It acts as a middleman between the Home Assistant integration and the `DeviceTagUpdater`,
    handling tasks such as error handling, data validation, and triggering updates to the
    Home Assistant state.

    Architecture:
    - This coordinator uses the `DeviceTagUpdater` to make the raw API calls.
    - It separates the API interaction logic from the Home Assistant integration logic.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta,
    ) -> None:
        """
        Initialize the DeviceTagUpdateCoordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key.
            scan_interval: Time interval for updates.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Device Tag Update",
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.api_fetcher = MerakiApiDataFetcher(
            api_key, None, None, None
        )  # api fetcher used for update only
        self.device_tag_updater = DeviceTagUpdater(self.api_fetcher)

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """
        Update tags for a single device.

        Args:
            serial: Serial number of the device.
            tags: List of tags to set for the device.

        Raises:
            UpdateFailed: If the update fails.
            ConfigEntryAuthFailed: If the API key is invalid.
        """
        try:
            await self.device_tag_updater.update_device_tags(serial, tags)
            await self.async_request_refresh()
        except UpdateFailed as e:
            raise e
        except ConfigEntryAuthFailed as e:
            raise e
        except Exception as e:
            _LOGGER.error(f"Error updating tags for device {serial}: {e}")
            raise UpdateFailed(f"Error updating tags for device {serial}: {e}")
