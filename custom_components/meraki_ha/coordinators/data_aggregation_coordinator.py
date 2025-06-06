"""Data Aggregation Coordinator for the Meraki Home Assistant integration.

This module defines `DataAggregationCoordinator`, responsible for taking raw
data fetched by `MerakiApiDataFetcher` (devices with tags, SSIDs, networks),
processing it using `MerakiDataProcessor`, and then aggregating it into a
unified structure with `DataAggregator`. This final structure is used by
Home Assistant entities.
"""

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

# SsidStatusCalculator is used by DataAggregator, not directly here.
from custom_components.meraki_ha.coordinators.data_aggregator import DataAggregator
from custom_components.meraki_ha.coordinators.data_processor import MerakiDataProcessor

if TYPE_CHECKING:
    # To avoid circular import issues, type hint the parent coordinator.
    from custom_components.meraki_ha.coordinators.base_coordinator import (
        MerakiDataUpdateCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class DataAggregationCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Aggregates raw Meraki data from various sources into a structured format.

    This coordinator is called by `MerakiDataUpdateCoordinator` (the parent)
    with raw data lists for devices, SSIDs, and networks. It uses
    `MerakiDataProcessor` to transform this raw data into a standardized format
    and then `DataAggregator` to combine it and calculate SSID statuses.
    Device tags are expected to be included within the `device_data`.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        scan_interval: timedelta,  # For DataUpdateCoordinator superclass
        relaxed_tag_match: bool,  # For DataAggregator configuration
        coordinator: "MerakiDataUpdateCoordinator",  # Parent coordinator instance
    ) -> None:
        """Initialize the DataAggregationCoordinator.

        Args:
            hass: The Home Assistant instance.
            scan_interval: The interval for updating data (passed to superclass).
                           This coordinator updates when `_async_update_data` is called.
            relaxed_tag_match: Boolean indicating if relaxed tag matching is enabled
                               for SSID status calculation.
            coordinator: The main `MerakiDataUpdateCoordinator` instance, providing
                         context (e.g., for MerakiDataProcessor).
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data Aggregation Coordinator",  # More specific name
            update_interval=scan_interval,
            # For DataUpdateCoordinator's scheduling if used independently.
        )
        self.relaxed_tag_match: bool = relaxed_tag_match
        # Store parent coordinator
        self.coordinator: "MerakiDataUpdateCoordinator" = coordinator

        # Initialize helper classes for data processing and aggregation.
        # MerakiDataProcessor handles initial structuring of raw data.
        self.data_processor: MerakiDataProcessor = MerakiDataProcessor(
            # Pass parent for context if needed by processor.
            coordinator=self.coordinator
        )

        # Initialize SsidStatusCalculator first
        from custom_components.meraki_ha.helpers.ssid_status_calculator import (
            SsidStatusCalculator,
        )
        self.ssid_status_calculator: SsidStatusCalculator = SsidStatusCalculator()

        # DataAggregator combines processed data and calculates SSID statuses.
        # It no longer takes data_processor as an argument.
        self.data_aggregator: DataAggregator = DataAggregator(
            relaxed_tag_match=self.relaxed_tag_match,
            ssid_status_calculator=self.ssid_status_calculator,
        )

        # Ensure `self.data` (from DataUpdateCoordinator) is initialized.
        self.data: Dict[str, Any] = {}

    async def _async_update_data(
        self,
        # Raw device data from ApiDataFetcher
        device_data: Optional[List[Dict[str, Any]]],
        # Raw SSID data from ApiDataFetcher
        ssid_data: Optional[List[Dict[str, Any]]],
        # Raw network data from ApiDataFetcher
        network_data: Optional[List[Dict[str, Any]]],
        client_data: Optional[List[Dict[str, Any]]],
        network_client_counts: Optional[Dict[str, int]],
        clients_on_ssids: int = 0,
        clients_on_appliances: int = 0,
        clients_on_wireless: int = 0,
        # The `device_tags` parameter has been removed; tags are in
        # `device_data`.
    ) -> Dict[str, Any]:
        """Process and aggregate raw Meraki data.

        This method is called by the parent `MerakiDataUpdateCoordinator` with the latest
        raw data fetched by `MerakiApiDataFetcher`. It uses `MerakiDataProcessor`
        to structure this data and `DataAggregator` to combine it and determine
        SSID operational statuses.

        Args:
            device_data: A list of raw device dictionaries from the API.
                         Expected to include tags and MR-specific details.
                         Can be None if initial fetching failed.
            ssid_data: A list of raw SSID dictionaries from the API.
                       Can be None if initial fetching failed.
            network_data: A list of raw network dictionaries from the API.
                          Can be None if initial fetching failed.

        Returns:
            A dictionary containing the aggregated and processed data, ready for
            use by Home Assistant entities. Returns an empty dictionary if
            essential input data is missing or an error occurs.

        Raises:
            UpdateFailed: If a significant error occurs during data processing
                          or aggregation that prevents a meaningful update.
        """
        _LOGGER.debug(
            "DataAggregationCoordinator received raw data. Processing and aggregating..."
        )
        try:
            # Validate that essential input data is available.
            if device_data is None or ssid_data is None or network_data is None:
                _LOGGER.warning(
                    "Essential data (devices, SSIDs, or networks) is None. "
                    "Skipping aggregation and returning empty data."
                )
                # Return empty dict to prevent errors in consuming entities.
                return {}

            # Step 1: Process raw device data using MerakiDataProcessor.
            # This standardizes the device structure.
            processed_devices: List[Dict[str, Any]] = []
            if isinstance(device_data, list):
                processed_devices = await self.data_processor.process_devices(
                    device_data
                )
                # The loop that previously iterated here to log MX devices (and before that, filter MR-only)
                # has been removed as it currently serves no purpose.
                # If specific processing for MX devices (or others) is needed at this stage in the future,
                # it can be re-added here.
            else:
                _LOGGER.warning(
                    "Device data is not a list as expected: %s. Proceeding with empty processed_devices.",
                    type(device_data),
                )

            # Step 2: Process raw network data.
            processed_networks: List[Dict[str, Any]] = []
            if isinstance(network_data, list):
                processed_networks = self.data_processor.process_networks(network_data)
            else:
                _LOGGER.warning(
                    "Network data is not a list as expected: %s. Proceeding with empty processed_networks.",
                    type(network_data),
                )

            # Step 3: Process raw SSID data.
            processed_ssids: List[Dict[str, Any]] = []
            if isinstance(ssid_data, list):
                processed_ssids = self.data_processor.process_ssids(ssid_data)
            else:
                _LOGGER.warning(
                    "SSID data is not a list as expected: %s. Proceeding with empty processed_ssids.",
                    type(ssid_data),
                )

            # Note: Device tags are now part of `processed_devices` due to changes in
            # `MerakiApiDataFetcher` and `MerakiDataProcessor`.
            # The separate `device_tags` parameter is no longer needed here or
            # in `DataAggregator`.

            # Step 4: Aggregate all processed data using DataAggregator.
            # `DataAggregator.aggregate_data` now expects devices to contain their tags.
            aggregated_data: Dict[str, Any] = await self.data_aggregator.aggregate_data(
                processed_devices,
                # Contains device info, including tags and MR-specific details.
                processed_ssids,
                processed_networks,
                client_data,
                network_client_counts,
                clients_on_ssids=clients_on_ssids,
                clients_on_appliances=clients_on_appliances,
                clients_on_wireless=clients_on_wireless,
                # The fourth `device_tags` argument was removed from
                # DataAggregator.
            )

            _LOGGER.debug(
                "Data aggregation successful. Processed %d devices (passed to aggregator), %d SSIDs, %d networks.",
                len(processed_devices),
                len(processed_ssids),
                len(processed_networks),
            )
            return aggregated_data

        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception("Error during Meraki data aggregation: %s", e)
            # Raise UpdateFailed to signal the main coordinator that this
            # update cycle failed.
            raise UpdateFailed(f"Error aggregating Meraki data: {e}") from e
