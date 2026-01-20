"""
Parsers for Meraki appliance data.

This module contains functions for parsing and structuring data related to
Meraki appliances.
"""

from __future__ import annotations

import logging
from typing import Any

from ...types import MerakiDevice

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
