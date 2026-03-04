"""Appliance fetch strategy."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...core.models.device import MerakiDevice
from .appliance_device import ApplianceDeviceHelper
from .appliance_traffic import ApplianceTrafficHelper
from .appliance_uplinks import ApplianceUplinkHelper
from .base import BaseFetchStrategy

if TYPE_CHECKING:
    from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


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

        self.traffic_helper = ApplianceTrafficHelper(self._disabled_features)
        self.uplink_helper = ApplianceUplinkHelper(self.client)
        self.device_helper = ApplianceDeviceHelper(self.client)

    def build_network_tasks(
        self,
        network_id: str,
        tasks: dict[str, Any],
    ) -> None:
        """Add appliance specific network tasks."""
        self._add_traffic_and_vlan_tasks(network_id, tasks)
        self._add_feature_based_tasks(network_id, tasks)
        self._add_standard_appliance_tasks(network_id, tasks)

    def _add_traffic_and_vlan_tasks(
        self, network_id: str, tasks: dict[str, Any]
    ) -> None:
        """Add traffic and vlan tasks if not disabled."""
        if f"traffic_{network_id}" not in self._disabled_features:
            tasks[f"traffic_{network_id}"] = self.client.run_with_semaphore(
                self.client.network.get_network_traffic(network_id, "appliance"),
            )

        if f"vlans_{network_id}" not in self._disabled_features:
            tasks[f"vlans_{network_id}"] = self.client.run_with_semaphore(
                self.client.network.get_vlan_data(network_id),
            )

    def _add_feature_based_tasks(self, network_id: str, tasks: dict[str, Any]) -> None:
        """Add tasks based on enabled features."""
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

    def _add_standard_appliance_tasks(
        self, network_id: str, tasks: dict[str, Any]
    ) -> None:
        """Add standard appliance tasks."""
        tasks[f"appliance_ports_{network_id}"] = self.client.run_with_semaphore(
            self.device_helper.get_appliance_ports(network_id),
        )
        tasks[f"content_filtering_{network_id}"] = self.client.run_with_semaphore(
            self.client.appliance.get_network_appliance_content_filtering(
                network_id,
            ),
        )
        tasks[f"uplink_performance_{network_id}"] = self.client.run_with_semaphore(
            self.uplink_helper.get_uplink_performance(network_id),
        )

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
        self.traffic_helper.process_network_traffic(
            network_id, detail_data, previous_data, appliance_traffic
        )

    def process_network_vlans(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        vlan_by_network: dict[str, Any],
    ) -> None:
        """Process VLAN data for a network."""
        self.traffic_helper.process_network_vlans(
            network_id, detail_data, previous_data, vlan_by_network
        )

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process appliance details."""
        self.device_helper.process_appliance_ports(device, detail_data, prev_device)
        self.device_helper.process_dynamic_dns(device, detail_data, prev_device)
        self.device_helper.process_management_interface(
            device, detail_data, prev_device
        )
        self.uplink_helper.process_uplink_performance(device, detail_data, prev_device)
