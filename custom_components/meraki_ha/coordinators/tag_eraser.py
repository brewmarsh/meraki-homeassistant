"""Tag Eraser for the meraki_ha integration."""

import logging

from .api_data_fetcher import MerakiApiDataFetcher
from .api.meraki_api.exceptions import (
    MerakiApiConnectionError,
    MerakiApiAuthError,  # This replaces MerakiApiInvalidApiKeyError
)

_LOGGER = logging.getLogger(__name__)


class TagEraser:
    """Class to erase tags for Meraki devices."""

    def __init__(self, api_fetcher: MerakiApiDataFetcher):
        """Initialize the TagEraser.

        Args:
            api_fetcher: An instance of `MerakiApiDataFetcher` used to make
                         API calls for updating device tags.
        """
        self.api_fetcher = api_fetcher

    async def erase_device_tags(self, serial: str) -> None:
        """Erase all tags for a single Meraki device by its serial number.

        This method calls the `async_update_device_tags` method of the
        `MerakiApiDataFetcher`, providing an empty list for the tags,
        which effectively removes all existing tags from the device.

        Args:
            serial: The serial number of the device whose tags are to be erased.

        Raises:
            This method logs errors on exceptions like `MerakiApiConnectionError`,
            `MerakiApiAuthError`, or other general exceptions but does not
            re-raise them. The success of the operation depends on the behavior
            of `api_fetcher.async_update_device_tags`.
        """
        try:
            await self.api_fetcher.meraki_client.async_update_device_tags(serial, [])
            _LOGGER.info(f"Tags erased for device: {serial}")
        except MerakiApiConnectionError as e:
            _LOGGER.error(f"Connection error erasing tags: {e}")
        except MerakiApiAuthError as e:  # Changed from MerakiApiInvalidApiKeyError
            _LOGGER.error(f"Invalid API key erasing tags: {e}")
        except Exception as e:
            _LOGGER.error(f"Error erasing tags for device {serial}: {e}")
