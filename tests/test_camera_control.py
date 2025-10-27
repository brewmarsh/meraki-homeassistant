"""Tests for the Meraki camera entity's stream control."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    # The coordinator's data is a dictionary that the entity will access
    coordinator.data = {
        "devices": [
            {
                **MOCK_DEVICE,
                "productType": "camera",
                "model": "MV12",
                "video_settings": {"rtspServerEnabled": False},
                "lanIp": "192.168.1.100",
            },
        ],
    }
    coordinator.async_update_listeners = MagicMock()
    coordinator.register_pending_update = MagicMock()
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_camera_turn_on_optimistic_update(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test that turning on the camera optimistically updates the coordinator.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    device_data = mock_coordinator.data["devices"][0]
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        device_data,
        mock_camera_service,
    )
    camera.hass = hass
    camera.entity_id = "camera.test_camera"

    # Act
    await camera.async_turn_on()

    # Assert
    # 1. Check that the coordinator's data was optimistically updated
    assert device_data["video_settings"]["rtspServerEnabled"]
    assert "rtspUrl" in device_data["video_settings"]
    assert device_data["video_settings"]["rtspUrl"] == "rtsp://192.168.1.100:9000/live"

    # 2. Check that listeners were notified of the change
    mock_coordinator.async_update_listeners.assert_called_once()

    # 3. Check that the API call was made
    mock_camera_service.async_set_rtsp_stream_enabled.assert_awaited_once_with(
        device_data["serial"],
        True,
    )

    # 4. Check that a cooldown was registered
    mock_coordinator.register_pending_update.assert_called_once_with(camera.unique_id)


@pytest.mark.asyncio
async def test_camera_turn_off_optimistic_update(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test that turning off the camera optimistically updates the coordinator.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    # Start with the camera on
    device_data = mock_coordinator.data["devices"][0]
    device_data["video_settings"]["rtspServerEnabled"] = True
    device_data["video_settings"]["rtspUrl"] = "rtsp://192.168.1.100:9000/live"

    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        device_data,
        mock_camera_service,
    )
    camera.hass = hass
    camera.entity_id = "camera.test_camera"

    # Act
    await camera.async_turn_off()

    # Assert
    # 1. Check that the coordinator's data was optimistically updated
    assert not device_data["video_settings"]["rtspServerEnabled"]
    assert device_data["video_settings"]["rtspUrl"] is None

    # 2. Check that listeners were notified
    mock_coordinator.async_update_listeners.assert_called_once()

    # 3. Check that the API call was made
    mock_camera_service.async_set_rtsp_stream_enabled.assert_awaited_once_with(
        device_data["serial"],
        False,
    )

    # 4. Check that a cooldown was registered
    mock_coordinator.register_pending_update.assert_called_once_with(camera.unique_id)
