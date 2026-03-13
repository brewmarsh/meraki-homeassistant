"""Tests for the Meraki camera serial guards and error handling."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.camera import MerakiRTSPStreamCamera
from custom_components.meraki_ha.core.models.device import MerakiDevice
from homeassistant.components.camera import CameraEntityFeature
from homeassistant.core import HomeAssistant


@pytest.fixture
def mock_camera(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> MerakiRTSPStreamCamera:
    """Create a mock MerakiRTSPStreamCamera entity."""
    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Test Device",
        mac="00:11:22:33:44:55",
        model="MV12",
        network_id="N_12345",
        product_type="camera",
        lan_ip="1.2.3.4",
        status="online",
    )

    mock_coordinator.get_device.return_value = device

    return MerakiRTSPStreamCamera(
        coordinator=mock_coordinator,
        device=device,
        camera_service=mock_camera_service,
        config_entry=mock_config_entry,
    )


@pytest.mark.asyncio
async def test_camera_supported_features(
    mock_camera: MerakiRTSPStreamCamera,
) -> None:
    """Test that camera supports the STREAM feature."""
    assert mock_camera.supported_features == CameraEntityFeature.STREAM


@pytest.mark.asyncio
async def test_camera_image_no_serial(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
) -> None:
    """Test that camera image returns None when serial is missing."""
    mock_camera.hass = hass
    # Force _device_serial to None for the test
    mock_camera._device_serial = None

    with patch("custom_components.meraki_ha.camera._LOGGER") as mock_logger:
        image = await mock_camera.async_camera_image()

        assert image is None
        mock_logger.debug.assert_called_with(
            "Cannot fetch snapshot: Camera serial is missing."
        )


@pytest.mark.asyncio
async def test_camera_image_500_error(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that camera image returns None and logs warning on 500 error."""
    mock_camera.hass = hass
    mock_camera_service.generate_snapshot.return_value = (
        "https://meraki.com/snapshot.jpg"
    )

    # Mock the aiohttp response to return a 500 status
    mock_response = MagicMock()
    mock_response.status = 500
    mock_response.read = AsyncMock(return_value=b"Internal Server Error HTML")

    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__ = AsyncMock(return_value=mock_response)
    mock_context_manager.__aexit__ = AsyncMock(return_value=None)

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession"
    ) as mock_session:
        mock_session.return_value.get.return_value = mock_context_manager

        with patch("custom_components.meraki_ha.camera._LOGGER") as mock_logger:
            image = await mock_camera.async_camera_image()

            assert image is None
            mock_logger.warning.assert_called()
            # Verify the warning contains the status code and camera name
            # When using _LOGGER.warning("msg %d", arg), the call args will be ("msg %d", arg)
            warning_call = mock_logger.warning.call_args
            assert "Meraki API returned %d" in warning_call[0][0]
            assert warning_call[0][1] == 500


@pytest.mark.asyncio
async def test_camera_stream_source_no_serial(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
) -> None:
    """Test that stream source returns None when serial is missing."""
    mock_camera.hass = hass
    # Force _device_serial to None for the test
    mock_camera._device_serial = None

    with patch("custom_components.meraki_ha.camera._LOGGER") as mock_logger:
        source = await mock_camera.async_stream_source()

        assert source is None
        mock_logger.debug.assert_called_with(
            "Cannot fetch stream: Camera serial is missing."
        )
