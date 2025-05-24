"""Data Aggregator for the meraki_ha integration."""

import logging
from typing import Dict, Any, List
from ..helpers.ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates data from various Meraki coordinators."""

    def __init__(self, relaxed_tag_match, data_processor, ssid_status_calculator):
        self.relaxed_tag_match = relaxed_tag_match
        self.data_processor = data_processor
        self.ssid_status_calculator = ssid_status_calculator

    async def aggregate_data(
        self,
        processed_devices: List[Dict[str, Any]],
        ssid_data: List[Dict[str, Any]],
        network_data: List[Dict[str, Any]],
        device_tags: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Aggregate data from Meraki coordinators."""
        # _LOGGER.debug(
        #    f"Aggregating data: processed_devices={processed_devices}, ssid_data={ssid_data}, network_data={network_data}, device_tags={device_tags}"
        # )
        try:
            aggregated_data = {
                "devices": processed_devices,
                "ssids": ssid_data,
                "networks": network_data,
                "device_tags": device_tags,
            }

            # Calculate SSID statuses
            processed_ssids_with_status = SsidStatusCalculator.calculate_ssid_status(
                ssid_data,
                processed_devices,
                device_tags,
                self.relaxed_tag_match,
            )

            # Combine processed data with SSID statuses
            combined_data = {
                **aggregated_data,
                "ssids": processed_ssids_with_status,  # Use the updated SSIDs
            }

            # _LOGGER.debug(
            #    f"Aggregated and processed data: {combined_data}"
            # )
            return combined_data

        except Exception as e:
            _LOGGER.error(f"Error in data aggregation: {e}")
            return {}
