"""Tests for the Meraki camera entity."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_DEVICE

# A mock camera device with all the data the entity expects
MOCK_CAMERA_DEVICE = {
    **MOCK_DEVICE,
    "productType": "camera",
    "model": "MV12",
    "video_settings": {
        "rtspServerEnabled": True,
        "rtspUrl": "rtsp://test.com/stream",
    },
}


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
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
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {"rtsp_stream_enabled": True}
    return entry


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.generate_snapshot = AsyncMock(return_value="http://test.com/snapshot.jpg")
    return service


@pytest.mark.asyncio
async def test_camera_stream_source(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test the camera stream source relies on coordinator data.

    Args:
    ----
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
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
    assert source == "rtsp://1.2.3.4:9000/live"


@pytest.mark.asyncio
async def test_camera_turn_on(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test turning the camera stream on.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )
    camera.hass = hass
    camera.entity_id = "camera.test_camera"

    # Act
    await camera.async_turn_on()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE["serial"],
        True,
    )
    mock_coordinator.register_pending_update.assert_called_once_with(camera.unique_id)


@pytest.mark.asyncio
async def test_camera_turn_off(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test turning the camera stream off.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )
    camera.hass = hass
    camera.entity_id = "camera.test_camera"

    # Act
    await camera.async_turn_off()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE["serial"],
        False,
    )
    mock_coordinator.register_pending_update.assert_called_once_with(camera.unique_id)


@pytest.mark.parametrize(
    ("video_settings", "expected_is_streaming"),
    [
        ({"rtspServerEnabled": True, "rtspUrl": "rtsp://test.com/stream"}, True),
        ({"rtspServerEnabled": False, "rtspUrl": "rtsp://test.com/stream"}, False),
        ({"rtspServerEnabled": True, "rtspUrl": None}, False),
        ({"rtspServerEnabled": True, "rtspUrl": "http://test.com/stream"}, False),
        ({"rtspUrl": "rtsp://test.com/stream"}, False),
    ],
)
def test_is_streaming_logic(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    video_settings: dict,
    expected_is_streaming: bool,
) -> None:
    """
    Test the logic of the is_streaming property.

    Args:
    ----
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.
        video_settings: The video settings to test.
        expected_is_streaming: The expected result.

    """
    # Arrange
    mock_device_data = {
        **MOCK_CAMERA_DEVICE,
        "video_settings": video_settings,
        # Ensure lanIp is None for this test to isolate rtspUrl logic
        "lanIp": None,
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
async def test_camera_image(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test the camera image fetching.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )
    camera.hass = hass

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession",
    ) as mock_session:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"image_bytes"
        # mock raise_for_status to not raise
        mock_response.raise_for_status = MagicMock()
        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )

        # Act
        image = await camera.async_camera_image()

        # Assert
        assert image == b"image_bytes"
        mock_camera_service.generate_snapshot.assert_called_once_with(
            MOCK_CAMERA_DEVICE["serial"],
        )


def test_entity_disabled_if_no_url(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test that the camera entity is disabled if no stream URL is available.

    Args:
    ----
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    # Create a mock device with no way to determine a stream URL
    mock_device_no_url = {
        **MOCK_CAMERA_DEVICE,
        "video_settings": {
            "rtspServerEnabled": True,
            "rtspUrl": None,
        },
        "lanIp": None,
    }

    # Act
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        mock_device_no_url,
        mock_camera_service,
    )

    # Assert
    assert not camera.entity_registry_enabled_default
    assert camera.extra_state_attributes["disabled_reason"] is not None
