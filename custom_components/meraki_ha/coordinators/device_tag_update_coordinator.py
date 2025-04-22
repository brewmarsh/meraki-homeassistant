"""Device Tag Update Coordinator for the meraki_ha integration."""

import logging
from typing import List, Dict  # Import List and Dict
from datetime import timedelta
from homeassistant.util import dt as dt_util
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed

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
        org_id: str,  # Add org_id
        base_url: str,  # Add base_url
        meraki_coordinator,  # Changed from MerakiSSIDDataUpdateCoordinator
    ) -> None:
        """Initialize the DeviceTagUpdateCoordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Device Tag Updates",  # Provide a specific name
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = org_id  # Store org_id
        self.base_url = base_url  # Store base_url
        self.meraki_coordinator = (
            meraki_coordinator  # Store the MerakiDataUpdateCoordinator
        )
        self.api_fetcher = MerakiApiDataFetcher(
            api_key, org_id, None, None  # Pass None for networks and ssid coordinators
        )  # api fetcher used for update only
        self.data: Dict[str, List[str]] = {}
        self.update_interval = timedelta(seconds=scan_interval.total_seconds() * 2)
        self._next_update_time = dt_util.now()

    async def _async_update_data(self) -> Dict[str, List[str]]:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to shrink its size after
        multiple updates.
        """
        # We don't need to fetch data in this coordinator, only update tags
        return {}  # Return an empty dictionary

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
            await self.api_fetcher.async_update_device_tags(serial, tags)
            await self.async_request_refresh()
        except UpdateFailed as e:
            raise e
        except ConfigEntryAuthFailed as e:
            raise e
        except Exception as e:
            _LOGGER.error(f"Error updating tags for device {serial}: {e}")
            raise UpdateFailed(f"Error updating tags for device {serial}: {e}")
