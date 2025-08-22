"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

import asyncio
from functools import partial
import logging
from typing import Any, Dict, List

import meraki  # type: ignore[import-untyped]

from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints
from ...core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiNetworkError,
)

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

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(10)

    async def _run_sync(self, func, *args, **kwargs) -> Any:
        """Run a synchronous function in a thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def _run_with_semaphore(self, coro):
        """Run a coroutine with the semaphore."""
        async with self._semaphore:
            return await coro

    async def get_all_data(self) -> dict:
        """Fetch all data from the Meraki API concurrently."""
        # Initial data fetch
        initial_tasks = [
            self._run_with_semaphore(self.organization.get_organization_networks()),
            self._run_with_semaphore(self.organization.get_organization_devices()),
            self._run_with_semaphore(
                self.organization.get_organization_devices_availabilities()
            ),
            self._run_with_semaphore(
                self.organization.get_organization_appliance_uplink_statuses()
            ),
        ]

        (
            networks_res,
            devices_res,
            devices_availabilities_res,
            appliance_uplink_statuses_res,
        ) = await asyncio.gather(*initial_tasks, return_exceptions=True)

        # Process initial data, checking for exceptions
        networks = networks_res if not isinstance(networks_res, Exception) else []
        if isinstance(networks_res, Exception):
            _LOGGER.warning("Could not fetch Meraki networks: %s", networks_res)

        devices = devices_res if not isinstance(devices_res, Exception) else []
        if isinstance(devices_res, Exception):
            _LOGGER.warning("Could not fetch Meraki devices: %s", devices_res)

        devices_availabilities = devices_availabilities_res if not isinstance(devices_availabilities_res, Exception) else []
        if isinstance(devices_availabilities_res, Exception):
            _LOGGER.warning("Could not fetch Meraki device availabilities: %s", devices_availabilities_res)

        appliance_uplink_statuses = appliance_uplink_statuses_res if not isinstance(appliance_uplink_statuses_res, Exception) else []
        if isinstance(appliance_uplink_statuses_res, Exception):
            _LOGGER.warning("Could not fetch Meraki appliance uplink statuses: %s", appliance_uplink_statuses_res)


        availabilities_by_serial = {
            availability["serial"]: availability
            for availability in devices_availabilities
            if isinstance(availability, dict) and "serial" in availability
        }
        for device in devices:
            if (
                isinstance(device, dict)
                and "serial" in device
                and (availability := availabilities_by_serial.get(device["serial"]))
            ):
                device["status"] = availability["status"]

        # Fetch detailed data concurrently
        client_tasks = [
            self._run_with_semaphore(self.network.get_network_clients(network["id"]))
            for network in networks
            if isinstance(network, dict) and "id" in network
        ]
        clients_results = await asyncio.gather(*client_tasks, return_exceptions=True)
        clients: List[Dict[str, Any]] = []
        for i, network in enumerate(networks):
            if isinstance(network, dict) and "id" in network:
                if not isinstance(clients_results[i], Exception):
                    for client in clients_results[i]:
                        client["networkId"] = network["id"]
                    clients.extend(clients_results[i])

        detail_tasks = {}
        for network in networks:
            if isinstance(network, dict) and "id" in network:
                detail_tasks[
                    f"ssids_{network['id']}"
                ] = self._run_with_semaphore(
                    self.wireless.get_network_ssids(network["id"])
                )
                if "appliance" in network.get("productTypes", []):
                    detail_tasks[
                        f"traffic_{network['id']}"
                    ] = self._run_with_semaphore(
                        self.network.get_network_traffic(network["id"], "appliance")
                    )
                    detail_tasks[
                        f"vlans_{network['id']}"
                    ] = self._run_with_semaphore(self.appliance.get_vlans(network["id"]))
                if "wireless" in network.get("productTypes", []):
                    detail_tasks[
                        f"rf_profiles_{network['id']}"
                    ] = self._run_with_semaphore(
                        self.wireless.get_network_wireless_rf_profiles(network["id"])
                    )

        for device in devices:
            if isinstance(device, dict) and "serial" in device:
                if device.get("productType") == "wireless":
                    detail_tasks[
                        f"wireless_settings_{device['serial']}"
                    ] = self._run_with_semaphore(
                        self.wireless.get_wireless_settings(device["serial"])
                    )
                elif device.get("productType") == "camera":
                    detail_tasks[
                        f"video_settings_{device['serial']}"
                    ] = self._run_with_semaphore(
                        self.camera.get_camera_video_settings(device["serial"])
                    )
                elif device.get("productType") == "switch":
                    detail_tasks[
                        f"ports_statuses_{device['serial']}"
                    ] = self._run_with_semaphore(
                        self.switch.get_device_switch_ports_statuses(device["serial"])
                    )
                elif device.get("productType") == "appliance":
                    detail_tasks[
                        f"appliance_settings_{device['serial']}"
                    ] = self._run_with_semaphore(
                        self.appliance.get_network_appliance_settings(
                            device["networkId"]
                        )
                    )

        detail_results = await asyncio.gather(
            *detail_tasks.values(), return_exceptions=True
        )
        detail_data = dict(zip(detail_tasks.keys(), detail_results))

        # Process detailed data
        ssids: List[Dict[str, Any]] = []
        appliance_traffic = {}
        vlan_by_network = {}
        rf_profiles_by_network = {}

        for network in networks:
            if isinstance(network, dict) and "id" in network:
                network_ssids = detail_data.get(f"ssids_{network['id']}")
                if network_ssids and not isinstance(network_ssids, Exception):
                    for ssid in network_ssids:
                        if (
                            isinstance(ssid, dict)
                            and "name" in ssid
                            and "unconfigured ssid" not in ssid["name"].lower()
                        ):
                            ssid["networkId"] = network["id"]
                            ssids.append(ssid)
                network_traffic = detail_data.get(f"traffic_{network['id']}")
                if isinstance(network_traffic, MerakiNetworkError):
                    appliance_traffic[network["id"]] = {
                        "error": "disabled",
                        "reason": str(network_traffic),
                    }
                elif network_traffic and not isinstance(network_traffic, Exception):
                    appliance_traffic[network["id"]] = network_traffic

                network_vlans = detail_data.get(f"vlans_{network['id']}")
                if isinstance(network_vlans, MerakiNetworkError):
                    vlan_by_network[network["id"]] = {
                        "error": "disabled",
                        "reason": str(network_vlans),
                    }
                elif network_vlans and not isinstance(network_vlans, Exception):
                    vlan_by_network[network["id"]] = network_vlans
                network_rf_profiles = detail_data.get(f"rf_profiles_{network['id']}")
                if network_rf_profiles and not isinstance(
                    network_rf_profiles, Exception
                ):
                    rf_profiles_by_network[network["id"]] = network_rf_profiles

        for device in devices:
            if isinstance(device, dict) and "serial" in device:
                if device.get("productType") == "wireless":
                    wireless_settings = detail_data.get(
                        f"wireless_settings_{device['serial']}"
                    )
                    if wireless_settings and not isinstance(
                        wireless_settings, Exception
                    ):
                        device["radio_settings"] = wireless_settings
                elif device.get("productType") == "camera":
                    video_settings = detail_data.get(
                        f"video_settings_{device['serial']}"
                    )
                    if video_settings and not isinstance(video_settings, Exception):
                        device["video_settings"] = video_settings
                elif device.get("productType") == "switch":
                    ports_statuses = detail_data.get(
                        f"ports_statuses_{device['serial']}"
                    )
                    if ports_statuses and not isinstance(ports_statuses, Exception):
                        device["ports_statuses"] = ports_statuses
                elif device.get("productType") == "appliance":
                    appliance_settings = detail_data.get(
                        f"appliance_settings_{device['serial']}"
                    )
                    if appliance_settings and not isinstance(
                        appliance_settings, Exception
                    ):
                        if "dynamicDns" in appliance_settings:
                            device["dynamicDns"] = appliance_settings["dynamicDns"]

        data = {
            "networks": networks,
            "devices": devices,
            "clients": clients,
            "ssids": ssids,
            "appliance_traffic": appliance_traffic,
            "vlans": vlan_by_network,
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
