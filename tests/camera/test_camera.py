"""Tests for the Meraki camera entity."""

from __future__ import annotations

import dataclasses
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_CAMERA_DEVICE


@pytest.fixture
def mock_camera(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> MerakiCamera:
    """Fixture for a mocked MerakiCamera."""
    # Ensure the camera device is available in the coordinator data
    if "devices" in mock_coordinator.data:
        # Check if already present to avoid duplicates
        if not any(
            d.serial == MOCK_CAMERA_DEVICE.serial for d in mock_coordinator.data["devices"]
        ):
            mock_coordinator.data["devices"].append(MOCK_CAMERA_DEVICE)

    # Mock get_device to return the camera device when requested
    def get_device_side_effect(serial: str):
        if serial == MOCK_CAMERA_DEVICE.serial:
            return MOCK_CAMERA_DEVICE
        return None

    mock_coordinator.get_device.side_effect = get_device_side_effect

    return MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        MOCK_CAMERA_DEVICE,
        mock_camera_service,
    )


@pytest.mark.asyncio
async def test_camera_stream_source(mock_camera: MerakiCamera) -> None:
    """
    Test the camera stream source relies on coordinator data.

    Args:
    ----
        mock_camera: The mocked camera.

    """
    # Act
    source = await mock_camera.stream_source()

    # Assert
    assert source == "rtsp://1.2.3.4:9000/live"


@pytest.mark.asyncio
async def test_camera_turn_on(
    hass: HomeAssistant,
    mock_camera: MerakiCamera,
    mock_coordinator: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test turning the camera stream on.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_camera: The mocked camera.
        mock_coordinator: The mocked coordinator.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    mock_camera.hass = hass
    mock_camera.entity_id = "camera.test_camera"

    # Act
    await mock_camera.async_turn_on()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE.serial,
        True,
    )
    mock_coordinator.register_pending_update.assert_called_once_with(
        mock_camera.unique_id
    )


@pytest.mark.asyncio
async def test_camera_turn_off(
    hass: HomeAssistant,
    mock_camera: MerakiCamera,
    mock_coordinator: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test turning the camera stream off.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_camera: The mocked camera.
        mock_coordinator: The mocked coordinator.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    mock_camera.hass = hass
    mock_camera.entity_id = "camera.test_camera"

    # Act
    await mock_camera.async_turn_off()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE.serial,
        False,
    )
    mock_coordinator.register_pending_update.assert_called_once_with(
        mock_camera.unique_id
    )


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
    mock_device_data = dataclasses.replace(
        MOCK_CAMERA_DEVICE,
        video_settings=video_settings,
        # Ensure lanIp is None for this test to isolate rtspUrl logic
        lan_ip=None,
        rtsp_url=video_settings.get("rtspUrl"),
    )
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
    mock_camera: MerakiCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test the camera image fetching.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_camera: The mocked camera.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    mock_camera.hass = hass

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
        image = await mock_camera.async_camera_image()

        # Assert
        assert image == b"image_bytes"
        mock_camera_service.generate_snapshot.assert_called_once_with(
            MOCK_CAMERA_DEVICE.serial,
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
    mock_device_no_url = dataclasses.replace(
        MOCK_CAMERA_DEVICE,
        video_settings={
            "rtspServerEnabled": True,
            "rtspUrl": None,
        },
        lan_ip=None,
    )

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
