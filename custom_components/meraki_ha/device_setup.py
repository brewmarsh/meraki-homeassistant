"""Device data coordinator for the meraki_ha integration."""

import logging
from typing import Any, Dict

import aiohttp
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch device data from Meraki API."""

    def __init__(
        self, hass, api_key, org_id, session, update_interval, device_name_format
    ):
        """Initialize the MerakiDeviceCoordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Devices",
            update_interval=update_interval,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.session = session
        self.device_name_format = device_name_format

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
            url = f"https://api.meraki.com/api/v1/{org_id}/networks"

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
                _LOGGER.debug(f"Processing device: {device['serial']}")  # added log
                device_data = {k: v for k, v in device.items() if k is not None}
                processed_devices.append(device_data)

                if (
                    device.get("productType") == "MR"
                    or device.get("productType") == "GR"
                ):
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
                                clients = await clients_resp.json()
                                _LOGGER.debug(
                                    f"Clients retrieved for device {device['serial']}: {clients}"
                                )
                                device["connected_clients"] = clients
                            else:
                                _LOGGER.warning(
                                    f"Failed to get clients for {device['serial']}. Status: {clients_resp.status}"
                                )
                                device["connected_clients"] = []

                    except Exception as client_error:
                        _LOGGER.warning(
                            f"Failed to fetch clients for {device['serial']}: {client_error}"
                        )
                        device["connected_clients"] = []
                else:
                    device["connected_clients"] = []

                # Device creation logic
                _LOGGER.debug(f"Creating/Updating device: {device['serial']}")
                model = device.get("model", "Unknown")
                device_name = (
                    device.get("name", "Unknown Device")
                    if device.get("name") is not None
                    else "Unknown Device"
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

                device_name_format = self.device_name_format

                if device_name_format == "prefix":
                    formatted_device_name = f"[{device_type}] {device_name}"
                elif device_name_format == "suffix":
                    formatted_device_name = f"{device_name} [{device_type}]"
                else:
                    formatted_device_name = device_name

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
