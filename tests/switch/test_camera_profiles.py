"""Tests for the Meraki camera profile switches."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.switch.camera_profiles import (
    MerakiCameraAudioDetectionSwitch,
    MerakiCameraSenseSwitch,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    mock_device_data = MerakiDevice(
        serial="cam1",
        name="Camera",
        model="MV12",
        product_type="camera",
        sense_settings={"sense_enabled": True},
        video_settings={"audio_detection": {"enabled": True}},
    )
    coordinator.data = {"devices": [mock_device_data]}
    coordinator.get_device.return_value = mock_device_data
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.camera = MagicMock()
    client.camera.update_camera_sense_settings = AsyncMock()
    client.camera.update_camera_video_settings = AsyncMock()
    return client


async def test_camera_sense_switch(hass, mock_device_coordinator, mock_api_client):
    """Test the camera sense switch."""
    device = mock_device_coordinator.data["devices"][0]

    switch = MerakiCameraSenseSwitch(mock_device_coordinator, mock_api_client, device)
    switch.hass = hass
    switch.entity_id = "switch.mv_sense"
    switch.async_write_ha_state = MagicMock()

    assert switch.unique_id == "cam1_sense_enabled"
    assert switch.name == "MV Sense"
    assert switch.is_on is True

    await switch.async_turn_off()
    mock_api_client.camera.update_camera_sense_settings.assert_called_once_with(
        serial="cam1", sense_enabled=False
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()

    mock_api_client.camera.update_camera_sense_settings.reset_mock()
    mock_device_coordinator.async_request_refresh.reset_mock()

    # Simulate the coordinator updating the state
    mock_device_coordinator.data["devices"][0].sense_settings["sense_enabled"] = False
    switch._handle_coordinator_update()
    assert switch.is_on is False

    await switch.async_turn_on()
    mock_api_client.camera.update_camera_sense_settings.assert_called_once_with(
        serial="cam1", sense_enabled=True
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()


async def test_camera_audio_detection_switch(
    hass, mock_device_coordinator, mock_api_client
):
    """Test the camera audio detection switch."""
    device = mock_device_coordinator.data["devices"][0]

    switch = MerakiCameraAudioDetectionSwitch(
        mock_device_coordinator, mock_api_client, device
    )
    switch.hass = hass
    switch.entity_id = "switch.audio_detection"
    switch.async_write_ha_state = MagicMock()

    assert switch.unique_id == "cam1_audio_detection"
    assert switch.name == "Audio Detection"
    assert switch.is_on is True

    await switch.async_turn_off()
    mock_api_client.camera.update_camera_video_settings.assert_called_once_with(
        serial="cam1", video_settings={"audio_detection": {"enabled": False}}
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()

    mock_api_client.camera.update_camera_video_settings.reset_mock()
    mock_device_coordinator.async_request_refresh.reset_mock()

    # Simulate the coordinator updating the state
    mock_device_coordinator.data["devices"][0].video_settings["audio_detection"][
        "enabled"
    ] = False
    switch._handle_coordinator_update()
    assert switch.is_on is False

    await switch.async_turn_on()
    mock_api_client.camera.update_camera_video_settings.assert_called_once_with(
        serial="cam1", video_settings={"audio_detection": {"enabled": True}}
    )
    mock_device_coordinator.async_request_refresh.assert_called_once()
