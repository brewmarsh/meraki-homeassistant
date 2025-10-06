"""
Meraki API sensor endpoints.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ..client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class SensorEndpoints:
    """Sensor endpoints for the Meraki API."""

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the sensor endpoints."""
        self._client = client

    async def create_device_sensor_command(
        self, serial: str, operation: str
    ) -> Dict[str, Any]:
        """Send a command to a sensor.

        Args:
            serial: The serial number of the device.
            operation: The operation to perform on the sensor.
        """
        _LOGGER.debug("Sending command '%s' to sensor %s", operation, serial)
        return await self._client._run_sync(
            self._client._dashboard.sensor.createDeviceSensorCommand,
            serial=serial,
            operation=operation,
        )