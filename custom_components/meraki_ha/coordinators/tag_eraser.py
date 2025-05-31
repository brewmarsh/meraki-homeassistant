"""Tag Eraser for the meraki_ha integration."""

import logging

from .api_data_fetcher import MerakiApiDataFetcher
from ..meraki_api.exceptions import (
    MerakiApiConnectionError,
    MerakiApiAuthError,  # This replaces MerakiApiInvalidApiKeyError
)

_LOGGER = logging.getLogger(__name__)


class TagEraser:
    """Class to erase tags for Meraki devices."""

    def __init__(self, api_fetcher: MerakiApiDataFetcher):
        """Initialize the TagEraser."""
        self.api_fetcher = api_fetcher

    async def erase_device_tags(self, serial: str) -> None:
        """Erase tags for a single device."""
        try:
            await self.api_fetcher.async_update_device_tags(serial, [])
            _LOGGER.info(f"Tags erased for device: {serial}")
        except MerakiApiConnectionError as e:
            _LOGGER.error(f"Connection error erasing tags: {e}")
        except MerakiApiAuthError as e:  # Changed from MerakiApiInvalidApiKeyError
            _LOGGER.error(f"Invalid API key erasing tags: {e}")
        except Exception as e:
            _LOGGER.error(f"Error erasing tags for device {serial}: {e}")
