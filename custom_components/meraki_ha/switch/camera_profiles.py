"""Switch entities for controlling Meraki Camera profiles."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.helpers.typing import UNDEFINED

<<<<<<< HEAD
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
=======
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
>>>>>>> origin/beta

from ..core.api.client import MerakiAPIClient
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the MV Sense (Computer Vision) state of a Meraki Camera."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> origin/beta
        meraki_client: MerakiAPIClient,
        device_data: dict[str, Any],
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
        if self.entity_description.name is UNDEFINED:
            return ""
        return self.entity_description.name or ""

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
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> origin/beta
        meraki_client: MerakiAPIClient,
        device_data: dict[str, Any],
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
        if self.entity_description.name is UNDEFINED:
            return ""
        return self.entity_description.name or ""

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
