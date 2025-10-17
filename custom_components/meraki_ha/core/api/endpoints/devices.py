"""Meraki API endpoints for devices."""

import logging
from typing import Any, Dict, List

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

_LOGGER = logging.getLogger(__name__)


class DevicesEndpoints:
    """Device-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    async def get_device_clients(self, serial: str) -> List[Dict[str, Any]]:
        """Get all clients for a device."""
        clients = await self._api_client._run_sync(
            self._dashboard.devices.getDeviceClients,
            serial,
            timespan=300,  # 5 minutes to get current clients
        )
        return validate_response(clients)

    @handle_meraki_errors
    async def get_device(self, serial: str) -> Dict[str, Any]:
        """Get a single device."""
        device = await self._api_client._run_sync(
            self._dashboard.devices.getDevice,
            serial=serial,
        )
        validated = validate_response(device)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_device did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_device(self, serial: str, **kwargs) -> Dict[str, Any]:
        """Update a device."""
        device = await self._api_client._run_sync(
            self._dashboard.devices.updateDevice,
            serial=serial,
            **kwargs,
        )
        validated = validate_response(device)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_device did not return a dict.")
            return {}
        return validated
