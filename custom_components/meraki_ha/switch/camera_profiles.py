"""Switch entities for controlling Meraki Camera profiles."""

import logging
from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityDescription

from ..const import DOMAIN
from ..core.api.client import MerakiAPIClient
from ..core.coordinators.device import MerakiDeviceCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the MV Sense (Computer Vision) state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Camera Sense switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "senseEnabled",
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
        coordinator: MerakiDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Camera Audio Detection switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "audio_detection",
            "audioDetection.enabled",
        )
        self.entity_description = EntityDescription(
            key="audio_detection", name="Audio Detection"
        )

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        return self.entity_description.name
