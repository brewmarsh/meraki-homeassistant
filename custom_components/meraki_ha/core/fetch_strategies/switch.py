"""Switch fetch strategy."""

from __future__ import annotations

import asyncio
from typing import Any

from ...core.models.device import MerakiDevice
from .base import BaseFetchStrategy


class SwitchFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching switch data."""

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
    ) -> None:
        """Add switch specific device tasks."""
        if "switch_ports" in capabilities:
            tasks[f"ports_statuses_{device.serial}"] = self.client.run_with_semaphore(
                self.client.switch.get_device_switch_ports_statuses(device.serial),
            )

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process switch details."""
        statuses_key = f"ports_statuses_{device.serial}"
        statuses = detail_data.get(statuses_key)
        if isinstance(statuses, list):
            device.ports_statuses = statuses
        elif prev_device and hasattr(prev_device, "ports_statuses"):
            device.ports_statuses = prev_device.ports_statuses
