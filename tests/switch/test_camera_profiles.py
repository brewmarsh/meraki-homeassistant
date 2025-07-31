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
        'devices': [
            {
                'serial': 'cam1',
                'name': 'Camera',
                'model': 'MV12',
                'productType': 'camera',
                'sense_settings': {
                    'senseEnabled': True,
                    'audioDetection': {'enabled': True},
                },
            }
        ]
    }
    return coordinator

@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.update_camera_sense_settings = AsyncMock()
    return client

def test_camera_sense_switch(mock_device_coordinator, mock_api_client):
    """Test the camera sense switch."""
    device = mock_device_coordinator.data['devices'][0]

    switch = MerakiCameraSenseSwitch(mock_device_coordinator, mock_api_client, device)
    assert switch.unique_id == 'cam1_sense_enabled_switch'
    assert switch.name == 'MV Sense'
    assert switch.is_on is True

    switch.turn_off()
    mock_api_client.update_camera_sense_settings.assert_called_once_with(
        serial='cam1', sense_enabled=False
    )

def test_camera_audio_detection_switch(mock_device_coordinator, mock_api_client):
    """Test the camera audio detection switch."""
    device = mock_device_coordinator.data['devices'][0]

    switch = MerakiCameraAudioDetectionSwitch(
        mock_device_coordinator, mock_api_client, device
    )
    assert switch.unique_id == 'cam1_audio_detection_switch'
    assert switch.name == 'Audio Detection'
    assert switch.is_on is True

    switch.turn_off()
    mock_api_client.update_camera_sense_settings.assert_called_with(
        serial='cam1', audio_detection_enabled=False
    )
