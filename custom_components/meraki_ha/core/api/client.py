"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

from __future__ import annotations

import asyncio
from functools import partial
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
import meraki  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiDevice, MerakiNetwork
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.devices import DevicesEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints
from .endpoints.sensor import SensorEndpoints
from ...core.errors import MerakiInformationalError

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """Facade for the Meraki Dashboard API client.

    This client provides access to various endpoint categories and handles
    the underlying API session and asynchronous execution.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        coordinator: "MerakiDataUpdateCoordinator" | None = None,
        base_url: str = "https://api.meraki.com/api/v1",
    ) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
        self.coordinator = coordinator
        self._cache = None
        # if hass:
        #     cache_dir = hass.config.path("meraki_cache")
        #     self._cache = dc.Cache(cache_dir)
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
        self.appliance = ApplianceEndpoints(self, self._hass)
        self.camera = CameraEndpoints(self)
        self.devices = DevicesEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.organization = OrganizationEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)
        self.sensor = SensorEndpoints(self)

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

    async def _run_sync(self, func, *args, **kwargs) -> Any:
        """Run a synchronous function in a thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def _run_with_semaphore(self, coro):
        """Run a coroutine with the semaphore."""
        async with self._semaphore:
            return await coro

    async def _async_fetch_initial_data(self) -> dict:
        """Fetch the initial batch of data from the Meraki API."""
        tasks = {
            "networks": self._run_with_semaphore(
                self.organization.get_organization_networks()
            ),
            "devices": self._run_with_semaphore(
                self.organization.get_organization_devices()
            ),
            "devices_availabilities": self._run_with_semaphore(
                self.organization.get_organization_devices_availabilities()
            ),
            "appliance_uplink_statuses": self._run_with_semaphore(
                self.appliance.get_organization_appliance_uplink_statuses()
            ),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        return dict(zip(tasks.keys(), results))

    def _process_initial_data(self, results: dict) -> dict:
        """Process the initial data, handling errors and merging."""
        networks_res = results.get("networks")
        devices_res = results.get("devices")
        devices_availabilities_res = results.get("devices_availabilities")
        appliance_uplink_statuses_res = results.get("appliance_uplink_statuses")

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

    async def _async_fetch_network_clients(
        self, networks: List[MerakiNetwork]
    ) -> List[Dict[str, Any]]:
        """Fetch client data for all networks, used for SSID sensors."""
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

    async def _async_fetch_device_clients(
        self, devices: List[MerakiDevice]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch client data for each device."""
        client_tasks = {
            device["serial"]: self._run_with_semaphore(
                self.devices.get_device_clients(device["serial"])
            )
            for device in devices
            if device.get("productType")
            in ["wireless", "appliance", "switch", "cellularGateway"]
        }
        results = await asyncio.gather(*client_tasks.values(), return_exceptions=True)
        clients_by_serial: Dict[str, List[Dict[str, Any]]] = {}
        for i, serial in enumerate(client_tasks.keys()):
            result = results[i]
            if isinstance(result, list):
                clients_by_serial[serial] = result
        return clients_by_serial

    def _build_detail_tasks(
        self, networks: List[MerakiNetwork], devices: List[MerakiDevice]
    ) -> dict:
        """Build a dictionary of tasks to fetch detailed data."""
        detail_tasks = {}
        for network in networks:
            product_types = network.get("productTypes", [])
            if "wireless" in product_types:
                detail_tasks[f"ssids_{network['id']}"] = self._run_with_semaphore(
                    self.wireless.get_network_ssids(network["id"])
                )
            if "appliance" in product_types:
                if not self.coordinator or self.coordinator.is_traffic_check_due(
                    network["id"]
                ):
                    detail_tasks[
                        f"traffic_{network['id']}"
                    ] = self._run_with_semaphore(
                        self.network.get_network_traffic(network["id"], "appliance")
                    )
                if not self.coordinator or self.coordinator.is_vlan_check_due(
                    network["id"]
                ):
                    detail_tasks[f"vlans_{network['id']}"] = self._run_with_semaphore(
                        self.appliance.get_network_vlans(network["id"])
                    )
                detail_tasks[
                    f"l3_firewall_rules_{network['id']}"
                ] = self._run_with_semaphore(
                    self.appliance.get_l3_firewall_rules(network["id"])
                )
                detail_tasks[
                    f"traffic_shaping_{network['id']}"
                ] = self._run_with_semaphore(
                    self.appliance.get_traffic_shaping(network["id"])
                )
                detail_tasks[f"vpn_status_{network['id']}"] = self._run_with_semaphore(
                    self.appliance.get_vpn_status(network["id"])
                )
                detail_tasks[
                    f"content_filtering_{network['id']}"
                ] = self._run_with_semaphore(
                    self.appliance.get_network_appliance_content_filtering(
                        network["id"]
                    )
                )
            if "wireless" in product_types:
                detail_tasks[f"rf_profiles_{network['id']}"] = self._run_with_semaphore(
                    self.wireless.get_network_wireless_rf_profiles(network["id"])
                )
        for device in devices:
            if device.get("productType") == "camera":
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
        previous_data: dict,
    ) -> dict:
        """Process the detailed data and merge it into the main data structure."""
        ssids: List[Dict[str, Any]] = []
        appliance_traffic: Dict[str, Any] = {}
        vlan_by_network: Dict[str, Any] = {}
        l3_firewall_rules_by_network: Dict[str, Any] = {}
        traffic_shaping_by_network: Dict[str, Any] = {}
        vpn_status_by_network: Dict[str, Any] = {}
        rf_profiles_by_network: Dict[str, Any] = {}
        content_filtering_by_network: Dict[str, Any] = {}

        for network in networks:
            network_ssids_key = f"ssids_{network['id']}"
            network_ssids = detail_data.get(network_ssids_key)
            if isinstance(network_ssids, list):
                for ssid in network_ssids:
                    if "unconfigured ssid" not in ssid.get("name", "").lower():
                        ssid["networkId"] = network["id"]
                        ssids.append(ssid)
            elif previous_data and network_ssids_key in previous_data:
                ssids.extend(previous_data[network_ssids_key])

            network_traffic_key = f"traffic_{network['id']}"
            network_traffic = detail_data.get(network_traffic_key)
            if isinstance(network_traffic, MerakiInformationalError):
                if "traffic analysis" in str(network_traffic).lower():
                    if self.coordinator:
                        self.coordinator.add_network_status_message(
                            network["id"],
                            "Traffic Analysis is not enabled for this network.",
                        )
                        self.coordinator.mark_traffic_check_done(network["id"])
                appliance_traffic[network["id"]] = {
                    "error": "disabled",
                    "reason": str(network_traffic),
                }
            elif isinstance(network_traffic, dict):
                appliance_traffic[network["id"]] = network_traffic
            elif previous_data and network_traffic_key in previous_data:
                appliance_traffic[network["id"]] = previous_data[network_traffic_key]

            network_vlans_key = f"vlans_{network['id']}"
            network_vlans = detail_data.get(network_vlans_key)
            if isinstance(network_vlans, MerakiInformationalError):
                if "vlans are not enabled" in str(network_vlans).lower():
                    if self.coordinator:
                        self.coordinator.add_network_status_message(
                            network["id"], "VLANs are not enabled for this network."
                        )
                        self.coordinator.mark_vlan_check_done(network["id"])
                vlan_by_network[network["id"]] = []
            elif isinstance(network_vlans, list):
                vlan_by_network[network["id"]] = network_vlans
            elif previous_data and network_vlans_key in previous_data:
                vlan_by_network[network["id"]] = previous_data[network_vlans_key]

            l3_firewall_rules_key = f"l3_firewall_rules_{network['id']}"
            l3_firewall_rules = detail_data.get(l3_firewall_rules_key)
            if isinstance(l3_firewall_rules, dict):
                l3_firewall_rules_by_network[network["id"]] = l3_firewall_rules
            elif previous_data and l3_firewall_rules_key in previous_data:
                l3_firewall_rules_by_network[network["id"]] = previous_data[
                    l3_firewall_rules_key
                ]

            traffic_shaping_key = f"traffic_shaping_{network['id']}"
            traffic_shaping = detail_data.get(traffic_shaping_key)
            if isinstance(traffic_shaping, dict):
                traffic_shaping_by_network[network["id"]] = traffic_shaping
            elif previous_data and traffic_shaping_key in previous_data:
                traffic_shaping_by_network[network["id"]] = previous_data[
                    traffic_shaping_key
                ]

            vpn_status_key = f"vpn_status_{network['id']}"
            vpn_status = detail_data.get(vpn_status_key)
            if isinstance(vpn_status, dict):
                vpn_status_by_network[network["id"]] = vpn_status
            elif previous_data and vpn_status_key in previous_data:
                vpn_status_by_network[network["id"]] = previous_data[vpn_status_key]

            network_rf_profiles_key = f"rf_profiles_{network['id']}"
            network_rf_profiles = detail_data.get(network_rf_profiles_key)
            if isinstance(network_rf_profiles, list):
                rf_profiles_by_network[network["id"]] = network_rf_profiles
            elif previous_data and network_rf_profiles_key in previous_data:
                rf_profiles_by_network[network["id"]] = previous_data[
                    network_rf_profiles_key
                ]

            content_filtering_key = f"content_filtering_{network['id']}"
            content_filtering = detail_data.get(content_filtering_key)
            if isinstance(content_filtering, dict):
                content_filtering_by_network[network["id"]] = content_filtering
            elif previous_data and content_filtering_key in previous_data:
                content_filtering_by_network[network["id"]] = previous_data[
                    content_filtering_key
                ]

        for device in devices:
            product_type = device.get("productType")
            if product_type == "camera":
                if settings := detail_data.get(f"video_settings_{device['serial']}"):
                    device["video_settings"] = settings
                    # The video_settings endpoint also provides the RTSP URL
                    if isinstance(settings, dict):
                        device["rtsp_url"] = settings.get("rtsp_url")
                    else:
                        device["rtsp_url"] = None
                if settings := detail_data.get(f"sense_settings_{device['serial']}"):
                    device["sense_settings"] = settings
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
            "l3_firewall_rules": l3_firewall_rules_by_network,
            "traffic_shaping": traffic_shaping_by_network,
            "vpn_status": vpn_status_by_network,
            "rf_profiles": rf_profiles_by_network,
            "content_filtering": content_filtering_by_network,
        }

    async def get_all_data(self, previous_data: Optional[dict] = None) -> dict:
        """Fetch all data from the Meraki API concurrently, with caching."""
        if previous_data is None:
            previous_data = {}

        # if self._cache:
        #     cache_key = f"meraki_data_{self._org_id}"
        #     cached_data = self._cache.get(cache_key)
        #     if cached_data:
        #         _LOGGER.debug("Returning cached Meraki data")
        #         return cached_data

        _LOGGER.debug("Fetching fresh Meraki data from API")
        initial_results = await self._async_fetch_initial_data()
        processed_initial_data = self._process_initial_data(initial_results)

        networks = processed_initial_data["networks"]
        devices = processed_initial_data["devices"]

        network_clients, device_clients = await asyncio.gather(
            self._async_fetch_network_clients(networks),
            self._async_fetch_device_clients(devices),
            return_exceptions=True,
        )

        detail_tasks = self._build_detail_tasks(networks, devices)
        detail_results = await asyncio.gather(
            *detail_tasks.values(), return_exceptions=True
        )
        detail_data = dict(zip(detail_tasks.keys(), detail_results))

        processed_detailed_data = self._process_detailed_data(
            detail_data, networks, devices, previous_data
        )

        fresh_data = {
            "networks": networks,
            "devices": devices,
            "clients": network_clients if isinstance(network_clients, list) else [],
            "clients_by_serial": device_clients if isinstance(device_clients, dict) else {},
            "appliance_uplink_statuses": processed_initial_data[
                "appliance_uplink_statuses"
            ],
            **processed_detailed_data,
        }
        # if fresh_data and self._cache:
        #     cache_key = f"meraki_data_{self._org_id}"
        #     self._cache.set(cache_key, fresh_data, expire=120)  # Cache for 2 minutes

        return fresh_data

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    def clear_cache(self) -> None:
        """Clear the main data cache entry."""
        if self._cache:
            cache_key = f"meraki_data_{self._org_id}"
            if self._cache.delete(cache_key):
                _LOGGER.debug("Meraki data cache entry deleted.")
            else:
                _LOGGER.debug("Meraki data cache entry not found to delete.")

    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """Register a webhook with the Meraki API."""
        await self.network.register_webhook(webhook_url, secret)

    async def unregister_webhook(self, webhook_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        await self.network.unregister_webhook(webhook_id)

    async def async_reboot_device(self, serial: str) -> dict:
        """Reboot a device."""
        return await self.appliance.reboot_device(serial)

    async def async_get_switch_port_statuses(self, serial: str) -> list[dict[str, Any]]:
        """Get statuses for all ports of a switch."""
        return await self.switch.get_device_switch_ports_statuses(serial)
