"""Appliance fetch strategy."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

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

    def _add_feature_based_tasks(
        self, network_id: str, tasks: dict[str, Any]
    ) -> None:
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
            self._async_get_appliance_ports(network_id),
        )
        tasks[f"content_filtering_{network_id}"] = self.client.run_with_semaphore(
            self.client.appliance.get_network_appliance_content_filtering(
                network_id,
            ),
        )
        tasks[f"uplink_performance_{network_id}"] = self.client.run_with_semaphore(
            self._get_uplink_performance(network_id),
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
                        "Port status/control requires VLANs to be "
                        "enabled in Meraki Dashboard."
                    )
                    _VLAN_WARNING_LOGGED = True
                return []
            raise

    async def _get_uplink_performance(self, network_id: str) -> list[dict[str, Any]]:
        """Fetch uplink performance with robust fallback."""
        methods = [
            ("getNetworkApplianceUplinksUsageHistory", {"timespan": 60}),
            ("getNetworkApplianceUplinksLossAndLatency", {}),
            ("getNetworkApplianceUplinksPerformance", {}),
        ]

        for method_name, extra_kwargs in methods:
            if result := await self._try_fetch_performance(
                network_id, method_name, extra_kwargs
            ):
                return result
        return []

    async def _try_fetch_performance(
        self, network_id: str, method_name: str, extra_kwargs: dict[str, Any]
    ) -> list[dict[str, Any]] | None:
        """Try to fetch performance data using a specific method."""
        if not hasattr(self.client.dashboard.appliance, method_name):
            return None

        method = getattr(self.client.dashboard.appliance, method_name)
        try:
            _LOGGER.debug(
                "Attempting to fetch uplink performance using %s", method_name
            )
            performance = await self.client.run_sync(
                method, networkId=network_id, **extra_kwargs
            )
            if isinstance(performance, list):
                return performance
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.debug(
                "Method %s failed for network %s: %s",
                method_name,
                network_id,
                e,
            )
        return None

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

        if result := self._handle_traffic_error(network_id, key, data):
            appliance_traffic[network_id] = result
        elif isinstance(data, dict):
            appliance_traffic[network_id] = data
        elif previous_data and key in previous_data:
            appliance_traffic[network_id] = previous_data[key]

    def _handle_traffic_error(
        self, network_id: str, key: str, data: Any
    ) -> dict[str, str] | None:
        """Handle traffic analysis errors."""
        if isinstance(data, MerakiTrafficAnalysisError):
            self._disabled_features.add(key)
            _LOGGER.info(
                "Traffic analysis is not enabled for network %s.",
                network_id,
            )
            return {"error": "disabled", "reason": str(data)}

        if (
            isinstance(data, MerakiInformationalError)
            and "traffic analysis" in str(data).lower()
        ):
            self._disabled_features.add(key)
            return {"error": "disabled", "reason": str(data)}

        return None

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

        if self._handle_vlan_error(key, data):
            vlan_by_network[network_id] = []
        elif isinstance(data, list):
            vlan_by_network[network_id] = data
        elif previous_data and key in previous_data:
            vlan_by_network[network_id] = previous_data[key]

    def _handle_vlan_error(self, key: str, data: Any) -> bool:
        """Handle VLAN errors and return True if feature should be disabled."""
        if isinstance(data, (MerakiVlanError, MerakiVlansDisabledError)):
            self._disabled_features.add(key)
            if isinstance(data, MerakiVlanError):
                _LOGGER.info(str(data))
            return True

        if isinstance(data, MerakiInformationalError):
            if "vlans are not enabled" in str(data).lower():
                self._disabled_features.add(key)
                return True

        return False

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process appliance details."""
        self._process_appliance_ports(device, detail_data, prev_device)
        self._process_dynamic_dns(device, detail_data, prev_device)
        self._process_management_interface(device, detail_data, prev_device)
        self._process_uplink_performance(device, detail_data, prev_device)

    def _process_appliance_ports(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process appliance ports."""
        if ports := detail_data.get(f"appliance_ports_{device.network_id}"):
            if isinstance(ports, list):
                device.appliance_ports = [
                    MerakiAppliancePort.from_dict(p)
                    for p in ports
                    if isinstance(p, dict)
                ]
        elif prev_device and hasattr(prev_device, "appliance_ports"):
            device.appliance_ports = prev_device.appliance_ports

    def _process_dynamic_dns(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process dynamic DNS settings."""
        if settings := detail_data.get(f"appliance_settings_{device.serial}"):
            # Defensive check: Ensure settings is a dict before calling .get()
            if isinstance(settings, dict) and isinstance(
                settings.get("dynamicDns"), dict
            ):
                device.dynamic_dns = settings["dynamicDns"]
        elif prev_device and hasattr(prev_device, "dynamic_dns"):
            device.dynamic_dns = prev_device.dynamic_dns

    def _process_management_interface(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process management interface settings."""
        interface_key = f"management_interface_{device.serial}"
        if management_interface := detail_data.get(interface_key):
            if isinstance(management_interface, dict):
                device.management_interface = management_interface
        elif prev_device and hasattr(prev_device, "management_interface"):
            device.management_interface = prev_device.management_interface

    def _process_uplink_performance(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process uplink performance data."""
        performance = detail_data.get(f"uplink_performance_{device.network_id}")

        if not isinstance(performance, list):
            if prev_device and hasattr(prev_device, "uplinks"):
                device.uplinks = prev_device.uplinks
            return

        normalized_performance = self._normalize_uplink_performance(performance)
        device_perf = [
            p for p in normalized_performance if p.get("serial") == device.serial
        ]

        device.uplinks = self._merge_uplink_status_and_performance(
            device.appliance_uplink_statuses, device_perf
        )

    def _merge_uplink_status_and_performance(
        self,
        statuses: list[dict[str, Any]],
        performance: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Merge uplink status and performance data."""
        perf_by_interface = {p.get("interface"): p for p in performance}
        merged_uplinks = []

        # Use appliance_uplink_statuses as the base for merging
        for status_uplink in statuses:
            interface = status_uplink.get("interface")
            perf = perf_by_interface.get(interface, {})
            merged_uplinks.append({**status_uplink, **perf})

        # Add any interfaces found in performance but not in status
        status_interfaces = {u.get("interface") for u in statuses}
        for interface, perf in perf_by_interface.items():
            if interface not in status_interfaces:
                merged_uplinks.append(perf)

        return merged_uplinks

    def _normalize_uplink_performance(
        self, performance: list[Any]
    ) -> list[dict[str, Any]]:
        """Normalize uplink performance data keys."""
        normalized = []
        for p in performance:
            if not isinstance(p, dict):
                continue
            item = p.copy()
            if "loss" in item and "lossPercent" not in item:
                item["lossPercent"] = item["loss"]
            if "latency" in item and "latencyMs" not in item:
                item["latencyMs"] = item["latency"]
            normalized.append(item)
        return normalized
