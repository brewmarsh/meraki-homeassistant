from unittest.mock import MagicMock, AsyncMock, patch
from custom_components.meraki_ha.camera import MerakiCamera

async def test_webrtc_offer_handler():
    """Test the WebRTC offer handler."""
    # Arrange
    device_data = {
        'serial': 'Q234-ABCD-5678',
        'model': 'MV12',
        'name': 'Test Camera',
        'status': 'online',
        'rtsp_url': 'rtsp://fake.url/live',
        'video_settings': {'rtspServerEnabled': True}
    }
    coordinator = MagicMock()
    coordinator.get_device.return_value = device_data
    coordinator.config_entry.options = {}

    config_entry = MagicMock()
    camera_service = AsyncMock()
    camera = MerakiCamera(coordinator, config_entry, device_data, camera_service)
    camera.hass = MagicMock()

    # Act
    with patch('custom_components.meraki_ha.camera.async_handle_webrtc_offer', new_callable=AsyncMock) as mock_webrtc_helper:
        await camera.async_handle_webrtc_offer("test_offer")

    # Assert
    stream_source = await camera.stream_source()
    assert stream_source == 'rtsp://fake.url/live'
    mock_webrtc_helper.assert_called_once_with(camera.hass, "test_offer", stream_source)
