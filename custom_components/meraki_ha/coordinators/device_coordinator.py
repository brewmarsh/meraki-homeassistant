"""Provides the MerakiDeviceCoordinator for the Meraki Home Assistant integration.

This module defines `MerakiDeviceCoordinator`, a Home Assistant
`DataUpdateCoordinator` responsible for fetching and processing Meraki device
data from the API. It also handles the creation and updating of device
entries in the Home Assistant device registry.
"""

import logging
from typing import Any, Dict
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ..const import DOMAIN
from .meraki_device_types import (
    map_meraki_model_to_device_type,
)  # Import the mapping function

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinates fetching and processing of Meraki device data.

    This coordinator is responsible for:
    1. Fetching all networks within an organization.
    2. Fetching all devices within each of those networks.
    3. For wireless devices (MR/GR models), fetching their connected client counts.
    4. Processing the raw device data.
    5. Creating or updating corresponding device entries in the Home Assistant
       device registry, formatting names based on user preference.

    Attributes:
        api_key (str): The Meraki API key.
        org_id (str): The Meraki organization ID.
        device_name_format (str): User-selected format for device names in
            Home Assistant (e.g., "prefix", "suffix", or default).
        scan_interval (timedelta): How often to update the data.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
    ) -> None:
        """Initializes the MerakiDeviceCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): The Meraki API key for authentication.
            org_id (str): The Meraki organization ID to scope data fetching.
            scan_interval (timedelta): The interval at which to periodically
                update the device data.
            device_name_format (str): A string indicating how to format device
                names (e.g., "prefix", "suffix", "omitted/default").
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Devices",  # Coordinator name for logging
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.device_name_format = device_name_format
        # scan_interval is already stored by the parent DataUpdateCoordinator
        # self.scan_interval = scan_interval

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetches, processes, and registers Meraki device data.

        This is the core method called by Home Assistant to update data.
        It fetches networks, then devices per network, client counts for
        wireless devices, and finally updates the HA device registry.

        Returns:
            Dict[str, Any]: A dictionary containing a single key "devices"
                which maps to a list of processed device dictionaries.

        Raises:
            UpdateFailed: If a critical error occurs during data fetching or
                processing that prevents a successful update.
        """
        device_registry = dr.async_get(self.hass)
        try:
            # Local import to avoid circular dependencies at module load time.
            from .api_data_fetcher import MerakiApiDataFetcher

            # Initialize the API fetcher. Note: `self` (this coordinator) and
            # None for other coordinators are passed, as MerakiApiDataFetcher
            # is used here primarily for its _fetch_data method with retry logic.
            api_fetcher = MerakiApiDataFetcher(self.api_key, self, None, None)

            # Step 1: Fetch all networks in the organization.
            networks_url = (
                f"https://api.meraki.com/api/v1/organizations/{self.org_id}/networks"
            )
            _LOGGER.debug("Fetching networks from URL: %s", networks_url)
            networks_raw = await api_fetcher._fetch_data(networks_url)

            all_devices_raw: list = []
            if networks_raw and isinstance(networks_raw, list):
                _LOGGER.info("Fetched %d networks. Now fetching devices per network.", len(networks_raw))
                for network in networks_raw:
                    network_id = network.get("id")
                    if not network_id:
                        _LOGGER.warning("Network found without ID: %s", network)
                        continue

                    # Step 2: Fetch devices for each network.
                    device_url = (
                        f"https://api.meraki.com/api/v1/networks/{network_id}/devices"
                    )
                    _LOGGER.debug(
                        "Fetching devices for network %s from URL: %s",
                        network_id,
                        device_url,
                    )
                    network_devices_raw = await api_fetcher._fetch_data(device_url)
                    if network_devices_raw and isinstance(network_devices_raw, list):
                        all_devices_raw.extend(network_devices_raw)
                    else:
                        _LOGGER.warning(
                            "No devices found or failed to fetch devices for network %s.",
                            network_id,
                        )
            else:
                _LOGGER.warning(
                    "No networks found for organization %s, or data format is unexpected.", self.org_id
                )
                # If no networks, no devices can be fetched.
                # Consider UpdateFailed if networks are essential. For now, returns empty list.

            _LOGGER.debug("Total raw Meraki devices returned: %d", len(all_devices_raw))

            processed_devices_list: List[Dict[str, Any]] = []
            for device_raw in all_devices_raw:
                if not isinstance(device_raw, dict):
                    _LOGGER.warning("Skipping non-dictionary device item: %s", device_raw)
                    continue

                serial = device_raw.get("serial")
                if not serial:
                    _LOGGER.warning("Device found without serial number: %s", device_raw)
                    continue

                _LOGGER.debug("Processing device: %s", serial)
                # Basic processing: filter out None keys (though unusual for dict keys)
                # More importantly, ensure all expected keys for HA entities exist.
                current_device_data = {
                    k: v for k, v in device_raw.items() if k is not None
                }

                # Step 3: Fetch connected client count for wireless devices (MR/GR models).
                model = current_device_data.get("model", "")
                network_id = current_device_data.get("networkId") # Used for client fetching
                if network_id and (model.startswith("MR") or model.startswith("GR")):
                    _LOGGER.debug("Fetching clients for wireless device %s (Model: %s)", serial, model)
                    try:
                        # API endpoint to get clients for a specific device in a network.
                        clients_url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients?perPage=1000&serials[]={serial}"
                        _LOGGER.debug(
                            "Fetching clients for device %s from URL: %s",
                            serial,
                            clients_url,
                        )
                        clients_raw = await api_fetcher._fetch_data(clients_url)

                        if clients_raw and isinstance(clients_raw, list):
                            # Filter clients that are actually connected to *this* AP.
                            # The `serials[]=` query param should ideally handle this,
                            # but `recentDeviceSerial` is a more explicit check if clients roam.
                            # Meraki API for /clients with `serials[]` param usually returns clients *last seen* by that serial.
                            # So, filtering by `recentDeviceSerial` might be redundant if API behaves as expected.
                            # However, if clients can be listed under a network but associated with a different AP in some edge cases, this is safer.
                            # For now, assuming `serials[]` correctly filters.
                            # If further filtering is needed:
                            # filtered_clients = [
                            #    c for c in clients_raw if isinstance(c, dict) and c.get("recentDeviceSerial") == serial and c.get("status") == "Online"
                            # ]
                            # current_device_data["connected_clients"] = len(filtered_clients)
                            current_device_data["connected_clients"] = len(clients_raw)
                            _LOGGER.debug(
                                "Device %s has %d connected clients.",
                                serial,
                                current_device_data["connected_clients"],
                            )
                        else:
                            _LOGGER.warning("No clients found or failed to fetch for device %s.", serial)
                            current_device_data["connected_clients"] = 0
                    except Exception as client_error:
                        _LOGGER.warning(
                            "Failed to fetch clients for device %s: %s. Setting count to 0.",
                            serial,
                            client_error,
                        )
                        current_device_data["connected_clients"] = 0
                else:
                    # Not a wireless device or no networkId, so no client count.
                    current_device_data["connected_clients"] = 0

                processed_devices_list.append(current_device_data)

                # Step 4: Create or update device in Home Assistant device registry.
                _LOGGER.debug("Registering/Updating device in HA: %s", serial)
                device_model = current_device_data.get("model", "Unknown")
                # Use device name if available, otherwise fall back to serial.
                device_name_ha = (
                    current_device_data.get("name")
                    if current_device_data.get("name")
                    else serial
                )

                # Map Meraki model to a more general device type (e.g., "Switch", "AP").
                device_type_mapped = map_meraki_model_to_device_type(device_model)

                # Apply user-defined name formatting.
                formatted_device_name_ha = device_name_ha
                if self.device_name_format == "prefix":
                    formatted_device_name_ha = f"[{device_type_mapped}] {device_name_ha}"
                elif self.device_name_format == "suffix":
                    formatted_device_name_ha = f"{device_name_ha} [{device_type_mapped}]"

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, serial)},  # Unique identifier for the device
                    manufacturer="Cisco Meraki",
                    model=device_model,
                    name=formatted_device_name_ha,
                    sw_version=current_device_data.get("firmware"),
                    # Add other relevant device info like hw_version, configuration_url if available
                )
                _LOGGER.debug("Device %s successfully registered/updated in HA.", serial)

            # Return the processed list of devices for other coordinators or entities to use.
            return {"devices": processed_devices_list}

        except aiohttp.ClientResponseError as err:
            # Handle specific API errors (e.g., auth, not found)
            _LOGGER.error("API request failed with status %s: %s", err.status, err.message)
            raise UpdateFailed(f"API request failed: {err.message} (Status: {err.status})") from err
        except aiohttp.ClientError as err:
            # Handle client-side errors (e.g., connection, timeout)
            _LOGGER.error("API client error: %s", err)
            raise UpdateFailed(f"API client error: {err}") from err
        except Exception as e:
            # Catch any other unexpected errors during the update process.
            _LOGGER.exception("Unexpected error updating Meraki device data: %s", e)
            raise UpdateFailed(f"Unexpected error updating device data: {e}") from e
