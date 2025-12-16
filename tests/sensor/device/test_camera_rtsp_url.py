"""Tests for the Meraki camera RTSP URL sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.camera_settings import (
    MerakiCameraRTSPUrlSensor,
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
                'video_settings': {
                    'externalRtspEnabled': True,
                    'rtspUrl': 'rtsp://...',
                },
            },
            {
                'serial': 'cam2',
                'name': 'Camera 2',
                'model': 'MV22',
                'productType': 'camera',
                'video_settings': {
                    'externalRtspEnabled': False,
                    'rtspUrl': None,
                },
            },
        ]
    }
    return coordinator

def test_camera_rtsp_url_sensor(mock_device_coordinator):
    """Test the camera RTSP URL sensor."""
    device1 = mock_device_coordinator.data['devices'][0]
    device2 = mock_device_coordinator.data['devices'][1]

    sensor1 = MerakiCameraRTSPUrlSensor(mock_device_coordinator, device1)
    assert sensor1.unique_id == 'cam1_rtsp_url'
    assert sensor1.name == 'Camera RTSP URL'
    assert sensor1.state == 'rtsp://...'

    sensor2 = MerakiCameraRTSPUrlSensor(mock_device_coordinator, device2)
    assert sensor2.unique_id == 'cam2_rtsp_url'
    assert sensor2.name == 'Camera 2 RTSP URL'
    assert sensor2.state == 'disabled'
