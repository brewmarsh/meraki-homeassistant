"""Appliance fetch strategy."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import meraki
from meraki.exceptions import APIError

from ...core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)
from ...core.models.device import MerakiAppliancePort, MerakiDevice
from .base import BaseFetchStrategy

if TYPE_CHECKING:
    from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

_VLAN_WARNING_LOGGED = False


class ApplianceFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching appliance data."""

    def __init__(
        self,
        client: MerakiAPIClient,
        _disabled_features: set[str],
        enable_vpn_management: bool,
        enable_firewall_rules: bool,
        enable_traffic_shaping: bool,
    ) -> None:
        """Initialize the appliance fetch strategy."""
        super().__init__(client, _disabled_features)
        self.enable_vpn_management = enable_vpn_management
        self.enable_firewall_rules = enable_firewall_rules
        self.enable_traffic_shaping = enable_traffic_shaping

    def build_network_tasks(
        self,
        network_id: str,
        tasks: dict[str, Any],
    ) -> None:
        """Add appliance specific network tasks."""
        if f"traffic_{network_id}" not in self._disabled_features:
            tasks[f"traffic_{network_id}"] = self.client.run_with_semaphore(
                self.client.network.get_network_traffic(network_id, "appliance"),
            )

        if f"vlans_{network_id}" not in self._disabled_features:
            tasks[f"vlans_{network_id}"] = self.client.run_with_semaphore(
                self.client.network.get_vlan_data(network_id),
            )

        if self.enable_firewall_rules:
            tasks[f"l3_firewall_rules_{network_id}"] = self.client.run_with_semaphore(
                self.client.appliance.get_l3_firewall_rules(network_id),
            )
        if self.enable_traffic_shaping:
            tasks[f"traffic_shaping_{network_id}"] = self.client.run_with_semaphore(
                self.client.appliance.get_traffic_shaping(network_id),
            )
        if self.enable_vpn_management:
            tasks[f"vpn_status_{network_id}"] = self.client.run_with_semaphore(
                self.client.appliance.get_vpn_status(network_id),
            )
        tasks[f"appliance_ports_{network_id}"] = self.client.run_with_semaphore(
            self._async_get_appliance_ports(network_id),
        )
        tasks[f"content_filtering_{network_id}"] = self.client.run_with_semaphore(
            self.client.appliance.get_network_appliance_content_filtering(
                network_id,
            ),
        )
        tasks[f"uplink_performance_{network_id}"] = self.client.run_with_semaphore(
            self.client.appliance.get_network_appliance_uplinks_performance(
                network_id,
            ),
        )

    async def _async_get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """Fetch appliance ports with graceful error handling for disabled VLANs."""
        try:
            return await self.client.appliance.get_appliance_ports(network_id)
        except APIError as e:
            if e.status == 400 and "VLANs" in str(e):
                global _VLAN_WARNING_LOGGED
                if not _VLAN_WARNING_LOGGED:
                    _LOGGER.warning(
                        "Port status/control requires VLANs to be enabled in Meraki Dashboard."
                    )
                    _VLAN_WARNING_LOGGED = True
                return []
            raise

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add appliance specific device tasks."""
        if device.network_id:
            tasks[f"appliance_settings_{device.serial}"] = (
                self.client.run_with_semaphore(
                    self.client.appliance.get_network_appliance_settings(
                        device.network_id,
                    ),
                )
            )
        if "led_control" in capabilities and device.serial:
            tasks[f"management_interface_{device.serial}"] = (
                self.client.run_with_semaphore(
                    self.client.devices.get_device_management_interface(device.serial),
                )
            )

    def process_network_traffic(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        appliance_traffic: dict[str, Any],
    ) -> None:
        """Process traffic data for a network."""
        key = f"traffic_{network_id}"
        data = detail_data.get(key)
        if isinstance(data, MerakiTrafficAnalysisError):
            self._disabled_features.add(key)
            _LOGGER.info(
                "Traffic analysis is not enabled for network %s.",
                network_id,
            )
            appliance_traffic[network_id] = {
                "error": "disabled",
                "reason": str(data),
            }
        elif (
            isinstance(data, MerakiInformationalError)
            and "traffic analysis" in str(data).lower()
        ):
            self._disabled_features.add(key)
            appliance_traffic[network_id] = {
                "error": "disabled",
                "reason": str(data),
            }
        elif isinstance(data, dict):
            appliance_traffic[network_id] = data
        elif previous_data and key in previous_data:
            appliance_traffic[network_id] = previous_data[key]

    def process_network_vlans(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        vlan_by_network: dict[str, Any],
    ) -> None:
        """Process VLAN data for a network."""
        key = f"vlans_{network_id}"
        data = detail_data.get(key)
        if isinstance(data, (MerakiVlanError, MerakiVlansDisabledError)):
            self._disabled_features.add(key)
            if isinstance(data, MerakiVlanError):
                _LOGGER.info(str(data))
            vlan_by_network[network_id] = []
        elif isinstance(data, MerakiInformationalError):
            if "vlans are not enabled" in str(data).lower():
                self._disabled_features.add(key)
                vlan_by_network[network_id] = []
        elif isinstance(data, list):
            vlan_by_network[network_id] = data
        elif previous_data and key in previous_data:
            vlan_by_network[network_id] = previous_data[key]

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process appliance details."""
        if ports := detail_data.get(f"appliance_ports_{device.network_id}"):
            if isinstance(ports, list):
                device.appliance_ports = [
                    MerakiAppliancePort.from_dict(p)
                    for p in ports
                    if isinstance(p, dict)
                ]
        elif prev_device and hasattr(prev_device, "appliance_ports"):
            device.appliance_ports = prev_device.appliance_ports

        if settings := detail_data.get(f"appliance_settings_{device.serial}"):
            # Defensive check: Ensure settings is a dict before calling .get()
            if isinstance(settings, dict) and isinstance(
                settings.get("dynamicDns"), dict
            ):
                device.dynamic_dns = settings["dynamicDns"]
        elif prev_device and hasattr(prev_device, "dynamic_dns"):
            device.dynamic_dns = prev_device.dynamic_dns

        interface_key = f"management_interface_{device.serial}"
        if management_interface := detail_data.get(interface_key):
            if isinstance(management_interface, dict):
                device.management_interface = management_interface
        elif prev_device and hasattr(prev_device, "management_interface"):
            device.management_interface = prev_device.management_interface

        if performance := detail_data.get(f"uplink_performance_{device.network_id}"):
            if isinstance(performance, list):
                # Filter performance data for this device
                device_perf = [
                    p for p in performance if p.get("serial") == device.serial
                ]
                # Merge with existing status data in device.uplinks
                perf_by_interface = {p.get("interface"): p for p in device_perf}
                merged_uplinks = []
                # Use appliance_uplink_statuses as the base for merging
                for status_uplink in device.appliance_uplink_statuses:
                    interface = status_uplink.get("interface")
                    perf = perf_by_interface.get(interface, {})
                    merged_uplinks.append({**status_uplink, **perf})

                # Add any interfaces found in performance but not in status
                status_interfaces = {
                    u.get("interface") for u in device.appliance_uplink_statuses
                }
                for interface, perf in perf_by_interface.items():
                    if interface not in status_interfaces:
                        merged_uplinks.append(perf)
                device.uplinks = merged_uplinks
        elif prev_device and hasattr(prev_device, "uplinks"):
            device.uplinks = prev_device.uplinks
