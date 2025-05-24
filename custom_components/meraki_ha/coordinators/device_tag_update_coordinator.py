"""Provides the DeviceTagUpdateCoordinator for the Meraki Home Assistant integration.

This module defines `DeviceTagUpdateCoordinator`, a Home Assistant
`DataUpdateCoordinator` that, similar to `DeviceTagFetchCoordinator`, acts
primarily as a pass-through for on-demand actions rather than managing
periodically updated data. It facilitates updating device tags via `DeviceTagUpdater`.
"""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed
from datetime import timedelta

from .device_tag_updater import DeviceTagUpdater
from .api_data_fetcher import MerakiApiDataFetcher

_LOGGER = logging.getLogger(__name__)


class DeviceTagUpdateCoordinator(DataUpdateCoordinator[None]): # Data type is None as it's action-oriented
    """Coordinates the updating of tags for Meraki devices.

    This coordinator, despite its `DataUpdateCoordinator` base, primarily serves
    as an action dispatcher for updating device tags. It uses `DeviceTagUpdater`
    to perform the actual API calls. After a successful update, it can trigger
    a refresh of other coordinators if needed (e.g., to reflect tag changes).

    It does not implement `_async_update_data` for periodic background updates,
    as tag updates are typically on-demand user actions.

    Attributes:
        api_key (str): The Meraki API key.
        api_fetcher (MerakiApiDataFetcher): An instance of `MerakiApiDataFetcher`
            used by the `DeviceTagUpdater`.
        device_tag_updater (DeviceTagUpdater): An instance of `DeviceTagUpdater`
            that handles the API calls to update device tags.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        scan_interval: timedelta, # scan_interval is for the parent, not directly used here
    ) -> None:
        """Initializes the DeviceTagUpdateCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): The Meraki API key for authentication.
            scan_interval (timedelta): The base scan interval, passed to the
                parent `DataUpdateCoordinator`. This coordinator itself doesn't
                perform scheduled updates with this interval.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Device Tag Update", # Name for logging and diagnostics
            # update_interval is set, but _async_update_data is not implemented.
            update_interval=scan_interval,
        )
        self.api_key = api_key
        # Initialize MerakiApiDataFetcher, which is a dependency for DeviceTagUpdater.
        # Passing None for unused coordinator dependencies of MerakiApiDataFetcher.
        self.api_fetcher = MerakiApiDataFetcher(self.api_key, None, None, None)
        self.device_tag_updater = DeviceTagUpdater(self.api_fetcher)

    # No _async_update_data method is implemented as this coordinator is action-based.

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Updates the tags for a single specified Meraki device.

        This method delegates the tag update operation to `DeviceTagUpdater`.
        If the update is successful, it triggers `async_request_refresh` which
        can notify listeners (typically other coordinators) that they might need
        to refresh their data if it depends on device tags.

        Args:
            serial (str): The serial number of the Meraki device whose tags are
                to be updated.
            tags (List[str]): A list of strings representing the new set of tags
                for the device. This will replace all existing tags.

        Raises:
            UpdateFailed: If the tag update operation fails due to an API error
                (not `ConfigEntryAuthFailed`) or other unexpected issues.
            ConfigEntryAuthFailed: If the API key is invalid, leading to an
                authentication failure during the tag update.
        """
        _LOGGER.info("Attempting to update tags for device %s to: %s", serial, tags)
        try:
            # Delegate the actual tag update to the DeviceTagUpdater instance.
            update_successful = await self.device_tag_updater.update_device_tags(
                serial, tags
            )

            if update_successful:
                _LOGGER.info(
                    "Successfully updated tags for device %s. Requesting refresh of dependent data.",
                    serial,
                )
                # Request a refresh of data for any coordinators that might depend on these tags.
                # This typically makes those coordinators run their _async_update_data.
                await self.async_request_refresh()
            else:
                # This case might occur if update_device_tags can return False
                # for non-exception failures (e.g., API returns success but with unexpected content).
                _LOGGER.warning(
                    "Tag update for device %s was reported as unsuccessful by updater, but no exception was raised.",
                    serial,
                )
                # Consider if this should also raise UpdateFailed.
                # For now, aligns with original behavior of only raising on exception.

        except ConfigEntryAuthFailed:
            # Re-raise ConfigEntryAuthFailed to be handled by Home Assistant core
            # for re-authentication flow.
            _LOGGER.error("Authentication failed while updating tags for device %s.", serial)
            raise
        except UpdateFailed:
            # Re-raise UpdateFailed if it was thrown by the updater.
            _LOGGER.error("UpdateFailed exception during tag update for device %s.", serial)
            raise
        except Exception as e:
            # Catch any other unexpected exceptions from the updater.
            _LOGGER.exception(
                "Unexpected error updating tags for device %s: %s", serial, e
            )
            raise UpdateFailed(
                f"Unexpected error updating tags for device {serial}: {e}"
            ) from e
