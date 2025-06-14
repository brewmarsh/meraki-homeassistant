"""Device Tag Update Coordinator for the Meraki Home Assistant integration.

This module defines the `DeviceTagUpdateCoordinator`, which is responsible for
orchestrating updates to device tags via the Meraki API. It uses the
`MerakiApiDataFetcher` for the actual API communication.
"""

import logging
from datetime import timedelta  # Used for scan_interval and self.update_interval

# Added Any for self.data generic
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
)

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN  # For logger naming consistency
from ..meraki_api.exceptions import MerakiApiError
from .api_data_fetcher import MerakiApiDataFetcher

if TYPE_CHECKING:
    # To avoid circular import issues at runtime
    from .base_coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


# Generic type for DataUpdateCoordinator data
class DeviceTagUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator to update tags for Meraki devices.

    This coordinator manages the process of sending tag updates to the
    Meraki API. It provides an interface for other parts of the
    integration to request tag changes for specific devices. The
    `_async_update_data` method is a placeholder as updates are on-demand.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta,
        org_id: str,
        # base_url: str,  # This parameter seems unused.
        # The MerakiApiDataFetcher constructs full URLs.
        main_coordinator: "MerakiDataUpdateCoordinator",
    ) -> None:
        """Initialize the DeviceTagUpdateCoordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key. (Note: Stored, but `api_fetcher` uses client from `main_coordinator`).
            scan_interval: The time interval for periodic updates.
                Primarily for the `_async_update_data` placeholder, as tag
                updates are typically on-demand.
            org_id: The Meraki Organization ID. (Note: Stored, but `api_fetcher` uses client from `main_coordinator`).
            main_coordinator: The main `MerakiDataUpdateCoordinator` instance, which provides
                the `MerakiAPIClient` (already initialized with API key and Org ID)
                used by this coordinator's `MerakiApiDataFetcher`.
        """
        super().__init__(
            hass,
            _LOGGER,
            # More specific name
            name=f"{DOMAIN} Device Tag Update ({org_id})",
            # For the placeholder _async_update_data
            update_interval=scan_interval,
        )
        self.api_key: str = api_key
        self.org_id: str = org_id
        # Storing if needed, but seems unused.
        # self.base_url: str = base_url
        self.main_coordinator: "MerakiDataUpdateCoordinator" = main_coordinator

        # Initialize MerakiApiDataFetcher for API communication.
        # Network and SSID coordinators are not relevant for tag updates.
        # MerakiApiDataFetcher now expects a MerakiAPIClient instance.
        # We should use the client from the main_coordinator.
        if not hasattr(main_coordinator, 'meraki_client'):
            # This would be a programming error if main_coordinator doesn't have it.
            _LOGGER.error("Main coordinator does not have a 'meraki_client' attribute. Cannot initialize ApiDataFetcher for DeviceTagUpdateCoordinator.")
            # Handle this gracefully, perhaps by setting api_fetcher to None or raising an error.
            # For now, let's assume it will be present.
            # If it could be None, then api_fetcher calls would need None checks.
            raise ValueError("Main coordinator missing meraki_client, required for DeviceTagUpdateCoordinator's ApiDataFetcher")

        self.api_fetcher: MerakiApiDataFetcher = MerakiApiDataFetcher(
            meraki_client=main_coordinator.meraki_client
        )

        # self.data is managed by DataUpdateCoordinator.
        # Initialize it if a specific structure is always expected.
        # The original had Dict[str, List[str]], but generic is Dict[str, Any].
        # As _async_update_data returns {}, this is fine.
        self.data: Dict[str, Any] = {}

        # The original code had a custom update_interval and
        # _next_update_time logic, which might conflict with or duplicate
        # DataUpdateCoordinator's internal scheduling. If specific timing
        # beyond the coordinator's `update_interval` is needed, it should
        # be handled carefully. For now, relying on superclass's interval.
        # self.update_interval = timedelta(
        #     seconds=scan_interval.total_seconds() * 2
        # )
        # self._next_update_time = dt_util.now()
        _LOGGER.debug(
            "DeviceTagUpdateCoordinator initialized for org %s. Update "
            "interval for placeholder: %s",
            self.org_id,
            self.update_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from API endpoint (placeholder).

        This method is part of the DataUpdateCoordinator pattern. For this
        coordinator, actual tag updates are on-demand via
        `async_update_device_tags`. This method currently serves as a
        placeholder and does not perform any data fetching or processing
        related to tag updates.

        Returns:
            An empty dictionary, as no global data fetching is performed
            here.
        """
        _LOGGER.debug(
            "DeviceTagUpdateCoordinator._async_update_data called, but it's a "
            "placeholder. Tag updates are on-demand via "
            "async_update_device_tags."
        )
        # Return an empty dictionary as per original and superclass expectation
        return {}

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Update tags for a single Meraki device.

        This method uses the `MerakiApiDataFetcher` to send a request to
        the Meraki API to update the tags for the specified device.

        Note: The effectiveness of this method depends on the
        implementation of `MerakiApiDataFetcher.async_update_device_tags`,
        which is noted as being a placeholder in its own documentation.

        Args:
            serial: The serial number of the device whose tags are to be
                updated.
            tags: A list of strings representing the new set of tags for
                the device. The Meraki API typically expects a complete
                list of tags, so this will overwrite existing tags.

        Raises:
            UpdateFailed: If the tag update operation fails due to an API
                error or other unexpected issue.
            ConfigEntryAuthFailed: If the Meraki API key is invalid or
                unauthorized, resulting in a 401 error from the API.
        """
        _LOGGER.debug(
            "Attempting to update tags for device serial %s to: %s",
            serial,
            tags,
        )
        try:
            # `async_update_device_tags` in api_fetcher is a placeholder.
            # Assuming it returns bool or raises on failure.
            success: bool = await self.api_fetcher.async_update_device_tags(
                serial, tags
            )
            if success:
                _LOGGER.info(
                    "Successfully updated tags for device %s. Requesting refresh.",
                    serial,
                )
                # After a successful update, you might want to trigger a
                # refresh of data that depends on these tags.
                # This refreshes this coordinator's data (which is {}),
                # and then _async_update_data (placeholder) runs.
                await self.async_request_refresh()
                # Consider if a refresh of the main_coordinator is needed:
                # await self.main_coordinator.async_request_refresh()
            else:
                # This path assumes async_update_device_tags returns False
                # on non-exception failure
                _LOGGER.warning(
                    "Tag update for device %s reported as unsuccessful by API "
                    "fetcher (returned False).",
                    serial,
                )
                raise UpdateFailed(
                    f"Tag update for device {serial} failed (API fetcher "
                    "indicated no success)."
                )

        except ConfigEntryAuthFailed:  # Specific re-raise
            _LOGGER.error(
                "Authentication failed while updating tags for device %s.",
                serial,
            )
            raise
        except MerakiApiError as e:  # Catch specific API errors from the fetcher
            _LOGGER.error("API error updating tags for device %s: %s", serial, e)
            raise UpdateFailed(
                f"API error updating tags for device {serial}: {e}"
            ) from e
        # UpdateFailed was already caught by original code, but it's good
        # to be explicit if MerakiApiError is a type of UpdateFailed or
        # if api_fetcher raises it. For now, assuming MerakiApiError is
        # distinct.
        except UpdateFailed:  # Re-raise if api_fetcher raises it
            _LOGGER.error(
                "UpdateFailed exception during tag update for device %s.",
                serial,
            )
            raise
        except Exception as e:  # Catch any other unexpected errors
            # Use .exception to include stack trace
            _LOGGER.exception(
                "Unexpected error updating tags for device %s: %s", serial, e
            )
            raise UpdateFailed(
                f"Unexpected error updating tags for device {serial}: {e}"
            ) from e
