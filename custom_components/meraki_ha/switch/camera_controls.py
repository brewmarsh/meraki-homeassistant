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


class RTSPStreamSwitch(MerakiCameraSettingSwitchBase):
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
            "rtsp_stream_enabled",
            "video_settings.rtspServerEnabled",
            config_entry,
        )
        self._attr_name = format_entity_name(
            format_device_name(device_data, config_entry.options),
            "RTSP Stream",
        )
        self._attr_icon = "mdi:cctv"

        # Set availability based on model
        model = device_data.get("model", "")
        if model.startswith("MV2"):
            self._attr_available = False

    async def _async_update_setting(self, is_on: bool) -> None:
        """Update the RTSP setting via the Meraki API."""
        try:
            await self.client.camera.update_camera_video_settings(
                serial=self._device_data["serial"], externalRtspEnabled=is_on
            )
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to update RTSP setting for %s: %s",
                self._device_data["serial"],
                e,
            )


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