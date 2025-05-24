"""Provides the MerakiDataProcessor for transforming raw Meraki API data.

This module defines the `MerakiDataProcessor` class, which contains static
methods for processing lists of raw data (devices, networks, SSIDs) obtained
from the Meraki API into a more structured and potentially filtered format
suitable for the integration's internal use.
"""

import logging
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)


class MerakiDataProcessor:
    """Processes raw data from the Meraki API into a structured format.

    This class provides static methods to transform lists of raw device, network,
    and SSID data obtained from the Meraki API into a more refined format.
    It selects relevant fields and can be extended to include more complex
    transformation logic if needed.
    """

    @staticmethod
    def process_devices(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes a list of raw device data from the Meraki API.

        Extracts key information for each device, such as name, serial number,
        MAC address, model, network ID, and tags. Other relevant attributes
        can be added to the `processed_device` dictionary as needed.

        Args:
            devices (List[Dict[str, Any]]): A list of dictionaries, where each
                dictionary represents a raw device object from the Meraki API.

        Returns:
            List[Dict[str, Any]]: A list of processed device dictionaries,
                each containing a curated set of key-value pairs. Returns an
                empty list if the input `devices` list is empty or None.
        """
        if not devices:
            return []

        processed_devices_list: List[Dict[str, Any]] = []
        for device in devices:
            if not isinstance(device, dict):
                _LOGGER.warning("Skipping non-dictionary item in devices list: %s", device)
                continue

            # Extract common and useful device attributes.
            # Using .get() provides default None if key is missing,
            # which is then preserved or handled by downstream consumers.
            # Defaulting 'tags' to an empty list if not present.
            processed_device = {
                "name": device.get("name"),
                "serial": device.get("serial"),
                "mac": device.get("mac"),
                "model": device.get("model"),
                "networkId": device.get("networkId"),
                "tags": device.get("tags", []),  # Ensure tags is always a list
                # Example of adding another attribute:
                # "lanIp": device.get("lanIp"),
                # "status": device.get("status"),
            }
            processed_devices_list.append(processed_device)
            _LOGGER.debug("Processed device: %s", processed_device.get("serial"))
        return processed_devices_list

    @staticmethod
    def process_networks(networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes a list of raw network data from the Meraki API.

        Extracts key information for each network, such as its ID, name, and type.
        More attributes can be added as required.

        Args:
            networks (List[Dict[str, Any]]): A list of dictionaries, where each
                dictionary represents a raw network object from the Meraki API.

        Returns:
            List[Dict[str, Any]]: A list of processed network dictionaries.
                Returns an empty list if the input `networks` list is empty or None.
        """
        if not networks:
            return []

        processed_networks_list: List[Dict[str, Any]] = []
        for network in networks:
            if not isinstance(network, dict):
                _LOGGER.warning("Skipping non-dictionary item in networks list: %s", network)
                continue

            # Extract essential network attributes.
            processed_network = {
                "id": network.get("id"),
                "name": network.get("name"),
                "type": network.get("type"),  # e.g., 'combined', 'wireless', 'switch', 'appliance'
                "organizationId": network.get("organizationId"),
                # "timeZone": network.get("timeZone"),
                # "productTypes": network.get("productTypes"),
            }
            processed_networks_list.append(processed_network)
            _LOGGER.debug("Processed network: %s", processed_network.get("id"))
        return processed_networks_list

    @staticmethod
    def process_ssids(ssids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes a list of raw SSID data from the Meraki API.

        Extracts key information for each SSID, such as its name and enabled status.
        Additional attributes like authentication mode, encryption, etc., can be added.

        Args:
            ssids (List[Dict[str, Any]]): A list of dictionaries, where each
                dictionary represents a raw SSID object from the Meraki API.

        Returns:
            List[Dict[str, Any]]: A list of processed SSID dictionaries.
                Returns an empty list if the input `ssids` list is empty or None.
        """
        if not ssids:
            return []

        processed_ssids_list: List[Dict[str, Any]] = []
        for ssid in ssids:
            if not isinstance(ssid, dict):
                _LOGGER.warning("Skipping non-dictionary item in SSIDs list: %s", ssid)
                continue

            # Extract important SSID attributes.
            # Note: SSID 'number' is also a key identifier.
            processed_ssid = {
                "number": ssid.get("number"), # SSID number (0-14)
                "name": ssid.get("name"),
                "enabled": ssid.get("enabled"),
                "authMode": ssid.get("authMode"),
                "encryptionMode": ssid.get("encryptionMode"),
                "psk": "********" if ssid.get("psk") else None, # Mask PSK for security
                # "ipAssignmentMode": ssid.get("ipAssignmentMode"),
                # "vlanId": ssid.get("vlanId"),
            }
            processed_ssids_list.append(processed_ssid)
            _LOGGER.debug("Processed SSID: %s (Number: %s)", processed_ssid.get("name"), processed_ssid.get("number"))
        return processed_ssids_list
