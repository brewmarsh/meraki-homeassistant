
from unittest.mock import MagicMock

from custom_components.meraki_ha.camera import MerakiCamera


async def test_camera_rtsp_enabled_via_fallback(mock_coordinator, mock_config_entry):
    """Test RTSP enabled via fallback when flag is False but LAN IP is present."""
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

    # Should be enabled now because of LAN IP fallback
    assert attrs["stream_status"] == "Enabled"
    assert attrs["rtsp_url"] == "rtsp://192.168.1.100:9000/live"
    assert camera.is_streaming is True

    # Verify no status message added
    mock_coordinator.add_status_message.assert_not_called()

async def test_camera_rtsp_disabled_when_no_ip(mock_coordinator, mock_config_entry):
    """Test RTSP disabled message shown when flag is False and no IP available."""
    device_data = {
        "serial": "Q234-ABCD-CAM2",
        "name": "Test Camera 2",
        "model": "MV33",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": None, # No IP
        "status": "online",
        "video_settings": {
            "rtspServerEnabled": False,
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

    assert attrs["stream_status"] == "Disabled in Meraki Dashboard"
    mock_coordinator.add_status_message.assert_called_with(
        "Q234-ABCD-CAM2", "RTSP stream is disabled in the Meraki dashboard."
    )
