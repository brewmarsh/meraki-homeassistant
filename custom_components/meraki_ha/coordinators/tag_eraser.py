"""Provides the TagEraser for the Meraki Home Assistant integration.

This module defines `TagEraser`, a class responsible for making API calls
to remove all tags from a specific Meraki device. It utilizes an instance
of `MerakiApiDataFetcher` to perform these actions.
"""

import logging

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)

_LOGGER = logging.getLogger(__name__)


class TagEraser:
    """Erases all tags from a specified Meraki device via API calls.

    This class provides functionality to clear all existing tags from a Meraki
    device by sending an empty list of tags to the device tag update endpoint.
    It relies on an injected `MerakiApiDataFetcher` instance for the actual
    API communication.

    Attributes:
        api_fetcher (MerakiApiDataFetcher): An instance of `MerakiApiDataFetcher`
            used to make calls to the Meraki API.
    """

    def __init__(self, api_fetcher: MerakiApiDataFetcher) -> None:
        """Initializes the TagEraser.

        Args:
            api_fetcher (MerakiApiDataFetcher): An instance of
                `MerakiApiDataFetcher` that will be used to perform the
                API calls for updating (erasing) device tags.
        """
        self.api_fetcher = api_fetcher

    async def erase_device_tags(self, serial: str) -> bool:
        """Erases all tags for a specified Meraki device.

        This is achieved by calling the `async_update_device_tags` method of the
        `api_fetcher` with an empty list of tags (`[]`). This action effectively
        removes all current tags from the device.

        Args:
            serial (str): The serial number of the Meraki device whose tags
                are to be erased.

        Returns:
            bool: True if the tag erasure operation was successfully initiated
                  (i.e., no exceptions were raised during the API call). False
                  if a known, handled exception occurs (e.g., connection error,
                  invalid API key) that prevents the operation from completing.

        Raises:
            This method aims to handle common exceptions internally and return
            True/False. However, if `api_fetcher.async_update_device_tags`
            raises an unhandled exception, it might propagate.
            (Note: The original implementation didn't explicitly raise but logged errors.
            The updated version will return False on handled errors for clarity).
        """
        _LOGGER.info("Attempting to erase all tags for device serial: %s", serial)
        try:
            # To erase tags, update the device with an empty list of tags.
            # IMPORTANT: This relies on MerakiApiDataFetcher.async_update_device_tags
            # being fully implemented to make a PUT request to `/devices/{serial}/tags`.
            await self.api_fetcher.async_update_device_tags(serial, [])
            _LOGGER.info("Successfully initiated tag erasure for device: %s", serial)
            return True
        except MerakiApiConnectionError as e:
            _LOGGER.error(
                "Connection error while erasing tags for device %s: %s", serial, e
            )
            return False
        except MerakiApiInvalidApiKeyError as e:
            # This error suggests an authentication problem.
            _LOGGER.error(
                "Invalid API key while erasing tags for device %s: %s", serial, e
            )
            # Depending on desired behavior, this could re-raise ConfigEntryAuthFailed
            # if the coordinator layer expects it. For now, returning False.
            return False
        except Exception as e:
            # Catch any other unexpected exceptions during the API call.
            _LOGGER.exception(
                "Unexpected error erasing tags for device %s: %s", serial, e
            )
            return False
