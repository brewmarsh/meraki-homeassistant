"""Tests for the Meraki camera snapshot error handling."""

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
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


@pytest.mark.asyncio
async def test_camera_image_api_error(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that camera image returns None and logs warning on API error."""
    mock_camera.hass = hass

    # Mock generate_snapshot to raise an APIError (simulating Meraki 500)
    mock_camera_service.generate_snapshot.side_effect = Exception(
        "Meraki API Error 500"
    )

    with patch("custom_components.meraki_ha.camera._LOGGER") as mock_logger:
        image = await mock_camera.async_camera_image()

        assert image is None
        mock_logger.warning.assert_called_once()
        assert "Failed to fetch camera snapshot" in mock_logger.warning.call_args[0][0]


@pytest.mark.asyncio
async def test_camera_image_download_error(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that camera image returns None and logs warning on download error."""
    mock_camera.hass = hass
    mock_camera_service.generate_snapshot.return_value = (
        "https://meraki.com/snapshot.jpg"
    )

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession",
    ) as mock_session:
        # Mock session.get to raise a ClientError
        mock_session.return_value.get.side_effect = aiohttp.ClientError(
            "Download failed"
        )

        with patch("custom_components.meraki_ha.camera._LOGGER") as mock_logger:
            image = await mock_camera.async_camera_image()

            assert image is None
            mock_logger.warning.assert_called_once()
            assert (
                "Failed to fetch camera snapshot" in mock_logger.warning.call_args[0][0]
            )
