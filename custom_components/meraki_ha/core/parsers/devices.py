"""Device data parsers."""

from __future__ import annotations

from typing import Any

from ...types import MerakiDevice


def parse_device_data(
    devices: list[MerakiDevice],
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

    statuses_by_serial = {
        status["serial"]: status for status in device_statuses if "serial" in status
    }

    for device in devices:
        serial = device.serial
        if serial in statuses_by_serial:
            status_data = statuses_by_serial[serial]
            for key, value in status_data.items():
                if hasattr(device, key):
                    setattr(device, key, value)
