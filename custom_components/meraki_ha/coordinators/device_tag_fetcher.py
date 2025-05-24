"""Provides the DeviceTagFetcher for the Meraki Home Assistant integration.

This module defines `DeviceTagFetcher`, a class responsible for the actual
API calls to retrieve tags for Meraki devices. It uses an instance of
`MerakiApiDataFetcher` to perform these calls.
"""

import logging
from typing import List

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetcher:
    """Fetches tags for Meraki devices using the Meraki API.

    This class encapsulates the logic for making API requests to retrieve
    the tags associated with a specific Meraki device. It relies on an
    instance of `MerakiApiDataFetcher` to handle the underlying HTTP requests
    and retry mechanisms.

    Attributes:
        api_fetcher (MerakiApiDataFetcher): An instance of `MerakiApiDataFetcher`
            used to make calls to the Meraki API.
    """

    def __init__(self, api_fetcher: MerakiApiDataFetcher) -> None:
        """Initializes the DeviceTagFetcher.

        Args:
            api_fetcher (MerakiApiDataFetcher): An instance of
                `MerakiApiDataFetcher` that will be used to perform the
                actual API calls.
        """
        self.api_fetcher = api_fetcher

    async def get_device_tags(self, serial: str) -> List[str]:
        """Fetches the list of tags for a given Meraki device serial number.

        This method calls the `async_get_device_tags` method of the injected
        `api_fetcher`. It handles common API-related exceptions and returns
        an empty list in case of such errors, ensuring that the caller
        receives a consistent return type.

        Args:
            serial (str): The serial number of the Meraki device.

        Returns:
            List[str]: A list of strings, where each string is a tag associated
                with the device. Returns an empty list if no tags are found,
                or if an error (e.g., connection error, invalid API key) occurs
                during the fetch.
        """
        _LOGGER.debug("Attempting to fetch tags for device serial: %s", serial)
        try:
            # Delegate the API call to the MerakiApiDataFetcher instance.
            # Note: The MerakiApiDataFetcher.async_get_device_tags is currently a placeholder.
            # For this to work, MerakiApiDataFetcher.async_get_device_tags needs to be
            # implemented to call the appropriate Meraki API endpoint for device tags,
            # e.g., by calling its own _fetch_data method with `/devices/{serial}/tags`.
            # If that method is still a placeholder, this will effectively return an empty list.
            tags = await self.api_fetcher.async_get_device_tags(serial)

            # Ensure a list is returned, even if tags is None.
            if tags is None:
                _LOGGER.warning("Received None for tags for device %s. Returning empty list.", serial)
                return []
            if not isinstance(tags, list):
                _LOGGER.warning("Expected list of tags for device %s, but got %s. Returning empty list.", serial, type(tags))
                return []

            _LOGGER.info("Successfully fetched tags for device %s: %s", serial, tags)
            return tags
        except MerakiApiConnectionError as e:
            # Handle specific connection errors logged by MerakiApiDataFetcher.
            _LOGGER.error(
                "Connection error while fetching tags for device %s: %s. Returning empty list.",
                serial,
                e,
            )
            return []
        except MerakiApiInvalidApiKeyError as e:
            # Handle invalid API key errors logged by MerakiApiDataFetcher.
            _LOGGER.error(
                "Invalid API key error while fetching tags for device %s: %s. Returning empty list.",
                serial,
                e,
            )
            return []
        except Exception as e:
            # Catch any other unexpected exceptions.
            _LOGGER.exception(
                "Unexpected error fetching tags for device %s: %s. Returning empty list.",
                serial,
                e,
            )
            return []
