"""Processes raw data fetched from the Meraki API.

This module defines the `MerakiDataProcessor` class, which is
responsible for transforming pre-fetched data (originally from the Meraki API)
into a more structured and usable format for the integration. This
includes extracting relevant fields. It no longer fetches data asynchronously.
"""

import logging # asyncio, Coroutine, Union, MerakiAPIClient removed
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    # Avoid circular import at runtime, only for type checking
    # Ensure this path is correct; if coordinator.py was deleted, it might be base_coordinator
    from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator 

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
        _LOGGER.debug("Processing %d devices.", len(devices))
        processed_devices_list: List[Dict[str, Any]] = []

        for device_data in devices:
            # Extract basic device information.
            # The input `device_data` is expected to have all fields pre-fetched by ApiDataFetcher.
            processed_device: Dict[str, Any] = {
                "name": device_data.get("name"),
                "serial": device_data.get("serial"),
                "mac": device_data.get("mac"),
                "model": device_data.get("model"),
                "networkId": device_data.get("networkId"),
                "tags": device_data.get("tags", []), # Default to empty list if tags are missing.
                # `connected_clients_count` and `radio_settings` are expected from ApiDataFetcher for MR devices.
                # For other device types, these might be None or absent.
                "connected_clients_count": device_data.get("connected_clients_count"),
                "radio_settings": device_data.get("radio_settings"),
            }
            processed_devices_list.append(processed_device)

        _LOGGER.debug("Finished processing %d devices.", len(processed_devices_list))
        return processed_devices_list

    @staticmethod
    def process_networks(networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of pre-fetched network data.

        Extracts key information for each network.

        Args:
            networks: A list of dictionaries, where each dictionary is a
                representation of a network with data pre-fetched.

        Returns:
            A list of processed network dictionaries. Each dictionary
            contains selected fields like 'id', 'name', and 'type'.
            Example: `[{"id": "N_123", "name": "Main Office", "type": "wireless"}, ...]`
        """
        processed_networks_list: List[Dict[str, Any]] = []
        if not isinstance(networks, list): # Basic type check.
            _LOGGER.warning("Network data is not a list as expected: %s. Returning empty list.", type(networks))
            return processed_networks_list

        for network in networks:
            if not isinstance(network, dict): # Ensure each item is a dictionary.
                _LOGGER.warning("Network item is not a dict: %s. Skipping item.", type(network))
                continue
            processed_network: Dict[str, Any] = {
                "id": network.get("id"),
                "name": network.get("name"),
                "type": network.get("type"),
                # Other relevant network attributes can be added here if needed in the future.
                # e.g., "timeZone": network.get("timeZone"), "tags": network.get("tags", []),
            }
            processed_networks_list.append(processed_network)
        _LOGGER.debug("Processed %d networks.", len(processed_networks_list))
        return processed_networks_list

    @staticmethod
    def process_ssids(ssids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of pre-fetched SSID data.

        Extracts key information for each SSID.

        Args:
            ssids: A list of dictionaries, where each dictionary is a
                representation of an SSID with data pre-fetched.

        Returns:
            A list of processed SSID dictionaries. Each dictionary
            contains selected fields like 'name', 'enabled', 'number',
            'splashPage', and 'authMode'.
            Example: `[{"name": "Guest SSID", "enabled": True, "number": 0, ...}, ...]`
        """
        processed_ssids_list: List[Dict[str, Any]] = []
        if not isinstance(ssids, list): # Basic type check.
            _LOGGER.warning("SSID data is not a list as expected: %s. Returning empty list.", type(ssids))
            return processed_ssids_list

        for ssid in ssids:
            if not isinstance(ssid, dict): # Ensure each item is a dictionary.
                _LOGGER.warning("SSID item is not a dict: %s. Skipping item.", type(ssid))
                continue
            processed_ssid: Dict[str, Any] = {
                "name": ssid.get("name"),
                "enabled": ssid.get("enabled"),
                "number": ssid.get("number"),  # SSID number (0-14 for MR devices).
                "splashPage": ssid.get("splashPage"),
                "authMode": ssid.get("authMode"),
                # Other relevant SSID attributes can be added here if needed in the future.
                # e.g., "ipAssignmentMode": ssid.get("ipAssignmentMode"),
            }
            processed_ssids_list.append(processed_ssid)
        _LOGGER.debug("Processed %d SSIDs.", len(processed_ssids_list))
        return processed_ssids_list
