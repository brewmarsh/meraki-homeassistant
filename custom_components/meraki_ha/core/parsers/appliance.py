"""
Parsers for Meraki appliance data.

This module contains functions for parsing and structuring data related to
Meraki appliances.
"""

from __future__ import annotations

import logging
from typing import Any

from ...types import MerakiAppliancePort, MerakiDevice

_LOGGER = logging.getLogger(__name__)


def parse_appliance_data(
    devices: list[MerakiDevice],
    appliance_uplink_statuses: list[dict[str, Any]] | Exception | None,
) -> None:
    """
    Parse appliance-specific data and update device objects.

    This function enriches device objects with data that is specific to
    appliances, such as uplink statuses.

    Args:
        devices: A list of device objects to update.
        appliance_uplink_statuses: A list of appliance uplink statuses.
    """
    if isinstance(appliance_uplink_statuses, Exception):
        _LOGGER.warning(
            "Could not fetch appliance uplink statuses, data will be unavailable: %s",
            appliance_uplink_statuses,
        )
        return

    if not appliance_uplink_statuses:
        return

    for status in appliance_uplink_statuses:
        serial = status.get("serial")
        if not serial:
            continue

        for device in devices:
            if device.serial == serial:
                device.appliance_uplink_statuses = status.get("uplinks", [])
                break


def parse_appliance_ports(
    devices: list[MerakiDevice],
    ports_by_serial: dict[str, list[dict[str, Any]]],
) -> None:
    """
    Parse appliance ports and update device objects.

    Args:
        devices: A list of device objects.
        ports_by_serial: A dictionary mapping serial to a list of port data.
    """
    if not ports_by_serial:
        return

    for device in devices:
        if ports_data := ports_by_serial.get(device.serial):
            device.appliance_ports = [
                MerakiAppliancePort.from_dict(port) for port in ports_data
            ]
