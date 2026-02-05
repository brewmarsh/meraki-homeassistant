"""Sensor fetch strategy."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .base import BaseFetchStrategy

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class SensorFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching sensor data."""

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add sensor specific device tasks."""
        # Only add relationships task if it's a sensor and we have relevant capabilities
        # This is the "guarded" fetch logic.
        # Fixed: Ensure device has a serial before scheduling API calls
        if (
            "battery" in capabilities or "temperature" in capabilities
        ) and device.serial:
            tasks[f"sensor_relationships_{device.serial}"] = (
                self.client.run_with_semaphore(
                    self.client.sensor.get_device_sensor_relationships(device.serial),
                )
            )

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process sensor details."""
        rel_key = f"sensor_relationships_{device.serial}"

        # Defensive: Use assignment expression and type check
        if relationships := detail_data.get(rel_key):
            if isinstance(relationships, list):
                device.sensor_relationships = relationships
        # Defensive: Use hasattr to prevent AttributeError if model changes
        elif prev_device and hasattr(prev_device, "sensor_relationships"):
            device.sensor_relationships = prev_device.sensor_relationships