"""Data Aggregator for the meraki_ha integration."""

import logging
from typing import Dict, Any
from ..helpers.ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates data from various Meraki coordinators."""

    def __init__(self, relaxed_tag_match, data_processor, ssid_status_calculator):
        self.relaxed_tag_match = relaxed_tag_match
        self.data_processor = data_processor
        self.ssid_status_calculator = ssid_status_calculator

    async def aggregate_data(
        self, device_data, ssid_data, network_data, device_tags
    ) -> Dict[str, Any]:
        """Aggregate data from Meraki coordinators."""
        _LOGGER.debug(
            f"Aggregating data: device_data={device_data}, ssid_data={ssid_data}, network_data={network_data}, device_tags={device_tags}"
        )  # added line
        try:
            processed_devices = (
                self.data_processor.process_devices(device_data)
                if isinstance(device_data, list)
                else []
            )
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

            aggregated_data = {
                "devices": processed_devices,
                "ssids": processed_ssids,
                "networks": processed_networks,
            }

            for device in aggregated_data.get("devices", []):
                serial = device.get("serial")
                if serial and serial in device_tags:
                    device["tags"] = device_tags[serial]

            # Calculate SSID statuses
            processed_ssids_with_status = SsidStatusCalculator.calculate_ssid_status(
                processed_ssids,
                processed_devices,
                device_tags,
                self.relaxed_tag_match,
            )

            # Combine processed data with SSID statuses
            combined_data = {
                **aggregated_data,
                "ssids": processed_ssids_with_status,  # Use the updated SSIDs
            }

            _LOGGER.debug(
                f"Aggregated and processed data: {combined_data}"
            )  # added line
            return combined_data

        except Exception as e:
            _LOGGER.error(f"Error in data aggregation: {e}")
            return {}
