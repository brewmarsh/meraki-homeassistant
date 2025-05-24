"""Tag Eraser Coordinator for the meraki_ha integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .tag_eraser import TagEraser
from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class TagEraserCoordinator(DataUpdateCoordinator):
    """
    Coordinator to erase tags for Meraki devices.

    This coordinator orchestrates the process of erasing device tags in the Meraki API.
    It acts as a middleman between the Home Assistant integration and the `TagEraser`,
    handling tasks such as error handling and triggering updates.

    Architecture:
    - This coordinator uses the `TagEraser` to make the raw API calls.
    - It separates the API interaction logic from the Home Assistant integration logic.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        base_url: str,
    ) -> None:
        """
        Initialize the TagEraserCoordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key.
            org_id: Meraki Organization ID.
            base_url: Base URL of the Meraki API.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Tag Eraser",
            update_interval=timedelta(seconds=60),  # Default interval, can be adjusted
        )
        self.api_key = api_key
        self.org_id = org_id
        self.base_url = base_url
        self.api_fetcher = MerakiApiDataFetcher(
            api_key, org_id, None, None
        )  # api fetcher used for erase only
        self.tag_eraser = TagEraser(self.api_fetcher)

    async def async_erase_device_tags(self, serial: str) -> None:
        """
        Erase tags for a single device.

        Args:
            serial: Serial number of the device.

        Raises:
            UpdateFailed: If the erase operation fails.
        """
        try:
            await self.tag_eraser.erase_device_tags(serial)
        except Exception as e:
            _LOGGER.error(f"Error erasing tags for device {serial}: {e}")
            raise UpdateFailed(f"Error erasing tags for device {serial}: {e}")
