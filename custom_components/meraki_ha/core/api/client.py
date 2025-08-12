"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

import asyncio
from functools import partial
import logging
from typing import Any

import meraki

from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints
from ...core.errors import MerakiAuthenticationError, MerakiConnectionError

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """
    Facade for the Meraki Dashboard API client.
    This client provides access to various endpoint categories and handles
    the underlying API session and asynchronous execution.
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.meraki.com/api/v1",
    ) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._org_id = org_id
        self._dashboard = meraki.DashboardAPI(
            api_key=api_key,
            base_url=base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

        # Initialize endpoint handlers
        self.appliance = ApplianceEndpoints(self)
        self.camera = CameraEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.organization = OrganizationEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)

    async def _run_sync(self, func, *args, **kwargs) -> Any:
        """Run a synchronous function in a thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def get_all_data(self) -> dict:
        """Fetch all data from the Meraki API."""
        networks = await self.organization.get_organization_networks()
        devices = await self.organization.get_organization_devices()
        devices_availabilities = (
            await self.organization.get_organization_devices_availabilities()
        )
        availabilities_by_serial = {
            availability["serial"]: availability
            for availability in devices_availabilities
        }

        for device in devices:
            if availability := availabilities_by_serial.get(device["serial"]):
                device["status"] = availability["status"]

        clients = []
        for network in networks:
            network_clients = await self.network.get_network_clients(network["id"])
            for client in network_clients:
                client["networkId"] = network["id"]
            clients.extend(network_clients)
        ssids = []
        for network in networks:
            network_ssids = await self.wireless.get_network_ssids(network["id"])
            configured_ssids = []
            for ssid in network_ssids:
                _LOGGER.debug("Processing SSID: '%s'", ssid.get("name"))
                if "unconfigured ssid" not in ssid.get("name", "").lower():
                    _LOGGER.debug("SSID '%s' is configured, adding.", ssid.get("name"))
                    ssid["networkId"] = network["id"]
                    configured_ssids.append(ssid)
                else:
                    _LOGGER.debug(
                        "SSID '%s' is unconfigured, filtering out.", ssid.get("name")
                    )
            ssids.extend(configured_ssids)

        for device in devices:
            if device.get("productType") == "wireless":
                radio_settings = await self.wireless.get_wireless_settings(
                    device["serial"]
                )
                device["radio_settings"] = radio_settings
            elif device.get("productType") == "appliance":
                appliance_settings = await self.appliance.get_network_appliance_settings(
                    device["networkId"]
                )
                if appliance_settings and "dynamicDns" in appliance_settings:
                    device["dynamicDns"] = appliance_settings["dynamicDns"]
            elif device.get("productType") == "camera":
                video_settings = await self.camera.get_camera_video_settings(
                    device["serial"]
                )
                device["video_settings"] = video_settings
            elif device.get("productType") == "switch":
                ports_statuses = await self.switch.get_device_switch_ports_statuses(
                    device["serial"]
                )
                device["ports_statuses"] = ports_statuses
        appliance_traffic = {}
        for network in networks:
            if "appliance" in network.get("productTypes", []):
                try:
                    traffic = await self.network.get_network_traffic(
                        network["id"], "appliance"
                    )
                    appliance_traffic[network["id"]] = traffic
                except (MerakiAuthenticationError, MerakiConnectionError) as e:
                    _LOGGER.warning(
                        "Could not fetch traffic data for network %s, please ensure 'Traffic analysis' is enabled in the Meraki Dashboard. Error: %s",
                        network["id"],
                        e,
                    )
                    appliance_traffic[network["id"]] = {"error": "disabled"}

        vlans_by_network = {}
        for network in networks:
            if "appliance" in network.get("productTypes", []):
                try:
                    vlans = await self.appliance.get_vlans(network["id"])
                    vlans_by_network[network["id"]] = vlans
                except (MerakiAuthenticationError, MerakiConnectionError) as e:
                    _LOGGER.warning(
                        "Could not fetch VLAN data for network %s, please ensure VLANs are enabled in the Meraki Dashboard. Error: %s",
                        network["id"],
                        e,
                    )
                    vlans_by_network[network["id"]] = []

        appliance_uplink_statuses = (
            await self.organization.get_organization_appliance_uplink_statuses()
        )

        rf_profiles_by_network = {}
        for network in networks:
            if "wireless" in network.get("productTypes", []):
                rf_profiles = await self.wireless.get_network_wireless_rf_profiles(
                    network["id"]
                )
                rf_profiles_by_network[network["id"]] = rf_profiles

        data = {
            "networks": networks,
            "devices": devices,
            "clients": clients,
            "ssids": ssids,
            "appliance_traffic": appliance_traffic,
            "vlans": vlans_by_network,
            "appliance_uplink_statuses": appliance_uplink_statuses,
            "rf_profiles": rf_profiles_by_network,
        }
        return data

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """Register a webhook with the Meraki API."""
        # This is a placeholder. The actual implementation will be added in a future step.
        pass

    async def unregister_webhook(self, webhook_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        # This is a placeholder. The actual implementation will be added in a future step.
        pass
