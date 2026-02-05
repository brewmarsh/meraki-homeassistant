"""Tests for the Meraki RTSP stream camera entity."""

import dataclasses
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import MerakiRTSPStreamCamera
from tests.const import MOCK_CAMERA_DEVICE


@pytest.fixture
def mock_camera(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> MerakiRTSPStreamCamera:
    """Create a mock MerakiRTSPStreamCamera entity."""
    mock_coordinator.get_device.return_value = MOCK_CAMERA_DEVICE
    return MerakiRTSPStreamCamera(
        coordinator=mock_coordinator,
        device=MOCK_CAMERA_DEVICE,
        camera_service=mock_camera_service,
        config_entry=mock_config_entry,
    )


async def test_camera_properties(mock_camera):
    """Test the properties of the camera entity."""
    assert mock_camera.name == "Stream"
    assert mock_camera.unique_id == f"{MOCK_CAMERA_DEVICE.serial}_camera"
    assert mock_camera.is_streaming is True
    assert await mock_camera.stream_source() == MOCK_CAMERA_DEVICE.rtsp_url


@pytest.mark.asyncio
async def test_camera_image(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test the camera image fetching."""
    mock_camera.hass = hass

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession",
    ) as mock_session:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"image_bytes"
        mock_response.raise_for_status = MagicMock()
        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )

        image = await mock_camera.async_camera_image()

        assert image == b"image_bytes"
        mock_camera_service.generate_snapshot.assert_called_once_with(
            MOCK_CAMERA_DEVICE.serial,
        )


async def test_camera_image_offline(
    mock_camera: MerakiRTSPStreamCamera,
    mock_coordinator: MagicMock,
) -> None:
    """Test that camera image returns None when offline."""
    offline_device = dataclasses.replace(MOCK_CAMERA_DEVICE, status="offline")
    mock_coordinator.get_device.return_value = offline_device

    image = await mock_camera.async_camera_image()

    assert image is None
