"""Tests for the Meraki camera entity's stream control."""

from __future__ import annotations

import dataclasses
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
            dataclasses.replace(
                MOCK_DEVICE,
                product_type="camera",
                model="MV12",
                video_settings={"rtspServerEnabled": False},
                lan_ip="192.168.1.100",
            ),
        ],
    }
    coordinator.async_update_listeners = MagicMock()
    coordinator.register_pending_update = MagicMock()
    coordinator.async_request_refresh = AsyncMock()
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
    # 1. Check that the API call was made
    mock_camera_service.async_set_rtsp_stream_enabled.assert_awaited_once_with(
        device_data.serial,
        True,
    )

    # 2. Check that a refresh was requested
    mock_coordinator.async_request_refresh.assert_called_once()


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
    # The device is a dataclass; modify its internal dicts for the test.
    # Modify the dicts inside rather than replacing the object.
    device_data.video_settings["rtspServerEnabled"] = True
    device_data.video_settings["rtspUrl"] = "rtsp://192.168.1.100:9000/live"

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
    # 1. Check that the API call was made
    mock_camera_service.async_set_rtsp_stream_enabled.assert_awaited_once_with(
        device_data.serial,
        False,
    )

    # 2. Check that a refresh was requested
    mock_coordinator.async_request_refresh.assert_called_once()
