"""Switch entities for controlling Meraki camera schedules."""

import logging
from typing import Any, Dict

from ..core.api.client import MerakiAPIClient
from ..core.coordinators.device import MerakiDeviceCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class MerakiCameraRTSPSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the RTSP server on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the RTSP switch."""
        super().__init__(coordinator, meraki_client, device_data, "rtsp_server_enabled", "video_settings.externalRtspEnabled")
        self._attr_name = "RTSP Server"
