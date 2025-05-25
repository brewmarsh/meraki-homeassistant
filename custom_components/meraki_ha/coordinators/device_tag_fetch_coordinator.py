"""Device Tag Fetch Coordinator for the Meraki Home Assistant integration.

This module defines the `DeviceTagFetchCoordinator`, which is responsible for
orchestrating the fetching of tags associated with Meraki devices. It uses
the `MerakiApiDataFetcher` to interact with the Meraki API.
"""
import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN # Assuming DOMAIN is used for logger name consistency
from .api_data_fetcher import MerakiApiDataFetcher, MerakiApiError

if TYPE_CHECKING:
    # To avoid circular import issues at runtime
    from .base_coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetchCoordinator(DataUpdateCoordinator[Dict[str, Any]]): # Generic type for DataUpdateCoordinator data
    """Coordinator to fetch tags for Meraki devices.

    This coordinator is specifically designed to retrieve tags for individual
    Meraki devices. It's typically used by other components that need up-to-date
    tag information. The `_async_update_data` method is a placeholder as this
    coordinator primarily provides an on-demand tag fetching service via
    `async_get_device_tags`.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta, # Interval for scheduled updates (if any)
        main_coordinator: "MerakiDataUpdateCoordinator",
    ) -> None:
        """Initialize the DeviceTagFetchCoordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            scan_interval: The time interval for periodic updates. Note that
                this coordinator's main function `async_get_device_tags` is
                on-demand. The interval is for the `_async_update_data` placeholder.
            main_coordinator: The main `MerakiDataUpdateCoordinator` instance,
                used to access shared properties like `org_id`.
        """
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} Device Tag Fetch ({main_coordinator.org_id})", # More specific name
            update_interval=scan_interval,
        )
        self.api_key: str = api_key
        self.org_id: str = main_coordinator.org_id
        self.main_coordinator: "MerakiDataUpdateCoordinator" = main_coordinator

        # Initialize MerakiApiDataFetcher for API communication.
        # The network_coordinator and ssid_coordinator arguments are not relevant
        # for fetching device tags, so they are passed as None.
        self.api_fetcher: MerakiApiDataFetcher = MerakiApiDataFetcher(
            api_key=self.api_key,
            org_id=self.org_id,
            network_coordinator=None,
            ssid_coordinator=None,
        )
        # Ensure self.data is initialized as per DataUpdateCoordinator's generic type
        self.data: Dict[str, Any] = {}


    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch all device tags (placeholder).

        This method is part of the DataUpdateCoordinator pattern. Currently,
        it's a placeholder as tags are fetched on-demand per device.
        If there's a need to periodically fetch all tags for all devices,
        this method would implement that logic.

        Returns:
            An empty dictionary, as no global tag update is performed by default.
        """
        _LOGGER.debug(
            "DeviceTagFetchCoordinator._async_update_data called, but it's a placeholder. "
            "Tags are fetched on-demand via async_get_device_tags."
        )
        # If, in the future, there's a need to fetch all tags for all devices:
        # 1. Get all devices (perhaps from main_coordinator.data).
        # 2. Loop through devices and call self.api_fetcher.async_get_device_tags(serial).
        # 3. Aggregate results into a dictionary, e.g., Dict[str, List[str]] (serial -> tags).
        # For now, it returns an empty dict as per original behavior.
        return {}

    async def async_get_device_tags(self, serial: str) -> Optional[List[str]]:
        """Fetch tags for a single Meraki device by its serial number.

        Args:
            serial: The serial number of the device for which to fetch tags.

        Returns:
            A list of tags (strings) associated with the device if successful.
            Returns None if the device has no tags or if an error occurs during
            the fetch operation that isn't a critical UpdateFailed.
            The `async_get_device_tags` in `api_fetcher` currently returns
            an empty list on error/no tags. This method will propagate that.

        Raises:
            UpdateFailed: If the underlying API call fails critically,
                preventing tag retrieval. This might be too strong if an
                individual device tag fetch failing shouldn't stop everything.
                Consider adjusting based on how failures should be handled by callers.
        """
        _LOGGER.debug("Fetching tags for device serial: %s", serial)
        try:
            # The `api_fetcher.async_get_device_tags` is currently a placeholder itself.
            # If it's implemented to return None or raise specific exceptions,
            # this error handling might need adjustment.
            tags: Optional[List[str]] = await self.api_fetcher.async_get_device_tags(
                serial
            )
            if tags is None: # Explicitly handle if api_fetcher could return None
                _LOGGER.warning("No tags found or error fetching tags for device %s, api_fetcher returned None.", serial)
                return [] # Consistent with api_fetcher's placeholder returning [] on error
            return tags
        except MerakiApiError as e: # Catch specific API errors from the fetcher
            _LOGGER.error(
                "API error fetching tags for device %s: %s", serial, e
            )
            # Depending on severity, could raise UpdateFailed or return None/empty list
            # Original code raised UpdateFailed for any Exception.
            # Let's make it more specific: raise for API errors, return empty for "not found" type issues.
            # However, async_get_device_tags in fetcher is a placeholder, so this is speculative.
            # For now, mirroring original behavior of raising UpdateFailed.
            raise UpdateFailed(
                f"API error fetching tags for device {serial}: {e}"
            ) from e
        except Exception as e: # Catch any other unexpected errors
            _LOGGER.exception( # Use .exception to include stack trace for unexpected errors
                "Unexpected error fetching tags for device %s: %s", serial, e
            )
            raise UpdateFailed(
                f"Unexpected error fetching tags for device {serial}: {e}"
            ) from e
