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

from ...types import MerakiDevice, MerakiNetwork
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints
from ...core.errors import MerakiNetworkError

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """Facade for the Meraki Dashboard API client.

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
            output_log=True,
            print_console=False,
            suppress_logging=False,
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

    async def _async_fetch_initial_data(self) -> tuple:
        """Fetch the initial batch of data from the Meraki API."""
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
        return await asyncio.gather(*initial_tasks, return_exceptions=True)

    def _process_initial_data(self, results: tuple) -> dict:
        """Process the initial data, handling errors and merging."""
        (
            networks_res,
            devices_res,
            devices_availabilities_res,
            appliance_uplink_statuses_res,
        ) = results

        networks: List[MerakiNetwork] = (
            networks_res if isinstance(networks_res, list) else []
        )
        if not isinstance(networks_res, list):
            _LOGGER.warning("Could not fetch Meraki networks: %s", networks_res)

        devices: List[MerakiDevice] = (
            devices_res if isinstance(devices_res, list) else []
        )
        if not isinstance(devices_res, list):
            _LOGGER.warning("Could not fetch Meraki devices: %s", devices_res)

        devices_availabilities: List[Dict[str, Any]] = (
            devices_availabilities_res
            if isinstance(devices_availabilities_res, list)
            else []
        )
        if not isinstance(devices_availabilities_res, list):
            _LOGGER.warning(
                "Could not fetch Meraki device availabilities: %s",
                devices_availabilities_res,
            )

        appliance_uplink_statuses: List[Dict[str, Any]] = (
            appliance_uplink_statuses_res
            if isinstance(appliance_uplink_statuses_res, list)
            else []
        )
        if not isinstance(appliance_uplink_statuses_res, list):
            _LOGGER.warning(
                "Could not fetch Meraki appliance uplink statuses: %s",
                appliance_uplink_statuses_res,
            )

        availabilities_by_serial = {
            availability["serial"]: availability
            for availability in devices_availabilities
            if isinstance(availability, dict) and "serial" in availability
        }

        for device in devices:
            if availability := availabilities_by_serial.get(device["serial"]):
                device["status"] = availability["status"]

        return {
            "networks": networks,
            "devices": devices,
            "appliance_uplink_statuses": appliance_uplink_statuses,
        }

    async def _async_fetch_client_data(
        self, networks: List[MerakiNetwork]
    ) -> List[Dict[str, Any]]:
        """Fetch client data for all networks."""
        client_tasks = [
            self._run_with_semaphore(self.network.get_network_clients(network["id"]))
            for network in networks
        ]
        clients_results = await asyncio.gather(*client_tasks, return_exceptions=True)
        clients: List[Dict[str, Any]] = []
        for i, network in enumerate(networks):
            result = clients_results[i]
            if isinstance(result, list):
                for client in result:
                    client["networkId"] = network["id"]
                clients.extend(result)
        return clients

    def _build_detail_tasks(
        self, networks: List[MerakiNetwork], devices: List[MerakiDevice]
    ) -> dict:
        """Build a dictionary of tasks to fetch detailed data."""
        detail_tasks = {}
        for network in networks:
            detail_tasks[f"ssids_{network['id']}"] = self._run_with_semaphore(
                self.wireless.get_network_ssids(network["id"])
            )
            if "appliance" in network["productTypes"]:
                detail_tasks[f"traffic_{network['id']}"] = self._run_with_semaphore(
                    self.network.get_network_traffic(network["id"], "appliance")
                )
                detail_tasks[f"vlans_{network['id']}"] = self._run_with_semaphore(
                    self.appliance.get_vlans(network["id"])
                )
            if "wireless" in network["productTypes"]:
                detail_tasks[f"rf_profiles_{network['id']}"] = self._run_with_semaphore(
                    self.wireless.get_network_wireless_rf_profiles(network["id"])
                )
        for device in devices:
            if device.get("productType") == "wireless":
                detail_tasks[f"wireless_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.wireless.get_wireless_settings(device["serial"])
                    )
                )
            elif device.get("productType") == "camera":
                detail_tasks[f"video_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.camera.get_camera_video_settings(device["serial"])
                    )
                )
                detail_tasks[f"sense_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.camera.get_camera_sense_settings(device["serial"])
                    )
                )
                # Also fetch the video link so we can get the RTSP stream URL
                detail_tasks[f"video_link_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.camera.get_device_camera_video_link(device["serial"])
                    )
                )
            elif device.get("productType") == "switch":
                detail_tasks[f"ports_statuses_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.switch.get_device_switch_ports_statuses(device["serial"])
                    )
                )
            elif device.get("productType") == "appliance" and "networkId" in device:
                detail_tasks[f"appliance_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.appliance.get_network_appliance_settings(
                            device["networkId"]
                        )
                    )
                )
        return detail_tasks

    def _process_detailed_data(
        self,
        detail_data: dict,
        networks: List[MerakiNetwork],
        devices: List[MerakiDevice],
    ) -> dict:
        """Process the detailed data and merge it into the main data structure."""
        ssids: List[Dict[str, Any]] = []
        appliance_traffic: Dict[str, Any] = {}
        vlan_by_network: Dict[str, Any] = {}
        rf_profiles_by_network: Dict[str, Any] = {}

        for network in networks:
            network_ssids = detail_data.get(f"ssids_{network['id']}")
            if isinstance(network_ssids, list):
                for ssid in network_ssids:
                    if "unconfigured ssid" not in ssid.get("name", "").lower():
                        ssid["networkId"] = network["id"]
                        ssids.append(ssid)

            network_traffic = detail_data.get(f"traffic_{network['id']}")
            if isinstance(network_traffic, MerakiNetworkError):
                if "traffic analysis" in str(network_traffic).lower():
                    _LOGGER.info(
                        "Traffic Analysis is not enabled for %s.", network["name"]
                    )
                appliance_traffic[network["id"]] = {
                    "error": "disabled",
                    "reason": str(network_traffic),
                }
            elif isinstance(network_traffic, dict):
                appliance_traffic[network["id"]] = network_traffic

            network_vlans = detail_data.get(f"vlans_{network['id']}")
            if isinstance(network_vlans, MerakiNetworkError):
                if "vlans are not enabled" in str(network_vlans).lower():
                    _LOGGER.info("VLANs are not enabled for %s.", network["name"])
                vlan_by_network[network["id"]] = []
            elif isinstance(network_vlans, list):
                vlan_by_network[network["id"]] = network_vlans

            network_rf_profiles = detail_data.get(f"rf_profiles_{network['id']}")
            if isinstance(network_rf_profiles, list):
                rf_profiles_by_network[network["id"]] = network_rf_profiles

        for device in devices:
            product_type = device.get("productType")
            if product_type == "wireless":
                if settings := detail_data.get(f"wireless_settings_{device['serial']}"):
                    device["radio_settings"] = settings
            elif product_type == "camera":
                if settings := detail_data.get(f"video_settings_{device['serial']}"):
                    device["video_settings"] = settings
                if settings := detail_data.get(f"sense_settings_{device['serial']}"):
                    device["sense_settings"] = settings
                if video_link := detail_data.get(f"video_link_{device['serial']}"):
                    if isinstance(video_link, dict):
                        device["rtsp_url"] = video_link.get("url")
                    else:
                        device["rtsp_url"] = None
            elif product_type == "switch":
                if statuses := detail_data.get(f"ports_statuses_{device['serial']}"):
                    device["ports_statuses"] = statuses
            elif product_type == "appliance":
                if settings := detail_data.get(
                    f"appliance_settings_{device['serial']}"
                ):
                    if isinstance(settings.get("dynamicDns"), dict):
                        device["dynamicDns"] = settings["dynamicDns"]

        return {
            "ssids": ssids,
            "appliance_traffic": appliance_traffic,
            "vlans": vlan_by_network,
            "rf_profiles": rf_profiles_by_network,
        }

    async def get_all_data(self) -> dict:
        """Fetch all data from the Meraki API concurrently."""
        initial_results = await self._async_fetch_initial_data()
        processed_initial_data = self._process_initial_data(initial_results)

        networks = processed_initial_data["networks"]
        devices = processed_initial_data["devices"]

        clients = await self._async_fetch_client_data(networks)

        detail_tasks = self._build_detail_tasks(networks, devices)
        detail_results = await asyncio.gather(
            *detail_tasks.values(), return_exceptions=True
        )
        detail_data = dict(zip(detail_tasks.keys(), detail_results))

        processed_detailed_data = self._process_detailed_data(
            detail_data, networks, devices
        )

        return {
            "networks": networks,
            "devices": devices,
            "clients": clients,
            "appliance_uplink_statuses": processed_initial_data[
                "appliance_uplink_statuses"
            ],
            **processed_detailed_data,
        }

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

    async def async_reboot_device(self, serial: str) -> dict:
        """Reboot a device."""
        return await self.appliance.reboot_device(serial)

    async def async_get_switch_port_statuses(self, serial: str) -> list[dict[str, Any]]:
        """Get statuses for all ports of a switch."""
        return await self.switch.get_device_switch_ports_statuses(serial)
