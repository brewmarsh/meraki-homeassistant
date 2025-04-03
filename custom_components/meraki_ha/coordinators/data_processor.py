"""Meraki Data Processor for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)


class MerakiDataProcessor:
    """Class to process data from the Meraki API."""

    @staticmethod
    def process_devices(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process device data."""
        processed_devices = []
        for device in devices:
            processed_device = {
                "name": device.get("name"),
                "serial": device.get("serial"),
                "mac": device.get("mac"),
                "model": device.get("model"),
                "networkId": device.get("networkId"),
                "tags": device.get("tags", []),
                # Add other relevant device attributes
            }
            processed_devices.append(processed_device)
        return processed_devices

    @staticmethod
    def process_networks(networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process network data."""
        processed_networks = []
        for network in networks:
            processed_network = {
                "id": network.get("id"),
                "name": network.get("name"),
                "type": network.get("type"),
                # Add other relevant network attributes
            }
            processed_networks.append(processed_network)
        return processed_networks

    @staticmethod
    def process_ssids(ssids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process SSID data."""
        processed_ssids = []
        for ssid in ssids:
            processed_ssid = {
                "name": ssid.get("name"),
                "enabled": ssid.get("enabled"),
                # Add other relevant SSID attributes
            }
            processed_ssids.append(processed_ssid)
        return processed_ssids
