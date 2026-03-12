"""
Parsers for Meraki appliance data.

This module contains functions for parsing and structuring data related to
Meraki appliances.
"""

from __future__ import annotations

import logging
from typing import Any

from ...core.models import MerakiAppliancePort
from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


def parse_appliance_data(
    devices: list[MerakiDevice],
    detail_data: dict[str, Any],
    previous_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Parse appliance-specific data and update device objects.

    This function enriches device objects with data that is specific to
    appliances, such as uplink statuses.

    Args:
        devices: A list of device objects to update.
        detail_data: Dictionary containing fetched data.
        previous_data: Dictionary containing previous data for fallback.

    Returns
    -------
        An empty dictionary.
    """
    appliance_uplink_statuses = detail_data.get("appliance_uplink_statuses")

    if appliance_uplink_statuses is None and previous_data:
        appliance_uplink_statuses = previous_data.get("appliance_uplink_statuses")

    if isinstance(appliance_uplink_statuses, Exception):
        _LOGGER.warning(
            "Could not fetch appliance uplink statuses, data will be unavailable: %s",
            appliance_uplink_statuses,
        )
        return {}

    if not appliance_uplink_statuses:
        return {}

    _LOGGER.debug("Parsing appliance data for %s items", len(appliance_uplink_statuses))

    for status in appliance_uplink_statuses:
        serial = status.get("serial")
        if not serial:
            continue

        for device in devices:
            if device.serial == serial:
                _LOGGER.debug("Matched uplink data for %s", serial)
                uplinks = status.get("uplinks", [])
                device.appliance_uplink_statuses = uplinks
                # Initialize uplinks with status data;
                # will be enriched with performance metrics later
                device.uplinks = uplinks
                break

    return {}


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
        serial: str | None = device.serial
        if serial and (ports_data := ports_by_serial.get(serial)):
            appliance_ports = []
            for port in ports_data:
                try:
                    appliance_ports.append(MerakiAppliancePort.from_dict(port))
                except Exception as e:
                    _LOGGER.error(
                        "Failed to parse appliance port data for device %s: %s. Data: %s",
                        serial,
                        e,
                        port,
                    )
            device.appliance_ports = appliance_ports
