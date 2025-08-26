"""Tests for the Meraki Camera RTSP URL sensor."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.sensor.device.camera_rtsp_url import (
    MerakiCameraRTSPUrlSensor,
)
from tests.const import MOCK_DEVICE

@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()

def create_coordinator_with_device_data(device_data):
    """Helper to create a mock coordinator with specific device data."""
    coordinator = MagicMock()
    coordinator.get_device.return_value = device_data
    return coordinator

def test_rtsp_sensor_enabled(mock_config_entry):
    """Test the RTSP URL sensor when the stream is enabled."""
    # Arrange
    device = MOCK_DEVICE.copy()
    device["video_settings"] = {
        "externalRtspEnabled": True,
        "rtspUrl": "rtsp://test.url/stream",
    }
    coordinator = create_coordinator_with_device_data(device)

    # Act
    sensor = MerakiCameraRTSPUrlSensor(coordinator, device, mock_config_entry)

    # Assert
    assert sensor.native_value == "rtsp://test.url/stream"

def test_rtsp_sensor_disabled(mock_config_entry):
    """Test the RTSP URL sensor when the stream is disabled."""
    # Arrange
    device = MOCK_DEVICE.copy()
    device["video_settings"] = {
        "externalRtspEnabled": False,
        "rtspUrl": "rtsp://test.url/stream",
    }
    coordinator = create_coordinator_with_device_data(device)

    # Act
    sensor = MerakiCameraRTSPUrlSensor(coordinator, device, mock_config_entry)

    # Assert
    assert sensor.native_value is None

def test_rtsp_sensor_no_video_settings(mock_config_entry):
    """Test the RTSP URL sensor when there are no video settings."""
    # Arrange
    device = MOCK_DEVICE.copy()
    coordinator = create_coordinator_with_device_data(device)

    # Act
    sensor = MerakiCameraRTSPUrlSensor(coordinator, device, mock_config_entry)

    # Assert
    assert sensor.native_value is None
