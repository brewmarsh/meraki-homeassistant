"""Provides the DeviceTagUpdater for the Meraki Home Assistant integration.

This module defines `DeviceTagUpdater`, a class responsible for the actual
API calls to update (replace) tags for Meraki devices. It uses an instance of
`MerakiApiDataFetcher` to perform these calls.
"""

import logging
from typing import List

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)


class DeviceTagUpdater:
    """Updates tags for Meraki devices by making API calls.

    This class handles the specifics of requesting a device tag update from
    the Meraki API. It uses an injected `MerakiApiDataFetcher` instance
    to perform the underlying HTTP PUT request.

    Attributes:
        api_fetcher (MerakiApiDataFetcher): An instance of `MerakiApiDataFetcher`
            used to make calls to the Meraki API.
    """

    def __init__(self, api_fetcher: MerakiApiDataFetcher) -> None:
        """Initializes the DeviceTagUpdater.

        Args:
            api_fetcher (MerakiApiDataFetcher): An instance of
                `MerakiApiDataFetcher` that will be used to perform the
                actual API calls.
        """
        self.api_fetcher = api_fetcher

    async def update_device_tags(self, serial: str, tags: List[str]) -> bool:
        """Updates the tags for a specified Meraki device.

        This method calls the `async_update_device_tags` method of the
        `api_fetcher` (which is currently a placeholder in `MerakiApiDataFetcher`
        and needs full implementation there to call the actual Meraki API endpoint
        like PUT `/devices/{serial}/tags`). It translates known API exceptions
        into Home Assistant specific exceptions.

        Args:
            serial (str): The serial number of the Meraki device.
            tags (List[str]): The complete list of tags to apply to the device.
                This will overwrite any existing tags. An empty list will remove
                all tags.

        Returns:
            bool: True if the tag update was successfully initiated by the
                  `api_fetcher` (assuming `async_update_device_tags` in
                  `api_fetcher` returns something to indicate success or
                  doesn't raise an exception on success). The current placeholder
                  in `api_fetcher` doesn't return a value, so success here is
                  inferred by lack of exceptions.

        Raises:
            UpdateFailed: If a connection error or other general error occurs
                during the API call.
            ConfigEntryAuthFailed: If the API key is invalid, resulting in an
                authentication error from the API.
        """
        _LOGGER.debug(
            "Attempting to update tags for device serial: %s with tags: %s",
            serial,
            tags,
        )
        try:
            # Delegate the API call to the MerakiApiDataFetcher instance.
            # IMPORTANT: MerakiApiDataFetcher.async_update_device_tags is currently a placeholder.
            # For this to function correctly, that method must be implemented to make a
            # PUT request to the `/devices/{serial}/tags` Meraki API endpoint
            # with the `tags` list as the JSON payload.
            await self.api_fetcher.async_update_device_tags(serial, tags)

            # Assuming success if no exception is raised by the fetcher.
            # The placeholder api_fetcher.async_update_device_tags returns None.
            _LOGGER.info("Successfully initiated tag update for device: %s with tags: %s", serial, tags)
            return True
        except MerakiApiConnectionError as e:
            # Handle specific connection errors.
            _LOGGER.error(
                "Connection error while updating tags for device %s: %s", serial, e
            )
            raise UpdateFailed(f"Failed to connect to Meraki API: {e}") from e
        except MerakiApiInvalidApiKeyError as e:
            # Handle invalid API key errors.
            _LOGGER.error(
                "Invalid API key while updating tags for device %s: %s", serial, e
            )
            raise ConfigEntryAuthFailed(f"Invalid Meraki API key: {e}") from e
        except Exception as e:
            # Catch any other unexpected exceptions from the API call.
            _LOGGER.exception(
                "Unexpected error updating tags for device %s: %s", serial, e
            )
            # Includes aiohttp.ClientResponseError if not caught by specific handlers above.
            raise UpdateFailed(
                f"Error updating tags for device {serial}: {e}"
            ) from e
