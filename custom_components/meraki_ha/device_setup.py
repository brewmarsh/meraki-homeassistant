"""Handles Meraki device setup and registration within Home Assistant.

This module defines `MerakiDeviceCoordinator`, a Home Assistant
DataUpdateCoordinator subclass responsible for fetching device
information from the Meraki API, processing it, and registering or
updating corresponding devices in the Home Assistant device registry.
"""
import logging
from datetime import timedelta  # For type hinting scan_interval
from typing import Any, Dict, List, Optional  # Added List, Optional

import aiohttp  # For API communication
from homeassistant.config_entries import ConfigEntry  # For self.config_entry type hint
from homeassistant.core import HomeAssistant  # For type hinting hass
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

# For device identifiers and logger naming
from .const import DOMAIN
# Assuming meraki_device_types.py exists in the same directory or a
# place that can be imported
from .coordinators.meraki_device_types import map_meraki_model_to_device_type


_LOGGER = logging.getLogger(__name__)

MERAKI_API_BASE_URL = "https://api.meraki.com/api/v1"


# Generic type for self.data
class MerakiDeviceCoordinator(
    DataUpdateCoordinator[Dict[str, List[Dict[str, Any]]]]
):
    """Coordinator to fetch, process, and register Meraki device data.

    This coordinator retrieves all devices across all networks within a
    Meraki organization. It enriches data for certain device types
    (e.g., client counts for wireless APs) and ensures each Meraki
    device is represented in the Home Assistant device registry with
    appropriate attributes.
    """

    # config_entry is automatically set by HA when the coordinator is
    # stored in hass.data
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        session: aiohttp.ClientSession,  # Expecting a shared aiohttp session
        update_interval: timedelta,
        device_name_format: str,
    ) -> None:
        """Initialize the MerakiDeviceCoordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key for authentication.
            org_id: The Meraki Organization ID to scope API calls.
            session: An `aiohttp.ClientSession` for making HTTP requests.
            update_interval: The interval at which to periodically update
                device data.
            device_name_format: The user-selected format for device names
                in Home Assistant (e.g., "prefix", "suffix", "omitted").
        """
        super().__init__(
            hass,
            _LOGGER,
            # Specific name for logging/debugging
            name=f"{DOMAIN} Devices ({org_id})",
            update_interval=update_interval,
        )
        self.api_key: str = api_key
        self.org_id: str = org_id
        self.session: aiohttp.ClientSession = session
        self.device_name_format: str = device_name_format
        # Initialize self.data to match the expected generic type
        self.data: Dict[str, List[Dict[str, Any]]] = {"devices": []}

    async def _async_update_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch, process, and register/update device data from Meraki API.

        This core method orchestrates the retrieval of networks, then
        devices within those networks. It enriches data for MR/GR access
        points by fetching their connected client counts. Finally, it
        uses the Home Assistant device registry to create or update
        entries for each Meraki device.

        Returns:
            A dictionary containing a list of processed device data under
            the "devices" key. Example: `{"devices": [{"serial":
            "Qxxx-xxxx-xxxx", "name": "AP1", ...}, ...]}`

        Raises:
            UpdateFailed: If a critical error occurs during API
                communication or data processing that prevents a
                successful update.
        """
        device_registry = dr.async_get(self.hass)
        headers: Dict[str, str] = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            _LOGGER.debug(
                "Fetching all networks for organization: %s", self.org_id
            )
            networks_url = (
                f"{MERAKI_API_BASE_URL}/organizations/{self.org_id}/networks"
            )
            async with self.session.get(
                networks_url, headers=headers
            ) as resp:
                _LOGGER.debug(
                    "API response status for networks org %s: %s",
                    self.org_id,
                    resp.status,
                )
                if resp.status != 200:
                    error_text = await resp.text()
                    _LOGGER.error(
                        "Error fetching networks for org %s: %s - %s",
                        self.org_id,
                        resp.status,
                        error_text,
                    )
                    raise UpdateFailed(
                        "Error communicating with Meraki API for networks: "
                        f"{resp.status}"
                    )
                networks: List[Dict[str, Any]] = await resp.json()
                _LOGGER.debug(
                    "Networks retrieved for org %s: %d",
                    self.org_id,
                    len(networks),
                )

            all_devices_raw: List[Dict[str, Any]] = []
            for network in networks:
                network_id: Optional[str] = network.get("id")
                if not network_id:
                    _LOGGER.warning(
                        "Network found without ID in org %s: %s",
                        self.org_id,
                        network,
                    )
                    continue

                devices_url = (
                    f"{MERAKI_API_BASE_URL}/networks/{network_id}/devices"
                )
                _LOGGER.debug(
                    "Fetching devices for network %s (org %s)",
                    network_id,
                    self.org_id,
                )
                async with self.session.get(
                    devices_url, headers=headers
                ) as device_resp:
                    _LOGGER.debug(
                        "API response status for devices in network %s: %s",
                        network_id,
                        device_resp.status,
                    )
                    if device_resp.status == 200:
                        network_devices: List[
                            Dict[str, Any]
                        ] = await device_resp.json()
                        all_devices_raw.extend(network_devices)
                    else:
                        error_text = await device_resp.text()
                        _LOGGER.warning(
                            "Failed to get devices from network %s (org %s). "
                            "Status: %s - %s",
                            network_id,
                            self.org_id,
                            device_resp.status,
                            error_text,
                        )
            _LOGGER.info(
                "Total raw devices fetched for org %s: %d",
                self.org_id,
                len(all_devices_raw),
            )

            processed_devices_list: List[Dict[str, Any]] = []
            for device_raw in all_devices_raw:
                serial = device_raw.get("serial")
                if not serial:
                    _LOGGER.warning(
                        "Device found without serial in org %s: %s",
                        self.org_id,
                        device_raw,
                    )
                    continue

                # Create a copy to avoid modifying the raw data if it's
                # used elsewhere or for retry logic
                device_processed = device_raw.copy()

                # Fetch connected clients for MR (Wireless AP) and GR
                # (Gateway Router with AP) devices
                model: str = device_processed.get("model", "")
                if model.upper().startswith(("MR", "GR")):
                    network_id_for_clients = device_processed.get("networkId")
                    if network_id_for_clients:
                        # API to get clients connected to a specific AP uses
                        # device serial in `serials[]` query param
                        clients_url = (
                            f"{MERAKI_API_BASE_URL}/networks/"
                            f"{network_id_for_clients}/clients"
                        )
                        # Max perPage to get all clients for this AP
                        params = {"serials[]": serial, "perPage": "1000"}
                        _LOGGER.debug(
                            "Fetching clients for AP %s (Serial: %s) in "
                            "network %s (org %s)",
                            device_processed.get("name", serial),
                            serial,
                            network_id_for_clients,
                            self.org_id,
                        )
                        try:
                            async with self.session.get(
                                clients_url, headers=headers, params=params
                            ) as clients_resp:
                                if clients_resp.status == 200:
                                    clients: List[
                                        Dict[str, Any]
                                    ] = await clients_resp.json()
                                    # The API with `serials[]` filter should
                                    # return only clients connected to this AP.
                                    device_processed[
                                        "connected_clients_count"
                                    ] = len(clients)
                                else:
                                    error_text = await clients_resp.text()
                                    _LOGGER.warning(
                                        "Failed to get clients for AP %s "
                                        "(Serial: %s). Status: %s - %s",
                                        serial,
                                        self.org_id,
                                        clients_resp.status,
                                        error_text,
                                    )
                                    # Default on error
                                    device_processed["connected_clients_count"] = 0
                        except aiohttp.ClientError as client_e:
                            _LOGGER.error(
                                "ClientError fetching clients for AP %s "
                                "(Serial: %s): %s",
                                serial,
                                self.org_id,
                                client_e,
                            )
                            device_processed["connected_clients_count"] = 0
                        except Exception as client_e:  # Catch broader errors
                            _LOGGER.exception(
                                "Unexpected error fetching clients for AP %s "
                                "(Serial: %s): %s",
                                serial,
                                self.org_id,
                                client_e,
                            )
                            device_processed["connected_clients_count"] = 0
                    else:
                        _LOGGER.warning(
                            "Missing networkId for AP %s (Serial: %s), "
                            "cannot fetch clients.",
                            serial,
                            self.org_id,
                        )
                        device_processed["connected_clients_count"] = 0
                else:
                    # Not an AP
                    device_processed["connected_clients_count"] = 0

                processed_devices_list.append(device_processed)

                # Register or update device in Home Assistant Device Registry
                # Fallback to serial
                device_name_raw: str = device_processed.get("name") or serial
                device_model_str: str = device_processed.get(
                    "model", "Unknown"
                )
                device_type_mapped: str = map_meraki_model_to_device_type(
                    device_model_str
                )
                firmware_version: Optional[
                    str
                ] = device_processed.get("firmware")

                formatted_device_name: str = device_name_raw
                if self.device_name_format == "prefix" and \
                   device_type_mapped != "Unknown":
                    formatted_device_name = (
                        f"[{device_type_mapped}] {device_name_raw}"
                    )
                elif self.device_name_format == "suffix" and \
                     device_type_mapped != "Unknown":
                    formatted_device_name = (
                        f"{device_name_raw} [{device_type_mapped}]"
                    )

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, serial)},
                    manufacturer="Cisco Meraki",
                    model=device_model_str,
                    name=formatted_device_name,
                    sw_version=firmware_version,
                )
                _LOGGER.debug(
                    "Device %s (Serial: %s, Model: %s) processed and "
                    "registered/updated in org %s.",
                    formatted_device_name,
                    serial,
                    device_model_str,
                    self.org_id,
                )
            self.data = {"devices": processed_devices_list}
            return self.data

        except aiohttp.ClientError as e:
            _LOGGER.error(
                "ClientError during Meraki device data update for org %s: %s",
                self.org_id,
                e,
            )
            raise UpdateFailed(f"API communication error: {e}") from e
        except Exception as e:  # Catch-all for other unexpected errors
            _LOGGER.exception(
                "Unexpected error during Meraki device data update for org %s: %s",
                self.org_id,
                e,
            )
            raise UpdateFailed(f"Unexpected error: {e}") from e
