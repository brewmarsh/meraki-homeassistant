"""Meraki API sensor endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ....helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..client import MerakiAPIClient

_LOGGER = MerakiLoggers.API


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

    @handle_meraki_errors
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
        if self._client.dashboard is None:
            return {}
        api = self._client.dashboard.sensor
        result = await api.createDeviceSensorCommand(serial=serial, operation=operation)
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("create_device_sensor_command did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
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
        if self._client.dashboard is None:
            return []
        api = self._client.dashboard.sensor
        result = await api.getOrganizationSensorReadingsLatest(
            organizationId=self._client.organization_id,
            total_pages="all",
        )
        validated = validate_response(result)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_sensor_readings_latest did not return a list"
            )
            return []
        return validated
