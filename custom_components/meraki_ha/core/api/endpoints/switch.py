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
    from ..client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class SwitchEndpoints:
    """Switch-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
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
        if self._api_client.dashboard is None:
            return []
        statuses = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getDeviceSwitchPortsStatuses,
            serial=serial,
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning("get_device_switch_ports_statuses did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_switch_ports_statuses_by_switch(
        self,
    ) -> list[dict[str, Any]]:
        """
        Get statuses for all switch ports in the organization.

        Returns
        -------
            A list of switch port statuses.

        """
        if self._api_client.dashboard is None:
            return []
        statuses = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getOrganizationSwitchPortsStatusesBySwitch,
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_switch_ports_statuses_by_switch did not return a list"
            )
            return []
        return validated

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
        if self._api_client.dashboard is None:
            return []
        ports = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getDeviceSwitchPorts, serial=serial
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_switch_ports did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def update_device_switch_port(
        self, serial: str, port_id: str, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a switch port.

        Args:
        ----
            serial: The serial number of the switch.
            port_id: The ID of the port to update.
            **kwargs: The settings to update.

        Returns
        -------
            The updated port configuration.

        """
        if self._api_client.dashboard is None:
            return None
        port = await self._api_client.run_sync(
            self._api_client.dashboard.switch.updateDeviceSwitchPort,
            serial=serial,
            portId=port_id,
            **kwargs,
        )
        return validate_response(port)

    @handle_meraki_errors
    async def update_device_switch_port(
        self, serial: str, port_id: str, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a switch port.

        Args:
        ----
            serial: The serial number of the switch.
            port_id: The ID of the port to update.
            **kwargs: The settings to update.

        Returns
        -------
            The updated port configuration.

        """
        if self._api_client.dashboard is None:
            return None
        port = await self._api_client.run_sync(
            self._api_client.dashboard.switch.updateDeviceSwitchPort,
            serial=serial,
            portId=port_id,
            **kwargs,
        )
        return validate_response(port)

    @handle_meraki_errors
    async def update_device_switch_port(
        self, serial: str, port_id: str, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a switch port.

        Args:
        ----
            serial: The serial number of the switch.
            port_id: The ID of the port to update.
            **kwargs: The settings to update.

        Returns
        -------
            The updated port configuration.

        """
        if self._api_client.dashboard is None:
            return None
        port = await self._api_client.run_sync(
            self._api_client.dashboard.switch.updateDeviceSwitchPort,
            serial=serial,
            portId=port_id,
            **kwargs,
        )
        return validate_response(port)
