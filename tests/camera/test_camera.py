"""Tests for the Meraki camera entity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import MerakiCamera

from ..const import MOCK_CONFIG_ENTRY


@pytest.fixture
def mock_coordinator():
    """Mock MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.get_device.return_value = {
        "serial": "Q234-ABCD-5678",
        "model": "MV12",
        "lanIp": "1.2.3.4",
        "status": "online",
        "video_settings": {"rtspServerEnabled": True},
        "rtsp_url": "rtsp://1.2.3.4:9000/live",
    }
    return coordinator


@pytest.fixture
def mock_camera_service():
    """Mock CameraService."""
    return AsyncMock()


@pytest.fixture
def camera_entity(mock_coordinator, mock_camera_service):
    """Fixture for a MerakiCamera entity."""
    camera = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=MOCK_CONFIG_ENTRY,
        device={"serial": "Q234-ABCD-5678"},
        camera_service=mock_camera_service,
    )
    camera.hass = MagicMock(spec=HomeAssistant)
    camera.hass.components = MagicMock()
    camera.entity_id = "camera.meraki_camera"
    return camera


async def test_webrtc_offer_stream_component_not_running(camera_entity: MerakiCamera):
    """Test WebRTC offer when the stream component is not running."""
    camera_entity.hass.components.get.return_value = None

    result = await camera_entity.async_handle_async_webrtc_offer(
        "test_offer", "test_peer"
    )

    assert result is None


async def test_webrtc_offer_no_stream_source(camera_entity: MerakiCamera):
    """Test WebRTC offer when the camera has no stream source."""
    with patch.object(
        camera_entity, "stream_source", new_callable=AsyncMock
    ) as mock_stream_source:
        mock_stream_source.return_value = None
        result = await camera_entity.async_handle_async_webrtc_offer(
            "test_offer", "test_peer"
        )

        assert result is None


async def test_webrtc_offer_success(camera_entity: MerakiCamera):
    """Test a successful WebRTC offer."""
    mock_stream = AsyncMock()
    mock_stream.async_handle_webrtc_offer.return_value = "test_answer"
    camera_entity.hass.components.stream = mock_stream
    with patch.object(
        camera_entity, "stream_source", new_callable=AsyncMock
    ) as mock_stream_source:
        mock_stream_source.return_value = "rtsp://stream.source"
        result = await camera_entity.async_handle_async_webrtc_offer(
            "test_offer", "test_peer"
        )

        assert result == "test_answer"
        mock_stream.async_handle_webrtc_offer.assert_called_once_with(
            camera_entity.entity_id, "test_offer", "test_peer", "rtsp://stream.source"
        )


async def test_webrtc_offer_exception(camera_entity: MerakiCamera, caplog):
    """Test WebRTC offer when an exception is raised."""
    mock_stream = AsyncMock()
    mock_stream.async_handle_webrtc_offer.side_effect = Exception("Test Error")
    camera_entity.hass.components.stream = mock_stream

    with patch.object(
        camera_entity, "stream_source", new_callable=AsyncMock
    ) as mock_stream_source:
        mock_stream_source.return_value = "rtsp://stream.source"
        result = await camera_entity.async_handle_async_webrtc_offer(
            "test_offer", "test_peer"
        )

        assert result is None
        assert "Error handling WebRTC offer" in caplog.text
