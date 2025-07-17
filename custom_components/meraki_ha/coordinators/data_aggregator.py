"""Data Aggregator for the Meraki Home Assistant integration.

This module defines the `DataAggregator` class, responsible for combining
processed data streams (devices with their tags, SSIDs, networks) into a
single, coherent structure. It primarily utilizes `SsidStatusCalculator`
to determine the operational status of SSIDs based on device information.
"""

import logging
from typing import Any, Dict, List, Optional

# For type hinting data_processor
from ...coordinators.data_processor import MerakiDataProcessor
from ...helpers.ssid_status_calculator import (
    SsidStatusCalculator,
)

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
        # data_processor: MerakiDataProcessor, # Removed as it's not used
        ssid_status_calculator: SsidStatusCalculator,
    ) -> None:
        """Initialize the DataAggregator.

        Args:
            # data_processor: An instance of `MerakiDataProcessor` was previously
            #                 accepted but found to be unused within this class.
            # relaxed_tag_match parameter was removed as SsidStatusCalculator now
            # always uses permissive (relaxed) tag matching.
            ssid_status_calculator: An instance of `SsidStatusCalculator`
                used to determine the status of SSIDs.
        """
        # self.data_processor: MerakiDataProcessor = data_processor
        # self.relaxed_tag_match is no longer needed as SsidStatusCalculator
        # now defaults to permissive matching.
        self.ssid_status_calculator: SsidStatusCalculator = ssid_status_calculator

    async def aggregate_data(
        self,
        # Devices list, tags are within each device dict.
        processed_devices: List[Dict[str, Any]],
        ssid_data: List[Dict[str, Any]],  # List of processed SSIDs.
        network_data: List[Dict[str, Any]],  # List of processed networks.
        client_data: Optional[List[Dict[str, Any]]],
        network_client_counts: Optional[Dict[str, int]],
        clients_on_ssids: int = 0,
        clients_on_appliances: int = 0,
        clients_on_wireless: int = 0,
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
            # is removed as it was redundant. The main task is SSID status
            # calculation.

            # Calculate SSID statuses using the SsidStatusCalculator.
            # This step enriches the SSID data with an operational 'status' field
            # (e.g., 'online', 'offline', 'partially_online') based on the
            # state of associated wireless access points (MR series devices).
            # The SsidStatusCalculator.calculate_ssid_status method is static and
            # expects:
            #   - `ssids`: A list of SSID dictionaries.
            #   - `devices`: A list of device dictionaries, where each wireless AP
            #                is expected to have its 'tags' directly included.
            # The matching logic is now permanently "permissive" (relaxed).
            processed_ssids_with_status: List[Dict[str, Any]] = (
                SsidStatusCalculator.calculate_ssid_status(
                    ssids=ssid_data,  # Original list of processed SSIDs.
                    devices=processed_devices,  # Devices with tags embedded.
                    # `relaxed_tag_match` argument was removed; calculator uses permissive logic.
                )
            )

            # Assemble the final aggregated data structure.
            # This dictionary will be the central source of truth for Meraki data
            # within Home Assistant entities and services.
            combined_data: Dict[str, Any] = {
                "devices": [],  # Placeholder; will be populated by the SSID-Device linking logic below.
                "ssids": processed_ssids_with_status,  # SSIDs with their calculated statuses.
                "networks": network_data,
                "clients": (
                    client_data if client_data is not None else []
                ),  # Add original client list
                # Add network client counts
                "network_client_counts": (
                    network_client_counts if network_client_counts is not None else {}
                ),
                "clients_on_ssids": clients_on_ssids,
                "clients_on_appliances": clients_on_appliances,
                "clients_on_wireless": clients_on_wireless,
            }

            # Link SSIDs to their respective MR (Wireless AP) devices.
            # This embeds a list of relevant SSIDs directly within each MR device's dictionary.
            # This is useful for entities that need to display SSIDs associated with a specific AP.
            devices_with_embedded_ssids: List[Dict[str, Any]] = []
            for device_info in processed_devices:  # Iterate through all processed devices.
                device_clone = device_info.copy()  # Work with a copy to avoid modifying the original list.

                # Check if the device is a Meraki Wireless AP (model starts with "MR").
                if device_clone.get("model") and device_clone.get("model", "").upper().startswith("MR"):
                    device_network_id = device_clone.get("networkId")
                    device_clone["ssids"] = [] # Initialize with empty list

                    if device_network_id:
                        # Find all SSIDs that belong to the same network as the current MR device.
                        # The `processed_ssids_with_status` list contains SSIDs from all networks,
                        # so filtering by `networkId` is crucial here.
                        # It's assumed that `networkId` is present in each SSID dictionary.
                        associated_ssids = [
                            ssid_info
                            for ssid_info in processed_ssids_with_status
                            if ssid_info.get("networkId") == device_network_id
                        ]
                        # Embed the list of matching SSIDs into the device's dictionary.
                        # The key "ssids" (defined by ATTR_SSIDS in const.py, effectively)
                        # is used to store this list.
                        device_clone["ssids"] = associated_ssids

                devices_with_embedded_ssids.append(device_clone)

            # Replace the placeholder "devices" list with the one containing embedded SSIDs.
            combined_data["devices"] = devices_with_embedded_ssids

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
            # Example: raise UpdateFailed(f"Aggregation failed due to: {e}")
            # from e
            if "devices" not in combined_data:
                combined_data["devices"] = []
            return combined_data
