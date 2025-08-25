"""Tests for the Meraki camera RTSP URL sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.camera_rtsp_url import (
    MerakiCameraRTSPUrlSensor,
)

from custom_components.meraki_ha.core.coordinators.meraki_data_coordinator import (
    MerakiDataCoordinator,
)


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock(spec=MerakiDataCoordinator)
    device1_data = {
        "serial": "cam1",
        "name": "Camera",
        "model": "MV12",
        "productType": "camera",
        "video_settings": {
            "externalRtspEnabled": True,
            "rtspUrl": "rtsp://...",
        },
    }
    device2_data = {
        "serial": "cam2",
        "name": "Camera 2",
        "model": "MV22",
        "productType": "camera",
        "video_settings": {
            "externalRtspEnabled": False,
            "rtspUrl": None,
        },
    }
    device3_data = {
        "serial": "cam3",
        "name": "Camera 3",
        "model": "MV12",
        "productType": "camera",
        "video_settings": {
            "externalRtspEnabled": True,
            "rtspUrl": None,
        },
    }

    def get_device(serial):
        if serial == "cam1":
            return device1_data
        if serial == "cam2":
            return device2_data
        if serial == "cam3":
            return device3_data
        return None

    coordinator.get_device = MagicMock(side_effect=get_device)
    coordinator.last_update_success = True
    return coordinator


def test_camera_rtsp_url_sensor(mock_device_coordinator):
    """Test the camera RTSP URL sensor."""
    device1 = {"serial": "cam1", "name": "Camera"}
    device2 = {"serial": "cam2", "name": "Camera 2"}
    device3 = {"serial": "cam3", "name": "Camera 3"}

    sensor1 = MerakiCameraRTSPUrlSensor(mock_device_coordinator, device1)
    sensor1._update_state()
    assert sensor1.unique_id == "cam1_rtsp_url"
    assert sensor1.name == "Camera RTSP Stream URL"
    assert sensor1.native_value == "rtsp://.../live"

    sensor2 = MerakiCameraRTSPUrlSensor(mock_device_coordinator, device2)
    sensor2._update_state()
    assert sensor2.unique_id == "cam2_rtsp_url"
    assert sensor2.name == "Camera 2 RTSP Stream URL"
    assert sensor2.native_value is None

    sensor3 = MerakiCameraRTSPUrlSensor(mock_device_coordinator, device3)
    sensor3._update_state()
    assert sensor3.unique_id == "cam3_rtsp_url"
    assert sensor3.name == "Camera 3 RTSP Stream URL"
    assert sensor3.native_value is None
