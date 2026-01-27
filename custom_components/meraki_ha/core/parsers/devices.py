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

    # Meraki API uses camelCase, but MerakiDevice dataclass uses snake_case
    # This maps camelCase API keys to snake_case dataclass attributes
    key_map = {
        "lanIp": "lan_ip",
        "wan1Ip": "wan1_ip",
        "wan2Ip": "wan2_ip",
        "publicIp": "public_ip",
        "firmware": "firmware",
    }

    for device in devices:
        serial = device.serial
        if serial in statuses_by_serial:
            status_data = statuses_by_serial[serial]
            for key, value in status_data.items():
                # map key to snake_case if needed, otherwise use key as is
                # (e.g. for 'status')
                attr_name = key_map.get(key, key)
                if hasattr(device, attr_name):
                    setattr(device, attr_name, value)
