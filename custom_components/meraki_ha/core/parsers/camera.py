"""Parser for Meraki camera data."""

from __future__ import annotations

import logging
from typing import Any

from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


def parse_camera_data(
    devices: list[MerakiDevice],
    detail_data: dict[str, Any],
) -> None:
    """
    Parse and enrich camera device data.

    Args:
        ----
        devices: A list of Meraki devices.
        detail_data: A dictionary of detailed data from the API.

    """
    for device in devices:
        if device.product_type == "camera":
            # Add analytics data
            analytics_data = detail_data.get(f"camera_analytics_{device.serial}")
            if isinstance(analytics_data, list):
                device.analytics = analytics_data
            else:
                _LOGGER.debug(
                    "No analytics data found for camera %s",
                    device.serial,
                )
