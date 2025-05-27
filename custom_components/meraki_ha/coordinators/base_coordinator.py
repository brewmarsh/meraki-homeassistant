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
from .device_tag_fetch_coordinator import DeviceTagFetchCoordinator
from .network_coordinator import MerakiNetworkCoordinator
from .ssid_coordinator import MerakiSsidCoordinator
from .tag_eraser_coordinator import TagEraserCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator to fetch and manage data from the Meraki API.

    This coordinator is responsible for the overall data flow, utilizing an
    API fetcher and several specialized sub-coordinators to gather and
    process information from the Meraki cloud.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
            # base_url: str,  # Unused; URLs constructed in api_fetcher
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
            relaxed_tag_match: Boolean for relaxed tag matching.
            config_entry: The config entry for this coordinator.
        """
        # Store essential configuration and context
        self.api_key: str = api_key
        self.org_id: str = org_id
        # self.base_url: str = base_url  # Handled by MerakiApiDataFetcher
        self.networks_coordinator: MerakiNetworkCoordinator = (
            networks_coordinator
        )
        self.ssid_coordinator: MerakiSsidCoordinator = ssid_coordinator
        # Store config entry for access to options, entry_id
        self.config_entry: ConfigEntry = config_entry
        self.relaxed_tag_match: bool = relaxed_tag_match
        # Determine if "erase_tags" option is enabled
        self.erase_tags: bool = config_entry.options.get("erase_tags", False)

        # Initialize the main API data fetcher.
        # This fetcher makes actual calls to the Meraki API.
        # It's given network/SSID coordinators, possibly to allow direct
        # updates or use their data, though less common if this coordinator
        # is the primary orchestrator.
        self.api_fetcher: MerakiApiDataFetcher = MerakiApiDataFetcher(
            api_key, org_id, self.networks_coordinator, self.ssid_coordinator
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
        # DeviceTagFetchCoordinator fetches tags for devices.
        self.device_tag_fetch_coordinator: DeviceTagFetchCoordinator = (
            DeviceTagFetchCoordinator(
                hass,
                api_key,  # Assuming direct API access for tags
                scan_interval,  # Use main or specific scan_interval for tags
                self,  # Pass self as parent/main coordinator
            )
        )
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
        _LOGGER.debug(
            "Starting Meraki data update for organization ID: %s", self.org_id
        )
        try:
            # Step 1: Fetch all primary data (networks, devices, SSIDs,
            # clients) using the api_fetcher. Arguments like hass, org_id are
            # passed. `update_interval` and `device_name_format` seem not
            # directly used by `fetch_all_data` itself but might be used by
            # methods it calls internally if they were part of its class.
            all_data: Dict[str, Any] = await self.api_fetcher.fetch_all_data(
                self.hass,  # Pass HomeAssistant instance
                self.org_id,  # Pass organization ID
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
        devices: List[Dict[str, Any]] = all_data.get("devices", [])
        ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
        networks: List[Dict[str, Any]] = all_data.get("networks", [])

        # Step 2: Fetch device tags for each discovered device.
        # Iterate devices, call device_tag_fetch_coordinator.
        device_tags: Dict[str, List[str]] = {}  # Tags keyed by device serial
        for device in devices:
            # Get device serial, default to empty string
            serial: str = device.get("serial", "")
            if not serial:  # Skip if device has no serial number
                _LOGGER.warning("Device found without a serial number: %s", device)
                continue
            try:
                # Fetch tags for the current device using its serial.
                tags = await self.device_tag_fetch_coordinator.async_get_device_tags(
                    serial
                )
                device_tags[serial] = tags  # Store tags for the serial
                # Add/update 'tags' key in the device's dictionary
                device["tags"] = tags
            except MerakiApiError as e:  # Handle API errors for single device
                _LOGGER.warning(
                    "Failed to fetch tags for device %s: %s. "
                    "Proceeding without its tags.",
                    serial,
                    e,
                )
                # Ensure 'tags' key exists for consistency
                device["tags"] = []
            # Note: UpdateFailed from async_get_device_tags might halt the
            # entire update if not caught here. Design for tolerance.

        # Step 3: Update data in sub-coordinators.
        # Allows entities associated with these sub-coordinators to access
        # latest data. Assumes these coordinators are primarily data holders
        # or their own refresh logic is supplemental.
        if self.networks_coordinator:
            self.networks_coordinator.data = networks  # Set networks data
        if self.ssid_coordinator:
            self.ssid_coordinator.data = ssids  # Set SSIDs data
            # Provide network data to ssid_coordinator if needed for context
            # (e.g., linking SSIDs to network names).
            self.ssid_coordinator.networks = networks

        # Store centrally fetched/processed devices list in `self.device_data`.
        # Useful if other parts of coordinator/integration need quick access.
        self.device_data = devices

        # Step 4: Aggregate all data using DataAggregationCoordinator.
        # Combines device data, SSID data (from its coordinator), network data
        # (from its coordinator), and device tags into a final structure.
        try:
            combined_data: Dict[
                str, Any
            ] = await self.data_aggregation_coordinator._async_update_data(
                self.device_data,  # Pass processed device list
                self.ssid_coordinator.data if self.ssid_coordinator else [],
                self.networks_coordinator.data if self.networks_coordinator else [],
                device_tags,  # Pass fetched device tags
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
