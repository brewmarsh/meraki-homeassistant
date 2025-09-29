"""Switch entities for controlling Meraki camera schedules."""

import logging
from typing import Any, Dict
from homeassistant.config_entries import ConfigEntry

from ..core.api.client import MerakiAPIClient
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase
from ..core.utils.naming_utils import format_device_name
from ..helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiCameraRTSPSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the RTSP server on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the RTSP switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "rtsp_server_enabled",
            "video_settings.externalRtspEnabled",
            config_entry,
        )
        self._attr_name = format_entity_name(
            format_device_name(device_data, config_entry.options), "RTSP Server"
        )
