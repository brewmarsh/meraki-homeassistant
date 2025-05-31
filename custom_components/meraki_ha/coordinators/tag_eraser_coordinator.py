"""Tag Eraser Coordinator for the meraki_ha integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from custom_components.meraki_ha.coordinators.tag_eraser import TagEraser

# MerakiApiDataFetcher is not directly used by TagEraserCoordinator after recent refactors.
# TagEraser itself will use MerakiAPIClient.
# from .api_data_fetcher import MerakiApiDataFetcher # Assuming this was
# for the client
# For direct client usage
from custom_components.meraki_ha.meraki_api import MerakiAPIClient

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
            # Default interval, can be adjusted
            update_interval=timedelta(seconds=60),
        )
        self.api_key = api_key
        self.org_id = org_id
        # base_url is likely not needed if MerakiAPIClient handles it.
        # self.base_url = base_url

        # TagEraser should take a MerakiAPIClient instance.
        # The MerakiApiDataFetcher is for fetching bulk data, not direct operations like tag erasing.
        # We need to instantiate a MerakiAPIClient here for the TagEraser.
        # This assumes TagEraser's __init__ is updated to accept MerakiAPIClient.
        # If TagEraser still expects MerakiApiDataFetcher, this needs more adjustment.
        # For now, let's assume TagEraser is refactored or we provide a client.
        # A dedicated client for tag erasing ensures separation of concerns.
        self.meraki_client_for_eraser = MerakiAPIClient(api_key=api_key, org_id=org_id)
        self.tag_eraser = TagEraser(self.meraki_client_for_eraser)  # Pass the client

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
