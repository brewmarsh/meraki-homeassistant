"""Device data parsers."""
from __future__ import annotations

from typing import Any


def parse_device_data(
    devices: list[dict[str, Any]],
    device_statuses: list[dict[str, Any]],
) -> None:
    """
    Parse and merge device data.

    Args:
    ----
        devices: A list of devices.
        device_statuses: A list of device statuses.

    """
    if not devices or not device_statuses:
        return

    statuses_by_serial = {status["serial"]: status for status in device_statuses}
    for device in devices:
        serial = device.get("serial")
        if serial in statuses_by_serial:
            device.update(statuses_by_serial[serial])
