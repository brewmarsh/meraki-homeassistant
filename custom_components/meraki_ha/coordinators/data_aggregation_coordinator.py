"""Data Aggregation Coordinator for the meraki_ha integration."""

import logging
from typing import Dict, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .data_aggregator import DataAggregator
from .data_processor import MerakiDataProcessor
from ..helpers.ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregationCoordinator(DataUpdateCoordinator):
    """
    Coordinator to aggregate data from Meraki coordinators.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        scan_interval: timedelta,
        relaxed_tag_match: bool,
    ) -> None:
        """
        Initialize the DataAggregationCoordinator.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data Aggregation",
            update_interval=scan_interval,
        )
        self.relaxed_tag_match = relaxed_tag_match
        self.data_processor = MerakiDataProcessor()
        self.ssid_status_calculator = SsidStatusCalculator()
        self.data_aggregator = DataAggregator(
            relaxed_tag_match=relaxed_tag_match,
            data_processor=self.data_processor,
            ssid_status_calculator=self.ssid_status_calculator,
        )

    async def _async_update_data(
        self, device_data, ssid_data, network_data, device_tags
    ) -> Dict[str, Any]:
        """Fetch and aggregate data from Meraki coordinators."""
        try:
            # Check if any coordinator data is None
            if device_data is None or ssid_data is None or network_data is None:
                _LOGGER.warning("One or more coordinator data is None.")
                return {}  # Return empty dict to prevent errors

            # Log the received data for debugging
            _LOGGER.debug(
                f"DataAggregationCoordinator received: device_data={device_data}, ssid_data={ssid_data}, network_data={network_data}, device_tags={device_tags}"
            )

            # Aggregate data
            aggregated_data = await self.data_aggregator.aggregate_data(
                device_data, ssid_data, network_data, device_tags
            )
            _LOGGER.debug(f"Aggregated data: {aggregated_data}")  # add this line
            return aggregated_data

        except Exception as e:
            _LOGGER.error(f"Error aggregating data: {e}")
            raise UpdateFailed(f"Error aggregating data: {e}")
