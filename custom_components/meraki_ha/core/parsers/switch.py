"""Parsers for Meraki switch data."""

from __future__ import annotations

from typing import Any

from ...core.models.device import MerakiDevice


def parse_switch_data(
    devices: list[MerakiDevice],
    detail_data: dict[str, Any],
) -> None:
    """
    Parse and process switch-level data.

    Args:
        devices: A list of Meraki devices.
        detail_data: The raw detailed data from the API.
    """
    for device in devices:
        if device.product_type != "switch":
            continue

        switch_ports_key = f"switch_ports_{device.serial}"
        ports_statuses = detail_data.get(switch_ports_key)
        if isinstance(ports_statuses, list):
            device.switch_ports = ports_statuses
