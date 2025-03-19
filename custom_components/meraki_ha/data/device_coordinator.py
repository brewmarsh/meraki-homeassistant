"""Device data coordinator for the meraki_ha integration."""

import logging
from typing import Any, Dict

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

            _LOGGER.debug(f"Making API call to get networks: {url}")  # added log
            async with self.session.get(url, headers=headers) as resp:
                _LOGGER.debug(
                    f"API response status for networks: {resp.status}"
                )  # added log
                if resp.status != 200:
                    raise UpdateFailed("Error communicating with Meraki API")
                networks = await resp.json()
                _LOGGER.debug(f"Networks retrieved: {networks}")  # added log
                devices = []
                for network in networks:
                    device_url = f"https://api.meraki.com/api/v1/networks/{network['id']}/devices"
                    _LOGGER.debug(
                        f"Making API call to get devices from network {network['id']}: {device_url}"
                    )  # added log
                    async with self.session.get(
                        device_url, headers=headers
                    ) as device_resp:
                        _LOGGER.debug(
                            f"API response status for devices: {device_resp.status}"
                        )  # added log
                        if device_resp.status == 200:
                            retrieved_devices = await device_resp.json()
                            _LOGGER.debug(
                                f"Devices retrieved from network {network['id']}: {retrieved_devices}"
                            )  # added log
                            devices.extend(retrieved_devices)

            _LOGGER.debug(f"Meraki devices returned: {devices}")

            processed_devices = []
            for device in devices:
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
                        )  # added log
                        async with self.session.get(
                            clients_url, headers=headers
                        ) as clients_resp:
                            _LOGGER.debug(
                                f"API response status for clients: {clients_resp.status}"
                            )  # added log
                            if clients_resp.status == 200:
                                clients = await clients_resp.json()
                                _LOGGER.debug(
                                    f"Clients retrieved for device {device['serial']}: {clients}"
                                )  # added log
                                device["connected_clients"] = clients
                            else:
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
                device_type = device.get("productType", "Unknown")
                device_name = device["name"]
                device_name_format = self.config_entry.options.get(
                    "device_name_format", "omitted"
                )

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
