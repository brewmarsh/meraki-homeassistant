"""Data Aggregator for the Meraki Home Assistant integration.

This module defines the `DataAggregator` class, responsible for combining
processed data streams (devices with their tags, SSIDs, networks) into a
single, coherent structure. It primarily utilizes `SsidStatusCalculator`
to determine the operational status of SSIDs based on device information.
"""
import logging
from typing import Any, Dict, List

from .data_processor import MerakiDataProcessor # For type hinting data_processor
from ..helpers.ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates processed data from various Meraki sources.

    This class takes lists of processed devices (which include their tags),
    SSIDs, and networks. Its main function is to use the `SsidStatusCalculator`
    to enrich SSID data with their current operational status (e.g., online,
    offline) based on the state of associated wireless access points.
    """

    def __init__(
        self,
        relaxed_tag_match: bool,
        data_processor: MerakiDataProcessor, # Type hint updated
        ssid_status_calculator: SsidStatusCalculator,
    ) -> None:
        """Initialize the DataAggregator.

        Args:
            relaxed_tag_match: Boolean indicating if relaxed tag matching
                should be used by the `SsidStatusCalculator`.
            data_processor: An instance of `MerakiDataProcessor`. While stored,
                it's not directly used in `aggregate_data` as processing
                is expected to have occurred before data is passed here.
                It's kept for potential future use or if sub-processing is needed.
            ssid_status_calculator: An instance of `SsidStatusCalculator`
                used to determine the status of SSIDs.
        """
        self.relaxed_tag_match: bool = relaxed_tag_match
        self.data_processor: MerakiDataProcessor = data_processor # Store for potential use
        self.ssid_status_calculator: SsidStatusCalculator = (
            ssid_status_calculator
        )

    async def aggregate_data(
        self,
        processed_devices: List[Dict[str, Any]], # Devices list, tags are within each device dict.
        ssid_data: List[Dict[str, Any]],         # List of processed SSIDs.
        network_data: List[Dict[str, Any]],      # List of processed networks.
        # The `device_tags` parameter has been removed.
    ) -> Dict[str, Any]:
        """Aggregate various processed Meraki data streams.

        This method combines the provided lists of devices (which are expected
        to include their tags), SSIDs, and networks. It then uses the
        `SsidStatusCalculator` to update the status of each SSID based on
        the properties of `processed_devices`.

        Args:
            processed_devices: A list of device dictionaries. Each device dict
                should represent a device that has already been processed
                (e.g., filtered for wireless APs) and must include its 'tags'.
            ssid_data: A list of processed SSID dictionaries.
            network_data: A list of processed network dictionaries.

        Returns:
            A dictionary containing the aggregated data, structured with keys
            like "devices", "ssids" (which now include a 'status' field),
            and "networks". Returns an empty dictionary if a critical error
            occurs during the aggregation process.
        """
        _LOGGER.debug(
            "Aggregating data for %d devices, %d SSIDs, %d networks.",
            len(processed_devices),
            len(ssid_data),
            len(network_data),
        )
        try:
            # The initial aggregation step creating `aggregated_data` with raw inputs
            # is removed as it was redundant. The main task is SSID status calculation.

            # Calculate SSID statuses using the SsidStatusCalculator.
            # `SsidStatusCalculator.calculate_ssid_status` is a static method.
            # It now relies on `processed_devices` containing the tags for each device.
            processed_ssids_with_status: List[
                Dict[str, Any]
            ] = SsidStatusCalculator.calculate_ssid_status(
                ssids=ssid_data,             # Pass the list of processed SSIDs.
                devices=processed_devices,   # Pass devices; tags are expected within each device.
                # `device_tags` argument is removed as tags are in `processed_devices`.
                relaxed_tag_match=self.relaxed_tag_match,
            )

            # Construct the final combined data structure.
            # This dictionary holds all the data to be used by the integration.
            combined_data: Dict[str, Any] = {
                "devices": processed_devices,
                "ssids": processed_ssids_with_status, # SSIDs now include their calculated status.
                "networks": network_data,
                # The separate "device_tags" key is no longer needed as tags are part of "devices".
            }

            _LOGGER.debug(
                "Data aggregation and SSID status calculation complete. "
                "Returning combined data structure."
            )
            return combined_data

        except Exception as e:  # pylint: disable=broad-except
            # Log any unexpected exception during aggregation with traceback.
            _LOGGER.exception("Critical error during data aggregation: %s", e)
            # Returning an empty dictionary in case of failure, as per previous behavior.
            # Depending on requirements, raising an UpdateFailed exception might be preferable
            # to propagate the error to the calling coordinator.
            # Example: raise UpdateFailed(f"Aggregation failed due to: {e}") from e
            return {}
