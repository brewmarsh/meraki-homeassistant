"""Switch entities for controlling Meraki camera settings."""

import logging
from typing import Any, Dict

from ..core.api.client import MerakiAPIClient
from ..core.coordinators import MerakiDataCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class RTSPStreamSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the RTSP server on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the RTSP switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "rtsp_stream_enabled",
            "video_settings.externalRtspEnabled",
        )
        self._attr_name = "RTSP Stream"


class AnalyticsSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control analytics on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the analytics switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense.analyticsEnabled",
        )
        self._attr_name = "Analytics"
