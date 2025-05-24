"""Provides the TagEraserCoordinator for the Meraki Home Assistant integration.

This module defines `TagEraserCoordinator`, a Home Assistant
`DataUpdateCoordinator`. Similar to other action-oriented coordinators in this
package (like `DeviceTagUpdateCoordinator`), its primary role is to dispatch
on-demand actions—specifically, erasing all tags from a Meraki device—rather
than managing periodically updated data. It uses `TagEraser` for the API interaction.
"""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .tag_eraser import TagEraser
from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class TagEraserCoordinator(DataUpdateCoordinator[None]): # Data type is None as it's action-oriented
    """Coordinates the erasure of tags for Meraki devices.

    This `DataUpdateCoordinator` is primarily used to trigger the action of
    erasing all tags from a specified Meraki device. It delegates the actual
    API call to an instance of `TagEraser`.

    It does not implement `_async_update_data` for periodic background data
    fetching, as tag erasure is an on-demand operation.

    Attributes:
        api_key (str): The Meraki API key.
        api_fetcher (MerakiApiDataFetcher): An instance of `MerakiApiDataFetcher`,
            which is a dependency for `TagEraser`.
        tag_eraser (TagEraser): An instance of `TagEraser` responsible for
            making the API call to erase device tags.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta, # Passed to parent, not used for periodic updates here
    ) -> None:
        """Initializes the TagEraserCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): The Meraki API key for authentication.
            scan_interval (timedelta): The base scan interval, passed to the
                parent `DataUpdateCoordinator`. This coordinator itself does not
                perform scheduled updates with this interval.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Tag Eraser", # Name for logging and diagnostics
            # update_interval is set, but _async_update_data is not implemented.
            update_interval=scan_interval,
        )
        self.api_key = api_key
        # Initialize MerakiApiDataFetcher, required by TagEraser.
        # Passing None for unused coordinator dependencies of MerakiApiDataFetcher.
        self.api_fetcher = MerakiApiDataFetcher(self.api_key, None, None, None)
        self.tag_eraser = TagEraser(self.api_fetcher)

    # No _async_update_data method is implemented as this coordinator is action-based.

    async def async_erase_device_tags(self, serial: str) -> None:
        """Erases all tags for a single specified Meraki device.

        This method calls the `erase_device_tags` method of its `TagEraser`
        instance. If the operation in `TagEraser` leads to an exception that
        is not handled there (or if `TagEraser.erase_device_tags` itself raises
        an error), this method will wrap it in an `UpdateFailed` exception.

        Args:
            serial (str): The serial number of the Meraki device whose tags
                are to be erased.

        Raises:
            UpdateFailed: If the tag erasure operation fails due to an API error
                or any other unexpected issue during the process.
        """
        _LOGGER.info("Attempting to erase tags for device serial (via coordinator): %s", serial)
        try:
            # Delegate the tag erasure to the TagEraser instance.
            success = await self.tag_eraser.erase_device_tags(serial)
            if not success:
                # If erase_device_tags returns False (indicating a handled error),
                # an UpdateFailed exception is raised to signal the failure to the caller.
                _LOGGER.warning(
                    "Tag erasure for device %s reported as unsuccessful by TagEraser.", serial
                )
                raise UpdateFailed(f"Tag erasure failed for device {serial} (handled error).")
            _LOGGER.info("Successfully initiated tag erasure for device %s.", serial)
            # Optionally, could call self.async_request_refresh() if other parts
            # of the system need to be notified of this change immediately.
        except Exception as e:
            # Catch any exception from TagEraser (including UpdateFailed if it were raised there)
            # or any other unexpected error.
            _LOGGER.exception(
                "Error during tag erasure for device %s (coordinator level): %s",
                serial,
                e,
            )
            # Ensure consistent UpdateFailed exception type from the coordinator.
            if isinstance(e, UpdateFailed):
                raise # Re-raise if it's already an UpdateFailed exception
            raise UpdateFailed(
                f"Error erasing tags for device {serial}: {e}"
            ) from e
