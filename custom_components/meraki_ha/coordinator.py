"""Contains the MerakiDataUpdateCoordinator for the meraki_ha integration.

This file defines the MerakiDataUpdateCoordinator class, which is responsible
for fetching data from the Meraki API, processing it, and providing it to
various platforms within the Home Assistant integration.
"""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .coordinators.api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)
from .const import ERASE_TAGS_WARNING
from .coordinators.device_coordinator import MerakiDeviceCoordinator
from .coordinators.ssid_coordinator import MerakiSsidCoordinator
from .coordinators.network_coordinator import MerakiNetworkCoordinator
from .coordinators.device_tag_update_coordinator import DeviceTagUpdateCoordinator
from .coordinators.tag_eraser_coordinator import TagEraserCoordinator
from .coordinators.data_aggregation_coordinator import DataAggregationCoordinator
from .coordinators.device_tag_fetch_coordinator import DeviceTagFetchCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator):
    """Manages fetching and updating data from the Meraki API.

    This coordinator orchestrates the retrieval of device, network, and SSID
    information from the Meraki API. It handles API communication, data
    aggregation, and regular updates to ensure Home Assistant entities
    have the latest information. It also manages device tag updates and
    optional tag erasure.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
        erase_tags: bool,
        relaxed_tag_match: bool,
    ) -> None:
        """Initialize the Meraki data coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key for authentication.
            org_id: The Meraki organization ID.
            scan_interval: The interval at which to update data.
            device_name_format: The format string for device names.
            erase_tags: A boolean indicating whether to erase existing device tags.
            relaxed_tag_match: A boolean indicating whether to use relaxed tag matching.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.data = {}
        self.erase_tags = erase_tags
        self.relaxed_tag_match = relaxed_tag_match
        self.device_name_format = device_name_format
        self.hass = hass
        self.scan_interval = scan_interval
        self.device_tag_update_coordinator = DeviceTagUpdateCoordinator(
            self.hass, self.api_key, self.scan_interval
        )
        self.tag_eraser_coordinator = TagEraserCoordinator(
            self.hass, self.api_key, self.scan_interval
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch and process data from the Meraki API.

        This method is called periodically by Home Assistant to update the
        integration's data. It fetches device, network, and SSID information,
        aggregates it, and handles potential API errors.

        Returns:
            A dictionary containing the fetched and processed Meraki data.

        Raises:
            ConfigEntryAuthFailed: If the Meraki API key is invalid.
            UpdateFailed: If there is a connection error or an unexpected
                          issue during the data fetching process.
        """
        _LOGGER.debug("Starting Meraki data update")
        try:
            # Initialize coordinators for different data aspects
            device_coordinator = MerakiDeviceCoordinator(
                self.hass,
                self.api_key,
                self.org_id,
                self.scan_interval,
                self.device_name_format,
            )
            network_coordinator = MerakiNetworkCoordinator(
                self.hass,
                self.api_key,
                self.org_id,
                self.scan_interval,
                self.device_name_format,
            )
            ssid_coordinator = MerakiSsidCoordinator(
                self.hass,
                self.api_key,
                self.org_id,
                self.scan_interval,
                self.device_name_format,
            )
            # Coordinator for fetching raw data from the API
            api_fetcher = MerakiApiDataFetcher(
                self.api_key, device_coordinator, network_coordinator, ssid_coordinator
            )
            # Coordinator for fetching device tags
            device_tag_fetch_coordinator = DeviceTagFetchCoordinator(
                self.hass, self.api_key, self.scan_interval
            )
            # Coordinator for aggregating data from various sources
            data_aggregation_coordinator = DataAggregationCoordinator(
                self.hass, self.scan_interval, self.relaxed_tag_match
            )

            # Fetch all data (devices, SSIDs, networks) from the Meraki API
            all_data = await api_fetcher.fetch_all_data(
                self.hass, self.org_id, self.scan_interval, self.device_name_format
            )

            devices: List[Dict[str, Any]] = all_data.get("devices", [])
            ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
            networks: List[Dict[str, Any]] = all_data.get("networks", [])
            device_tags: Dict[str, List[str]] = {}

            # Fetch tags for each device
            for device in devices:
                serial = device["serial"]
                tags = await device_tag_fetch_coordinator.async_get_device_tags(serial)
                device_tags[serial] = tags
                device["tags"] = device_tags[serial]  # Add tags to device data

            # Explicitly update the data of individual coordinators
            device_coordinator.data = devices
            ssid_coordinator.data = ssids
            network_coordinator.data = networks

            # Combine all fetched and processed data
            combined_data = await data_aggregation_coordinator._async_update_data(
                device_coordinator.data,
                ssid_coordinator.data,
                network_coordinator.data,
                device_tags,
            )

            _LOGGER.debug(f"Meraki data update completed: {combined_data}")
            self.data = combined_data  # Store aggregated data in the main coordinator
            _LOGGER.debug(f"Coordinator data: {self.data}")

            # Erase device tags if configured to do so
            if self.erase_tags:
                _LOGGER.warning(ERASE_TAGS_WARNING)
                for device in devices:
                    await self.tag_eraser_coordinator.async_erase_device_tags(
                        device["serial"]
                    )
            _LOGGER.debug(f"Coordinator data before return: {self.data}")

            return combined_data
        except MerakiApiConnectionError as e:
            # Handle API connection errors
            _LOGGER.error(f"Connection error: {e}")
            raise UpdateFailed(f"Failed to connect to Meraki API: {e}")
        except MerakiApiInvalidApiKeyError as e:
            # Handle invalid API key errors
            _LOGGER.error(f"Invalid API key: {e}")
            raise ConfigEntryAuthFailed(f"Invalid Meraki API key: {e}")
        except UpdateFailed as update_error:
            # Handle generic update failures
            _LOGGER.error(f"Update failed: {update_error}")
            raise update_error
        except Exception as error:
            # Handle any other unexpected errors
            _LOGGER.exception(f"Unexpected error: {error}")
            raise UpdateFailed(f"Unexpected error: {error}")

    async def _async_shutdown(self):
        """Perform any cleanup needed when the coordinator is shut down."""
        # This coordinator currently has no specific shutdown tasks.
        pass

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of a config entry.

        This method is called by Home Assistant after the config entry is set up.
        It triggers an initial data fetch.
        """
        try:
            await super().async_config_entry_first_refresh()
        finally:
            # Ensure any resources are cleaned up if needed, though not currently used.
            pass
