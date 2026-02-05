"""Switch fetch strategy."""

from __future__ import annotations

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
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add switch specific device tasks."""
        # 1. Capability Guard: Does this device physically support switch ports?
        if "switch_ports" in capabilities:
            statuses_key = f"ports_statuses_{device.serial}"

            # 2. Batch Awareness: Do we already have this data from the bulk fetch?
            # If detail_data has the key, we skip the task to save an API call.
            if not detail_data or statuses_key not in detail_data:
                tasks[statuses_key] = self.client.run_with_semaphore(
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

        # Defensive coding: Only assign if we got a valid list
        if isinstance(statuses, list):
            device.ports_statuses = statuses
        elif prev_device and hasattr(prev_device, "ports_statuses"):
            # Fallback to previous data if the API failed this round
            device.ports_statuses = prev_device.ports_statuses
