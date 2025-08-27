"""Tests for the Meraki camera entity."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {"rtsp_stream_enabled": True}
    return entry


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_video_stream_url = AsyncMock(return_value="rtsp://test.com/stream")
    service.generate_snapshot = AsyncMock(return_value="http://test.com/snapshot.jpg")
    return service


@pytest.mark.asyncio
async def test_camera_stream_source(
    mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test the camera stream source."""
    # Arrange
    device = MOCK_DEVICE.copy()
    camera = MerakiCamera(
        mock_coordinator, mock_config_entry, device, mock_camera_service
    )

    # Act
    source = await camera.stream_source()

    # Assert
    assert source == "rtsp://test.com/stream"


@pytest.mark.asyncio
async def test_camera_image(mock_coordinator, mock_config_entry, mock_camera_service):
    """Test the camera image."""
    # Arrange
    device = MOCK_DEVICE.copy()
    camera = MerakiCamera(
        mock_coordinator, mock_config_entry, device, mock_camera_service
    )

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession"
    ) as mock_session:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"image_bytes"
        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )
        camera.hass = MagicMock()

        # Act
        image = await camera.async_camera_image()

        # Assert
        assert image == b"image_bytes"
