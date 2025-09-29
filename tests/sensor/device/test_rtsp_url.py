"""Tests for the Meraki RTSP URL sensor entity."""

from unittest.mock import MagicMock
import pytest

from custom_components.meraki_ha.sensor.device.rtsp_url import MerakiRtspUrlSensor
from tests.const import MOCK_DEVICE

# A mock camera device with all the data the entity expects
MOCK_CAMERA_DEVICE = {
    **MOCK_DEVICE,
    "productType": "camera",
    "model": "MV12",
    "lanIp": "192.168.1.100",
    "video_settings": {
        "rtspServerEnabled": True,
        "rtspUrl": "rtsp://cloud.meraki.com/stream",
    },
}

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {"devices": [MOCK_CAMERA_DEVICE]}
    return coordinator

@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry

def _setup_sensor(hass, mock_coordinator, mock_config_entry, device_data):
    """Helper to set up a sensor entity for testing."""
    sensor = MerakiRtspUrlSensor(
        mock_coordinator, device_data, mock_config_entry
    )
    sensor.hass = hass
    sensor.entity_id = "sensor.test_rtsp_url"
    sensor.async_write_ha_state = MagicMock()
    return sensor

def test_rtsp_url_sensor_state_enabled(hass, mock_coordinator, mock_config_entry):
    """Test the RTSP URL sensor state when the stream is enabled."""
    # Arrange
    sensor = _setup_sensor(hass, mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE)

    # Act
    sensor._handle_coordinator_update()

    # Assert
    assert sensor.native_value == "rtsp://192.168.1.100/"

def test_rtsp_url_sensor_state_disabled(hass, mock_coordinator, mock_config_entry):
    """Test the RTSP URL sensor state when the stream is disabled."""
    # Arrange
    disabled_device = MOCK_CAMERA_DEVICE.copy()
    disabled_device["video_settings"] = {"rtspServerEnabled": False}
    mock_coordinator.data = {"devices": [disabled_device]}
    sensor = _setup_sensor(hass, mock_coordinator, mock_config_entry, disabled_device)

    # Act
    sensor._handle_coordinator_update()

    # Assert
    assert sensor.native_value == "Disabled"

def test_rtsp_url_sensor_fallback_to_cloud(hass, mock_coordinator, mock_config_entry):
    """Test the sensor falls back to the cloud URL when LAN IP is unavailable."""
    # Arrange
    no_lan_ip_device = MOCK_CAMERA_DEVICE.copy()
    no_lan_ip_device["lanIp"] = None
    mock_coordinator.data = {"devices": [no_lan_ip_device]}
    sensor = _setup_sensor(hass, mock_coordinator, mock_config_entry, no_lan_ip_device)

    # Act
    sensor._handle_coordinator_update()

    # Assert
    assert sensor.native_value == "rtsp://cloud.meraki.com/stream"

def test_rtsp_url_sensor_unavailable(hass, mock_coordinator, mock_config_entry):
    """Test the sensor state when no valid URL is available."""
    # Arrange
    no_url_device = MOCK_CAMERA_DEVICE.copy()
    no_url_device["lanIp"] = None
    no_url_device["video_settings"] = {"rtspServerEnabled": True, "rtspUrl": None}
    mock_coordinator.data = {"devices": [no_url_device]}
    sensor = _setup_sensor(hass, mock_coordinator, mock_config_entry, no_url_device)

    # Act
    sensor._handle_coordinator_update()

    # Assert
    assert sensor.native_value == "Not available"