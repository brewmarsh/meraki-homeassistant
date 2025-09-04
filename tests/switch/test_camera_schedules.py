"""Tests for the Meraki camera schedule switches."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.meraki_ha.switch.camera_schedules import MerakiCameraRTSPSwitch
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.coordinators.meraki_data_coordinator import MerakiDataCoordinator


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock(spec=MerakiDataCoordinator)
    coordinator.get_device.return_value = {
        "serial": "cam1",
        "name": "Camera",
        "model": "MV12",
        "productType": "camera",
        "video_settings": {
            "externalRtspEnabled": True,
        },
    }
    coordinator.last_update_success = True
    return coordinator


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock(spec=MerakiAPIClient)
    client.camera = MagicMock()
    client.camera.update_camera_video_settings = AsyncMock(
        return_value={"externalRtspEnabled": False}
    )
    return client


async def test_camera_rtsp_switch(hass, mock_device_coordinator, mock_api_client):
    """Test the camera RTSP switch."""
    device = mock_device_coordinator.get_device.return_value

    switch = MerakiCameraRTSPSwitch(mock_device_coordinator, mock_api_client, device)
    switch.hass = hass
    switch.entity_id = "switch.test"
    switch.async_write_ha_state = AsyncMock()

    assert switch.is_on is True

    await switch.async_turn_off()
    mock_api_client.camera.update_camera_video_settings.assert_called_with(
        serial="cam1", externalRtspEnabled=False
    )

    # Simulate coordinator update
    mock_device_coordinator.get_device.return_value["video_settings"]["externalRtspEnabled"] = False
    await switch._handle_coordinator_update()
    assert switch.is_on is False

    await switch.async_turn_on()
    mock_api_client.camera.update_camera_video_settings.assert_called_with(
        serial="cam1", externalRtspEnabled=True
    )

    # Simulate coordinator update
    mock_device_coordinator.get_device.return_value["video_settings"]["externalRtspEnabled"] = True
    await switch._handle_coordinator_update()
    assert switch.is_on is True
