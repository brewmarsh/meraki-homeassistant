"""Processes raw data fetched from the Meraki API.

This module defines the `MerakiDataProcessor` class, which is
responsible for transforming pre-fetched data (originally from the Meraki API)
into a more structured and usable format for the integration. This
includes extracting relevant fields. It no longer fetches data asynchronously.
"""

import logging  # asyncio, Coroutine, Union, MerakiAPIClient removed
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    # Avoid circular import at runtime, only for type checking
    # Ensure this path is correct; if coordinator.py was deleted, it might be
    # base_coordinator
    from custom_components.meraki_ha.coordinators.base_coordinator import (
        MerakiDataUpdateCoordinator,
    )

_LOGGER = logging.getLogger(__name__)


class MerakiDataProcessor:
    """Class to process data fetched from the Meraki API.

    This processor takes raw data lists/dictionaries (pre-fetched by
    MerakiApiDataFetcher) and formats them, selecting relevant fields.
    It no longer makes its own API calls.
    """

    def __init__(self, coordinator: "MerakiDataUpdateCoordinator") -> None:
        """Initialize the MerakiDataProcessor.

        Args:
            coordinator: The main MerakiDataUpdateCoordinator instance, used to
                access shared information or configuration if needed.
                It is not used for making API calls from this class.
        """
        self.coordinator: "MerakiDataUpdateCoordinator" = coordinator
        # self.api_client initialization removed.

    async def process_devices(
        self, devices: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process a list of pre-fetched device data.

        Extracts key information for each device. The input `devices` list
        is expected to already contain all necessary information, including
        `tags`, and for MR devices, `connected_clients_count` and
        `radio_settings`, as fetched by `MerakiApiDataFetcher`.

        Args:
            devices: A list of raw device dictionaries. Each dictionary is expected
                to represent a device and ideally contains keys such as:
                - 'serial' (str): Device serial number (critical).
                - 'model' (str): Device model (critical).
                - 'name' (Optional[str]): Device name.
                - 'mac' (Optional[str]): Device MAC address.
                - 'networkId' (Optional[str]): ID of the network the device belongs to.
                - 'status' (Optional[str]): Current status of the device.
                - 'productType' (Optional[str]): Type of product (e.g., "switch", "wireless").
                - 'tags' (Optional[List[str]]): List of tags. Non-string tags will be converted.
                - 'connected_clients_count' (Optional[int]): For MR devices.
                - 'radio_settings' (Optional[Any]): For MR devices.
                - 'externalRtspEnabled' (Optional[bool]): For MV cameras.
                - 'rtspUrl' (Optional[str]): For MV cameras.
                - Other API-provided fields like 'wan1Ip', 'firmware', etc., are also preserved.

        Returns:
            A list of processed device dictionaries. Each dictionary contains a
            standardized set of fields. Critical fields like 'serial' and 'model' are required.
            Other fields default to None or empty list if missing/invalid.
            Example device dict structure:
            {
                'name': Optional[str], 'serial': str, 'mac': Optional[str],
                'model': str, 'networkId': Optional[str], 'status': Optional[str],
                'productType': Optional[str], 'tags': List[str],
                'connected_clients_count': Optional[int], 'radio_settings': Optional[Any],
                'externalRtspEnabled': Optional[bool], 'rtspUrl': Optional[str],
                # ... other fields like wan1Ip, firmware_up_to_date, etc.
            }
        """
        if not isinstance(devices, list):
            _LOGGER.error( # Changed to error as this is a fundamental type mismatch
                "Input 'devices' is not a list (type: %s). Cannot process. Returning empty list.",
                type(devices).__name__,
            )
            return []
        if not devices: # Handle empty list input
            _LOGGER.debug("Input 'devices' is an empty list. Returning empty list.")
            return []

        _LOGGER.debug("Processing %d raw device entries.", len(devices))
        processed_devices_list: List[Dict[str, Any]] = []

        for i, device_raw_data in enumerate(devices):
            if not isinstance(device_raw_data, dict):
                _LOGGER.warning("Item at index %d in 'devices' is not a dictionary, skipping: %s", i, str(device_raw_data)[:100])
                continue

            serial = device_raw_data.get("serial")
            if not serial or not isinstance(serial, str):
                _LOGGER.warning("Device item at index %d missing or invalid 'serial' (type: %s, value: %s), skipping.",
                                i, type(serial).__name__, str(serial)[:50])
                continue

            model = device_raw_data.get("model")
            if not model or not isinstance(model, str):
                _LOGGER.warning("Device item (Serial: %s) missing or invalid 'model' (type: %s, value: %s). Using 'Unknown'.",
                                serial, type(model).__name__, str(model)[:50])
                model_str = "Unknown" # Use a safe default for model string
            else:
                model_str = model

            original_mx_product_type = None
            is_mx_device = False
            if model_str.upper().startswith("MX"): # Use validated model_str
                is_mx_device = True
                original_mx_product_type = device_raw_data.get("productType") # Still get original for comparison

            # Process tags: ensure it's a list of strings
            tags_raw = device_raw_data.get("tags")
            processed_tags: List[str] = []
            if isinstance(tags_raw, list):
                for tag_idx, tag_item in enumerate(tags_raw):
                    if isinstance(tag_item, str):
                        processed_tags.append(tag_item)
                    else:
                        _LOGGER.warning("Device (Serial: %s) has non-string tag at index %d (type: %s, value: %s). Converting to string.",
                                        serial, tag_idx, type(tag_item).__name__, str(tag_item)[:50])
                        processed_tags.append(str(tag_item)) # Convert to string as a fallback
            elif tags_raw is not None: # Tags field is present but not a list
                _LOGGER.warning("Device (Serial: %s) 'tags' field is not a list (type: %s). Using empty list for tags.",
                                serial, type(tags_raw).__name__)
            # If tags_raw is None, processed_tags remains []

            # Extract basic device information.
            # The input `device_raw_data` is expected to have all fields
            # pre-fetched by ApiDataFetcher.
            # Name this `processed_device_data` to avoid confusion with device_raw_data
            processed_device_data: Dict[str, Any] = {
                "name": device_raw_data.get("name"), # Name can be None
                "serial": serial, # Validated non-empty string
                "mac": device_raw_data.get("mac"), # MAC can be None
                "model": model_str, # Validated string (or "Unknown")
                "networkId": device_raw_data.get("networkId"), # Can be None
                "status": device_raw_data.get("status"), # Can be None
                "productType": device_raw_data.get("productType"),
                "tags": processed_tags, # Validated list of strings
                "connected_clients_count": device_raw_data.get("connected_clients_count"),
                "radio_settings": device_raw_data.get("radio_settings"),
                "externalRtspEnabled": device_raw_data.get("externalRtspEnabled"),
                "rtspUrl": device_raw_data.get("rtspUrl"),
            }

            # Fields known to be added by MerakiApiDataFetcher for MX or all devices
            fields_to_copy = [
                "wan1Ip",
                "wan2Ip",
                "publicIp",
                "lanIp",
                "firmware_up_to_date",
                "latest_firmware_version",
                "wan1_dns_servers",
                "wan2_dns_servers",
                "lan_dns_settings",
                "firmware",  # ensure standard firmware field is copied if present
                # "tags", "networkId", "mac", "status" are already handled in initial dict creation
                # "productType" is handled by specific logic below
                # "connected_clients_count", "radio_settings" also handled in initial dict
            ]

            for field in fields_to_copy:
                if field in device_raw_data:
                    processed_device_data[field] = device_raw_data[field]

            if is_mx_device:  # Check the flag set at the beginning of the loop
                # Preserve "appliance" if that's what came in, otherwise force it.
                # This ensures that if api_data_fetcher correctly set it to "appliance", it's kept.
                # If it was somehow None or different despite api_data_fetcher's efforts, this also corrects it.
                current_ptype_before_override = processed_device_data.get("productType")
                if original_mx_product_type == "appliance":
                    processed_device_data["productType"] = "appliance"
                else:  # If original wasn't appliance, or was None, force it for MX.
                    processed_device_data["productType"] = "appliance"

                if (
                    current_ptype_before_override
                    != processed_device_data["productType"]
                ):
                    _LOGGER.debug(
                        "MX Device %s (Serial: %s) productType was '%s', overridden/set to '%s' in process_devices.",
                        processed_device_data.get("name", "Unknown"),
                        processed_device_data.get("serial", "N/A"),
                        current_ptype_before_override,
                        processed_device_data["productType"],
                    )
                elif (
                    original_mx_product_type != processed_device_data["productType"]
                ):  # Log if original was different but override resulted in same (e.g. both None, now appliance)
                    _LOGGER.debug(
                        "MX Device %s (Serial: %s) productType was originally '%s', now set to '%s' in process_devices.",
                        processed_device_data.get("name", "Unknown"),
                        processed_device_data.get("serial", "N/A"),
                        original_mx_product_type,  # original_mx_product_type is from device_raw_data
                        processed_device_data["productType"],
                    )
                else:  # Log if no change happened but it's an MX device, for completeness
                    _LOGGER.debug(
                        "MX Device %s (Serial: %s) productType remains '%s' in process_devices.",
                        processed_device_data.get("name", "Unknown"),
                        processed_device_data.get("serial", "N/A"),
                        processed_device_data["productType"],
                    )

            processed_devices_list.append(processed_device_data)

        _LOGGER.debug("Finished processing %d devices.", len(processed_devices_list))
        return processed_devices_list

    @staticmethod
    def process_networks(networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of pre-fetched network data.

        Extracts key information for each network.

        Args:
            networks: A list of raw network dictionaries. Each dictionary is expected
                to ideally contain keys such as:
                - 'id' (str): Network ID (critical).
                - 'name' (Optional[str]): Network name.
                - 'type' (Optional[str]): Network type (e.g., "wireless", "switch").
                - 'timeZone' (Optional[str]): Timezone of the network.
                - 'tags' (Optional[List[str]]): Tags associated with the network.

        Returns:
            A list of processed network dictionaries. Each dictionary
            contains selected fields like 'id', 'name', and 'type'.
            Example: `[{"id": "N_123", "name": "Main Office", "type": "wireless"}, ...]`
            Critical keys: 'id' (str).
        """
        if not isinstance(networks, list):
            _LOGGER.error( # Changed to error
                "Input 'networks' is not a list (type: %s). Cannot process. Returning empty list.",
                type(networks).__name__,
            )
            return []
        if not networks:
            _LOGGER.debug("Input 'networks' is an empty list. Returning empty list.")
            return []

        processed_networks_list: List[Dict[str, Any]] = []
        _LOGGER.debug("Processing %d raw network entries.", len(networks))

        for i, network_raw_data in enumerate(networks):
            if not isinstance(network_raw_data, dict):
                _LOGGER.warning("Item at index %d in 'networks' is not a dictionary, skipping: %s", i, str(network_raw_data)[:100])
                continue

            network_id = network_raw_data.get("id")
            if not network_id or not isinstance(network_id, str):
                _LOGGER.warning("Network item at index %d missing or invalid 'id' (type: %s, value: %s), skipping.",
                                i, type(network_id).__name__, str(network_id)[:50])
                continue

            # Name can be None, type can be None. These are handled by .get()
            processed_network: Dict[str, Any] = {
                "id": network_id, # Validated
                "name": network_raw_data.get("name"),
                "type": network_raw_data.get("type"),
                # "timeZone": network_raw_data.get("timeZone"), # Example of other fields
                # "tags": network_raw_data.get("tags", []),     # Example of other fields
            }
            processed_networks_list.append(processed_network)
        _LOGGER.debug("Finished processing %d networks.", len(processed_networks_list))
        return processed_networks_list

    @staticmethod
    def process_ssids(ssids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of pre-fetched SSID data.

        Extracts key information for each SSID.

        Args:
            ssids: A list of raw SSID dictionaries. Each dictionary is expected
                to ideally contain keys such as:
                - 'number' (Union[int, str]): SSID number (critical, 0-14 for MR).
                - 'enabled' (bool): Whether the SSID is enabled (critical).
                - 'name' (Optional[str]): SSID name.
                - 'networkId' (Optional[str]): ID of the network this SSID belongs to.
                - 'splashPage' (Optional[str]): Splash page setting.
                - 'authMode' (Optional[str]): Authentication mode.

        Returns:
            A list of processed SSID dictionaries. Each dictionary
            contains selected fields like 'name', 'enabled', 'number',
            'splashPage', and 'authMode'.
            Example: `[{"name": "Guest SSID", "enabled": True, "number": 0, ...}, ...]`
            Critical keys: 'number' (int/str that can be int), 'enabled' (bool).
        """
        if not isinstance(ssids, list):
            _LOGGER.error( # Changed to error
                "Input 'ssids' is not a list (type: %s). Cannot process. Returning empty list.",
                type(ssids).__name__,
            )
            return []
        if not ssids:
            _LOGGER.debug("Input 'ssids' is an empty list. Returning empty list.")
            return []

        processed_ssids_list: List[Dict[str, Any]] = []
        _LOGGER.debug("Processing %d raw SSID entries.", len(ssids))

        for i, ssid_raw_data in enumerate(ssids):
            if not isinstance(ssid_raw_data, dict):
                _LOGGER.warning("Item at index %d in 'ssids' is not a dictionary, skipping: %s", i, str(ssid_raw_data)[:100])
                continue

            ssid_number = ssid_raw_data.get("number")
            # SSID number is critical, usually an integer 0-14. API might return as string.
            if ssid_number is None:
                _LOGGER.warning("SSID item at index %d missing 'number', skipping: %s", i, str(ssid_raw_data)[:100])
                continue
            try:
                # Ensure number is treated as an integer for consistency if it's a string digit
                processed_number = int(ssid_number)
            except (ValueError, TypeError):
                _LOGGER.warning("SSID item at index %d 'number' is not a valid integer (value: %s, type: %s), skipping.",
                                i, str(ssid_number)[:50], type(ssid_number).__name__)
                continue

            is_enabled = ssid_raw_data.get("enabled")
            if not isinstance(is_enabled, bool):
                _LOGGER.warning("SSID item (Number: %s) 'enabled' flag is not boolean (type: %s, value: %s). Defaulting to False.",
                                processed_number, type(is_enabled).__name__, str(is_enabled)[:50])
                is_enabled = False # Default to False if not a valid boolean

            processed_ssid: Dict[str, Any] = {
                "name": ssid_raw_data.get("name"), # Name can be None
                "enabled": is_enabled, # Validated boolean
                "number": processed_number, # Validated integer
                "splashPage": ssid_raw_data.get("splashPage"),
                "authMode": ssid_raw_data.get("authMode"),
                "networkId": ssid_raw_data.get("networkId"),
            }
            processed_ssids_list.append(processed_ssid)
        _LOGGER.debug("Finished processing %d SSIDs.", len(processed_ssids_list))
        return processed_ssids_list

    @staticmethod
    def process_network_client_counts(
        clients: Optional[List[Dict[str, Any]]],
    ) -> Dict[str, int]:
        """Process a list of client data to count clients per network.

        Args:
            clients: An optional list of raw client dictionaries. If provided, each
                     dictionary is expected to ideally contain keys such as:
                     - 'networkId' (str): ID of the network the client is on (critical for this method).
                     - Other client details (e.g., 'mac', 'ip') are not directly used by this method
                       but might be present in the raw data.

        Returns:
            A dictionary mapping networkId (str) to client count (int).
            Example: `{"N_123": 10, "N_456": 5}`
            Each client dict in `clients` list must have 'networkId' (str).
        """
        counts: Dict[str, int] = {}
        if clients is None: # Allow None input, return empty
            _LOGGER.debug("Input 'clients' is None. Returning empty client counts.")
            return counts

        if not isinstance(clients, list):
            _LOGGER.error( # Changed to error
                "Input 'clients' is not a list (type: %s). Cannot process client counts. Returning empty counts.",
                type(clients).__name__,
            )
            return counts

        if not clients: # Handle empty list
            _LOGGER.debug("Input 'clients' is an empty list. Returning empty client counts.")
            return counts

        _LOGGER.debug("Processing %d raw client entries for network counts.", len(clients))
        for i, client_raw_data in enumerate(clients):
            if not isinstance(client_raw_data, dict):
                _LOGGER.warning("Item at index %d in 'clients' is not a dictionary, skipping for network count: %s", i, str(client_raw_data)[:100])
                continue

            network_id = client_raw_data.get("networkId")
            if not network_id or not isinstance(network_id, str): # networkId must be a string to be a dict key
                _LOGGER.warning("Client item at index %d missing or invalid 'networkId' (type: %s, value: %s), skipping for network count.",
                                i, type(network_id).__name__, str(network_id)[:50])
                continue

            counts[network_id] = counts.get(network_id, 0) + 1
        _LOGGER.debug("Finished processing network client counts: %s", counts)
        return counts
