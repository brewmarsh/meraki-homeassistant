"""Device data parsers."""

from __future__ import annotations

import logging
from typing import Any

from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


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
            status_dict = statuses_by_serial[serial]

            _LOGGER.debug(
                "Mapping status for %s: extracted_status='%s', raw_payload_keys=%s",
                device.serial,
                status_dict.get("status"),
                list(status_dict.keys())
            )

            for key, value in status_dict.items():
                # map key to snake_case if needed, otherwise use key as is
                # (e.g. for 'status')
                attr_name = key_map.get(key, key)

                # Normalize status to lowercase for consistency
                if attr_name == "status" and isinstance(value, str):
                    value = value.lower()

                if hasattr(device, attr_name):
                    setattr(device, attr_name, value)
