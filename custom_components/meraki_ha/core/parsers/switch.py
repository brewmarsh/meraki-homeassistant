"""Parsers for Meraki switch data."""

from __future__ import annotations

from typing import Any

from ...types import MerakiDevice


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

        ports_statuses_key = f"ports_statuses_{device.serial}"
        ports_statuses = detail_data.get(ports_statuses_key)
        if isinstance(ports_statuses, list):
            device.ports_statuses = ports_statuses
