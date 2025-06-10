"""Data Aggregator for the Meraki Home Assistant integration.

This module defines the `DataAggregator` class, responsible for combining
processed data streams (devices with their tags, SSIDs, networks) into a
single, coherent structure. It primarily utilizes `SsidStatusCalculator`
to determine the operational status of SSIDs based on device information.
"""

import logging
from typing import Any, Dict, List, Optional

# For type hinting data_processor
from custom_components.meraki_ha.coordinators.data_processor import MerakiDataProcessor
from custom_components.meraki_ha.helpers.ssid_status_calculator import (
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
            ssid_status_calculator: An instance of `SsidStatusCalculator`
                used to determine the status of SSIDs.
        """
        # self.data_processor: MerakiDataProcessor = data_processor
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
            processed_devices: A list of processed device dictionaries. Expected structure for relevant items:
                `{'serial': Optional[str], 'model': str, 'status': Optional[str], 'tags': List[str], ...}`
            ssid_data: A list of processed SSID dictionaries. Expected structure for relevant items:
                `{'id': Optional[Any], 'number': Optional[Any], 'name': Optional[str], 'enabled': bool, 'tags': List[str], ...}`
            network_data: A list of processed network dictionaries. (Structure less critical for this method's direct logic beyond being a list of dicts).
            client_data: Optional list of processed client dictionaries.
            network_client_counts: Optional dictionary mapping network IDs to client counts.
            clients_on_ssids: Total count of clients on SSIDs.
            clients_on_appliances: Total count of clients on appliances.
            clients_on_wireless: Total count of wireless clients.

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

            # Sanitize data for SsidStatusCalculator
            # For SSIDs: ensure 'enabled' is bool, 'tags' is List[str]
            sanitized_ssids_for_calculator: List[Dict[str, Any]] = []
            if isinstance(ssid_data, list):
                for i, ssid_item in enumerate(ssid_data):
                    if not isinstance(ssid_item, dict):
                        _LOGGER.warning("Item at index %d in ssid_data is not a dictionary, skipping for SSID status calculation: %s",
                                        i, str(ssid_item)[:100])
                        continue

                    # Validate/default 'enabled'
                    is_enabled = ssid_item.get("enabled")
                    if not isinstance(is_enabled, bool):
                        _LOGGER.warning("SSID item (ID: %s, Name: %s) 'enabled' flag is not bool (type: %s, value: %s). Defaulting to False for status calculation.",
                                        ssid_item.get('id', 'N/A'), ssid_item.get('name', 'N/A'), type(is_enabled).__name__, is_enabled)
                        ssid_item["enabled"] = False # Modify a copy if original should be preserved, but processor should have handled this

                    # Validate/sanitize 'tags'
                    raw_tags = ssid_item.get("tags")
                    processed_tags: List[str] = []
                    if isinstance(raw_tags, list):
                        for tag_idx, tag_item in enumerate(raw_tags):
                            if isinstance(tag_item, str):
                                processed_tags.append(tag_item)
                            else:
                                _LOGGER.warning("SSID (ID: %s, Name: %s) has non-string tag at index %d (type: %s, value: %s). Converting to string for status calculation.",
                                                ssid_item.get('id', 'N/A'), ssid_item.get('name', 'N/A'), tag_idx, type(tag_item).__name__, str(tag_item)[:50])
                                processed_tags.append(str(tag_item))
                    elif raw_tags is not None:
                        _LOGGER.warning("SSID (ID: %s, Name: %s) 'tags' field is not a list (type: %s). Using empty list for status calculation.",
                                        ssid_item.get('id', 'N/A'), ssid_item.get('name', 'N/A'), type(raw_tags).__name__)
                    ssid_item["tags"] = processed_tags # Ensure calculator gets clean tags
                    sanitized_ssids_for_calculator.append(ssid_item)
            else:
                _LOGGER.warning("'ssid_data' is not a list. Cannot calculate SSID statuses.")
                # processed_ssids_with_status will be empty if we can't proceed

            # For Devices: ensure 'model' is str, 'tags' is List[str]
            sanitized_devices_for_calculator: List[Dict[str, Any]] = []
            if isinstance(processed_devices, list):
                for i, device_item in enumerate(processed_devices):
                    if not isinstance(device_item, dict):
                        _LOGGER.warning("Item at index %d in processed_devices is not a dictionary, skipping for SSID status calculation: %s",
                                        i, str(device_item)[:100])
                        continue

                    # Validate 'model'
                    model = device_item.get("model")
                    if not isinstance(model, str):
                        _LOGGER.warning("Device item (Serial: %s) 'model' is not a string (type: %s, value: %s). Defaulting to empty string for status calculation.",
                                        device_item.get('serial', 'N/A'), type(model).__name__, model)
                        device_item["model"] = "" # Calculator expects a string for .upper().startswith("MR")

                    # Validate/sanitize 'tags'
                    raw_tags = device_item.get("tags")
                    processed_tags_dev: List[str] = []
                    if isinstance(raw_tags, list):
                        for tag_idx, tag_item in enumerate(raw_tags):
                            if isinstance(tag_item, str):
                                processed_tags_dev.append(tag_item)
                            else:
                                _LOGGER.warning("Device (Serial: %s) has non-string tag at index %d (type: %s, value: %s). Converting to string for status calculation.",
                                                device_item.get('serial', 'N/A'), tag_idx, type(tag_item).__name__, str(tag_item)[:50])
                                processed_tags_dev.append(str(tag_item))
                    elif raw_tags is not None:
                         _LOGGER.warning("Device (Serial: %s) 'tags' field is not a list (type: %s). Using empty list for status calculation.",
                                        device_item.get('serial', 'N/A'), type(raw_tags).__name__)
                    device_item["tags"] = processed_tags_dev
                    sanitized_devices_for_calculator.append(device_item)
            else:
                _LOGGER.warning("'processed_devices' is not a list. Cannot calculate SSID statuses accurately.")
                # SsidStatusCalculator handles devices=None by marking SSIDs as unknown, which is acceptable.

            processed_ssids_with_status: List[Dict[str, Any]] = (
                SsidStatusCalculator.calculate_ssid_status(
                    ssids=sanitized_ssids_for_calculator, # Use sanitized list
                    devices=sanitized_devices_for_calculator, # Use sanitized list
                )
            )

            # Construct the final combined data structure.
            # This dictionary holds all the data to be used by the integration.
            combined_data: Dict[str, Any] = {
                "devices": [],  # To be populated by new logic below
                "ssids": processed_ssids_with_status,
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

            # Implement SSID-Device Linking
            devices_with_embedded_ssids = []
            if isinstance(processed_devices, list): # Iterate original processed_devices for linking
                for i, device_dict_orig in enumerate(processed_devices):
                    if not isinstance(device_dict_orig, dict):
                        _LOGGER.warning("Item at index %d in processed_devices (for linking) is not a dictionary, skipping: %s",
                                        i, str(device_dict_orig)[:100])
                        continue

                    device_clone = device_dict_orig.copy() # Work with a copy
                    model_str = device_clone.get("model")
                    # Ensure model is a string before .upper()
                    if not isinstance(model_str, str):
                        model_str = "" # Default to empty string if model is not string, effectively skipping MR check

                    if model_str.upper().startswith("MR"):
                        dev_network_id = device_clone.get("networkId")
                        if dev_network_id: # Network ID is crucial for linking
                            matching_ssids = []
                            for j, ssid_status_item in enumerate(processed_ssids_with_status):
                                if not isinstance(ssid_status_item, dict):
                                    _LOGGER.warning("Item at index %d in processed_ssids_with_status is not a dictionary, skipping for linking: %s",
                                                    j, str(ssid_status_item)[:100])
                                    continue
                                if ssid_status_item.get("networkId") == dev_network_id:
                                    matching_ssids.append(ssid_status_item)
                            device_clone["ssids"] = matching_ssids
                    devices_with_embedded_ssids.append(device_clone)
            else: # Should not happen if DataAggregationCoordinator validated inputs
                _LOGGER.error("'processed_devices' is not a list when attempting SSID-Device linking. This is unexpected.")

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
            return {}
