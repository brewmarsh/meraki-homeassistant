"""Data Aggregation Coordinator for the meraki_ha integration."""

import logging
from typing import Dict, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from .base_coordinator import MerakiDataUpdateCoordinator
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
        coordinator: "MerakiDataUpdateCoordinator",
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
        self.coordinator = coordinator
        self.data_processor = MerakiDataProcessor(
            coordinator=self.coordinator
        )  # Pass coordinator
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
            # _LOGGER.debug(
            #    f"DataAggregationCoordinator received: device_data={device_data}, ssid_data={ssid_data}, network_data={network_data}, device_tags={device_tags}"
            # )

            # Process devices and filter for wireless APs
            processed_devices = []
            if isinstance(device_data, list):
                processed_devices = await self.data_processor.process_devices(
                    device_data
                )  # Add 'await' here
                processed_devices = [
                    device
                    for device in processed_devices
                    if device.get("model", "").startswith("MR")
                ]
            else:
                processed_devices = []

            processed_networks = (
                self.data_processor.process_networks(network_data)
                if isinstance(network_data, list)
                else []
            )
            processed_ssids = (
                self.data_processor.process_ssids(ssid_data)
                if isinstance(ssid_data, list)
                else []
            )

            # Aggregate data
            aggregated_data = await self.data_aggregator.aggregate_data(
                processed_devices, processed_ssids, processed_networks, device_tags
            )
            # _LOGGER.debug(f"Aggregated data: {aggregated_data}")
            return aggregated_data

        except Exception as e:
            _LOGGER.error(f"Error aggregating data: {e}")
            raise UpdateFailed(f"Error aggregating data: {e}")
