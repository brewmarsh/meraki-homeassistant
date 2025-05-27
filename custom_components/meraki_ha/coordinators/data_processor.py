"""Processes raw data fetched from the Meraki API.

This module defines the `MerakiDataProcessor` class, which is
responsible for transforming the raw JSON responses from the Meraki API
into a more structured and usable format for the integration. This
includes extracting relevant fields and, for certain device types
(like MR wireless access points), fetching additional details
asynchronously.
"""

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Coroutine, Dict, List, Optional, Union
from ..meraki_api import MerakiAPIClient 

if TYPE_CHECKING:
    # Avoid circular import at runtime, only for type checking
    from ..coordinator import MerakiDataUpdateCoordinator

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
                representation of a device with all data pre-fetched.

        Returns:
            A list of processed device dictionaries. Each dictionary
            contains selected fields like 'name', 'serial', 'mac',
            'model', 'networkId', 'tags', 'connected_clients_count',
            and 'radio_settings'.
        """
        _LOGGER.debug("Processing %d devices.", len(devices))
        processed_devices_list: List[Dict[str, Any]] = []

        for device_data in devices:
            # Basic device information extraction
            # The input `device_data` is expected to have all necessary fields.
            processed_device: Dict[str, Any] = {
                "name": device_data.get("name"),
                "serial": device_data.get("serial"),
                "mac": device_data.get("mac"),
                "model": device_data.get("model"),
                "networkId": device_data.get("networkId"),
                "tags": device_data.get("tags", []), # Ensure tags default to empty list
                # connected_clients_count and radio_settings are expected to be present
                # for MR devices, or None/absent for others, as fetched by ApiDataFetcher.
                "connected_clients_count": device_data.get("connected_clients_count"),
                "radio_settings": device_data.get("radio_settings"),
            }
            processed_devices_list.append(processed_device)

        _LOGGER.debug("Finished processing %d devices.", len(processed_devices_list))
        return processed_devices_list

    @staticmethod
    def process_networks(networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of network data from the Meraki API.

        Extracts key information for each network.

        Args:
            networks: A list of dictionaries, where each dictionary is a
                raw representation of a network from the Meraki API.

        Returns:
            A list of processed network dictionaries. Each dictionary
            contains selected fields like 'id', 'name', and 'type'.
            Example: `[{"id": "N_123", "name": "Main Office",
            "type": "wireless"}, ...]`
        """
        processed_networks_list: List[Dict[str, Any]] = []
        if not isinstance(networks, list):
            _LOGGER.warning("Network data is not a list: %s", type(networks))
            return processed_networks_list

        for network in networks:
            if not isinstance(network, dict):
                _LOGGER.warning("Network item is not a dict: %s", type(network))
                continue
            processed_network: Dict[str, Any] = {
                "id": network.get("id"),
                "name": network.get("name"),
                "type": network.get("type"),
                # Add other relevant network attributes here if needed
                # in the future
                # e.g., "timeZone": network.get("timeZone"),
                # "tags": network.get("tags", []),
            }
            processed_networks_list.append(processed_network)
        _LOGGER.debug("Processed %d networks.", len(processed_networks_list))
        return processed_networks_list

    @staticmethod
    def process_ssids(ssids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of SSID data from the Meraki API.

        Extracts key information for each SSID.

        Args:
            ssids: A list of dictionaries, where each dictionary is a raw
                representation of an SSID from the Meraki API.

        Returns:
            A list of processed SSID dictionaries. Each dictionary
            contains selected fields like 'name' and 'enabled'.
            Example: `[{"name": "Guest SSID", "enabled": True,
            "number": 0}, ...]` (assuming 'number' is also a relevant
            field from SSID details)
        """
        processed_ssids_list: List[Dict[str, Any]] = []
        if not isinstance(ssids, list):
            _LOGGER.warning("SSID data is not a list: %s", type(ssids))
            return processed_ssids_list

        for ssid in ssids:
            if not isinstance(ssid, dict):
                _LOGGER.warning("SSID item is not a dict: %s", type(ssid))
                continue
            processed_ssid: Dict[str, Any] = {
                "name": ssid.get("name"),
                "enabled": ssid.get("enabled"),
                "number": ssid.get("number"),  # SSID number is often important
                "splashPage": ssid.get("splashPage"),
                "authMode": ssid.get("authMode"),
                # Add other relevant SSID attributes here if needed
                # e.g., "ipAssignmentMode": ssid.get("ipAssignmentMode"),
                # "adminAccess": ssid.get("adminAccessCategory"),
            }
            processed_ssids_list.append(processed_ssid)
        _LOGGER.debug("Processed %d SSIDs.", len(processed_ssids_list))
        return processed_ssids_list
