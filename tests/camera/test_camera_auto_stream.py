"""Tests for the Meraki RTSP stream camera auto-enablement."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.camera import MerakiRTSPStreamCamera
from custom_components.meraki_ha.const_conf import CONF_ENABLE_CAMERA_ENTITIES
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


@pytest.mark.asyncio
async def test_camera_auto_enables_stream(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that the camera auto-enables RTSP stream when missing."""
    # Arrange
    mock_camera.hass = hass
    # Set device data to have no RTSP URL
    # We need to make sure the property returns this
    from unittest.mock import PropertyMock

    with patch.object(
        MerakiRTSPStreamCamera, "device_data", new_callable=PropertyMock
    ) as mock_device_data:
        # Create a copy with None rtsp_url
        import dataclasses

        device_no_rtsp = dataclasses.replace(MOCK_CAMERA_DEVICE, rtsp_url=None)
        mock_device_data.return_value = device_no_rtsp

        # Enable camera entities option
        mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: True}

        # Act
        await mock_camera.async_added_to_hass()

        # Assert
        mock_camera_service.async_set_rtsp_stream_enabled.assert_awaited_once_with(
            MOCK_CAMERA_DEVICE.serial, True
        )


@pytest.mark.asyncio
async def test_camera_does_not_auto_enable_if_already_streaming(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that the camera does not auto-enable if RTSP URL is already present."""
    # Arrange
    mock_camera.hass = hass
    # device_data already has rtsp_url from MOCK_CAMERA_DEVICE
    mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: True}

    # Act
    await mock_camera.async_added_to_hass()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_not_called()


@pytest.mark.asyncio
async def test_camera_does_not_auto_enable_if_option_disabled(
    hass: HomeAssistant,
    mock_camera: MerakiRTSPStreamCamera,
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """Test that the camera does not auto-enable if option is disabled."""
    # Arrange
    mock_camera.hass = hass
    # Set device data to have no RTSP URL
    from unittest.mock import PropertyMock

    with patch.object(
        MerakiRTSPStreamCamera, "device_data", new_callable=PropertyMock
    ) as mock_device_data:
        import dataclasses

        device_no_rtsp = dataclasses.replace(MOCK_CAMERA_DEVICE, rtsp_url=None)
        mock_device_data.return_value = device_no_rtsp

        # Disable camera entities option
        mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: False}

        # Act
        await mock_camera.async_added_to_hass()

        # Assert
        mock_camera_service.async_set_rtsp_stream_enabled.assert_not_called()
