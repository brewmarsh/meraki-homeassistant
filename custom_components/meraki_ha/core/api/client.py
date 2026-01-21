"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from functools import partial
from typing import TYPE_CHECKING, Any

import meraki
<<<<<<< HEAD

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from ...core.errors import (
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)
=======
from homeassistant.core import HomeAssistant

from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.camera import parse_camera_data
from ...core.parsers.devices import parse_device_data
from ...core.parsers.network import parse_network_data
from ...core.parsers.sensors import parse_sensor_data
from ...core.parsers.switch import parse_switch_data
from ...core.parsers.wireless import parse_wireless_data
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from ...types import MerakiDevice, MerakiNetwork
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.devices import DevicesEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.sensor import SensorEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints

<<<<<<< HEAD
=======
if TYPE_CHECKING:
    from ...coordinator import MerakiDataUpdateCoordinator


>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """
    Facade for the Meraki Dashboard API client.

    This client provides access to various endpoint categories and handles
    the underlying API session and asynchronous execution.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
<<<<<<< HEAD
=======
        coordinator: MerakiDataUpdateCoordinator | None = None,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        base_url: str = "https://api.meraki.com/api/v1",
    ) -> None:
        """
        Initialize the API client.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The organization ID.
<<<<<<< HEAD
=======
            coordinator: The data update coordinator.
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            base_url: The base URL for the Meraki API.

        """
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
<<<<<<< HEAD
        self._base_url = base_url

        self.dashboard: meraki.DashboardAPI | None = None
=======
        self.coordinator = coordinator

        self.dashboard: meraki.DashboardAPI = meraki.DashboardAPI(
            api_key=api_key,
            base_url=base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

        # Initialize endpoint handlers
        self.appliance = ApplianceEndpoints(self, self._hass)
        self.camera = CameraEndpoints(self)
        self.devices = DevicesEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.organization = OrganizationEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)
        self.sensor = SensorEndpoints(self)

<<<<<<< HEAD
        # Set to store network IDs that have failed traffic analysis
        self.traffic_analysis_failed_networks: set[str] = set()

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

    async def async_setup(self) -> None:
        """Perform asynchronous setup of the API client."""
        self.dashboard = await self._hass.async_add_executor_job(
            self._create_dashboard_api
        )

    def _create_dashboard_api(self) -> meraki.DashboardAPI:
        """Create and return the MerakiDashboardAPI instance."""
        return meraki.DashboardAPI(
            api_key=self._api_key,
            base_url=self._base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

=======
        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    async def run_sync(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Run a synchronous function in a thread pool.

        Args:
            func: The synchronous function to run.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns
        -------
            The result of the function.

        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def _run_with_semaphore(self, coro: Awaitable[Any]) -> Any:
        """
        Run an awaitable with the semaphore.

        Args:
            coro: The awaitable to run.

        Returns
        -------
            The result of the awaitable.

        """
        async with self._semaphore:
            return await coro

    async def _async_fetch_initial_data(self) -> dict[str, Any]:
        """
        Fetch the initial batch of data from the Meraki API.

        Returns
        -------
            A dictionary of initial data.

        """
        tasks = {
<<<<<<< HEAD
=======
            "organization": self._run_with_semaphore(
                self.organization.get_organization(),
            ),
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            "networks": self._run_with_semaphore(
                self.organization.get_organization_networks(),
            ),
            "devices": self._run_with_semaphore(
                self.organization.get_organization_devices(),
            ),
<<<<<<< HEAD
=======
            "device_statuses": self._run_with_semaphore(
                self.organization.get_organization_devices_statuses(),
            ),
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            "devices_availabilities": self._run_with_semaphore(
                self.organization.get_organization_devices_availabilities(),
            ),
            "appliance_uplink_statuses": self._run_with_semaphore(
                self.appliance.get_organization_appliance_uplink_statuses(),
            ),
            "sensor_readings": self._run_with_semaphore(
                self.sensor.get_organization_sensor_readings_latest(),
            ),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
<<<<<<< HEAD
        return dict(zip(tasks.keys(), results, strict=True))

    def _process_initial_data(self, results: dict[str, Any]) -> dict[str, Any]:
        """
        Process the initial data, handling errors and merging.

        Args:
            results: The raw initial data from the API.

        Returns
        -------
            The processed initial data.

        """
        networks_res = results.get("networks")
        devices_res = results.get("devices")
        devices_availabilities_res = results.get("devices_availabilities")
        appliance_uplink_statuses_res = results.get("appliance_uplink_statuses")
        sensor_readings_res = results.get("sensor_readings")

        networks: list[MerakiNetwork] = (
            networks_res if isinstance(networks_res, list) else []
        )
        if not isinstance(networks_res, list):
            _LOGGER.warning("Could not fetch Meraki networks: %s", networks_res)

        devices: list[MerakiDevice] = (
            devices_res if isinstance(devices_res, list) else []
        )
        if not isinstance(devices_res, list):
            _LOGGER.warning("Could not fetch Meraki devices: %s", devices_res)

        devices_availabilities: list[dict[str, Any]] = (
            devices_availabilities_res
            if isinstance(devices_availabilities_res, list)
            else []
        )
        if not isinstance(devices_availabilities_res, list):
            _LOGGER.warning(
                "Could not fetch Meraki device availabilities: %s",
                devices_availabilities_res,
            )

        appliance_uplink_statuses: list[dict[str, Any]] = (
            appliance_uplink_statuses_res
            if isinstance(appliance_uplink_statuses_res, list)
            else []
        )
        if not isinstance(appliance_uplink_statuses_res, list):
            _LOGGER.warning(
                "Could not fetch Meraki appliance uplink statuses: %s",
                appliance_uplink_statuses_res,
            )

        sensor_readings: list[dict[str, Any]] = (
            sensor_readings_res if isinstance(sensor_readings_res, list) else []
        )
        if not isinstance(sensor_readings_res, list):
            _LOGGER.warning(
                "Could not fetch Meraki sensor readings: %s", sensor_readings_res
            )

        availabilities_by_serial = {
            availability["serial"]: availability
            for availability in devices_availabilities
            if isinstance(availability, dict) and "serial" in availability
        }

        readings_by_serial = {
            reading["serial"]: reading.get("readings", [])
            for reading in sensor_readings
            if isinstance(reading, dict) and "serial" in reading
        }

        for device in devices:
            if availability := availabilities_by_serial.get(device["serial"]):
                device["status"] = availability["status"]
            if readings := readings_by_serial.get(device["serial"]):
                device["readings"] = readings

        return {
            "networks": networks,
            "devices": devices,
            "appliance_uplink_statuses": appliance_uplink_statuses,
        }
=======
        data = dict(zip(tasks.keys(), results, strict=True))

        # Fetch battery data separately
        devices_res = data.get("devices")
        if isinstance(devices_res, list):
            mt_serials = [
                device["serial"]
                for device in devices_res
                if device.get("model", "").startswith("MT")
            ]
            if mt_serials:
                battery_data_res = await self._run_with_semaphore(
                    self.sensor.get_organization_sensor_readings_latest_for_serials(
                        serials=mt_serials,
                        metrics=["battery"],
                    ),
                )
                data["battery_readings"] = battery_data_res

        return data
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    async def _async_fetch_network_clients(
        self,
        networks: list[MerakiNetwork],
    ) -> list[dict[str, Any]]:
        """
        Fetch client data for all networks, used for SSID sensors.

        Args:
            networks: A list of networks to fetch clients for.

        Returns
        -------
            A list of clients.

        """
        client_tasks = [
<<<<<<< HEAD
            self._run_with_semaphore(self.network.get_network_clients(network["id"]))
=======
            self._run_with_semaphore(
                self.network.get_network_clients(
                    network.id,
                    perPage=1000,
                    total_pages="all",
                ),
            )
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            for network in networks
        ]
        clients_results = await asyncio.gather(*client_tasks, return_exceptions=True)
        clients: list[dict[str, Any]] = []
        for i, network in enumerate(networks):
            result = clients_results[i]
            if isinstance(result, list):
<<<<<<< HEAD
                for client in result:
                    client["networkId"] = network["id"]
=======
                _LOGGER.debug(
                    "Fetched %d clients for network %s", len(result), network.name
                )
                for client in result:
                    client["networkId"] = network.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
                clients.extend(result)
        return clients

    async def _async_fetch_device_clients(
        self,
        devices: list[MerakiDevice],
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Fetch client data for each device.

        Args:
            devices: A list of devices to fetch clients for.

        Returns
        -------
            A dictionary of clients by device serial.

        """
        client_tasks = {
<<<<<<< HEAD
            device["serial"]: self._run_with_semaphore(
                self.devices.get_device_clients(device["serial"]),
            )
            for device in devices
            if device.get("productType")
=======
            device.serial: self._run_with_semaphore(
                self.devices.get_device_clients(device.serial),
            )
            for device in devices
            if device.product_type
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            in ["wireless", "appliance", "switch", "cellularGateway"]
        }
        results = await asyncio.gather(*client_tasks.values(), return_exceptions=True)
        clients_by_serial: dict[str, list[dict[str, Any]]] = {}
        for i, serial in enumerate(client_tasks.keys()):
            result = results[i]
            if isinstance(result, list):
                clients_by_serial[serial] = result
        return clients_by_serial

    def _build_detail_tasks(
        self,
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
<<<<<<< HEAD
    ) -> dict[str, Awaitable[Any]]:
