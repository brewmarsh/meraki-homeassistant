"""Tag Eraser Coordinator for the meraki_ha integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from typing import Dict, Any

from .tag_eraser import TagEraser
from ..api.meraki_api import MerakiAPIClient
from ..api.meraki_api.exceptions import MerakiApiError, MerakiApiAuthError, MerakiApiConnectionError

_LOGGER = logging.getLogger(__name__)


class TagEraserCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
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
    ) -> None:
        """
        Initialize the TagEraserCoordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key, used to initialize a dedicated MerakiAPIClient.
            org_id: Meraki Organization ID, used to initialize a dedicated MerakiAPIClient and for coordinator naming.
        """
        super().__init__(
            hass,
            _LOGGER,
            name=f"Meraki Tag Eraser ({org_id})",
            update_interval=timedelta(seconds=60),
        )
        self.api_key = api_key
        self.org_id = org_id

        from .api_data_fetcher import MerakiApiDataFetcher
        self.meraki_client_for_eraser = MerakiAPIClient(api_key=api_key, org_id=org_id)
        self.tag_eraser = TagEraser(MerakiApiDataFetcher(self.meraki_client_for_eraser))

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
        except MerakiApiAuthError as e:
            _LOGGER.error("Authentication error while erasing tags for device %s: %s", serial, e)
            raise ConfigEntryAuthFailed(f"Authentication error erasing tags for device {serial}: {e}") from e
        except MerakiApiConnectionError as e:
            _LOGGER.error("Connection error while erasing tags for device %s: %s", serial, e)
            raise UpdateFailed(f"Connection error erasing tags for device {serial}: {e}") from e
        except MerakiApiError as e:
            _LOGGER.error("Meraki API error while erasing tags for device %s: %s", serial, e)
            raise UpdateFailed(f"Meraki API error erasing tags for device {serial}: {e}") from e
        except Exception as e:
            _LOGGER.exception(f"Unexpected error erasing tags for device {serial}: {e}")
            raise UpdateFailed(f"Unexpected error erasing tags for device {serial}: {e}") from e

    async def _async_update_data(self) -> Dict[str, Any]:
        """Placeholder for DataUpdateCoordinator. Tag erasing is on-demand."""
        _LOGGER.debug("TagEraserCoordinator._async_update_data called (placeholder).")
        return {}
