"""Base data update coordinator for the Meraki Home Assistant integration.

This module defines the `MerakiDataUpdateCoordinator`, which is the
primary coordinator responsible for orchestrating data fetching and
updates from the Meraki API. It manages several sub-coordinators for
specific data types like networks, SSIDs, devices, and tags.
"""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional  # Added Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN, ERASE_TAGS_WARNING  # Added DOMAIN
from .api_data_fetcher import MerakiApiDataFetcher, MerakiApiError
from .data_aggregation_coordinator import DataAggregationCoordinator
# DeviceTagFetchCoordinator is no longer used
# MerakiNetworkCoordinator and MerakiSsidCoordinator are no longer used
from .tag_eraser_coordinator import TagEraserCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator to fetch and manage data from the Meraki API.

    This coordinator is responsible for the overall data flow, utilizing an
    API fetcher and a data aggregation sub-coordinator to gather and process
    information from the Meraki cloud. Device tags, network data, and SSID data
    are all fetched by MerakiApiDataFetcher and passed directly to the
    DataAggregationCoordinator.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
            # base_url: str,  # Unused; URLs constructed in api_fetcher
        scan_interval: timedelta,
        # networks_coordinator and ssid_coordinator parameters removed
        relaxed_tag_match: bool,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki data update coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            scan_interval: The interval at which to update data.
            # networks_coordinator and ssid_coordinator parameters removed
            relaxed_tag_match: Boolean for relaxed tag matching.
            config_entry: The config entry for this coordinator.
        """
        # Store essential configuration and context
        self.api_key: str = api_key
        self.org_id: str = org_id
        # self.base_url: str = base_url  # Handled by MerakiApiDataFetcher
        # self.networks_coordinator and self.ssid_coordinator attributes removed
        # Store config entry for access to options, entry_id
        self.config_entry: ConfigEntry = config_entry
        self.relaxed_tag_match: bool = relaxed_tag_match
        # Determine if "erase_tags" option is enabled
        self.erase_tags: bool = config_entry.options.get("erase_tags", False)

        # Initialize the MerakiAPIClient
        # This client will be used by the api_fetcher.
        # It's important to store it here so its close() method can be called on unload.
        from ..meraki_api import MerakiAPIClient # Import here to avoid circular dependency at module level if not careful
        self.meraki_client: MerakiAPIClient = MerakiAPIClient(
            api_key=api_key,
            org_id=org_id
            # Add other necessary params for MerakiAPIClient if any (e.g., base_url, though SDK handles it)
        )

        # Initialize the main API data fetcher, passing the created client
        # The MerakiApiDataFetcher __init__ was updated to take meraki_client as first arg
        self.api_fetcher: MerakiApiDataFetcher = MerakiApiDataFetcher(
            meraki_client=self.meraki_client,
            # network_coordinator and ssid_coordinator arguments removed
        )

        # Initialize specialized sub-coordinators.
        # These might handle specific aspects of data processing or fetching.
        # DataAggregationCoordinator likely combines data from various sources.
        self.data_aggregation_coordinator: DataAggregationCoordinator = (
            DataAggregationCoordinator(
                hass,
                scan_interval,  # Pass main scan_interval, or specific if needed
                relaxed_tag_match,  # Pass tag matching preference
                self,  # Pass self as parent/main coordinator
            )
        )
        # DeviceTagFetchCoordinator is no longer used as tags are fetched with device data.
        # TagEraserCoordinator handles removing tags from devices.
        # Initialized only if 'erase_tags' option is true.
        self.tag_eraser_coordinator: Optional[TagEraserCoordinator] = None
        if self.erase_tags:  # Conditional initialization
            self.tag_eraser_coordinator = TagEraserCoordinator(
                hass,
                api_key,  # Needs API key for write operations
                org_id,  # Needs org ID for context
                # base_url,  # Potentially needed for direct API calls
            )
            # Log a warning if tag erasing is enabled.
            _LOGGER.warning(ERASE_TAGS_WARNING)

        # Initialize internal data stores.
        # `device_data` stores the list of processed devices.
        # SSID/network data managed by their respective coordinators.
        self.device_data: List[Dict[str, Any]] = []
        # self.ssid_data: List[Dict[str, Any]] = []  # Managed by ssid_coord
        # self.network_data: List[Dict[str, Any]] = []  # Managed by ntwk_coord

        # Call superclass constructor for DataUpdateCoordinator initialization.
        # Sets up periodic updates via `_async_update_data`.
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({org_id})",  # Descriptive name for logging
            update_interval=scan_interval,  # Interval for _async_update_data
        )
        # Ensure `self.data` (main store for CoordinatorEntity) is initialized.
        # Structure should match `Dict[str, Any]`.
        self.data: Dict[str, Any] = {}


    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from the Meraki API endpoint and process it.

        This method orchestrates the fetching of all data (networks, devices with tags, SSIDs),
        aggregates the data, and handles tag erasing if enabled.
        Device tags are now expected to be part of the device data from `api_fetcher.fetch_all_data`.
        This is the primary method called by the DataUpdateCoordinator's schedule.

        Returns:
            A dictionary containing the combined and processed data for the integration.
            This data is then made available to entities via `self.data`.

        Raises:
            UpdateFailed: If there is a critical error in fetching or processing data
                          that prevents the integration from updating.
        """
        _LOGGER.debug(
            "Starting Meraki data update for organization ID: %s", self.org_id
        )
        try:
            # Step 1: Fetch all primary data (networks, devices with tags, SSIDs,
            # clients) using the api_fetcher.
            all_data: Dict[str, Any] = await self.api_fetcher.fetch_all_data(
                self.hass,  # Pass HomeAssistant instance
                # org_id is available via self.api_fetcher.org_id, so not passed here.
                # scan_interval param for fetch_all_data was removed
                # device_name_format param for fetch_all_data was removed
            )
        except MerakiApiError as e:  # Handle specific API errors
            _LOGGER.error("API error during Meraki data fetch: %s", e)
            raise UpdateFailed(
                f"Failed to fetch data from Meraki API: {e}"
            ) from e
        except Exception as e:  # Catch other unexpected errors during main fetch
            _LOGGER.exception("Unexpected error during Meraki data fetch: %s", e)
            raise UpdateFailed(f"Unexpected error fetching data: {e}") from e

        # Extract data types from `all_data`, default to empty lists.
        # Device tags are expected to be included in the 'devices' list from fetch_all_data.
        devices: List[Dict[str, Any]] = all_data.get("devices", [])
        ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
        networks: List[Dict[str, Any]] = all_data.get("networks", [])

        # Step 2: Device tags are now part of the 'devices' list.
        # The separate fetching step for device tags is removed.

        # Step 3: Update data in sub-coordinators (Removed).
        # Network and SSID data are directly passed to DataAggregationCoordinator.

        # Store centrally fetched/processed devices list in `self.device_data`.
        # This also includes networks and ssids from all_data for aggregation.
        self.device_data = devices # Contains devices with tags, client counts, radio settings

        # Step 4: Aggregate all data using DataAggregationCoordinator.
        # Passes the raw devices, ssids, and networks lists from all_data.
        # DataAggregationCoordinator will internally use its DataProcessor.
        try:
            combined_data: Dict[
                str, Any
            ] = await self.data_aggregation_coordinator._async_update_data(
                devices,  # Pass raw device list (with tags, etc.)
                ssids,    # Pass raw SSID list
                networks, # Pass raw network list
                # The fourth (device_tags) argument was already removed from DataAggregationCoordinator
            )
        except Exception as e:  # Catch errors from aggregation step
            _LOGGER.exception("Error during data aggregation: %s", e)
            raise UpdateFailed(f"Failed to aggregate Meraki data: {e}") from e

        # Step 5: Update the main `self.data` attribute.
        # This is the data entities listening to this coordinator receive.
        self.data = combined_data
        # Optional: Explicitly include raw devices list in self.data if needed,
        # though it might be redundant if aggregation_coord includes it.
        # self.data["devices"] = devices

        _LOGGER.debug(
            "Meraki data update completed. %d devices, %d SSIDs, "
            "%d networks processed.",
            len(devices),
            len(ssids),
            len(networks),
        )

        # Step 6: Handle tag erasing if enabled.
        # Iterates devices, calls tag_eraser_coordinator for each.
        if self.erase_tags and self.tag_eraser_coordinator:
            _LOGGER.warning(
                "Tag erasing is enabled for organization %s. "
                "Processing devices for tag removal.",
                self.org_id,
            )
            for device in devices:  # Iterate through the same device list
                serial = device.get("serial")
                if serial:  # Ensure serial exists
                    try:
                        # Call tag eraser to remove tags from device.
                        await self.tag_eraser_coordinator.async_erase_device_tags(
                            serial
                        )
                    except MerakiApiError as e:  # Handle errors for single device
                        _LOGGER.error(
                            "Failed to erase tags for device %s: %s", serial, e
                        )
        # Return final, combined data to be stored in `self.data`.
        return self.data

    async def _async_shutdown(self) -> None:
        """Clean up resources when the coordinator is shut down.

        This method can be used to cancel any ongoing tasks or close
        connections.
        """
        _LOGGER.debug(
            "MerakiDataUpdateCoordinator shutting down for org %s.", self.org_id
        )
        # Perform any necessary cleanup, e.g., cancel listeners or tasks
        # (DataUpdateCoordinator handles listener removal automatically)
        await super()._async_shutdown()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of the config entry.

        This is called by Home Assistant after the config entry has been
        set up to perform an initial data fetch.
        """
        _LOGGER.debug(
            "Performing first data refresh for Meraki config entry (org %s).",
            self.org_id,
        )
        await super().async_config_entry_first_refresh()
        _LOGGER.debug(
            "First data refresh completed for org %s.", self.org_id
        )
