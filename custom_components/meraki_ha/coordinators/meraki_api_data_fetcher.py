"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices (including tags), SSIDs, and device-specific details
like client counts and radio settings for MR devices, using the Meraki SDK.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError  # type: ignore

from ..api.meraki_api import MerakiAPIClient
from .meraki_api_client import MerakiAPIClientWrapper
from .meraki_data_processor import process_firmware_upgrades
from .meraki_device_types import map_meraki_model_to_device_type

_LOGGER = logging.getLogger(__name__)


class MerakiApiDataFetcher:
    """Class to fetch data from the Meraki API using the Meraki SDK."""

    def __init__(self, meraki_client: MerakiAPIClient) -> None:
        """Initialize the MerakiApiDataFetcher."""
        self.meraki_client: MerakiAPIClient = meraki_client
        self.org_id: str = meraki_client.org_id
        self.api_client = MerakiAPIClientWrapper(self.meraki_client)
        self.devices: list[dict[str, Any]] | None = None
        self.networks: list[dict[str, Any]] | None = None

    async def fetch_all_data(self, hass: HomeAssistant) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization."""
        _LOGGER.debug(f"Fetching all data for organization ID: {self.org_id} using SDK")

        results = await asyncio.gather(
            self.api_client.call(
                self.meraki_client.organizations.getOrganizations(),
                "getOrganizations",
            ),
            self.async_get_networks(self.org_id),
            self.async_get_organization_devices(self.org_id),
            self.api_client.call(
                self.meraki_client.organizations.getOrganizationDevicesStatuses(
                    self.org_id, total_pages="all"
                ),
                "getOrganizationDevicesStatuses",
            ),
            self.api_client.call(
                self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                    self.org_id
                ),
                "getOrganizationFirmwareUpgrades",
            ),
            return_exceptions=True,
        )

        (
            organizations,
            networks,
            devices,
            statuses_data,
            firmware_upgrade_data_raw,
        ) = results

        if networks is None:
            raise UpdateFailed(f"Could not fetch Meraki networks for org {self.org_id}.")
        if devices is None:
            raise UpdateFailed(f"Fetched Meraki devices data is None for org {self.org_id}.")

        self._process_device_statuses(devices, statuses_data)
        await self._fetch_additional_device_details(devices)
        process_firmware_upgrades(devices, firmware_upgrade_data_raw, self.org_id)

        ssids = await self._fetch_ssids(networks)
        all_clients = await self._fetch_all_clients(networks)
        (
            clients_on_ssids,
            clients_on_appliances,
            clients_on_wireless,
        ) = self._aggregate_client_counts(all_clients, devices)

        org_name = self._get_org_name(organizations)

        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
            "clients": all_clients,
            "clients_on_ssids": clients_on_ssids,
            "clients_on_appliances": clients_on_appliances,
            "clients_on_wireless": clients_on_wireless,
            "org_name": org_name,
        }

    def _get_org_name(self, organizations: Optional[List[Dict[str, Any]]]) -> Optional[str]:
        """Extract the organization name from the list of organizations."""
        if isinstance(organizations, list):
            for org in organizations:
                if org.get("id") == self.org_id:
                    return org.get("name")
        return None

    def _process_device_statuses(
        self,
        devices: List[Dict[str, Any]],
        statuses_data: Optional[List[Dict[str, Any]]],
    ) -> None:
        """Merge device statuses into the device list."""
        if not statuses_data or not isinstance(statuses_data, list):
            _LOGGER.warning("Device status data is unavailable or not a list.")
            return

        device_statuses_map = {
            status["serial"]: status
            for status in statuses_data
            if isinstance(status, dict) and "serial" in status
        }

        for device in devices:
            if not isinstance(device, dict):
                continue
            serial = device.get("serial")
            if serial in device_statuses_map:
                device.update(device_statuses_map[serial])

    async def _fetch_additional_device_details(
        self, devices: List[Dict[str, Any]]
    ) -> None:
        """Fetch additional details for specific device types."""
        tasks = []
        for device in devices:
            if not isinstance(device, dict):
                continue

            device_model = device.get("model", "")
            generic_device_type = map_meraki_model_to_device_type(device_model)

            if map_meraki_model_to_device_type(device.get("model", "")) == "Wireless" or "MR" in device.get("model", "") or "GR" in device.get("model", "") or "CW" in device.get("model", ""):
                tasks.append(self._async_get_mr_device_details(device, device.get("serial")))
            elif device_model.upper().startswith("MX"):
                tasks.append(self._async_get_mx_device_uplink_settings(device))
                tasks.append(self._async_get_mx_lan_dns_settings(device))
            elif device.get("productType") == "camera" or device_model.upper().startswith(
                "MV"
            ):
                tasks.append(self._async_get_camera_video_settings(device))

        if tasks:
            await asyncio.gather(*tasks)

    async def _fetch_ssids(self, networks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fetch all SSIDs for the given networks."""
        ssid_tasks = [
            self.api_client.call(
                self.meraki_client.wireless.getNetworkWirelessSsids(network["id"]),
                f"getNetworkWirelessSsids(networkId={network['id']})",
                return_empty_list_on_404=True,
            )
            for network in networks
            if "id" in network
        ]
        results = await asyncio.gather(*ssid_tasks, return_exceptions=True)
        ssids = []
        for result in results:
            if isinstance(result, list):
                ssids.extend(result)
            elif result is not None:
                _LOGGER.error("Error fetching SSIDs: %s", result)
        return ssids

    def _aggregate_client_counts(
        self, all_clients: List[Dict[str, Any]], devices: List[Dict[str, Any]]
    ) -> tuple[int, int, int]:
        """Aggregate client counts based on device types."""
        device_serial_to_type_map = {
            device["serial"]: map_meraki_model_to_device_type(device.get("model", ""))
            for device in devices
            if "serial" in device
        }

        clients_on_ssids = 0
        clients_on_wireless = 0
        clients_on_appliances = 0

        for client in all_clients:
            if not isinstance(client, dict):
                continue
            if client.get("ssid"):
                clients_on_ssids += 1

            ap_serial = client.get("ap_serial")
            if ap_serial and ap_serial in device_serial_to_type_map:
                device_type = device_serial_to_type_map[ap_serial]
                if device_type == "Wireless":
                    clients_on_wireless += 1
                elif device_type == "Appliance":
                    clients_on_appliances += 1

        return clients_on_ssids, clients_on_appliances, clients_on_wireless

    async def _async_get_mr_device_details(self, device: Dict[str, Any], serial: str) -> None:
        """Fetch details for MR (wireless) devices."""
        if not serial:
            return

        clients_data = await self.api_client.call(
            self.meraki_client.devices.getDeviceClients(serial=serial),
            f"getDeviceClients(serial={serial})",
        )
        device["connected_clients_count"] = (
            len(clients_data) if isinstance(clients_data, list) else 0
        )

        radio_settings_data = await self.api_client.call(
            self.meraki_client.wireless.getDeviceWirelessRadioSettings(serial=serial),
            f"getDeviceWirelessRadioSettings(serial={serial})",
        )
        device["radio_settings"] = radio_settings_data

    async def _async_get_mx_device_uplink_settings(self, device: Dict[str, Any]) -> None:
        """Fetch uplink settings for MX (appliance) devices."""
        serial = device.get("serial")
        if not serial:
            return

        uplink_settings = await self.api_client.call(
            self.meraki_client.devices.getDeviceClients(serial=serial),
            f"getDeviceClients(serial={serial})",
        )
        device["uplink_settings"] = uplink_settings

    async def _async_get_mx_lan_dns_settings(self, device: Dict[str, Any]) -> None:
        """Fetch LAN DNS settings for MX (appliance) devices."""
        network_id = device.get("networkId")
        if not network_id:
            return

        lan_dns_settings = await self.api_client.call(
            self.meraki_client.networks.getNetworkAlertsSettings(
                networkId=network_id
            ),
            f"getNetworkAlertsSettings(networkId={network_id})",
        )
        device["lan_dns_settings"] = lan_dns_settings

    async def _async_get_camera_video_settings(self, device: Dict[str, Any]) -> None:
        """Fetch video settings for camera devices."""
        serial = device.get("serial")
        if not serial:
            return

        video_settings = await self.api_client.call(
            self.meraki_client.camera.getDeviceCameraVideoSettings(serial=serial),
            f"getDeviceCameraVideoSettings(serial={serial})",
        )
        if video_settings:
            device["externalRtspEnabled"] = video_settings.get("externalRtspEnabled")
            device["rtspUrl"] = video_settings.get("rtspUrl")

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization."""
        return await self.api_client.call(
            self.meraki_client.organizations.getOrganizationNetworks(
                organizationId=org_id
            ),
            f"getOrganizationNetworks(organizationId={org_id})",
            return_empty_list_on_404=True,
        )

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization."""
        return await self.api_client.call(
            self.meraki_client.organizations.getOrganizationDevices(
                organizationId=org_id
            ),
            f"getOrganizationDevices(organizationId={org_id})",
            return_empty_list_on_404=True,
        )

    async def _fetch_all_clients(
        self, networks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fetch all clients for a list of networks."""
        client_tasks = [
            self.api_client.call(
                self.meraki_client.networks.getNetworkClients(
                    network["id"], timespan=3600
                ),
                f"getNetworkClients(networkId={network['id']})",
                return_empty_list_on_404=True,
            )
            for network in networks
            if "id" in network
        ]
        results = await asyncio.gather(*client_tasks, return_exceptions=True)
        all_clients = []
        for result in results:
            if isinstance(result, list):
                all_clients.extend(result)
            elif result is not None:
                _LOGGER.error("Error fetching clients: %s", result)
        return all_clients
