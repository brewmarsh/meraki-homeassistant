"""Data Aggregator for the Meraki Home Assistant integration.

This module defines the `DataAggregator` class, which is responsible for
combining various processed data streams (devices, SSIDs, networks,
tags) into a single, coherent structure. It utilizes an
`SsidStatusCalculator` to determine the operational status of SSIDs
based on device and tag information.
"""
import logging
from typing import Any, Dict, List

# Assuming MerakiDataProcessor is a class, import it for type hinting
# If it's part of the same module or a base class, adjust import as needed.
# from .data_processor import MerakiDataProcessor
from ..helpers.ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates processed data from various Meraki sources.

    This class takes lists of processed devices, SSIDs, networks, and
    device tags, and combines them. A key part of its role is to use the
    `SsidStatusCalculator` to enrich SSID data with their current
    operational status.
    """

    def __init__(
        self,
        relaxed_tag_match: bool,
        # Assuming data_processor is an instance of MerakiDataProcessor
        data_processor: Any,  # Replace Any with MerakiDataProcessor
                              # if available
        ssid_status_calculator: SsidStatusCalculator,
    ) -> None:
        """Initialize the DataAggregator.

        Args:
            relaxed_tag_match: Boolean indicating if relaxed tag matching
                should be used by the SSID status calculator.
            data_processor: An instance of `MerakiDataProcessor` (or
                similar class) that provides methods for processing raw
                data. (Currently, this parameter doesn't seem to be
                directly used in `aggregate_data` but is stored).
            ssid_status_calculator: An instance of `SsidStatusCalculator`
                used to determine the status of SSIDs.
        """
        self.relaxed_tag_match: bool = relaxed_tag_match
        # Store MerakiDataProcessor instance
        self.data_processor: Any = data_processor
        self.ssid_status_calculator: SsidStatusCalculator = (
            ssid_status_calculator
        )

    async def aggregate_data(
        self,
        processed_devices: List[Dict[str, Any]],
        ssid_data: List[Dict[str, Any]],
        network_data: List[Dict[str, Any]],
        device_tags: Dict[str, List[str]],  # Changed type from Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate data from various processed Meraki data sources.

        This method combines the provided lists of devices, SSIDs, and
        networks with device tags. It then uses `SsidStatusCalculator`
        to update the status of each SSID.

        Args:
            processed_devices: A list of dictionaries, where each
                dictionary represents a device that has already been
                processed (e.g., filtered for relevant types like
                wireless APs).
            ssid_data: A list of dictionaries, where each dictionary
                represents an SSID.
            network_data: A list of dictionaries, where each dictionary
                represents a network.
            device_tags: A dictionary mapping device serial numbers to a
                list of their tags.

        Returns:
            A dictionary containing the aggregated data, with keys like
            "devices", "ssids" (now including status), "networks", and
            "device_tags". Returns an empty dictionary if a critical error
            occurs during aggregation.
        """
        _LOGGER.debug(
            "Aggregating data for %d devices, %d SSIDs, %d networks.",
            len(processed_devices),
            len(ssid_data),
            len(network_data),
        )
        try:
            # Initial aggregation of the provided data (now commented out as unused)
            # aggregated_data: Dict[str, Any] = {
            #     "devices": processed_devices,
            #     "ssids": ssid_data,  # Original SSIDs before status calculation
            #     "networks": network_data,
            #     "device_tags": device_tags,
            # }

            # Calculate SSID statuses using the SsidStatusCalculator
            # The SsidStatusCalculator.calculate_ssid_status is a static method.
            processed_ssids_with_status: List[
                Dict[str, Any]
            ] = SsidStatusCalculator.calculate_ssid_status(
                ssids=ssid_data,  # Pass the original list of SSIDs
                devices=processed_devices,
                device_tags=device_tags,
                relaxed_tag_match=self.relaxed_tag_match,
            )

            # Update the aggregated data with SSIDs that now include their status
            # This creates a new dictionary for combined_data to ensure clarity
            combined_data: Dict[str, Any] = {
                "devices": processed_devices,
                # Use SSIDs with calculated status
                "ssids": processed_ssids_with_status,
                "networks": network_data,
                "device_tags": device_tags,
            }

            _LOGGER.debug(
                "Data aggregation and SSID status calculation complete. "
                "Returning combined data."
            )
            return combined_data

        except Exception as e:  # pylint: disable=broad-except
            # Log the exception with traceback for better debugging
            _LOGGER.exception("Error during data aggregation: %s", e)
            # It might be better to raise an exception here if the caller
            # is equipped to handle it, e.g.,
            # raise UpdateFailed(f"Aggregation failed: {e}")
            return {}  # Return empty dict as per original behavior
