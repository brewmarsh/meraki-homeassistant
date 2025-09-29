"""Tests for the Meraki camera entity."""

import copy
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_DEVICE

# A mock camera device with all the data the entity expects
MOCK_CAMERA_DEVICE = {
    **MOCK_DEVICE,
    "productType": "camera",
    "model": "MV12",
    "lanIp": "1.2.3.4",
    "video_settings": {
        "rtspServerEnabled": True,
        "rtspUrl": "rtsp://cloud.meraki.com/stream",
    },
}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    # Use deepcopy to ensure each test gets a fresh copy of the data
    coordinator.data = {"devices": [copy.deepcopy(MOCK_CAMERA_DEVICE)]}
    coordinator.async_request_refresh = AsyncMock()
    coordinator.register_pending_update = MagicMock()
    coordinator.is_pending = MagicMock(return_value=False)
    coordinator.async_update_listeners = MagicMock()
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.generate_snapshot = AsyncMock(return_value="http://test.com/snapshot.jpg")
    service.async_set_rtsp_stream_enabled = AsyncMock()
    return service


def _setup_camera(
    hass, mock_coordinator, mock_config_entry, mock_camera_service, device_data
):
    """Helper to set up a camera entity for testing."""
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        device_data,
        mock_camera_service,
    )
    camera.hass = hass
    camera.entity_id = "camera.test_camera"
    # Mock the method that writes state to Home Assistant
    camera.async_write_ha_state = MagicMock()
    return camera


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "device_data_override, expected_url",
    [
        (
            {
                "lanIp": "192.168.1.100",
                "video_settings": {"rtspServerEnabled": True, "rtspUrl": "rtsp://c.com"},
            },
            "rtsp://192.168.1.100/",
        ),
        (
            {
                "lanIp": None,
                "video_settings": {
                    "rtspServerEnabled": True,
                    "rtspUrl": "rtsp://cloud.com/stream",
                },
            },
            "rtsp://cloud.com/stream",
        ),
        (
            {
                "lanIp": None,
                "video_settings": {
                    "rtspServerEnabled": True,
                    "rtspUrl": "http://invalid.com",
                },
            },
            None,
        ),
    ],
)
async def test_rtsp_url_logic(
    hass,
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    device_data_override,
    expected_url,
):
    """Test the RTSP URL selection logic."""
    device = mock_coordinator.data["devices"][0]
    device.update(device_data_override)
    camera = _setup_camera(
        hass,
        mock_coordinator,
        mock_config_entry,
        mock_camera_service,
        device,
    )
    source = await camera.stream_source()
    assert source == expected_url


@pytest.mark.asyncio
async def test_camera_turn_on(
    hass, mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test turning the camera stream on using the optimistic pattern."""
    device = mock_coordinator.data["devices"][0]
    camera = _setup_camera(
        hass, mock_coordinator, mock_config_entry, mock_camera_service, device
    )
    await camera.async_turn_on()
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        device["serial"], True
    )
    assert mock_coordinator.async_update_listeners.called


@pytest.mark.asyncio
async def test_camera_turn_off(
    hass, mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test turning the camera stream off using the optimistic pattern."""
    device = mock_coordinator.data["devices"][0]
    camera = _setup_camera(
        hass, mock_coordinator, mock_config_entry, mock_camera_service, device
    )
    await camera.async_turn_off()
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        device["serial"], False
    )
    assert mock_coordinator.async_update_listeners.called


@pytest.mark.asyncio
async def test_camera_image(
    hass, mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test the camera image fetching."""
    device = mock_coordinator.data["devices"][0]
    camera = _setup_camera(
        hass, mock_coordinator, mock_config_entry, mock_camera_service, device
    )
    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession"
    ) as mock_session:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"image_bytes"
        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )
        image = await camera.async_camera_image()
        assert image == b"image_bytes"
        mock_camera_service.generate_snapshot.assert_called_once_with(
            device["serial"]
        )


def test_coordinator_update(
    hass, mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test that the entity state updates when the coordinator data changes."""
    device = mock_coordinator.data["devices"][0]
    camera = _setup_camera(
        hass, mock_coordinator, mock_config_entry, mock_camera_service, device
    )
    camera._handle_coordinator_update()
    assert camera.is_streaming is True
    assert camera.async_write_ha_state.call_count == 1

    # Now, update the coordinator's data
    mock_coordinator.data["devices"][0]["video_settings"]["rtspServerEnabled"] = False
    camera._handle_coordinator_update()

    assert camera.is_streaming is False
    assert camera.async_write_ha_state.call_count == 2


def test_entity_disabled_for_unsupported_model(
    hass, mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test that the camera entity is disabled by default for unsupported models (MV2)."""
    mock_mv2_device = mock_coordinator.data["devices"][0]
    mock_mv2_device["model"] = "MV2"
    camera = _setup_camera(
        hass, mock_coordinator, mock_config_entry, mock_camera_service, mock_mv2_device
    )
    assert camera.entity_registry_enabled_default is False


def test_entity_enabled_for_supported_model(
    hass, mock_coordinator, mock_config_entry, mock_camera_service
):
    """Test that the camera entity is enabled by default for supported models."""
    device = mock_coordinator.data["devices"][0]
    camera = _setup_camera(
        hass, mock_coordinator, mock_config_entry, mock_camera_service, device
    )
    assert camera.entity_registry_enabled_default is True