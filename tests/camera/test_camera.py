"""Tests for the Meraki camera entity."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.camera import MerakiCamera


async def test_camera_rtsp_disabled_when_flag_is_false(
    mock_coordinator, mock_config_entry
):
    """Test RTSP disabled when rtspServerEnabled flag is False."""
    device_data = {
        "serial": "Q234-ABCD-CAM1",
        "name": "Test Camera",
        "model": "MV33",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": "192.168.1.100",
        "status": "online",
        "video_settings": {
            "rtspServerEnabled": False,
        },
        "rtsp_url": None,
    }

    # Setup coordinator to return this device
    mock_coordinator.get_device.return_value = device_data
    mock_coordinator.config_entry = mock_config_entry

    camera_service = MagicMock()

    camera = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=device_data,
        camera_service=camera_service,
    )

    # Check extra_state_attributes
    attrs = camera.extra_state_attributes

    # RTSP is disabled because rtspServerEnabled is False
    assert attrs["stream_status"] == "RTSP Disabled in Dashboard"


async def test_camera_rtsp_disabled_when_no_ip(mock_coordinator, mock_config_entry):
    """Test RTSP URL not available when flag is True but no URL."""
    device_data = {
        "serial": "Q234-ABCD-CAM2",
        "name": "Test Camera 2",
        "model": "MV33",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": None,
        "status": "online",
        "video_settings": {
            "rtspServerEnabled": True,
        },
        "rtsp_url": None,
    }

    mock_coordinator.get_device.return_value = device_data
    mock_coordinator.config_entry = mock_config_entry

    camera_service = MagicMock()

    camera = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=device_data,
        camera_service=camera_service,
    )

    # Check extra_state_attributes
    attrs = camera.extra_state_attributes

    # RTSP enabled but URL not available
    assert attrs["stream_status"] == "RTSP URL Not Available"


async def test_camera_rtsp_enabled(mock_coordinator, mock_config_entry):
    """Test RTSP enabled when flag is True and URL is present."""
    device_data = {
        "serial": "Q234-ABCD-CAM3",
        "name": "Test Camera 3",
        "model": "MV33",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": "192.168.1.100",
        "status": "online",
        "video_settings": {
            "rtspServerEnabled": True,
        },
        "rtsp_url": "rtsp://192.168.1.100:9000/live",
    }

    mock_coordinator.get_device.return_value = device_data
    mock_coordinator.config_entry = mock_config_entry

    camera_service = MagicMock()

    camera = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=device_data,
        camera_service=camera_service,
    )

    # Check extra_state_attributes
    attrs = camera.extra_state_attributes

    # RTSP is enabled
    assert attrs["stream_status"] == "RTSP Enabled"
    assert camera.is_streaming is True
