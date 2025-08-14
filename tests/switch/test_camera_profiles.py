"""Tests for the Meraki camera profile switches."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.meraki_ha.switch.camera_profiles import (
    MerakiCameraSenseSwitch,
    MerakiCameraAudioDetectionSwitch,
)


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "cam1",
                "name": "Camera",
                "model": "MV12",
                "productType": "camera",
                "sense": {"senseEnabled": True},
                "audioDetection": {"enabled": True},
            }
        ]
    }
    return coordinator


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.camera = MagicMock()
    client.camera.update_camera_sense_settings = AsyncMock()
    client.camera.update_camera_video_settings = AsyncMock()
    return client


async def test_camera_sense_switch(mock_device_coordinator, mock_api_client):
    """Test the camera sense switch."""
    device = mock_device_coordinator.data["devices"][0]

    switch = MerakiCameraSenseSwitch(mock_device_coordinator, mock_api_client, device)

    assert switch.unique_id == "cam1_sense_enabled"
    assert switch.name == "MV Sense"
    assert switch.is_on is True

    await switch.async_turn_off()
    mock_api_client.camera.update_camera_sense_settings.assert_called_once_with(
        serial="cam1", senseEnabled=False
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()

    mock_api_client.camera.update_camera_sense_settings.reset_mock()
    mock_device_coordinator.async_request_refresh.reset_mock()

    # Simulate the coordinator updating the state
    mock_device_coordinator.data["devices"][0]["sense"]["senseEnabled"] = False
    assert switch.is_on is False

    await switch.async_turn_on()
    mock_api_client.camera.update_camera_sense_settings.assert_called_once_with(
        serial="cam1", senseEnabled=True
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()


async def test_camera_audio_detection_switch(mock_device_coordinator, mock_api_client):
    """Test the camera audio detection switch."""
    device = mock_device_coordinator.data["devices"][0]

    switch = MerakiCameraAudioDetectionSwitch(
        mock_device_coordinator, mock_api_client, device
    )

    assert switch.unique_id == "cam1_audio_detection"
    assert switch.name == "Audio Detection"
    assert switch.is_on is True

    await switch.async_turn_off()
    mock_api_client.camera.update_camera_video_settings.assert_called_once_with(
        serial="cam1", audioDetection={"enabled": False}
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()

    mock_api_client.camera.update_camera_video_settings.reset_mock()
    mock_device_coordinator.async_request_refresh.reset_mock()

    # Simulate the coordinator updating the state
    mock_device_coordinator.data["devices"][0]["audioDetection"]["enabled"] = False
    assert switch.is_on is False

    await switch.async_turn_on()
    mock_api_client.camera.update_camera_video_settings.assert_called_once_with(
        serial="cam1", audioDetection={"enabled": True}
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()
