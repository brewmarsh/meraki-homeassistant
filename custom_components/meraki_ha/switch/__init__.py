# custom_components/meraki_ha/switch/__init__.py
"""Switch platform for Meraki to control SSID and Camera settings (Ultra-minimal for diagnostics)."""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Comment out other imports if they are specific to the full functionality and might interfere
# For example:
# from .meraki_ssid_device_switch import MerakiSSIDDeviceSwitch # Example
# from .camera_settings import (
#     MerakiCameraSenseSwitch,
#     MerakiCameraAudioDetectionSwitch,
#     MerakiCameraRTSPSwitch,
# )
# from ..const import DOMAIN, DATA_CLIENT, DATA_COORDINATOR, DATA_SSID_DEVICES_COORDINATOR # Example
# from ..meraki_api import MerakiAPIClient # Example
# from ..coordinators import MerakiDataUpdateCoordinator, SSIDDeviceCoordinator # Example

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    _LOGGER.info("switch/__init__.py: Ultra-minimal async_setup_entry FORCED for diagnostics.")
    # All other logic originally in this function (getting coordinators, creating entities, calling async_add_entities)
    # MUST be commented out or removed for this diagnostic step.
    return True

# Ensure any other functions or significant logic in this file are also commented out if they could affect loading.
# __all__ = ["async_setup_entry"] # Keep if standard, or remove if part of the "ultra-minimal" approach