=======
    ) -> dict[str, asyncio.Task[Any]]:
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        """
        Build a dictionary of tasks to fetch detailed data.

        Args:
            networks: A list of networks.
            devices: A list of devices.

        Returns
        -------
            A dictionary of tasks.

        """
<<<<<<< HEAD
        detail_tasks: dict[str, Awaitable[Any]] = {}
        for network in networks:
            product_types = network.get("productTypes", [])
            if "wireless" in product_types:
                detail_tasks[f"ssids_{network['id']}"] = self._run_with_semaphore(
                    self.wireless.get_network_ssids(network["id"]),
                )
                detail_tasks[f"wireless_settings_{network['id']}"] = (
                    self._run_with_semaphore(
                        self.wireless.get_network_wireless_settings(network["id"]),
                    )
                )
            if "appliance" in product_types:
                if network["id"] not in self.traffic_analysis_failed_networks:
                    detail_tasks[f"traffic_{network['id']}"] = self._run_with_semaphore(
                        self.network.get_network_traffic(network["id"], "appliance"),
                    )
                detail_tasks[f"vlans_{network['id']}"] = self._run_with_semaphore(
                    self.appliance.get_network_vlans(network["id"]),
                )
                detail_tasks[f"l3_firewall_rules_{network['id']}"] = (
                    self._run_with_semaphore(
                        self.appliance.get_l3_firewall_rules(network["id"]),
                    )
                )
                detail_tasks[f"traffic_shaping_{network['id']}"] = (
                    self._run_with_semaphore(
                        self.appliance.get_traffic_shaping(network["id"]),
                    )
                )
                detail_tasks[f"vpn_status_{network['id']}"] = self._run_with_semaphore(
                    self.appliance.get_vpn_status(network["id"]),
                )
                detail_tasks[f"content_filtering_{network['id']}"] = (
                    self._run_with_semaphore(
                        self.appliance.get_network_appliance_content_filtering(
                            network["id"],
=======
        detail_tasks: dict[str, asyncio.Task[Any]] = {}
        for network in networks:
            product_types = network.product_types
            if "wireless" in product_types:
                detail_tasks[f"ssids_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.wireless.get_network_ssids(network.id),
                    )
                )
            if "appliance" in product_types:
                if not self.coordinator or self.coordinator.is_traffic_check_due(
                    network.id,
                ):
                    detail_tasks[f"traffic_{network.id}"] = asyncio.create_task(
                        self._run_with_semaphore(
                            self.network.get_network_traffic(network.id, "appliance"),
                        )
                    )
                if not self.coordinator or self.coordinator.is_vlan_check_due(
                    network.id,
                ):
                    detail_tasks[f"vlans_{network.id}"] = asyncio.create_task(
                        self._run_with_semaphore(
                            self.appliance.get_network_vlans(network.id),
                        )
                    )
                detail_tasks[f"l3_firewall_rules_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_l3_firewall_rules(network.id),
                    )
                )
                detail_tasks[f"traffic_shaping_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_traffic_shaping(network.id),
                    )
                )
                detail_tasks[f"vpn_status_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_vpn_status(network.id),
                    )
                )
                detail_tasks[f"content_filtering_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_network_appliance_content_filtering(
                            network.id,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
                        ),
                    )
                )
            if "wireless" in product_types:
