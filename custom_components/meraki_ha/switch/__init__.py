# custom_components/meraki_ha/switch/__init__.py
"""Switch platform for Meraki to control SSID and Camera settings."""

import logging
from typing import Optional # Added Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR, # Main coordinator for physical devices
    DATA_SSID_DEVICES_COORDINATOR, # SSID coordinator
)
from ..meraki_api import MerakiAPIClient
from ..coordinators import MerakiDataUpdateCoordinator # Main coordinator type
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

# Import SSID switch classes (original functionality)
from .meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)

# Import Camera switch classes (new functionality)
from .camera_settings import (
    MerakiCameraSenseSwitch,
    MerakiCameraAudioDetectionSwitch,
    MerakiCameraRTSPSwitch,  # Added RTSP Switch
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    # Assume _LOGGER is defined globally in this file.
    _LOGGER.info("switch/__init__.py: Ultra-minimal async_setup_entry called, intentionally doing nothing, returning True for diagnostics.")
    return True


__all__ = ["async_setup_entry"]
