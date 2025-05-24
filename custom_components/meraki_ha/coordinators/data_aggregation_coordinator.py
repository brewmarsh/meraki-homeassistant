"""Coordinates the aggregation of data from various Meraki sources.

This module defines the `DataAggregationCoordinator`, a Home Assistant
`DataUpdateCoordinator` responsible for orchestrating the collection and
combination of data related to Meraki devices, SSIDs, networks, and device tags.
It utilizes a `DataAggregator` to perform the actual merging and processing.
"""

import logging
from typing import Dict, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .data_aggregator import DataAggregator
from .data_processor import MerakiDataProcessor
from ..helpers.ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregationCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Orchestrates the aggregation of data from various Meraki sources.

    This coordinator takes data fetched by other, more specialized coordinators
    (e.g., for devices, SSIDs, networks, tags) and uses a `DataAggregator`
    instance to combine this information into a unified structure. This
    aggregated data is then made available to the integration's entities.

    Attributes:
        relaxed_tag_match (bool): Indicates if relaxed tag matching logic
            should be used during aggregation.
        data_processor (MerakiDataProcessor): An instance of `MerakiDataProcessor`
            used by the aggregator for processing raw data.
        ssid_status_calculator (SsidStatusCalculator): An instance of
            `SsidStatusCalculator` used by the aggregator.
        data_aggregator (DataAggregator): The core component responsible for
            the actual data aggregation logic.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        scan_interval: timedelta,
        relaxed_tag_match: bool,
    ) -> None:
        """Initializes the DataAggregationCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            scan_interval (timedelta): The interval at which this coordinator
                should attempt to update its data.
            relaxed_tag_match (bool): Specifies whether to use relaxed tag
                matching rules during data aggregation.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data Aggregation",  # Name for logging and diagnostics
            update_interval=scan_interval,
        )
        self.relaxed_tag_match = relaxed_tag_match
        # Initialize helper components required by the DataAggregator
        self.data_processor = MerakiDataProcessor()
        self.ssid_status_calculator = SsidStatusCalculator()
        # Initialize the DataAggregator with its dependencies
        self.data_aggregator = DataAggregator(
            relaxed_tag_match=self.relaxed_tag_match,
            data_processor=self.data_processor,
            ssid_status_calculator=self.ssid_status_calculator,
        )

    async def _async_update_data(
        self,
        device_data: Dict[str, Any],
        ssid_data: Dict[str, Any],
        network_data: Dict[str, Any],
        device_tags: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Fetches (or receives) and aggregates data from Meraki sources.

        This method is the core logic of the coordinator. It takes data from
        various sources (presumably fetched by other coordinators and passed here)
        and uses the `DataAggregator` to combine them.

        Args:
            device_data (Dict[str, Any]): Raw data related to Meraki devices.
            ssid_data (Dict[str, Any]): Raw data related to Meraki SSIDs.
            network_data (Dict[str, Any]): Raw data related to Meraki networks.
            device_tags (Dict[str, Any]): Data related to tags associated with devices.

        Returns:
            Dict[str, Any]: A dictionary containing the aggregated data. Returns
                an empty dictionary if essential input data is missing.

        Raises:
            UpdateFailed: If any unexpected error occurs during the aggregation process.
        """
        try:
            # Validate that essential data inputs are not None.
            # If any core data is missing, aggregation cannot proceed meaningfully.
            if device_data is None or ssid_data is None or network_data is None:
                _LOGGER.warning(
                    "One or more essential data sources (device, SSID, or network) is None. "
                    "Cannot perform aggregation."
                )
                return {}  # Return an empty dict to prevent errors downstream.

            _LOGGER.debug(
                "DataAggregationCoordinator received input data: device_data keys: %s, "
                "ssid_data keys: %s, network_data keys: %s, device_tags keys: %s",
                device_data.keys() if device_data else "None",
                ssid_data.keys() if ssid_data else "None",
                network_data.keys() if network_data else "None",
                device_tags.keys() if device_tags else "None",
            )

            # Perform data aggregation using the DataAggregator instance.
            aggregated_data = await self.data_aggregator.aggregate_data(
                device_data, ssid_data, network_data, device_tags
            )
            _LOGGER.debug("Successfully aggregated data. Result keys: %s", aggregated_data.keys())
            return aggregated_data

        except Exception as e:
            # Catch any other unexpected errors during aggregation.
            _LOGGER.exception("Error during data aggregation: %s", e)
            raise UpdateFailed(f"Error aggregating data: {e}") from e
