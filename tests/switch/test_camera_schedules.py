"""Tests for the Meraki camera schedule switches."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.meraki_ha.switch.camera_schedules import MerakiCameraRTSPSwitch


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
                "video_settings": {
                    "externalRtspEnabled": True,
                },
            }
        ]
    }
    return coordinator


from custom_components.meraki_ha.core.api.client import MerakiAPIClient


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock(spec=MerakiAPIClient)
    client.camera = MagicMock()
    client.camera.update_camera_video_settings = AsyncMock(
        return_value={"externalRtspEnabled": False}
    )
    return client


async def test_camera_rtsp_switch(mock_device_coordinator, mock_api_client):
    """Test the camera RTSP switch."""
    device = mock_device_coordinator.data["devices"][0]

    switch = MerakiCameraRTSPSwitch(mock_device_coordinator, mock_api_client, device)

    assert switch.unique_id == "cam1_rtsp_server_enabled"
    assert switch.name == "RTSP Server"
    assert switch.is_on is True

    await switch.async_turn_off()
    mock_api_client.camera.update_camera_video_settings.assert_called_with(
        serial="cam1", externalRtspEnabled=False
    )

    await switch.async_turn_on()
    mock_api_client.camera.update_camera_video_settings.assert_called_with(
        serial="cam1", externalRtspEnabled=True
    )
