"""Helper for fetching and parsing appliance uplinks."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...core.api.client import MerakiAPIClient
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class ApplianceUplinkHelper:
    """Helper class for appliance uplink operations."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """Initialize the helper."""
        self.client = client

    async def get_uplink_performance(self, network_id: str) -> list[dict[str, Any]]:
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

    def process_uplink_performance(
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
