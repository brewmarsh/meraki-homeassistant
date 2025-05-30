"""Device Tag Fetcher for the Meraki Home Assistant integration.

This module provides the `DeviceTagFetcher` class, a utility designed for direct
fetching of device tags from the Meraki API using an instance of `MerakiApiDataFetcher`.
It's a simpler alternative to `DeviceTagFetchCoordinator` for scenarios where
coordinator overhead is not needed.
"""
import logging
from typing import List, Optional  # Added Optional

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiError,  # Catching the base MerakiApiError is often better
    MerakiApiConnectionError,  # Specific error type
    MerakiApiInvalidApiKeyError,  # Specific error type
)

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetcher:
    """Class to fetch tags for Meraki devices directly using MerakiApiDataFetcher.

    This class provides a straightforward way to get device tags without the
    overhead of a `DataUpdateCoordinator`. It relies on an injected
    `MerakiApiDataFetcher` instance for API communication.
    """

    def __init__(self, api_fetcher: MerakiApiDataFetcher) -> None:
        """Initialize the DeviceTagFetcher.

        Args:
            api_fetcher: An instance of `MerakiApiDataFetcher` to be used for
                making API calls to retrieve device tags.
        """
        self.api_fetcher: MerakiApiDataFetcher = api_fetcher

    async def get_device_tags(self, serial: str) -> List[str]:
        """Fetch tags for a single Meraki device by its serial number.

        This method attempts to retrieve tags using the `async_get_device_tags`
        method of the `MerakiApiDataFetcher`. It includes error handling for
        common API issues and returns an empty list if tags cannot be fetched
        or if the device has no tags.

        Note: The effectiveness of this method depends on the implementation of
        `MerakiApiDataFetcher.async_get_device_tags`, which is noted as being
        a placeholder in its own documentation. If that method doesn't actually
        fetch tags, this one will consequently not return them.

        Args:
            serial: The serial number of the device for which to fetch tags.

        Returns:
            A list of tags (strings) associated with the device. Returns an
            empty list if no tags are found, if the device has no tags, or if
            any error occurs during the fetching process.
        """
        _LOGGER.debug("Attempting to fetch tags for device serial: %s", serial)
        try:
            # `async_get_device_tags` in api_fetcher is a placeholder.
            # If it's implemented, it should return Optional[List[str]] or
            # List[str].
            tags: Optional[List[str]] = await self.api_fetcher.async_get_device_tags(
                serial
            )
            if tags is None:
                _LOGGER.info(
                    "No tags returned by API fetcher for device %s (or fetcher returned None).",
                    serial)
                return []
            _LOGGER.debug(
                "Successfully fetched %d tags for device %s.",
                len(tags),
                serial)
            return tags
        except MerakiApiConnectionError as e:
            _LOGGER.error(
                "Connection error while fetching tags for device %s: %s",
                serial,
                e)
            return []
        except MerakiApiInvalidApiKeyError as e:
            _LOGGER.error(
                "Invalid API key error while fetching tags for device %s: %s",
                serial,
                e)
            return []
        except MerakiApiError as e:  # Catch other Meraki API specific errors
            _LOGGER.error(
                "A Meraki API error occurred fetching tags for device %s: %s",
                serial,
                e)
            return []
        except Exception as e:  # Catch any other unexpected errors
            _LOGGER.exception(  # Use .exception to include stack trace
                "Unexpected error fetching tags for device %s: %s", serial, e
            )
            return []
