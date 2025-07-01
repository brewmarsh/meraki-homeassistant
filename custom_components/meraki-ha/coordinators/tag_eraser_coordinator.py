"""Tag Eraser Coordinator for the meraki-ha integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed # Added
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from typing import Dict, Any # Added

from custom_components.meraki_ha.coordinators.tag_eraser import TagEraser
from custom_components.meraki_ha.meraki_api import MerakiAPIClient
from ..meraki_api.exceptions import MerakiApiError, MerakiApiAuthError, MerakiApiConnectionError # Added

_LOGGER = logging.getLogger(__name__)


class TagEraserCoordinator(DataUpdateCoordinator[Dict[str, Any]]): # Added generic type
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
        # base_url: str, # Removed base_url
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
            name=f"Meraki Tag Eraser ({org_id})", # Incorporate org_id for clarity if multiple orgs
            update_interval=timedelta(seconds=60), # Default, actual updates are on-demand
        )
        self.api_key = api_key # Stored if needed by TagEraser directly, though client is preferred
        self.org_id = org_id

        # TagEraser takes a MerakiAPIClient instance.
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
