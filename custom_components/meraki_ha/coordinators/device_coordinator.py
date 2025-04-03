"""Device data coordinator for the meraki_ha integration."""

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


class MerakiDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch device data from Meraki API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
    ) -> None:
        """Initialize the Meraki device coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Devices",
            update_interval=scan_interval,  # Pass scan_interval to super()
        )
        self.api_key = api_key
        self.org_id = org_id
        self.device_name_format = device_name_format
        self.scan_interval = scan_interval  # Store scan_interval as an attribute

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch and process device data from Meraki API."""
        device_registry = dr.async_get(self.hass)
        try:
            from .api_data_fetcher import (
                MerakiApiDataFetcher,
            )  # Import here to avoid circular dependencies

            api_fetcher = MerakiApiDataFetcher(
                self.api_key, self, None, None
            )  # Only Device Coordinator is used here.

            # Get network data to get device data
            networks_url = (
                f"https://api.meraki.com/api/v1/organizations/{self.org_id}/networks"
            )
            networks = await api_fetcher._fetch_data(networks_url)

            devices = []
            if networks:
                for network in networks:
                    device_url = f"https://api.meraki.com/api/v1/networks/{network['id']}/devices"
                    _LOGGER.debug(
                        f"Making API call to get devices from network {network['id']}: {device_url}"
                    )
                    device_data = await api_fetcher._fetch_data(
                        device_url
                    )  # Fetch devices for each network
                    if device_data:
                        devices.extend(device_data)
                    else:
                        _LOGGER.warning(
                            f"Failed to get devices from network {network['id']}."
                        )
            else:
                _LOGGER.warning("No networks found to fetch devices from.")

            _LOGGER.debug(f"Meraki devices returned: {devices}")

            processed_devices = []
            for device in devices:
                _LOGGER.debug(f"Processing device: {device['serial']}")
                device_data = {k: v for k, v in device.items() if k is not None}
                processed_devices.append(device_data)

                _LOGGER.debug(
                    f"Device {device['serial']} productType: {device.get('productType')}"
                )

                if device.get("model", "").startswith("MR") or device.get(
                    "model", ""
                ).startswith("GR"):
                    _LOGGER.debug(f"Fetching clients for {device['serial']}")
                    try:
                        clients_url = f"https://api.meraki.com/api/v1/networks/{device['networkId']}/clients?perPage=1000&serials[]={device['serial']}"
                        _LOGGER.debug(
                            f"Making API call to get clients for device {device['serial']}: {clients_url}"
                        )
                        clients = await api_fetcher._fetch_data(clients_url)
                        if clients:
                            # Filter clients to only those connected to the current device
                            filtered_clients = [
                                client
                                for client in clients
                                if client.get("recentDeviceSerial") == device["serial"]
                            ]
                            device["connected_clients"] = len(
                                filtered_clients
                            )  # Store the count here
                            _LOGGER.debug(
                                f"Added connected_clients key for {device['serial']}: {device['connected_clients']}"
                            )  # added log
                        else:
                            _LOGGER.warning(
                                f"Failed to get clients for {device['serial']}."
                            )
                            device["connected_clients"] = 0  # store 0 if no clients
                            _LOGGER.debug(
                                f"Added connected_clients key for {device['serial']}: {device['connected_clients']}"
                            )  # added log

                    except Exception as client_error:
                        _LOGGER.warning(
                            f"Failed to fetch clients for {device['serial']}: {client_error}"
                        )
                        device["connected_clients"] = 0  # store 0 if client error.
                        _LOGGER.debug(
                            f"Added connected_clients key for {device['serial']}: {device['connected_clients']}"
                        )  # added log

                else:
                    device["connected_clients"] = 0  # store 0 for non wireless devices.
                    _LOGGER.debug(
                        f"Added connected_clients key for {device['serial']}: {device['connected_clients']}"
                    )  # added log

                # Device creation logic
                _LOGGER.debug(f"Creating/Updating device: {device['serial']}")
                model = device.get("model", "Unknown")
                device_name = (
                    device.get("name")
                    if device.get("name") is not None
                    else device["serial"]
                )

                # Map model to device type
                device_type = map_meraki_model_to_device_type(model)

                device_name_format = self.device_name_format

                formatted_device_name = device_name  # default

                if device_name_format == "prefix":
                    formatted_device_name = f"[{device_type}] {device_name}"
                elif device_name_format == "suffix":
                    formatted_device_name = f"{device_name} [{device_type}]"

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, device["serial"])},
                    manufacturer="Cisco Meraki",
                    model=device["model"],
                    name=formatted_device_name,
                    sw_version=device.get("firmware"),
                )
                _LOGGER.debug(f"Device {device['serial']} created/updated")

            return {"devices": processed_devices}

        except Exception as e:
            _LOGGER.error(f"Error updating device data: {e}")
            raise UpdateFailed(f"Error updating device data: {e}")
