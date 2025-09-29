"""Switch entities for controlling Meraki Camera profiles."""

import logging
from typing import Any, Dict
from homeassistant.config_entries import ConfigEntry

from homeassistant.helpers.entity import EntityDescription

from ..core.api.client import MerakiAPIClient
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the MV Sense (Computer Vision) state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Camera Sense switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense_settings.sense_enabled",
            config_entry,
        )
        self.entity_description = EntityDescription(
            key="sense_enabled", name="MV Sense"
        )

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        return self.entity_description.name


class MerakiCameraAudioDetectionSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the Audio Detection state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Camera Audio Detection switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "audio_detection",
            "video_settings.audio_detection.enabled",
            config_entry,
        )
        self.entity_description = EntityDescription(
            key="audio_detection", name="Audio Detection"
        )

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        return self.entity_description.name
