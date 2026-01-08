"""Switch entities for controlling Meraki Camera profiles."""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.helpers.typing import UNDEFINED

from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator

from ..core.api.client import MerakiAPIClient
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the MV Sense (Computer Vision) state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Mapping[str, Any],
    ) -> None:
        """Initialize the Camera Sense switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense_settings.sense_enabled",
        )
        self.entity_description = SwitchEntityDescription(
            key="sense_enabled", name="MV Sense"
        )

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        if (
            self.entity_description.name is UNDEFINED
            or self.entity_description.name is None
        ):
            return ""
        return str(self.entity_description.name)

    async def _async_update_setting(self, is_on: bool) -> None:
        """Update the setting via the Meraki API.

        Args:
        ----
            is_on: Whether the setting is on or off.
        """
        await self.client.camera.update_camera_sense_settings(
            serial=self._device_data["serial"], senseEnabled=is_on
        )


class MerakiCameraAudioDetectionSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the Audio Detection state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Mapping[str, Any],
    ) -> None:
        """Initialize the Camera Audio Detection switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "audio_detection",
            "video_settings.audio_detection.enabled",
        )
        self.entity_description = SwitchEntityDescription(
            key="audio_detection", name="Audio Detection"
        )

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        if (
            self.entity_description.name is UNDEFINED
            or self.entity_description.name is None
        ):
            return ""
        return str(self.entity_description.name)

    async def _async_update_setting(self, is_on: bool) -> None:
        """Update the setting via the Meraki API.

        Args:
        ----
            is_on: Whether the setting is on or off.
        """
        await self.client.camera.update_camera_sense_settings(
            serial=self._device_data["serial"],
            audioDetection={"enabled": is_on},
        )
