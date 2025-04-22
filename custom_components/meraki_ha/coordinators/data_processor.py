import logging
from typing import Any, Dict, List
import asyncio
from ..meraki_api.wireless import (
    get_meraki_device_wireless_radio_settings,
    get_meraki_connected_client_count,
)
from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataProcessor:
    """Class to process data from the Meraki API."""

    def __init__(self, coordinator: "MerakiDataUpdateCoordinator"):
        """Initialize with the Meraki data update coordinator."""
        self.coordinator = coordinator
        self.api_key = coordinator.api_key

    async def process_devices(
        self, devices: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process device data and fetch additional details for MR devices."""
        processed_devices = []
        tasks = []
        for device in devices:
            processed_device = {
                "name": device.get("name"),
                "serial": device.get("serial"),
                "mac": device.get("mac"),
                "model": device.get("model"),
                "networkId": device.get("networkId"),
                "tags": device.get("tags", []),
                "connected_clients": None,
                "radio_settings": None,
            }
            if device.get("model", "").startswith("MR"):
                network_id = device.get("networkId")
                mac_address = device.get("mac")
                serial = device.get("serial")
                if network_id and mac_address:
                    tasks.append(
                        get_meraki_connected_client_count(
                            self.api_key, network_id, mac_address
                        )
                    )
                else:
                    tasks.append(None)  # Placeholder if info is missing

                if serial:
                    tasks.append(
                        get_meraki_device_wireless_radio_settings(self.api_key, serial)
                    )
                else:
                    tasks.append(None)  # Placeholder if serial is missing

            processed_devices.append(processed_device)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        task_index = 0
        for i, p_device in enumerate(processed_devices):
            if p_device["model"].startswith("MR"):
                client_result = results[task_index]
                task_index += 1
                radio_result = results[task_index]
                task_index += 1

                if isinstance(client_result, int):
                    p_device["connected_clients"] = client_result
                elif client_result is not None and isinstance(client_result, Exception):
                    _LOGGER.warning(
                        f"Error fetching client count for {p_device.get('name')}: {client_result}"
                    )

                if isinstance(radio_result, dict):
                    p_device["radio_settings"] = radio_result
                elif radio_result is not None and isinstance(radio_result, Exception):
                    _LOGGER.warning(
                        f"Error fetching radio settings for {p_device.get('name')}: {radio_result}"
                    )

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
