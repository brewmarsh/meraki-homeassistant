"""Provides a MerakiDeviceCoordinator for device data fetching and registration.

Note: This module and its `MerakiDeviceCoordinator` class appear to have
overlapping functionality with `custom_components/meraki_ha/coordinators/device_coordinator.py`.
Consider reviewing for redundancy and refactoring to use the primary coordinator
from the `coordinators` package to avoid duplicated logic and potential conflicts.

This coordinator fetches Meraki device data from the API and registers these
devices within the Home Assistant device registry.
"""

import logging
from typing import Any, Dict

import aiohttp
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


from homeassistant.core import HomeAssistant # Added for type hinting
from datetime import timedelta # Added for type hinting


class MerakiDeviceCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator for fetching and managing Meraki device data.

    Note: This class seems to duplicate functionality present in
    `coordinators.device_coordinator.MerakiDeviceCoordinator`.
    It's recommended to consolidate into a single device coordinator.

    This coordinator handles:
    - Fetching all networks for an organization.
    - Fetching all devices within each network.
    - For wireless devices (MR/GR), fetching their connected client list (raw data).
    - Processing and storing device data.
    - Registering/updating devices in the Home Assistant device registry.

    Attributes:
        api_key (str): The Meraki API key.
        org_id (str): The Meraki organization ID.
        session (aiohttp.ClientSession): An aiohttp client session for making API requests.
            Note: Using a shared session passed in `__init__` can be problematic if not
            managed carefully (e.g., closed appropriately). The `MerakiApiDataFetcher`
            in the `coordinators` package manages its own session per request or a shared one internally.
        device_name_format (str): Formatting rule for device names in Home Assistant.
        hass (HomeAssistant): The Home Assistant instance.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        session: aiohttp.ClientSession, # Consider if this session is managed outside.
        update_interval: timedelta,
        device_name_format: str,
    ) -> None:
        """Initializes the MerakiDeviceCoordinator (device_setup.py version).

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): Meraki API key.
            org_id (str): Meraki organization ID.
            session (aiohttp.ClientSession): An externally managed aiohttp client session.
                Be cautious with session lifecycle management if it's passed like this.
            update_interval (timedelta): How often to poll for new data.
            device_name_format (str): Format for device names ("prefix", "suffix", "omitted").
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Devices (device_setup)", # Clarified name for logging
            update_interval=update_interval,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.session = session # Stores the passed-in session
        self.device_name_format = device_name_format
        # self.hass is available from the parent DataUpdateCoordinator class.

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetches and processes Meraki device data from the API.

        This method performs the following steps:
        1. Fetches all networks for the configured organization.
        2. For each network, fetches its list of devices.
        3. For devices identified as wireless APs (MR/GR models), it attempts to
           fetch a list of connected clients.
        4. Processes the raw device data, including client lists for APs.
        5. Registers or updates each Meraki device in the Home Assistant device
           registry, formatting its name according to `device_name_format`.

        Returns:
            Dict[str, Any]: A dictionary containing a key "devices", which maps to
                a list of processed device dictionaries.

        Raises:
            UpdateFailed: If there's a critical error in communicating with the
                Meraki API or processing the data.
        """
        device_registry = dr.async_get(self.hass)
        try:
            _LOGGER.info(
                "Device_setup.py coordinator: Starting Meraki device data update for Org ID %s.",
                self.org_id
            )
            headers = {
                "X-Cisco-Meraki-API-Key": self.api_key,
                "Content-Type": "application/json",
            }
            # Step 1: Fetch networks
            networks_url = (
                f"https://api.meraki.com/api/v1/organizations/{self.org_id}/networks"
            )
            _LOGGER.debug("Fetching networks from: %s", networks_url)
            async with self.session.get(networks_url, headers=headers, timeout=10) as resp:
                if resp.status != 200:
                    _LOGGER.error(
                        "Error fetching networks from Meraki API. Status: %s, Response: %s",
                        resp.status, await resp.text()
                    )
                    raise UpdateFailed(f"Error fetching networks: Status {resp.status}")
                networks_raw = await resp.json()
                _LOGGER.debug("Successfully retrieved %d networks.", len(networks_raw))

            # Step 2: Fetch devices for each network
            all_devices_raw: List[Dict[str, Any]] = []
            if isinstance(networks_raw, list):
                for network in networks_raw:
                    network_id = network.get("id")
                    if not network_id:
                        _LOGGER.warning("Network found without ID: %s", network)
                        continue
                    device_url = (
                        f"https://api.meraki.com/api/v1/networks/{network_id}/devices"
                    )
                    _LOGGER.debug("Fetching devices for network %s from: %s", network_id, device_url)
                    async with self.session.get(device_url, headers=headers, timeout=10) as device_resp:
                        if device_resp.status == 200:
                            network_devices = await device_resp.json()
                            if isinstance(network_devices, list):
                                all_devices_raw.extend(network_devices)
                                _LOGGER.debug("Retrieved %d devices from network %s.", len(network_devices), network_id)
                        else:
                            _LOGGER.warning(
                                "Failed to get devices from network %s. Status: %s, Response: %s",
                                network_id, device_resp.status, await device_resp.text()
                            )
            else:
                _LOGGER.warning("Networks data is not a list: %s", networks_raw)


            _LOGGER.debug("Total raw Meraki devices fetched: %d", len(all_devices_raw))

            # Step 3 & 4: Process devices, fetch clients for APs, and register in HA
            processed_devices_list: List[Dict[str, Any]] = []
            for device_raw in all_devices_raw:
                if not isinstance(device_raw, dict):
                    _LOGGER.warning("Skipping non-dictionary device item: %s", device_raw)
                    continue

                serial = device_raw.get("serial")
                if not serial:
                    _LOGGER.warning("Device found without serial number: %s", device_raw)
                    continue

                # Basic processing (e.g., ensuring no None keys, though rare for dict keys)
                current_device_data = {
                    k: v for k, v in device_raw.items() if k is not None
                }

                # Fetch clients for wireless devices
                product_type = current_device_data.get("productType")
                network_id = current_device_data.get("networkId")
                if network_id and (product_type == "MR" or product_type == "GR"): # Meraki product types for APs
                    _LOGGER.debug("Fetching clients for wireless device %s (Model: %s)", serial, current_device_data.get("model"))
                    try:
                        clients_url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients?perPage=1000&serials[]={serial}"
                        async with self.session.get(clients_url, headers=headers, timeout=10) as clients_resp:
                            if clients_resp.status == 200:
                                clients_data = await clients_resp.json()
                                # Storing raw client list; count can be derived later if needed.
                                current_device_data["connected_clients_raw"] = clients_data
                                _LOGGER.debug("Fetched %d raw client entries for device %s.", len(clients_data) if clients_data else 0, serial)
                            else:
                                _LOGGER.warning(
                                    "Failed to get clients for device %s. Status: %s, Response: %s",
                                    serial, clients_resp.status, await clients_resp.text()
                                )
                                current_device_data["connected_clients_raw"] = []
                    except Exception as client_error:
                        _LOGGER.error("Error fetching clients for device %s: %s", serial, client_error)
                        current_device_data["connected_clients_raw"] = []
                else:
                    current_device_data["connected_clients_raw"] = [] # Ensure key exists

                processed_devices_list.append(current_device_data)

                # Register/Update device in Home Assistant Device Registry
                device_model_ha = current_device_data.get("model", "Unknown")
                device_name_meraki = current_device_data.get("name", serial) # Fallback to serial if name is missing

                # Map Meraki model to a generic device type for naming.
                # This logic is duplicated from coordinators/meraki_device_types.py.
                # Ideally, should use the centralized map_meraki_model_to_device_type function.
                generic_device_type = "Unknown"
                if device_model_ha.startswith("MR") or device_model_ha.startswith("GR"):
                    generic_device_type = "Wireless"
                elif device_model_ha.startswith("MS") or device_model_ha.startswith("GS"):
                    generic_device_type = "Switch"
                elif device_model_ha.startswith("MX"):
                    generic_device_type = "Appliance"
                elif device_model_ha.startswith("MV"):
                    generic_device_type = "Camera"
                elif device_model_ha.startswith("MT"):
                    generic_device_type = "Sensor"

                # Apply name formatting.
                formatted_device_name_ha = device_name_meraki
                if self.device_name_format == "prefix":
                    formatted_device_name_ha = f"[{generic_device_type}] {device_name_meraki}"
                elif self.device_name_format == "suffix":
                    formatted_device_name_ha = f"{device_name_meraki} [{generic_device_type}]"

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, serial)},
                    manufacturer="Cisco Meraki",
                    model=device_model_ha,
                    name=formatted_device_name_ha,
                    sw_version=current_device_data.get("firmware"),
                )
                _LOGGER.debug("Device %s (Model: %s) registered/updated in HA.", serial, device_model_ha)

            _LOGGER.info("Successfully processed %d devices.", len(processed_devices_list))
            return {"devices": processed_devices_list}

        except aiohttp.ClientError as e:
            _LOGGER.error("Network error during Meraki device data update (device_setup.py): %s", e)
            raise UpdateFailed(f"Network error updating device data: {e}") from e
        except UpdateFailed: # Re-raise UpdateFailed if thrown explicitly above
            raise
        except Exception as e:
            _LOGGER.exception("Unexpected error updating Meraki device data (device_setup.py): %s", e)
            raise UpdateFailed(f"Unexpected error updating device data: {e}") from e
