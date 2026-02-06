"""Meraki API endpoints for switches."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..protocol import MerakiApiClientProtocol


_LOGGER = logging.getLogger(__name__)


class SwitchEndpoints:
    """Switch-related endpoints."""

    def __init__(self, api_client: MerakiApiClientProtocol) -> None:
        """
        Initialize the endpoint.

        Args:
        ----
            api_client: The Meraki API client.

        """
        self._api_client = api_client

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_device_switch_ports_statuses(
        self, serial: str
    ) -> list[dict[str, Any]]:
        """
        Get statuses for all ports of a switch.

        Args:
        ----
            serial: The serial number of the switch.

        Returns
        -------
            A list of port statuses.

        """
        statuses = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getDeviceSwitchPortsStatuses,
            serial=serial,
        )
        res = validate_response(statuses)
        # Type Normalization: Meraki sometimes returns {} instead of [] for no data
        return [] if not res else res

    @handle_meraki_errors
    @async_timed_cache()
    async def get_switch_ports(self, serial: str) -> list[dict[str, Any]]:
        """
        Get ports for a switch.

        Args:
        ----
            serial: The serial number of the switch.

        Returns
        -------
            A list of ports.

        """
        ports = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getDeviceSwitchPorts, serial=serial
        )
        res = validate_response(ports)
        # Type Normalization: Meraki sometimes returns {} instead of [] for no data
        return [] if not res else res

    @handle_meraki_errors
    async def cycle_device_switch_ports(
        self,
        serial: str,
        ports: list[str],
    ) -> dict[str, Any] | list[Any]:
        """
        Cycle a set of switch ports.

        Args:
        ----
            serial: The serial number of the switch.
            ports: A list of port IDs to cycle.

        Returns
        -------
            The API response.

        """
        response = await self._api_client.run_sync(
            self._api_client.dashboard.switch.cycleDeviceSwitchPorts,
            serial=serial,
            ports=ports,
        )
        return validate_response(response)

    @handle_meraki_errors
    async def update_device_switch_port(
        self,
        serial: str,
        port_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update a switch port.

        Args:
        ----
            serial: The serial number of the switch.
            port_id: The port ID or number.
            **kwargs: The parameters to update (e.g., enabled=True).

        Returns
        -------
            The updated port configuration.

        """
        response = await self._api_client.run_sync(
            self._api_client.dashboard.switch.updateDeviceSwitchPort,
            serial=serial,
            portId=port_id,
            **kwargs,
        )
        return validate_response(response)
