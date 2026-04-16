"""Tests for the Meraki RTSP stream camera entity."""

import dataclasses
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.camera import MerakiRTSPStreamCamera
from homeassistant.core import HomeAssistant
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


async def test_camera_properties(mock_camera, mock_camera_service):
    """Test the properties of the camera entity."""
    assert mock_camera.name is None
    assert (
        mock_camera.unique_id == f"{MOCK_CAMERA_DEVICE.serial}_merakirtspstreamcamera"
    )
    assert mock_camera.is_streaming is True

    # Test stream_source calls the service
    mock_camera_service.get_video_stream_url.return_value = "rtsp://test_service_url"
    assert await mock_camera.stream_source() == "rtsp://test_service_url"
    mock_camera_service.get_video_stream_url.assert_called_once_with(
        MOCK_CAMERA_DEVICE.serial
    )


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


async def test_camera_image_throttling(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that camera image fetching is throttled."""
    mock_camera.hass = hass
    mock_camera._last_image = b"cached_image"
    mock_camera._last_image_time = time.time() - 10.0  # 10 seconds ago

    image = await mock_camera.async_camera_image()

    assert image == b"cached_image"
    mock_camera_service.generate_snapshot.assert_not_called()


async def test_camera_image_error(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test handling of errors during camera image fetching."""
    mock_camera.hass = hass
    mock_camera._last_image = b"cached_image"
    mock_camera_service.generate_snapshot.side_effect = Exception("API Error")

    image = await mock_camera.async_camera_image()

    assert image == b"cached_image"  # Returns cached image on error


async def test_camera_stream_source_error(
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test handling of errors during stream source fetching."""
    mock_camera_service.get_video_stream_url.side_effect = Exception("API Error")

    assert await mock_camera.stream_source() is None


async def test_camera_turn_on_off(
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
    mock_coordinator: MagicMock,
) -> None:
    """Test turning the camera stream on and off."""
    await mock_camera.async_turn_on()
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_with(
        MOCK_CAMERA_DEVICE.serial, True
    )
    mock_coordinator.async_request_refresh.assert_called_once()

    await mock_camera.async_turn_off()
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_with(
        MOCK_CAMERA_DEVICE.serial, False
    )


async def test_camera_is_streaming(
    mock_camera: MerakiRTSPStreamCamera,
    mock_coordinator: MagicMock,
) -> None:
    """Test the is_streaming property."""
    # Has RTSP URL
    assert mock_camera.is_streaming is True

    # No RTSP URL
    device_no_rtsp = dataclasses.replace(MOCK_CAMERA_DEVICE, rtsp_url=None)
    mock_coordinator.get_device.return_value = device_no_rtsp
    assert mock_camera.is_streaming is False


async def test_camera_extra_state_attributes(mock_camera):
    """Test the extra state attributes."""
    assert mock_camera.extra_state_attributes == {
        "rtsp_url": MOCK_CAMERA_DEVICE.rtsp_url
    }


async def test_async_enable_rtsp(
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test enabling RTSP in the background."""
    mock_camera_service.get_video_stream_url.return_value = "rtsp://new_url"

    await mock_camera._async_enable_rtsp()

    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_with(
        MOCK_CAMERA_DEVICE.serial, True
    )
    assert MOCK_CAMERA_DEVICE.rtsp_url == "rtsp://new_url"


async def test_async_setup_entry(
    hass: HomeAssistant,
    mock_config_entry: MagicMock,
    mock_coordinator: MagicMock,
) -> None:
    """Test setting up camera entities."""
    from custom_components.meraki_ha.camera import async_setup_entry
    from custom_components.meraki_ha.const.integration import DOMAIN

    mock_camera_service = AsyncMock()
    mock_camera_coordinator = MagicMock()
    mock_camera_coordinator.devices_by_serial = {
        MOCK_CAMERA_DEVICE.serial: MOCK_CAMERA_DEVICE
    }

    hass.data[DOMAIN] = {
        mock_config_entry.entry_id: {
            "camera_coordinator": mock_camera_coordinator,
            "camera_service": mock_camera_service,
        }
    }

    async_add_entities = MagicMock()

    await async_setup_entry(hass, mock_config_entry, async_add_entities)

    async_add_entities.assert_called_once()
    entities = async_add_entities.call_args[0][0]
    assert len(entities) == 1
    assert isinstance(entities[0], MerakiRTSPStreamCamera)
