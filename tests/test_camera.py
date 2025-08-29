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
    # Set the coordinator's data attribute to contain our mock device
    coordinator.data = {"devices": [MOCK_CAMERA_DEVICE]}
    # Mock the async_request_refresh method so it can be awaited
    coordinator.async_request_refresh = AsyncMock()
    # Mock async_write_ha_state
    coordinator.async_write_ha_state = MagicMock()
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


@pytest.mark.parametrize(
    "video_settings, rtsp_url, expected_is_streaming",
    [
        ({"rtspServerEnabled": True}, "rtsp://test.com/stream", True),
        ({"rtspServerEnabled": False}, "rtsp://test.com/stream", False),
        ({"rtspServerEnabled": True}, None, False),
        ({"rtspServerEnabled": True}, "http://test.com/stream", False),
        ({}, "rtsp://test.com/stream", False),
    ],
)
def test_is_streaming_logic(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    video_settings,
    rtsp_url,
    expected_is_streaming,
):
    """Test the logic of the is_streaming property."""
    # Arrange
    mock_device_data = {
        **MOCK_CAMERA_DEVICE,
        "video_settings": video_settings,
        "rtsp_url": rtsp_url,
    }
    # The entity is initialized with this data, so we pass it directly
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        mock_device_data,
        mock_camera_service,
    )

    # Act & Assert
    assert camera.is_streaming == expected_is_streaming


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


def test_coordinator_update(mock_coordinator, mock_config_entry, mock_camera_service):
    """Test that the entity state updates when the coordinator data changes."""
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )
    # The initial state should be streaming
    assert camera.is_streaming is True

    # Act
    # Simulate a coordinator update with new data where the stream is disabled
    updated_device_data = {
        **MOCK_CAMERA_DEVICE,
        "video_settings": {"rtspServerEnabled": False},
    }
    mock_coordinator.data = {"devices": [updated_device_data]}
    camera._handle_coordinator_update()

    # Assert
    # The camera's internal state should now reflect the new data
    assert camera.is_streaming is False
    # Check that async_write_ha_state was called to notify HA of the change
    camera.async_write_ha_state.assert_called_once()
