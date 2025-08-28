"""Tests for the Meraki camera entity."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_DEVICE

# A mock camera device with all the data the entity expects
MOCK_CAMERA_DEVICE = {
    **MOCK_DEVICE,
    "productType": "camera",
    "model": "MV12",
    "video_settings": {"rtspServerEnabled": True},
    "rtsp_url": "rtsp://test.com/stream",
}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    # Configure get_device to return our mock camera data
    coordinator.get_device.return_value = MOCK_CAMERA_DEVICE
    # Mock the async_request_refresh method so it can be awaited
    coordinator.async_request_refresh = AsyncMock()
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
    service.generate_snapshot = AsyncMock(return_value="http://test.com/snapshot.jpg")
    return service


@pytest.mark.asyncio
async def test_camera_stream_source(
    mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test the camera stream source relies on coordinator data."""
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )

    # Act
    source = await camera.stream_source()

    # Assert
    assert source == "rtsp://test.com/stream"
    # Ensure get_device was called to fetch the state
    mock_coordinator.get_device.assert_called_with(MOCK_CAMERA_DEVICE["serial"])


@pytest.mark.asyncio
async def test_camera_turn_on(mock_coordinator, mock_config_entry, mock_camera_service):
    """Test turning the camera stream on."""
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )

    # Act
    await camera.async_turn_on()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE["serial"], True
    )
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_camera_turn_off(mock_coordinator, mock_config_entry, mock_camera_service):
    """Test turning the camera stream off."""
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )

    # Act
    await camera.async_turn_off()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE["serial"], False
    )
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_camera_image(mock_coordinator, mock_config_entry, mock_camera_service):
    """Test the camera image fetching."""
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession"
    ) as mock_session:
        mock_response = AsyncMock()
        mock_response.read.return_value = b"image_bytes"
        # mock raise_for_status to not raise
        mock_response.raise_for_status = MagicMock()
        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )
        camera.hass = MagicMock()

        # Act
        image = await camera.async_camera_image()

        # Assert
        assert image == b"image_bytes"
        mock_camera_service.generate_snapshot.assert_called_once_with(
            MOCK_CAMERA_DEVICE["serial"]
        )
