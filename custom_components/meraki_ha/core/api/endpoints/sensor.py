"""Meraki API sensor endpoints."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class SensorEndpoints:
    """Sensor endpoints for the Meraki API."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """
        Initialize the sensor endpoints.

        Args:
        ----
            client: The Meraki API client.

        """
        self._client = client

    async def create_device_sensor_command(
        self,
        serial: str,
        operation: str,
    ) -> dict[str, Any]:
        """
        Send a command to a sensor.

        Args:
        ----
            serial: The serial number of the device.
            operation: The operation to perform on the sensor.

        Returns
        -------
            The response from the API.

        """
        _LOGGER.debug("Sending command '%s' to sensor %s", operation, serial)
        return await self._client.run_sync(
            self._client.dashboard.sensor.createDeviceSensorCommand,
            serial=serial,
            operation=operation,
        )

    async def get_organization_sensor_readings_latest(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return the latest available reading for each metric from each sensor.

        Returns
        -------
            The response from the API.

        """
        _LOGGER.debug("Getting latest sensor readings for organization")
        return await self._client.run_sync(
            self._client.dashboard.sensor.getOrganizationSensorReadingsLatest,
            organizationId=self._client.organization_id,
            total_pages="all",
        )

    async def get_organization_door_sensor_readings_latest(
        self,
        serials: list[str],
    ) -> list[dict[str, Any]]:
        """
        Return the latest available reading for the door metric from each sensor.

        Returns
        -------
            The response from the API.

        """
        _LOGGER.debug("Getting latest door sensor readings for organization")
        return await self._client.run_sync(
            self._client.dashboard.sensor.getOrganizationSensorReadingsLatest,
            organizationId=self._client.organization_id,
            serials=serials,
            metrics=["door"],
            total_pages="all",
        )
