"""Tests for the Meraki camera settings switches."""
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.switch.camera_settings import (
    MerakiCameraSenseSwitch,
    MerakiCameraAudioDetectionSwitch,
    MerakiCameraRTSPSwitch,
)


async def test_meraki_camera_sense_switch(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki camera sense switch."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "senseEnabled": True,
            }
        ]
    }
    meraki_client = MagicMock()
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    switch = MerakiCameraSenseSwitch(
        coordinator, meraki_client, device_data
    )
    switch._update_internal_state()
    assert switch.is_on is True


async def test_meraki_camera_audio_detection_switch(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki camera audio detection switch."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "audioDetection": {"enabled": True},
            }
        ]
    }
    meraki_client = MagicMock()
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    switch = MerakiCameraAudioDetectionSwitch(
        coordinator, meraki_client, device_data
    )
    switch._update_internal_state()
    assert switch.is_on is True


async def test_meraki_camera_rtsp_switch(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki camera RTSP switch."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "externalRtspEnabled": True,
            }
        ]
    }
    meraki_client = MagicMock()
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    switch = MerakiCameraRTSPSwitch(
        coordinator, meraki_client, device_data
    )
    switch._update_internal_state()
    assert switch.is_on is True
