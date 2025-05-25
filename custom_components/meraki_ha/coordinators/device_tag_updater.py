"""Device Tag Updater for the Meraki Home Assistant integration.

This module provides the `DeviceTagUpdater` class, a utility for updating
device tags on the Meraki platform. It uses an instance of `MerakiApiDataFetcher`
to perform the necessary API calls and handles API-specific errors, translating
them into Home Assistant exceptions where appropriate.
"""
import logging
from typing import List

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed # Used for raising errors

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiError, # Catching base is good, then specific if needed
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)

_LOGGER = logging.getLogger(__name__)


class DeviceTagUpdater:
    """Class to update tags for Meraki devices using MerakiApiDataFetcher.

    This utility class provides a method to update device tags. It's designed
    to be used by components that need to modify tags and handles the API
    interaction and error translation.
    """

    def __init__(self, api_fetcher: MerakiApiDataFetcher) -> None:
        """Initialize the DeviceTagUpdater.

        Args:
            api_fetcher: An instance of `MerakiApiDataFetcher` to be used for
                making API calls to update device tags.
        """
        self.api_fetcher: MerakiApiDataFetcher = api_fetcher

    async def update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Update tags for a single Meraki device by its serial number.

        This method attempts to update the tags for the specified device using the
        `async_update_device_tags` method of the `MerakiApiDataFetcher`.
        It translates specific Meraki API errors into Home Assistant exceptions.

        Note: The success of this operation heavily depends on the implementation
        of `MerakiApiDataFetcher.async_update_device_tags`, which is currently
        a placeholder. If that method doesn't correctly update tags or always
        returns False/raises an error, this method will reflect that.

        Args:
            serial: The serial number of the device whose tags are to be updated.
            tags: A list of strings representing the new set of tags for the device.
                  The Meraki API typically expects a complete list of tags, which
                  means existing tags will be overwritten by this list.

        Raises:
            UpdateFailed: If the tag update operation fails due to a connection
                error, a general Meraki API error, or other unexpected issues.
            ConfigEntryAuthFailed: If the Meraki API key is invalid or
                unauthorized, resulting in a 401 error from the API.
        """
        _LOGGER.debug(
            "Attempting to update tags for device serial %s to: %s", serial, tags
        )
        try:
            # `async_update_device_tags` in api_fetcher is a placeholder.
            # Assuming it returns True on success, False on known failure,
            # or raises MerakiApiError for API issues.
            success: bool = await self.api_fetcher.async_update_device_tags(
                serial, tags
            )
            if success:
                _LOGGER.info(
                    "Successfully initiated tag update for device %s with tags: %s.",
                    serial,
                    tags,
                )
            else:
                # This case handles if async_update_device_tags itself returns False
                # without raising an exception, indicating a non-exceptional failure.
                _LOGGER.warning(
                    "Tag update for device %s was reported as unsuccessful by API fetcher (returned False).",
                    serial
                )
                raise UpdateFailed(
                    f"Tag update for device {serial} failed (API fetcher indicated no success)."
                )
        except MerakiApiConnectionError as e:
            _LOGGER.error(
                "Connection error while updating tags for device %s: %s", serial, e
            )
            raise UpdateFailed(
                f"Failed to connect to Meraki API while updating tags for {serial}: {e}"
            ) from e
        except MerakiApiInvalidApiKeyError as e:
            _LOGGER.error(
                "Invalid API key error while updating tags for device %s: %s", serial, e
            )
            raise ConfigEntryAuthFailed(
                f"Invalid Meraki API key when updating tags for {serial}: {e}"
            ) from e
        except MerakiApiError as e: # Catch other specific Meraki API errors
            _LOGGER.error(
                "A Meraki API error occurred updating tags for device %s: %s", serial, e
            )
            raise UpdateFailed(
                f"Meraki API error updating tags for device {serial}: {e}"
            ) from e
        except UpdateFailed: # Re-raise if already UpdateFailed
            raise
        except ConfigEntryAuthFailed: # Re-raise if already ConfigEntryAuthFailed
            raise
        except Exception as e: # Catch any other unexpected errors
            _LOGGER.exception( # Use .exception to include stack trace
                "Unexpected error updating tags for device %s: %s", serial, e
            )
            raise UpdateFailed(
                f"Unexpected error updating tags for device {serial}: {e}"
            ) from e
