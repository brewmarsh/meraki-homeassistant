"""Meraki API endpoints for switches."""

import logging
from typing import Any, Dict, List

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)
from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class SwitchEndpoints:
    """Switch-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_device_switch_ports_statuses(
        self, serial: str
    ) -> List[Dict[str, Any]]:
        """Get statuses for all ports of a switch."""
        statuses = await self._api_client._run_sync(
            self._dashboard.switch.getDeviceSwitchPortsStatuses, serial=serial
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning("get_device_switch_ports_statuses did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_switch_ports(self, serial: str) -> List[Dict[str, Any]]:
        """Get ports for a switch."""
        ports = await self._api_client._run_sync(
            self._dashboard.switch.getDeviceSwitchPorts, serial=serial
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_switch_ports did not return a list.")
            return []
        return validated