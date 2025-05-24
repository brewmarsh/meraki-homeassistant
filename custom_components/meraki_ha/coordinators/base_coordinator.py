"""Base data update coordinator for the Meraki Home Assistant integration.

This module defines the `MerakiDataUpdateCoordinator`, which is the primary
coordinator responsible for orchestrating data fetching and updates from the
Meraki API. It manages several sub-coordinators for specific data types
like networks, SSIDs, devices, and tags.
"""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional # Added Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN, ERASE_TAGS_WARNING # Added DOMAIN
from .api_data_fetcher import MerakiApiDataFetcher, MerakiApiError
from .data_aggregation_coordinator import DataAggregationCoordinator
from .device_tag_fetch_coordinator import DeviceTagFetchCoordinator
from .network_coordinator import MerakiNetworkCoordinator
from .ssid_coordinator import MerakiSsidCoordinator
from .tag_eraser_coordinator import TagEraserCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator to fetch and manage data from the Meraki API.

    This coordinator is responsible for the overall data flow, utilizing
    an API fetcher and several specialized sub-coordinators to gather
    and process information from the Meraki cloud.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        # base_url: str, # Appears unused in favor of constructing URLs in api_fetcher
        scan_interval: timedelta,
        networks_coordinator: MerakiNetworkCoordinator,
        ssid_coordinator: MerakiSsidCoordinator,
        relaxed_tag_match: bool,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki data update coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            scan_interval: The interval at which to update data.
            networks_coordinator: Coordinator for network-specific data.
            ssid_coordinator: Coordinator for SSID-specific data.
            relaxed_tag_match: Boolean indicating if relaxed tag matching is enabled.
            config_entry: The config entry associated with this coordinator.
        """
        # Store essential configuration and context passed from async_setup_entry
        self.api_key: str = api_key
        self.org_id: str = org_id
        # self.base_url: str = base_url # Base URL is generally handled by MerakiApiDataFetcher now.
        self.networks_coordinator: MerakiNetworkCoordinator = networks_coordinator
        self.ssid_coordinator: MerakiSsidCoordinator = ssid_coordinator
        self.config_entry: ConfigEntry = config_entry # Store the config entry for access to options, entry_id
        self.relaxed_tag_match: bool = relaxed_tag_match
        # Determine if the "erase_tags" option is enabled from the config entry's options.
        self.erase_tags: bool = config_entry.options.get("erase_tags", False)

        # Initialize the main API data fetcher.
        # This fetcher is responsible for making the actual calls to the Meraki API.
        # It's given references to network and SSID coordinators, possibly to allow it
        # to directly update them or use their data, though this pattern is less common
        # if this MerakiDataUpdateCoordinator is the primary orchestrator.
        self.api_fetcher: MerakiApiDataFetcher = MerakiApiDataFetcher(
            api_key, org_id, self.networks_coordinator, self.ssid_coordinator
        )

        # Initialize specialized sub-coordinators.
        # These coordinators might handle specific aspects of data processing or fetching.
        # DataAggregationCoordinator likely combines data from various sources.
        self.data_aggregation_coordinator: DataAggregationCoordinator = (
            DataAggregationCoordinator(
                hass,
                scan_interval, # Pass the main scan_interval, or a specific one if needed
                relaxed_tag_match, # Pass tag matching preference
                self, # Pass self (this MerakiDataUpdateCoordinator) as the parent/main coordinator
            )
        )
        # DeviceTagFetchCoordinator is responsible for fetching tags for devices.
        self.device_tag_fetch_coordinator: DeviceTagFetchCoordinator = (
            DeviceTagFetchCoordinator(
                hass,
                api_key, # Assuming it needs direct API access for tags
                scan_interval, # Use main scan_interval or a specific one for tags
                self, # Pass self as the parent/main coordinator
            )
        )
        # TagEraserCoordinator is initialized only if the 'erase_tags' option is true.
        # This coordinator would handle the logic for removing tags from devices.
        self.tag_eraser_coordinator: Optional[TagEraserCoordinator] = None
        if self.erase_tags: # Conditional initialization based on user option
            self.tag_eraser_coordinator = TagEraserCoordinator(
                hass,
                api_key, # Needs API key for write operations
                org_id,  # Needs org ID for context
                # base_url, # Potentially needed if it makes direct API calls not via api_fetcher
            )
            _LOGGER.warning(ERASE_TAGS_WARNING) # Log a warning if tag erasing is enabled.


        # Initialize internal data stores.
        # `device_data` will store the list of processed devices.
        # Data for SSIDs and networks are primarily managed by their respective coordinators.
        self.device_data: List[Dict[str, Any]] = []
        # self.ssid_data: List[Dict[str, Any]] = [] # Data now managed by self.ssid_coordinator.data
        # self.network_data: List[Dict[str, Any]] = [] # Data now managed by self.networks_coordinator.data

        # Call the superclass constructor to complete DataUpdateCoordinator initialization.
        # This sets up periodic updates via `_async_update_data`.
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({org_id})", # A descriptive name for logging, including domain and org_id
            update_interval=scan_interval, # The interval for calling `_async_update_data`
        )
        # Ensure `self.data` (the main data store for CoordinatorEntity) is initialized.
        # Its structure should match the generic type `Dict[str, Any]`.
        self.data: Dict[str, Any] = {}


    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from the Meraki API endpoint and process it.

        This method orchestrates the fetching of all data (networks, devices, SSIDs),
        retrieves device tags, aggregates the data, and handles tag erasing if enabled.
        This is the primary method called by the DataUpdateCoordinator's schedule.

        Returns:
            A dictionary containing the combined and processed data for the integration.
            This data is then made available to entities via `self.data`.

        Raises:
            UpdateFailed: If there is a critical error in fetching or processing data
                          that prevents the integration from updating.
        """
        _LOGGER.debug("Starting Meraki data update for organization ID: %s", self.org_id)
        try:
            # Step 1: Fetch all primary data (networks, devices, SSIDs, clients) using the api_fetcher.
            # Arguments like hass, org_id are passed. `update_interval` and `device_name_format`
            # seem not to be directly used by `fetch_all_data` itself but might be used by
            # methods it calls internally if they were part of its class structure.
            all_data: Dict[str, Any] = await self.api_fetcher.fetch_all_data(
                self.hass, # Pass HomeAssistant instance
                self.org_id, # Pass organization ID
                # scan_interval parameter for fetch_all_data was removed in its definition
                # device_name_format parameter for fetch_all_data was removed in its definition
            )
        except MerakiApiError as e: # Handle specific API errors from the fetcher
            _LOGGER.error("API error during Meraki data fetch: %s", e)
            raise UpdateFailed(f"Failed to fetch data from Meraki API: {e}") from e
        except Exception as e: # Catch any other unexpected errors during the main fetch
            _LOGGER.exception("Unexpected error during Meraki data fetch: %s", e)
            raise UpdateFailed(f"Unexpected error fetching data: {e}") from e

        # Extract different data types from the `all_data` dictionary.
        # Default to empty lists if keys are missing to prevent KeyErrors.
        devices: List[Dict[str, Any]] = all_data.get("devices", [])
        ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
        networks: List[Dict[str, Any]] = all_data.get("networks", [])

        # Step 2: Fetch device tags for each discovered device.
        # This involves iterating through devices and calling the device_tag_fetch_coordinator.
        device_tags: Dict[str, List[str]] = {} # Stores tags keyed by device serial
        for device in devices:
            serial: str = device.get("serial", "") # Get device serial, default to empty string if missing
            if not serial: # Skip if device has no serial number
                _LOGGER.warning("Device found without a serial number: %s", device)
                continue
            try:
                # Fetch tags for the current device using its serial number.
                tags = (
                    await self.device_tag_fetch_coordinator.async_get_device_tags(
                        serial
                    )
                )
                device_tags[serial] = tags # Store tags associated with the serial
                device["tags"] = tags  # Add/update the 'tags' key directly in the device's dictionary
            except MerakiApiError as e: # Handle API errors during tag fetching for a single device
                _LOGGER.warning(
                    "Failed to fetch tags for device %s: %s. Proceeding without its tags.",
                    serial,
                    e,
                )
                device["tags"] = [] # Ensure 'tags' key exists, even if empty, for consistency
            # Note: UpdateFailed from async_get_device_tags might halt the entire update if not caught here.
            # Depending on design, individual tag fetch failures might be tolerated.

        # Step 3: Update data in sub-coordinators (networks_coordinator, ssid_coordinator).
        # This allows entities associated with these sub-coordinators to access the latest data.
        # This assumes these coordinators are primarily data holders or their own refresh logic
        # is supplemental to this central update.
        if self.networks_coordinator:
            self.networks_coordinator.data = networks # Set the fetched networks data
        if self.ssid_coordinator:
            self.ssid_coordinator.data = ssids # Set the fetched SSIDs data
            # Provide network data to ssid_coordinator if it needs this for context (e.g., linking SSIDs to network names).
            self.ssid_coordinator.networks = networks

        # Store the centrally fetched and processed list of devices in `self.device_data`.
        # This can be useful if other parts of this coordinator or integration need quick access
        # to the device list without going through `self.data` or `all_data`.
        self.device_data = devices

        # Step 4: Aggregate all fetched and processed data using the DataAggregationCoordinator.
        # This coordinator combines device data, SSID data (from its coordinator),
        # network data (from its coordinator), and device tags into a final structured dictionary.
        try:
            combined_data: Dict[
                str, Any
            ] = await self.data_aggregation_coordinator._async_update_data(
                self.device_data, # Pass the processed device list
                self.ssid_coordinator.data if self.ssid_coordinator else [], # Pass SSID data
                self.networks_coordinator.data if self.networks_coordinator else [], # Pass network data
                device_tags, # Pass the fetched device tags
            )
        except Exception as e: # Catch errors specifically from the aggregation step
            _LOGGER.exception("Error during data aggregation: %s", e)
            raise UpdateFailed(f"Failed to aggregate Meraki data: {e}") from e

        # Step 5: Update the main `self.data` attribute of this coordinator.
        # This is the data that entities listening to this coordinator will receive.
        self.data = combined_data
        # Optional: Explicitly include the raw devices list in self.data if needed by some entities directly,
        # though it might be redundant if the aggregation coordinator already includes it appropriately.
        # self.data["devices"] = devices

        _LOGGER.debug(
            "Meraki data update completed. %d devices, %d SSIDs, %d networks processed.",
            len(devices),
            len(ssids),
            len(networks),
        )

        # Step 6: Handle tag erasing if the feature is enabled.
        # This iterates through devices and calls the tag_eraser_coordinator for each.
        if self.erase_tags and self.tag_eraser_coordinator:
            _LOGGER.warning(
                "Tag erasing is enabled for organization %s. Processing devices for tag removal.",
                 self.org_id
            )
            for device in devices: # Iterate through the same device list
                serial = device.get("serial")
                if serial: # Ensure serial exists
                    try:
                        # Call the tag eraser to remove tags from the device.
                        await self.tag_eraser_coordinator.async_erase_device_tags(
                            serial
                        )
                    except MerakiApiError as e: # Handle errors during tag erasing for a single device
                        _LOGGER.error(
                            "Failed to erase tags for device %s: %s", serial, e
                        )
        # Return the final, combined data that will be stored in `self.data`.
        return self.data

    async def _async_shutdown(self) -> None:
        """Clean up resources when the coordinator is shut down.

        This method can be used to cancel any ongoing tasks or close connections.
        """
        _LOGGER.debug("MerakiDataUpdateCoordinator shutting down for org %s.", self.org_id)
        # Perform any necessary cleanup, e.g., cancel listeners or tasks
        # (Currently, DataUpdateCoordinator handles listener removal automatically)
        await super()._async_shutdown()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of the config entry.

        This is called by Home Assistant after the config entry has been set up
        to perform an initial data fetch.
        """
        _LOGGER.debug(
            "Performing first data refresh for Meraki config entry (org %s).",
            self.org_id
        )
        await super().async_config_entry_first_refresh()
        _LOGGER.debug("First data refresh completed for org %s.", self.org_id)
