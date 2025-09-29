"""Tests for the Meraki camera control switch entities."""

from unittest.mock import MagicMock, AsyncMock
import pytest

from custom_components.meraki_ha.switch.camera_controls import RTSPStreamSwitch
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
    coordinator.data = {"devices": [MOCK_CAMERA_DEVICE]}
    coordinator.is_pending = MagicMock(return_value=False)
    coordinator.register_pending_update = MagicMock()
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
    service.async_set_rtsp_stream_enabled = AsyncMock()
    return service

def _setup_switch(hass, mock_coordinator, mock_camera_service, mock_config_entry, device_data):
    """Helper to set up a switch entity for testing."""
    switch = RTSPStreamSwitch(
        mock_coordinator, mock_camera_service, device_data, mock_config_entry
    )
    switch.hass = hass
    switch.entity_id = "switch.test_rtsp_switch"
    switch.async_write_ha_state = MagicMock()
    return switch

def test_rtsp_switch_state(hass, mock_coordinator, mock_camera_service, mock_config_entry):
    """Test the state of the RTSP switch is correctly derived from the coordinator."""
    # Arrange: Initial state is 'on'
    switch = _setup_switch(hass, mock_coordinator, mock_camera_service, mock_config_entry, MOCK_CAMERA_DEVICE)

    # Act
    switch._handle_coordinator_update()

    # Assert
    assert switch.is_on is True

    # Arrange: Change coordinator data to reflect 'off' state
    off_device = MOCK_CAMERA_DEVICE.copy()
    off_device["video_settings"] = {"rtspServerEnabled": False}
    mock_coordinator.data = {"devices": [off_device]}

    # Act
    switch._handle_coordinator_update()

    # Assert
    assert switch.is_on is False

@pytest.mark.asyncio
async def test_rtsp_switch_turn_on(hass, mock_coordinator, mock_camera_service, mock_config_entry):
    """Test turning on the RTSP switch follows the optimistic pattern."""
    # Arrange
    switch = _setup_switch(hass, mock_coordinator, mock_camera_service, mock_config_entry, MOCK_CAMERA_DEVICE)

    # Act
    await switch.async_turn_on()

    # Assert
    assert switch.is_on is True
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(MOCK_CAMERA_DEVICE["serial"], True)
    mock_coordinator.register_pending_update.assert_called_once_with(switch.unique_id)

@pytest.mark.asyncio
async def test_rtsp_switch_turn_off(hass, mock_coordinator, mock_camera_service, mock_config_entry):
    """Test turning off the RTSP switch follows the optimistic pattern."""
    # Arrange
    switch = _setup_switch(hass, mock_coordinator, mock_camera_service, mock_config_entry, MOCK_CAMERA_DEVICE)

    # Act
    await switch.async_turn_off()

    # Assert
    assert switch.is_on is False
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(MOCK_CAMERA_DEVICE["serial"], False)
    mock_coordinator.register_pending_update.assert_called_once_with(switch.unique_id)