<<<<<<< HEAD
                detail_tasks[f"rf_profiles_{network['id']}"] = self._run_with_semaphore(
                    self.wireless.get_network_wireless_rf_profiles(network["id"]),
                )
        for device in devices:
            if device.get("productType") == "camera":
                detail_tasks[f"video_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.camera.get_camera_video_settings(device["serial"]),
                    )
                )
                detail_tasks[f"sense_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.camera.get_camera_sense_settings(device["serial"]),
                    )
                )
            elif device.get("productType") == "switch":
                detail_tasks[f"ports_statuses_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.switch.get_device_switch_ports_statuses(device["serial"]),
                    )
                )
            elif device.get("productType") == "appliance" and "networkId" in device:
                detail_tasks[f"appliance_settings_{device['serial']}"] = (
                    self._run_with_semaphore(
                        self.appliance.get_network_appliance_settings(
                            device["networkId"],
                        ),
                    )
                )
        return detail_tasks

    def _process_detailed_data(
        self,
        detail_data: dict[str, Any],
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
        previous_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process the detailed data and merge it into the main data structure.

        Args:
            detail_data: The raw detailed data from the API.
            networks: A list of networks.
            devices: A list of devices.
            previous_data: The previous data from the coordinator.

        Returns
        -------
            The processed detailed data.

        """
        ssids: list[dict[str, Any]] = []
        appliance_traffic: dict[str, Any] = {}
        vlan_by_network: dict[str, Any] = {}
        l3_firewall_rules_by_network: dict[str, Any] = {}
        traffic_shaping_by_network: dict[str, Any] = {}
        vpn_status_by_network: dict[str, Any] = {}
        rf_profiles_by_network: dict[str, Any] = {}
        content_filtering_by_network: dict[str, Any] = {}
        wireless_settings_by_network: dict[str, Any] = {}

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
            if isinstance(network_traffic, MerakiTrafficAnalysisError):
                _LOGGER.info(
                    "Traffic analysis is not enabled for network '%s'. "
                    "This is not an error and can be ignored if you do not "
                    "use this feature.",
                    network["name"],
                )
                self.traffic_analysis_failed_networks.add(network["id"])
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
            if isinstance(network_vlans, MerakiVlansDisabledError):
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

            wireless_settings_key = f"wireless_settings_{network['id']}"
            wireless_settings = detail_data.get(wireless_settings_key)
            if isinstance(wireless_settings, dict):
                wireless_settings_by_network[network["id"]] = wireless_settings
            elif previous_data and wireless_settings_key in previous_data:
                wireless_settings_by_network[network["id"]] = previous_data[
                    wireless_settings_key
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
                statuses_key = f"ports_statuses_{device['serial']}"
                statuses = detail_data.get(statuses_key)
                if isinstance(statuses, list):
                    device["ports_statuses"] = statuses
                elif previous_data:
                    # Try to retrieve from previous data based on serial
                    prev_devices = previous_data.get("devices", [])
                    prev_device = next(
                        (
                            d
                            for d in prev_devices
                            if d.get("serial") == device["serial"]
                        ),
                        None,
                    )
                    if prev_device and "ports_statuses" in prev_device:
                        device["ports_statuses"] = prev_device["ports_statuses"]

            elif product_type == "appliance":
                if settings := detail_data.get(
                    f"appliance_settings_{device['serial']}",
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
            "wireless_settings": wireless_settings_by_network,
        }

=======
                detail_tasks[f"rf_profiles_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.wireless.get_network_wireless_rf_profiles(network.id),
                    )
                )
        for device in devices:
            if device.product_type == "camera":
                detail_tasks[f"video_settings_{device.serial}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.camera.get_camera_video_settings(device.serial),
                    )
                )
                detail_tasks[f"sense_settings_{device.serial}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.camera.get_camera_sense_settings(device.serial),
                    )
                )
                detail_tasks[f"camera_analytics_{device.serial}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.camera.get_device_camera_analytics_recent(
                            device.serial,
                        ),
                    )
                )
            elif device.product_type == "switch":
                detail_tasks[f"ports_statuses_{device.serial}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.switch.get_device_switch_ports_statuses(device.serial),
                    )
                )
            elif device.product_type == "appliance" and device.network_id:
                detail_tasks[f"appliance_settings_{device.serial}"] = (
                    asyncio.create_task(
                        self._run_with_semaphore(
                            self.appliance.get_network_appliance_settings(
                                device.network_id,
                            ),
                        )
                    )
                )
        return detail_tasks

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    async def get_all_data(
        self,
        previous_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Fetch all data from the Meraki API concurrently, with caching.

        Args:
            previous_data: The previous data from the coordinator.

        Returns
        -------
            A dictionary of all data.

        """
        if previous_data is None:
            previous_data = {}

        _LOGGER.debug("Fetching fresh Meraki data from API")
        initial_results = await self._async_fetch_initial_data()
<<<<<<< HEAD
        processed_initial_data = self._process_initial_data(initial_results)

        networks = processed_initial_data["networks"]
        devices = processed_initial_data["devices"]

        network_clients, device_clients = await asyncio.gather(
            self._async_fetch_network_clients(networks),
            self._async_fetch_device_clients(devices),
            return_exceptions=True,
        )
=======

        networks_res = initial_results.get("networks", [])
        if isinstance(networks_res, Exception):
            _LOGGER.warning(
                "Could not fetch networks, network data will be unavailable: %s",
                networks_res,
            )
            networks: list[MerakiNetwork] = []
        else:
            networks: list[MerakiNetwork] = [
                MerakiNetwork.from_dict(n) for n in networks_res
            ]

        devices_res = initial_results.get("devices", [])
        if isinstance(devices_res, Exception):
            _LOGGER.warning(
                "Could not fetch devices, device data will be unavailable: %s",
                devices_res,
            )
            devices: list[MerakiDevice] = []
        else:
            devices: list[MerakiDevice] = [
                MerakiDevice.from_dict(d) for d in devices_res
            ]

        device_statuses = initial_results.get("device_statuses", [])
        if isinstance(device_statuses, Exception):
            _LOGGER.warning(
                "Could not fetch device statuses, "
                "device status data will be unavailable: %s",
                device_statuses,
            )
            device_statuses = []

        parse_device_data(devices, device_statuses)
        appliance_uplink_statuses = initial_results.get("appliance_uplink_statuses")
        sensor_readings = initial_results.get("sensor_readings")
        battery_readings = initial_results.get("battery_readings")

        parse_appliance_data(devices, appliance_uplink_statuses)
        parse_sensor_data(devices, sensor_readings, battery_readings)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

        detail_tasks = self._build_detail_tasks(networks, devices)
        detail_results = await asyncio.gather(
            *detail_tasks.values(),
            return_exceptions=True,
        )
        detail_data = dict(zip(detail_tasks.keys(), detail_results, strict=True))

<<<<<<< HEAD
        processed_detailed_data = self._process_detailed_data(
            detail_data,
            networks,
            devices,
            previous_data,
        )

        return {
=======
        parse_camera_data(devices, detail_data)
        parse_switch_data(devices, detail_data)

        network_clients, device_clients = await asyncio.gather(
            self._async_fetch_network_clients(networks),
            self._async_fetch_device_clients(devices),
            return_exceptions=True,
        )

        processed_network_data = parse_network_data(
            detail_data,
            networks,
            previous_data,
            self.coordinator,
        )
        processed_wireless_data = parse_wireless_data(
            detail_data,
            networks,
            previous_data,
            clients=network_clients if isinstance(network_clients, list) else [],
        )

        switch_ports_statuses: dict[str, Any] = {}
        for key, value in detail_data.items():
            if key.startswith("ports_statuses_"):
                serial = key.replace("ports_statuses_", "")
                if isinstance(value, list):
                    switch_ports_statuses[serial] = value

        organization_res = initial_results.get("organization", {})
        org_name = (
            organization_res.get("name")
            if isinstance(organization_res, dict)
            else "Unknown Organization"
        )

        return {
            "org_name": org_name,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            "networks": networks,
            "devices": devices,
            "clients": network_clients if isinstance(network_clients, list) else [],
            "clients_by_serial": (
                device_clients if isinstance(device_clients, dict) else {}
            ),
<<<<<<< HEAD
            "appliance_uplink_statuses": processed_initial_data[
                "appliance_uplink_statuses"
            ],
            **processed_detailed_data,
=======
            "ssids": processed_wireless_data.get("ssids", []),
            "switch_ports_statuses": switch_ports_statuses,
            **processed_network_data,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        }

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """
        Register a webhook with the Meraki API.

        Args:
            webhook_url: The URL of the webhook.
            secret: The secret for the webhook.

        """
        await self.network.register_webhook(webhook_url, secret)

<<<<<<< HEAD
    async def unregister_webhook(self, webhook_url: str) -> None:
=======
    async def unregister_webhook(self, webhook_id: str) -> None:
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        """
        Unregister a webhook with the Meraki API.

        Args:
<<<<<<< HEAD
        ----
            webhook_url: The URL of the webhook to unregister.

        """
        await self.network.unregister_webhook(webhook_url)
=======
            webhook_id: The ID of the webhook to unregister.

        """
        await self.network.unregister_webhook(webhook_id)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    async def async_reboot_device(self, serial: str) -> dict[str, Any]:
        """
        Reboot a device.

        Args:
            serial: The serial number of the device to reboot.

        Returns
        -------
            The API response.

        """
        return await self.appliance.reboot_device(serial)

    async def async_get_switch_port_statuses(
        self,
        serial: str,
    ) -> list[dict[str, Any]]:
        """
        Get statuses for all ports of a switch.

        Args:
            serial: The serial number of the switch.

        Returns
        -------
            A list of port statuses.

        """
        return await self.switch.get_device_switch_ports_statuses(serial)
<<<<<<< HEAD
=======

    async def async_cycle_switch_ports(
        self,
        serial: str,
        ports: list[str],
    ) -> dict[str, Any]:
        """
        Cycle a set of switch ports.

        Args:
            serial: The serial number of the switch.
            ports: A list of port IDs to cycle.

        Returns
        -------
            The API response.

        """
        return await self.switch.cycle_device_switch_ports(serial, ports)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
