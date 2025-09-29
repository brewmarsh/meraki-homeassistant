"""Switch entities for controlling Meraki camera settings."""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from ..core.api.client import MerakiAPIClient
from ..coordinator import MerakiDataUpdateCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase
from ..helpers.entity_helpers import format_entity_name
from ..core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class AnalyticsSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control analytics on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the analytics switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense.analyticsEnabled",
            config_entry,
        )
        self._attr_name = format_entity_name(
            format_device_name(device_data, config_entry.options),
            "Analytics",
        )
        self._attr_icon = "mdi:chart-bar"