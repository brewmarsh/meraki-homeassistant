"""Data Aggregation Coordinator for the Meraki Home Assistant integration.

This module defines the `DataAggregationCoordinator`, which is responsible for
collecting data from various other coordinators (like device, SSID, network)
and device tags, then processing and aggregating this data into a unified
structure. It utilizes `DataAggregator` for the aggregation logic and
`MerakiDataProcessor` for initial data processing.
"""
import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..helpers.ssid_status_calculator import SsidStatusCalculator
from .data_aggregator import DataAggregator
from .data_processor import MerakiDataProcessor

if TYPE_CHECKING:
    # To avoid circular import issues, type hint MerakiDataUpdateCoordinator
    # only during static analysis.
    from .base_coordinator import MerakiDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


class DataAggregationCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator to aggregate data from various Meraki data sources.

    This coordinator doesn't fetch data itself but relies on data passed
    to its `_async_update_data` method, which is typically called by a
    parent coordinator (`MerakiDataUpdateCoordinator`). It processes and
    aggregates device, SSID, network, and tag information.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        scan_interval: timedelta,
        relaxed_tag_match: bool,
        # The parent coordinator instance
        coordinator: "MerakiDataUpdateCoordinator",
    ) -> None:
        """Initialize the DataAggregationCoordinator.

        Args:
            hass: The Home Assistant instance.
            scan_interval: The interval for updating data. Note that this
                coordinator updates when its `_async_update_data` is
                called, so this interval might be more for consistency or
                if it were to schedule its own updates.
            relaxed_tag_match: Boolean indicating if relaxed tag matching
                               is enabled.
            coordinator: The main MerakiDataUpdateCoordinator instance,
                         used to access shared data or services if needed.
        """
        super().__init__(
            hass,
            _LOGGER,
            # Consider making name more specific if multiple instances
            name="Meraki Data Aggregation",
            update_interval=scan_interval,
        )
        self.relaxed_tag_match: bool = relaxed_tag_match
        # The parent coordinator instance
        self.coordinator: "MerakiDataUpdateCoordinator" = coordinator

        # Initialize helper classes for data processing and aggregation
        self.data_processor: MerakiDataProcessor = MerakiDataProcessor(
            coordinator=self.coordinator
        )
        self.ssid_status_calculator: SsidStatusCalculator = SsidStatusCalculator()
        self.data_aggregator: DataAggregator = DataAggregator(
            relaxed_tag_match=self.relaxed_tag_match,
            data_processor=self.data_processor,
            ssid_status_calculator=self.ssid_status_calculator,
        )
        # Ensure self.data is initialized as per DataUpdateCoordinator's
        # generic type
        self.data: Dict[str, Any] = {}

    async def _async_update_data(
        self,
        device_data: Optional[List[Dict[str, Any]]],
        ssid_data: Optional[List[Dict[str, Any]]],
        network_data: Optional[List[Dict[str, Any]]],
        device_tags: Optional[Dict[str, List[str]]],
    ) -> Dict[str, Any]:
        """Fetch (from other coordinators) and aggregate data.

        This method is called by the parent `MerakiDataUpdateCoordinator`
        with the latest fetched data. It processes this data and then
        aggregates it.

        Args:
            device_data: A list of dictionaries, where each dictionary
                represents a Meraki device. Can be None if data is missing.
            ssid_data: A list of dictionaries, where each dictionary
                represents an SSID. Can be None if data is missing.
            network_data: A list of dictionaries, where each dictionary
                represents a network. Can be None if data is missing.
            device_tags: A dictionary mapping device serial numbers to their
                         tags. Can be None if data is missing.

        Returns:
            A dictionary containing the aggregated data. Returns an empty
            dictionary if essential input data (devices, SSIDs, networks)
            is missing.

        Raises:
            UpdateFailed: If a significant error occurs during data processing
                          or aggregation.
        """
        _LOGGER.debug(
            "DataAggregationCoordinator attempting to update with provided data."
        )
        try:
            # Validate that essential data is provided
            if device_data is None or ssid_data is None or network_data is None:
                _LOGGER.warning(
                    "One or more essential data sources (devices, SSIDs, "
                    "networks) is None. Skipping aggregation."
                )
                # Return empty dict to prevent errors down the line
                return {}

            # Process devices: filter for wireless APs (model starting with "MR")
            processed_devices: List[Dict[str, Any]] = []
            if isinstance(device_data, list):
                # Assuming process_devices is async as per original 'await'
                processed_devices = (
                    await self.data_processor.process_devices(device_data)
                )
                # Filter for Meraki wireless APs (Access Points)
                processed_devices = [
                    device
                    for device in processed_devices
                    if device.get("model", "").upper().startswith("MR")
                ]
            else:
                _LOGGER.warning(
                    "Device data is not a list as expected: %s",
                    type(device_data),
                )

            # Process networks
            processed_networks: List[Dict[str, Any]] = []
            if isinstance(network_data, list):
                processed_networks = self.data_processor.process_networks(network_data)
            else:
                _LOGGER.warning(
                    "Network data is not a list as expected: %s",
                    type(network_data),
                )

            # Process SSIDs
            processed_ssids: List[Dict[str, Any]] = []
            if isinstance(ssid_data, list):
                processed_ssids = self.data_processor.process_ssids(ssid_data)
            else:
                _LOGGER.warning(
                    "SSID data is not a list as expected: %s", type(ssid_data)
                )

            # Device tags can be None, DataAggregator should handle it
            if device_tags is None:
                _LOGGER.warning(
                    "Device tags data is None. Proceeding without tags."
                )
                device_tags = {}
            # Aggregate data using the DataAggregator
            # Assuming aggregate_data is async as per original 'await'
            aggregated_data: Dict[
                str, Any
            ] = await self.data_aggregator.aggregate_data(
                processed_devices,
                processed_ssids,
                processed_networks,
                device_tags,
            )

            _LOGGER.debug(
                "Data aggregation successful. Processed %d devices, %d SSIDs, "
                "%d networks.",
                len(processed_devices),
                len(processed_ssids),
                len(processed_networks),
            )
            return aggregated_data

        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception("Error aggregating Meraki data: %s", e)
            raise UpdateFailed(f"Error aggregating data: {e}") from e
