"""Device data coordinator for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import UpdateFailed

from .base_coordinator import MerakiBaseCoordinator
from ..const import DOMAIN
import aiohttp

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(MerakiBaseCoordinator):
    """Coordinator to fetch device data from Meraki API."""

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch and process device data from Meraki API."""
        device_registry = dr.async_get(self.hass)
        try:
            api_key = self.api_key
            org_id = self.org_id

            _LOGGER.debug("Fetching Meraki devices")
            headers = {
                "X-Cisco-Meraki-API-Key": api_key,
                "Content-Type": "application/json",
            }
            url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"

            _LOGGER.debug(f"Making API call to get networks: {url}")
            async with self.session.get(url, headers=headers) as resp:
                _LOGGER.debug(f"API response status for networks: {resp.status}")
                if resp.status != 200:
                    raise UpdateFailed(
                        "Error communicating with Meraki API for networks"
                    )
                networks = await resp.json()
                _LOGGER.debug(f"Networks retrieved: {networks}")
                devices = []
                for network in networks:
                    device_url = f"https://api.meraki.com/api/v1/networks/{network['id']}/devices"
                    _LOGGER.debug(
                        f"Making API call to get devices from network {network['id']}: {device_url}"
                    )
                    async with self.session.get(
                        device_url, headers=headers
                    ) as device_resp:
                        _LOGGER.debug(
                            f"API response status for devices: {device_resp.status}"
                        )
                        if device_resp.status == 200:
                            retrieved_devices = await device_resp.json()
                            _LOGGER.debug(
                                f"Devices retrieved from network {network['id']}: {retrieved_devices}"
                            )
                            devices.extend(retrieved_devices)
                        else:
                            _LOGGER.warning(
                                f"Failed to get devices from network {network['id']}. Status: {device_resp.status}"
                            )

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
                        async with self.session.get(
                            clients_url, headers=headers
                        ) as clients_resp:
                            _LOGGER.debug(
                                f"API response status for clients: {clients_resp.status}"
                            )
                            if clients_resp.status == 200:
                                clients: List[Dict[str, Any]] = (
                                    await clients_resp.json()
                                )
                                _LOGGER.debug(
                                    f"Clients retrieved for device {device['serial']}: {clients}"
                                )
                                # Filter clients to only those connected to the current device
                                filtered_clients = [
                                    client
                                    for client in clients
                                    if client.get("recentDeviceSerial")
                                    == device["serial"]
                                ]
                                device["connected_clients"] = len(
                                    filtered_clients
                                )  # Store the count here
                                _LOGGER.debug(
                                    f"Added connected_clients key for {device['serial']}: {device['connected_clients']}"
                                )  # added log
                            else:
                                _LOGGER.warning(
                                    f"Failed to get clients for {device['serial']}. Status: {clients_resp.status}"
                                )
                                _LOGGER.debug(
                                    f"Clients API response: {await clients_resp.text()}"
                                )  # added log.
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
                if model.startswith("MR") or model.startswith("GR"):
                    device_type = "Wireless"
                elif model.startswith("MS") or model.startswith("GS"):
                    device_type = "Switch"
                elif model.startswith("MX"):
                    device_type = "Appliance"
                elif model.startswith("MV"):
                    device_type = "Camera"
                elif model.startswith("MT"):
                    device_type = "Sensor"
                else:
                    device_type = "Unknown"

                device_name_format = self.config_entry.options.get(
                    "device_name_format", "omitted"
                )

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

        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error updating device data: {e}")
            raise UpdateFailed(f"Error updating device data: {e}")
        except Exception as e:
            _LOGGER.error(f"Error updating device data: {e}")
            raise UpdateFailed(f"Error updating device data: {e}")
