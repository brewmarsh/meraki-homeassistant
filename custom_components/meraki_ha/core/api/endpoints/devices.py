"""Meraki API endpoints for devices."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ....async_logging import async_log_time
from ....helpers.logging_helper import MerakiLoggers
from ...utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = MerakiLoggers.API


class DevicesEndpoints:
    """Device-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """
        Initialize the endpoint.

        Args:
        ----
            api_client: The Meraki API client.

        """
        self._api_client = api_client

    @handle_meraki_errors
    @async_log_time(slow_threshold=3.0)
    async def get_device_clients(self, serial: str) -> list[dict[str, Any]]:
        """
        Get all clients for a device.

        Args:
        ----
            serial: The serial number of the device.

        Returns
        -------
            A list of clients.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.devices
        clients = await api.getDeviceClients(
            serial,
            timespan=300,  # 5 minutes to get current clients
        )
        validated = validate_response(clients)
        if isinstance(validated, list):
            return validated
        return []

    @handle_meraki_errors
    @async_log_time(slow_threshold=3.0)
    async def get_device(self, serial: str) -> dict[str, Any]:
        """
        Get a single device.

        Args:
        ----
            serial: The serial number of the device.

        Returns
        -------
            The device details.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.devices
        device = await api.getDevice(serial=serial)
        validated = validate_response(device)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_device did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def reboot_device(self, serial: str) -> dict[str, Any]:
        """
        Reboot a device.

        Args:
            serial: The serial number of the device.

        Returns
        -------
            The response from the API.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.devices
        result = await api.rebootDevice(serial=serial)
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("reboot_device did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_device(self, serial: str, **kwargs: Any) -> dict[str, Any]:
        """
        Update a device.

        Args:
        ----
            serial: The serial number of the device.
            **kwargs: The device settings to update.

        Returns
        -------
            The updated device.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.devices
        device = await api.updateDevice(serial=serial, **kwargs)
        validated = validate_response(device)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_device did not return a dict.")
            return {}
        return validated
