"""Provides the DataAggregator class for the Meraki Home Assistant integration.

This module defines `DataAggregator`, a class responsible for combining and
processing raw data from various Meraki API endpoints (devices, SSIDs, networks,
and device tags) into a structured format suitable for use by the integration's
coordinators and entities.
"""

import logging
from typing import Dict, Any, List # Added List for type hinting
from ..helpers.ssid_status_calculator import SsidStatusCalculator
# Assuming DataProcessor is in the same directory or properly pathed.
# If it's in .data_processor, the import should be:
from .data_processor import MerakiDataProcessor


_LOGGER = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates and processes data from various Meraki sources.

    This class takes raw data lists for devices, SSIDs, and networks,
    along with a dictionary of device tags, processes them using a
    `MerakiDataProcessor`, and then enriches the SSID data by calculating
    their operational status based on associated devices and tags using an
    `SsidStatusCalculator`.

    Attributes:
        relaxed_tag_match (bool): Configuration option for tag matching logic,
            passed to the `SsidStatusCalculator`.
        data_processor (MerakiDataProcessor): An instance used to perform initial
            processing of raw device, network, and SSID data.
        ssid_status_calculator (SsidStatusCalculator): An instance used to
            determine the operational status of SSIDs.
    """

    def __init__(
        self,
        relaxed_tag_match: bool,
        data_processor: MerakiDataProcessor,
        ssid_status_calculator: SsidStatusCalculator,
    ):
        """Initializes the DataAggregator.

        Args:
            relaxed_tag_match (bool): If True, relaxed tag matching rules are
                applied when calculating SSID status.
            data_processor (MerakiDataProcessor): An instance of `MerakiDataProcessor`
                to handle initial data structuring.
            ssid_status_calculator (SsidStatusCalculator): An instance of
                `SsidStatusCalculator` to determine SSID operational states.
        """
        self.relaxed_tag_match = relaxed_tag_match
        self.data_processor = data_processor
        self.ssid_status_calculator = ssid_status_calculator

    async def aggregate_data(
        self,
        device_data: List[Dict[str, Any]],
        ssid_data: List[Dict[str, Any]],
        network_data: List[Dict[str, Any]],
        device_tags: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        """Aggregates and processes data from Meraki API sources.

        The method first processes the raw lists of devices, networks, and SSIDs
        using the `data_processor`. Then, it associates tags with their respective
        devices. Finally, it calculates the operational status of each SSID based
        on the processed device data and tags.

        Args:
            device_data (List[Dict[str, Any]]): A list of dictionaries, where
                each dictionary represents a raw Meraki device.
            ssid_data (List[Dict[str, Any]]): A list of dictionaries, where
                each dictionary represents a raw Meraki SSID.
            network_data (List[Dict[str, Any]]): A list of dictionaries, where
                each dictionary represents a raw Meraki network.
            device_tags (Dict[str, List[str]]): A dictionary mapping device serial
                numbers to a list of their tags.

        Returns:
            Dict[str, Any]: A dictionary containing the processed and aggregated
                data, structured with keys like "devices", "ssids" (with status),
                and "networks". Returns an empty dictionary if a critical error
                occurs during aggregation.
        """
        _LOGGER.debug(
            "Starting data aggregation. Device count: %s, SSID count: %s, Network count: %s, Device tags count: %s",
            len(device_data) if device_data else "None",
            len(ssid_data) if ssid_data else "None",
            len(network_data) if network_data else "None",
            len(device_tags) if device_tags else "None",
        )
        try:
            # Perform initial processing of raw data.
            # Ensure input data is a list before processing, otherwise use empty list.
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

            # Initial structure for aggregated data.
            aggregated_data = {
                "devices": processed_devices,
                "ssids": processed_ssids,
                "networks": processed_networks,
            }

            # Associate tags with their respective devices.
            # This assumes `device_tags` is a dict mapping serials to tag lists.
            for device in aggregated_data.get("devices", []):
                serial = device.get("serial")
                if serial and device_tags and serial in device_tags:
                    device["tags"] = device_tags[serial]
                else:
                    # Ensure 'tags' key exists even if no tags are found.
                    device["tags"] = []


            # Calculate SSID operational statuses using the SsidStatusCalculator.
            # This method is static in SsidStatusCalculator, so can be called directly.
            processed_ssids_with_status = (
                self.ssid_status_calculator.calculate_ssid_status(
                    processed_ssids,
                    processed_devices,
                    device_tags if device_tags else {}, # Pass empty dict if None
                    self.relaxed_tag_match,
                )
            )

            # Update the aggregated data with SSIDs that now include their status.
            combined_data = {
                **aggregated_data,
                "ssids": processed_ssids_with_status,
            }

            _LOGGER.debug(
                "Successfully aggregated and processed data. Device count: %s, SSID count: %s, Network count: %s",
                len(combined_data.get("devices", [])),
                len(combined_data.get("ssids", [])),
                len(combined_data.get("networks", [])),
            )
            return combined_data

        except Exception as e:
            # Catch any unexpected errors during the aggregation process.
            _LOGGER.exception("Critical error during data aggregation: %s", e)
            # Return an empty dictionary to prevent cascading failures if aggregation fails.
            return {}
