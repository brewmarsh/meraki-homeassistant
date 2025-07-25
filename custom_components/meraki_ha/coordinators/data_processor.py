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
    from .base_coordinator import (
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
            devices: A list of dictionaries, where each dictionary is a
                representation of a device with all necessary data (including
                tags, and for MR devices, `connected_clients_count` and
                `radio_settings`) already fetched.

        Returns:
            A list of processed device dictionaries. Each dictionary
            contains a standardized set of fields: 'name', 'serial', 'mac',
            'model', 'networkId', 'tags', 'connected_clients_count',
            and 'radio_settings'.
        """
        if not isinstance(devices, list):
            _LOGGER.warning(
                "Device data is not a list as expected: %s. Returning empty list.",
                type(devices),
            )
            return []

            # _LOGGER.debug("Processing %d devices.", len(devices))
        processed_devices_list: List[Dict[str, Any]] = []

        for device_raw_data in devices:
            # These variables are kept for future MX device-specific logic
            original_mx_product_type = None  # noqa: F841
            is_mx_device = False  # noqa: F841
            if isinstance(device_raw_data, dict):
                model = device_raw_data.get("model", "").upper()
                # Note: Previously collected MX-specific data that wasn't used
                # TODO: Consider if we need to handle MX devices specially

            processed_device_data: Dict[str, Any] = {
                "name": device_raw_data.get("name"),
                "serial": device_raw_data.get("serial"),
                "mac": device_raw_data.get("mac"),
                "model": device_raw_data.get("model"),
                "networkId": device_raw_data.get("networkId"),
                "status": device_raw_data.get("status"),
                "productType": device_raw_data.get(
                    "productType"
                ),  # Ensure productType is copied initially
                # Default to empty list if tags are missing.
                "tags": (
                    device_raw_data.get("tags", "").split()
                    if isinstance(device_raw_data.get("tags"), str)
                    else device_raw_data.get("tags", [])
                ),
                # `connected_clients_count` and `radio_settings` are expected from ApiDataFetcher for MR devices.
                # For other device types, these might be None or absent.
                "connected_clients_count": device_raw_data.get(
                    "connected_clients_count"
                ),
                "radio_settings": device_raw_data.get("radio_settings"),
                "externalRtspEnabled": device_raw_data.get("externalRtspEnabled"),
                "rtspUrl": device_raw_data.get("rtspUrl"),  # ADD THIS LINE
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

            from ..coordinators.meraki_device_types import (
                map_meraki_model_to_device_type,
            )

            model = processed_device_data.get("model")
            if model:
                device_type = map_meraki_model_to_device_type(model)
                current_ptype_before_override = processed_device_data.get("productType")
                if device_type != "unknown":
                    processed_device_data["productType"] = device_type

                if (
                    current_ptype_before_override
                    != processed_device_data["productType"]
                ):
                    _LOGGER.debug(
                        "Device %s (Serial: %s) productType was '%s', overridden/set to '%s' in process_devices.",
                        processed_device_data.get("name", "Unknown"),
                        processed_device_data.get("serial", "N/A"),
                        current_ptype_before_override,
                        processed_device_data["productType"],
                    )

                # If this is a wireless device, ensure client count and radio settings are properly initialized
                if processed_device_data["productType"] == "wireless":
                    if processed_device_data.get("connected_clients_count") is None:
                        processed_device_data["connected_clients_count"] = 0
                    if processed_device_data.get("radio_settings") is None:
                        processed_device_data["radio_settings"] = {
                            "status": "unavailable",
                            "24": {"channel": 0, "power": 0},
                            "5": {"channel": 0, "power": 0},
                        }

            processed_devices_list.append(processed_device_data)

            # _LOGGER.debug("Finished processing %d devices.", len(processed_devices_list))
        return processed_devices_list

    @staticmethod
    def process_networks(networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_networks_list: List[Dict[str, Any]] = []
        if not isinstance(networks, list):
            _LOGGER.warning(
                "Network data is not a list as expected: %s. Returning empty list.",
                type(networks),
            )
            return processed_networks_list

        for network in networks:
            if not isinstance(network, dict):
                _LOGGER.warning(
                    "Network item is not a dict: %s. Skipping item.", type(network)
                )
                continue
            processed_network: Dict[str, Any] = {
                "id": network.get("id"),
                "name": network.get("name"),
                "type": network.get("type"),
            }
            processed_networks_list.append(processed_network)
        # _LOGGER.debug("Processed %d networks.", len(processed_networks_list))
        return processed_networks_list

    @staticmethod
    def process_ssids(ssids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_ssids_list: List[Dict[str, Any]] = []
        if not isinstance(ssids, list):
            _LOGGER.warning(
                "SSID data is not a list as expected: %s. Returning empty list.",
                type(ssids),
            )
            return processed_ssids_list

        for ssid in ssids:
            if not isinstance(ssid, dict):
                _LOGGER.warning(
                    "SSID item is not a dict: %s. Skipping item.", type(ssid)
                )
                continue
            processed_ssid: Dict[str, Any] = {
                "name": ssid.get("name"),
                "enabled": ssid.get("enabled"),
                "number": ssid.get("number"),
                "splashPage": ssid.get("splashPage"),
                "authMode": ssid.get("authMode"),
                "networkId": ssid.get("networkId"),
            }
            processed_ssids_list.append(processed_ssid)
        # _LOGGER.debug("Processed %d SSIDs.", len(processed_ssids_list))
        return processed_ssids_list

    @staticmethod
    def process_network_client_counts(
        clients: Optional[List[Dict[str, Any]]],
    ) -> Dict[str, int]:
        """Process a list of client data to count clients per network.

        Args:
            clients: A list of dictionaries, where each dictionary represents
                     a client and is expected to have a 'networkId' key.
                     Can be None or an empty list.

        Returns:
            A dictionary mapping networkId (str) to client count (int).
            Example: `{"N_123": 10, "N_456": 5}`
        """
        counts: Dict[str, int] = {}
        if not clients:
            return counts
        for client in clients:
            network_id = client.get("networkId")
            if network_id:
                counts[network_id] = counts.get(network_id, 0) + 1
        # _LOGGER.debug("Processed network client counts: %s", counts) # Reduced verbosity
        return counts
