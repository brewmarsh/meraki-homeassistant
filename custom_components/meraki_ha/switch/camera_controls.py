"""Switch entities for controlling Meraki camera settings."""

import logging
from typing import Any

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..core.utils.naming_utils import format_device_name
from ..helpers.entity_helpers import format_entity_name
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class AnalyticsSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control analytics on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: dict[str, Any],
    ) -> None:
        """Initialize the analytics switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense.analyticsEnabled",
        )
        self._attr_name = format_entity_name(
            format_device_name(device_data, coordinator.config_entry.options),
            "Analytics",
        )
        self._attr_icon = "mdi:chart-bar"
