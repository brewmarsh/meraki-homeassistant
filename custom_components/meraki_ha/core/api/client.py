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
from typing import TYPE_CHECKING, Any, cast

import meraki
from homeassistant.core import HomeAssistant

from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.camera import parse_camera_data
from ...core.parsers.devices import parse_device_data
from ...core.parsers.network import parse_network_data
from ...core.parsers.sensors import parse_sensor_data
from ...core.parsers.switch import parse_switch_data
from ...core.parsers.wireless import parse_wireless_data
from ...types import MerakiDevice, MerakiNetwork
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.devices import DevicesEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.sensor import SensorEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints

if TYPE_CHECKING:
    from ...coordinator import MerakiDataUpdateCoordinator


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
        coordinator: MerakiDataUpdateCoordinator | None = None,
        base_url: str = "https://api.meraki.com/api/v1",
        enable_vpn_management: bool = False,
    ) -> None:
        """
        Initialize the API client.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The organization ID.
            coordinator: The data update coordinator.
            base_url: The base URL for the Meraki API.
            enable_vpn_management: Whether to enable VPN management.

        """
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
        self.coordinator = coordinator
        self._enable_vpn_management = enable_vpn_management

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
            "organization": self._run_with_semaphore(
                self.organization.get_organization(),
            ),
            "networks": self._run_with_semaphore(
                self.organization.get_organization_networks(),
            ),
            "devices": self._run_with_semaphore(
                self.organization.get_organization_devices(),
            ),
            "device_statuses": self._run_with_semaphore(
                self.organization.get_organization_devices_statuses(),
            ),
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
            self._run_with_semaphore(
                self.network.get_network_clients(
                    network.id,
                    perPage=1000,
                    total_pages="all",
                ),
            )
            for network in networks
        ]
        clients_results = await asyncio.gather(*client_tasks, return_exceptions=True)
        clients: list[dict[str, Any]] = []
        for i, network in enumerate(networks):
            result = clients_results[i]
            if isinstance(result, list):
                _LOGGER.debug(
                    "Fetched %d clients for network %s", len(result), network.name
                )
                for client in result:
                    client["networkId"] = network.id
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
            device.serial: self._run_with_semaphore(
                self.devices.get_device_clients(device.serial),
            )
            for device in devices
            if device.serial
            and device.product_type
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
    ) -> dict[str, asyncio.Task[Any]]:
        """
        Build a dictionary of tasks to fetch detailed data.

        Args:
            networks: A list of networks.
            devices: A list of devices.

        Returns
        -------
            A dictionary of tasks.

        """
        detail_tasks: dict[str, asyncio.Task[Any]] = {}
        for network in networks:
            network_id: str | None = network.id
            if not network_id:
                continue
            product_types = network.product_types
            if "wireless" in product_types:
                detail_tasks[f"ssids_{network_id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.wireless.get_network_ssids(network_id),
                    )
                )
            if "appliance" in product_types:
                if not self.coordinator or self.coordinator.is_traffic_check_due(
                    network_id,
                ):
                    detail_tasks[f"traffic_{network_id}"] = asyncio.create_task(
                        self._run_with_semaphore(
                            self.network.get_network_traffic(network_id, "appliance"),
                        )
                    )
                if not self.coordinator or self.coordinator.is_vlan_check_due(
                    network_id,
                ):
                    detail_tasks[f"vlans_{network_id}"] = asyncio.create_task(
                        self._run_with_semaphore(
                            self.appliance.get_network_vlans(network_id),
                        )
                    )
                detail_tasks[f"l3_firewall_rules_{network_id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_l3_firewall_rules(network_id),
                    )
                )
                detail_tasks[f"traffic_shaping_{network_id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_traffic_shaping(network_id),
                    )
                )
                if self._enable_vpn_management:
                    detail_tasks[f"vpn_status_{network.id}"] = asyncio.create_task(
                        self._run_with_semaphore(
                            self.appliance.get_vpn_status(network.id),
                        )
                    )
                detail_tasks[f"content_filtering_{network.id}"] = asyncio.create_task(
                    self._run_with_semaphore(
                        self.appliance.get_network_appliance_content_filtering(
                            network.id,
                        ),
                    )
                )
            if "wireless" in product_types:
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

        networks_res = initial_results.get("networks", [])
        if isinstance(networks_res, Exception):
            _LOGGER.warning(
                "Could not fetch networks, network data will be unavailable: %s",
                networks_res,
            )
            networks_list = []
        else:
            networks_list = [MerakiNetwork.from_dict(n) for n in networks_res]

        devices_res = initial_results.get("devices", [])
        if isinstance(devices_res, Exception):
            _LOGGER.warning(
                "Could not fetch devices, device data will be unavailable: %s",
                devices_res,
            )
            devices_list = []
        else:
            devices_list = [MerakiDevice.from_dict(d) for d in devices_res]

        device_statuses = initial_results.get("device_statuses", [])
        if isinstance(device_statuses, Exception):
            _LOGGER.warning(
                "Could not fetch device statuses, "
                "device status data will be unavailable: %s",
                device_statuses,
            )
            device_statuses = []

        parse_device_data(devices_list, device_statuses)
        appliance_uplink_statuses = initial_results.get("appliance_uplink_statuses")
        sensor_readings = initial_results.get("sensor_readings")
        battery_readings = initial_results.get("battery_readings")

        parse_appliance_data(devices_list, appliance_uplink_statuses)
        parse_sensor_data(devices_list, sensor_readings, battery_readings)

        detail_tasks = self._build_detail_tasks(networks_list, devices_list)
        detail_results = await asyncio.gather(
            *detail_tasks.values(),
            return_exceptions=True,
        )
        detail_data = dict(zip(detail_tasks.keys(), detail_results, strict=True))

        parse_camera_data(devices_list, detail_data)
        parse_switch_data(devices_list, detail_data)

        network_clients, device_clients = await asyncio.gather(
            self._async_fetch_network_clients(networks_list),
            self._async_fetch_device_clients(devices_list),
            return_exceptions=True,
        )

        processed_network_data = parse_network_data(
            detail_data,
            networks_list,
            previous_data,
            self.coordinator,
        )
        processed_wireless_data = parse_wireless_data(
            detail_data,
            networks_list,
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
            "networks": networks_list,
            "devices": devices_list,
            "clients": network_clients if isinstance(network_clients, list) else [],
            "clients_by_serial": (
                device_clients if isinstance(device_clients, dict) else {}
            ),
            "ssids": processed_wireless_data.get("ssids", []),
            "switch_ports_statuses": switch_ports_statuses,
            **processed_network_data,
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

    async def unregister_webhook(self, webhook_id: str) -> None:
        """
        Unregister a webhook with the Meraki API.

        Args:
            webhook_id: The ID of the webhook to unregister.

        """
        await self.network.unregister_webhook(webhook_id)

    async def async_reboot_device(self, serial: str) -> dict[str, Any]:
        """
        Reboot a device.

        Args:
            serial: The serial number of the device to reboot.

        Returns
        -------
            The API response.

        """
        return cast(dict[str, Any], await self.appliance.reboot_device(serial))

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
