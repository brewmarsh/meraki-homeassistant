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
<<<<<<< HEAD
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

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
<<<<<<< HEAD
<<<<<<< HEAD
        statuses = await self._api_client.run_sync(
            self._dashboard.switch.getDeviceSwitchPortsStatuses, serial=serial
=======
<<<<<<< HEAD
        statuses = await self._api_client.run_sync(
            self._dashboard.switch.getDeviceSwitchPortsStatuses, serial=serial
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        statuses = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getDeviceSwitchPortsStatuses,
            serial=serial,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning("get_device_switch_ports_statuses did not return a list.")
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
<<<<<<< HEAD
<<<<<<< HEAD
        ports = await self._api_client.run_sync(
            self._dashboard.switch.getDeviceSwitchPorts, serial=serial
=======
<<<<<<< HEAD
        ports = await self._api_client.run_sync(
            self._dashboard.switch.getDeviceSwitchPorts, serial=serial
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        ports = await self._api_client.run_sync(
            self._api_client.dashboard.switch.getDeviceSwitchPorts, serial=serial
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_switch_ports did not return a list.")
            return []
        return validated
