"""Processes raw data fetched from the Meraki API.

This module defines the `MerakiDataProcessor` class, which is responsible for
transforming the raw JSON responses from the Meraki API into a more structured
and usable format for the integration. This includes extracting relevant fields
and, for certain device types (like MR wireless access points), fetching
additional details asynchronously.
"""
import asyncio
import logging
from typing import TYPE_CHECKING, Any, Coroutine, Dict, List, Optional, Union

from ..meraki_api._api_client import MerakiAPIClient

if TYPE_CHECKING:
    # Avoid circular import at runtime, only for type checking
    from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataProcessor:
    """Class to process data fetched from the Meraki API.

    This processor takes raw data lists/dictionaries from the API and
    formats them, selects relevant fields, and enriches data for specific
    device types by making additional API calls if necessary.
    """

    def __init__(self, coordinator: "MerakiDataUpdateCoordinator") -> None:
        """Initialize the MerakiDataProcessor.

        Args:
            coordinator: The main MerakiDataUpdateCoordinator instance, used to
                access shared information like the API key and org_id.
        """
        self.coordinator: "MerakiDataUpdateCoordinator" = coordinator
        # self.api_key: str = coordinator.api_key # Can be removed if not used directly elsewhere
        self.api_client = MerakiAPIClient(
            api_key=self.coordinator.api_key,
            org_id=self.coordinator.org_id  # Assuming org_id is available on coordinator
        )

    async def process_devices(
        self, devices: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process a list of device data from the Meraki API.

        Extracts key information for each device. For Meraki MR devices (wireless APs),
        it additionally fetches the connected client count and wireless radio settings
        asynchronously.

        Args:
            devices: A list of dictionaries, where each dictionary is a raw
                representation of a device from the Meraki API.

        Returns:
            A list of processed device dictionaries. Each dictionary contains
            selected fields like 'name', 'serial', 'mac', 'model', 'networkId',
            'tags', and potentially 'connected_clients' and 'radio_settings'
            for MR devices.
        """
        _LOGGER.debug("Processing %d devices.", len(devices))
        processed_devices_list: List[Dict[str, Any]] = []
        # Tasks for asyncio.gather to fetch additional data for MR devices
        async_tasks: List[Optional[Coroutine[Any, Any, Any]]] = []
        # Keep track of which processed_device maps to which tasks
        mr_device_indices: List[int] = []

        for i, device in enumerate(devices):
            # Basic device information extraction
            processed_device: Dict[str, Any] = {
                "name": device.get("name"),
                "serial": device.get("serial"),
                "mac": device.get("mac"),
                "model": device.get("model"),
                "networkId": device.get("networkId"),
                "tags": device.get("tags", []),  # Default to empty list if no tags
                "connected_clients": None,  # Initialize as None
                "radio_settings": None,  # Initialize as None
            }
            processed_devices_list.append(processed_device)

            # For MR (wireless access point) devices, create tasks to fetch more details
            if isinstance(device.get("model"), str) and device.get(
                "model", ""
            ).upper().startswith("MR"):
                network_id: Optional[str] = device.get("networkId")
                # MAC address seems to be used as device_serial by get_meraki_connected_client_count
                # but the function name implies it might be specific to client counting on an AP.
                # The original code used mac_address for client count.
                # Let's assume mac_address is the identifier needed by that specific function.
                ap_identifier_for_clients: Optional[str] = device.get("mac") # or device.get("serial")
                device_serial_for_radio: Optional[str] = device.get("serial")

                mr_device_indices.append(i) # Store index of this MR device

                # Task for connected client count
                if network_id and ap_identifier_for_clients: # ap_identifier_for_clients might not be needed
                    async_tasks.append(
                        self.api_client.wireless.async_get_network_client_count(
                            network_id=network_id # Using network_id as per target method
                        )
                    )
                else:
                    _LOGGER.warning(
                        "Missing networkId or MAC/serial for client count on MR device: %s (%s)",
                        processed_device.get("name"),
                        processed_device.get("serial"),
                    )
                    async_tasks.append(None)  # Placeholder for missing info

                # Task for wireless radio settings
                if device_serial_for_radio:
                    async_tasks.append(
                        self.api_client.wireless.async_get_device_wireless_radio_settings(
                            serial=device_serial_for_radio
                        )
                    )
                else:
                    _LOGGER.warning(
                        "Missing serial for radio settings on MR device: %s (%s)",
                        processed_device.get("name"),
                        processed_device.get("serial"),
                    )
                    async_tasks.append(None)  # Placeholder for missing serial
            # Non-MR devices don't get additional tasks, their slots in `results` will be implicitly skipped.

        # Execute all created tasks concurrently if any exist
        if async_tasks:
            # `return_exceptions=True` allows us to handle individual task failures
            results: List[Union[Any, Exception]] = await asyncio.gather(
                *[task for task in async_tasks if task is not None], return_exceptions=True
            )

            # Assign results back to the corresponding MR devices
            result_idx = 0
            for mr_idx in mr_device_indices:
                target_device = processed_devices_list[mr_idx]
                # Each MR device had two tasks: client count, then radio settings.
                # Only attempt to access results if corresponding tasks were not None.
                # This logic assumes tasks were added in pairs for MR devices.

                # Client count result
                client_task_was_valid = (mr_idx * 2) < len(async_tasks) and async_tasks[mr_idx * 2] is not None
                if client_task_was_valid and result_idx < len(results):
                    client_result = results[result_idx]
                    if isinstance(client_result, int):
                        target_device["connected_clients"] = client_result
                    elif isinstance(client_result, Exception):
                        _LOGGER.warning(
                            "Error fetching client count for MR device %s (%s): %s",
                            target_device.get("name"),
                            target_device.get("serial"),
                            client_result,
                        )
                    result_idx +=1
                elif not client_task_was_valid: # if the task was None to begin with
                    _LOGGER.debug("Skipped client count for MR device %s due to missing info.", target_device.get("serial"))


                # Radio settings result
                radio_task_was_valid = (mr_idx * 2 + 1) < len(async_tasks) and async_tasks[mr_idx * 2 + 1] is not None
                if radio_task_was_valid and result_idx < len(results):
                    radio_result = results[result_idx]
                    if isinstance(radio_result, dict): # Assuming radio settings are a dict
                        target_device["radio_settings"] = radio_result
                    elif isinstance(radio_result, Exception):
                        _LOGGER.warning(
                            "Error fetching radio settings for MR device %s (%s): %s",
                            target_device.get("name"),
                            target_device.get("serial"),
                            radio_result,
                        )
                    result_idx += 1
                elif not radio_task_was_valid: # if the task was None to begin with
                     _LOGGER.debug("Skipped radio settings for MR device %s due to missing info.", target_device.get("serial"))


        _LOGGER.debug("Finished processing %d devices.", len(processed_devices_list))
        return processed_devices_list

    @staticmethod
    def process_networks(
        networks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process a list of network data from the Meraki API.

        Extracts key information for each network.

        Args:
            networks: A list of dictionaries, where each dictionary is a raw
                representation of a network from the Meraki API.

        Returns:
            A list of processed network dictionaries. Each dictionary contains
            selected fields like 'id', 'name', and 'type'.
            Example: `[{"id": "N_123", "name": "Main Office", "type": "wireless"}, ...]`
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
                # Add other relevant network attributes here if needed in the future
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
            A list of processed SSID dictionaries. Each dictionary contains
            selected fields like 'name' and 'enabled'.
            Example: `[{"name": "Guest SSID", "enabled": True, "number": 0}, ...]`
            (assuming 'number' is also a relevant field from SSID details)
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
                "number": ssid.get("number"), # SSID number is often important
                "splashPage": ssid.get("splashPage"),
                "authMode": ssid.get("authMode"),
                # Add other relevant SSID attributes here if needed
                # e.g., "ipAssignmentMode": ssid.get("ipAssignmentMode"),
                # "adminAccess": ssid.get("adminAccessCategory"),
            }
            processed_ssids_list.append(processed_ssid)
        _LOGGER.debug("Processed %d SSIDs.", len(processed_ssids_list))
        return processed_ssids_list
