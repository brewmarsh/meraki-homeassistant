"""Tests for the Meraki camera RTSP URL sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.rtsp_url import MerakiRtspUrlSensor


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "cam1",
                "name": "Camera",
                "model": "MV12",
                "productType": "camera",
                "lanIp": "192.168.1.100",
                "video_settings": {
                    "rtspServerEnabled": True,
                },
            },
            {
                "serial": "cam2",
                "name": "Camera 2",
                "model": "MV22",
                "productType": "camera",
                "lanIp": "192.168.1.101",
                "video_settings": {
                    "rtspServerEnabled": False,
                },
            },
        ]
    }
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


def test_camera_rtsp_url_sensor(mock_coordinator, mock_config_entry):
    """Test the camera RTSP URL sensor."""
    device1 = mock_coordinator.data["devices"][0]
    device2 = mock_coordinator.data["devices"][1]

    sensor1 = MerakiRtspUrlSensor(mock_coordinator, device1, mock_config_entry)
    assert sensor1.unique_id == "cam1-rtsp-url"

    sensor2 = MerakiRtspUrlSensor(mock_coordinator, device2, mock_config_entry)
    assert sensor2.unique_id == "cam2-rtsp-url"
