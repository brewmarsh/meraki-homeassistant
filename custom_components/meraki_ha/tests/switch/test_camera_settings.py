"""Tests for Meraki camera settings switches."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.switch.camera_settings import (
    MerakiCameraSenseSwitch,
    MerakiCameraAudioDetectionSwitch,
)
from custom_components.meraki_ha.coordinators import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.meraki_api import MerakiAPIClient, MerakiApiError

# Mock device data
MOCK_CAMERA_DEVICE_SERIAL = "Q234-BCDE-5679"
MOCK_CAMERA_DEVICE_INFO_BASE = {
    "serial": MOCK_CAMERA_DEVICE_SERIAL,
    "name": "Test Switch Camera",
    "model": "MV22",
    "productType": "camera",
    "mac": "00:11:22:33:44:66",
}

from datetime import timedelta # Added for coordinator scan_interval

# Data as if returned by get_camera_sense_settings and placed in coordinator
MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON = {
    **MOCK_CAMERA_DEVICE_INFO_BASE,
    "name": "Cam Switch SOn AOn",
    "senseEnabled": True,
    "audioDetection": {"enabled": True},
}

MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF = {
    **MOCK_CAMERA_DEVICE_INFO_BASE,
    "name": "Cam Switch SOff AOff",
    "senseEnabled": False,
    "audioDetection": {"enabled": False},
}

# For availability tests
MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING = {
    **MOCK_CAMERA_DEVICE_INFO_BASE, "name": "CamSenseKeyMissing", "audioDetection": {"enabled": True}
}
if "senseEnabled" in MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING: del MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING["senseEnabled"]

MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING = {
    **MOCK_CAMERA_DEVICE_INFO_BASE, "name": "CamAudioKeyMissing", "senseEnabled": True
}
if "audioDetection" in MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING: del MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING["audioDetection"]

MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NOT_DICT = {
    **MOCK_CAMERA_DEVICE_INFO_BASE, "name": "CamAudioNotDict", "senseEnabled": True, "audioDetection": "not_a_dict"
}

MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED = {
    **MOCK_CAMERA_DEVICE_INFO_BASE, "name": "CamAudioNoEnabled", "senseEnabled": True, "audioDetection": {"other_key": True}
}


@pytest.fixture
def mock_meraki_api_client_switch_fixture():
    """Fixture for a mock MerakiAPIClient for switch tests."""
    client = MagicMock(spec=MerakiAPIClient)
    client.get_camera_sense_settings = AsyncMock(return_value={"senseEnabled": True, "audioDetection": {"enabled": True}})
    client.update_camera_sense_settings = AsyncMock(return_value={})
    return client

@pytest.fixture
def mock_coordinator_switch_fixture(mock_meraki_api_client_switch_fixture: MagicMock):
    """Fixture for a mock MerakiDataUpdateCoordinator for switches."""
    coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
    coordinator.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    coordinator.last_update_success = True
    return coordinator


async def setup_switch_entity(
    coordinator: MerakiDataUpdateCoordinator,
    api_client: MerakiAPIClient, switch_class, device_info: dict
):
    """Helper to setup a switch entity."""
    switch = switch_class(coordinator, api_client, device_info)
    switch.entity_id = f"switch.test_{switch.unique_id.lower()}"
    return switch

# --- MerakiCameraSenseSwitch Tests ---

async def test_sense_switch_creation_and_properties(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch creation and basic properties for SenseSwitch."""
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_sense_enabled_switch"
    assert switch.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert switch.available is True # Based on default coordinator data


async def test_sense_switch_initial_state_on(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test SenseSwitch initial state when sense is ON."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is True

async def test_sense_switch_initial_state_off(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test SenseSwitch initial state when sense is OFF."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is False


async def test_sense_switch_turn_on(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning ON the SenseSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is False

    await switch.async_turn_on()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, sense_enabled=True
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is True


async def test_sense_switch_turn_off(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning OFF the SenseSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is True

    await switch.async_turn_off()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, sense_enabled=False
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is False


async def test_sense_switch_update_from_coordinator(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test SenseSwitch state updates from coordinator."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is True

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    switch._handle_coordinator_update()
    assert switch.is_on is False
    assert switch.name == f"{MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF['name']} MV Sense"


async def test_sense_switch_api_error_on_update(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test API error during SenseSwitch update."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is False

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.side_effect = MerakiApiError("API Update Failed")

    await switch.async_turn_on()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, sense_enabled=True
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is True

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    switch._handle_coordinator_update()
    assert switch.is_on is False


# --- MerakiCameraAudioDetectionSwitch Tests ---

async def test_audio_switch_creation_and_properties(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch creation and basic properties for AudioDetectionSwitch."""
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_audio_detection_switch"
    assert switch.name == f"{device_data['name']} Audio Detection"
    assert switch.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert switch.available is True


async def test_audio_switch_initial_state_on(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test AudioDetectionSwitch initial state when audio is ON."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is True


async def test_audio_switch_initial_state_off(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test AudioDetectionSwitch initial state when audio is OFF."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is False


async def test_audio_switch_turn_on(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning ON the AudioDetectionSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is False

    await switch.async_turn_on()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, audio_detection_enabled=True
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is True


async def test_audio_switch_turn_off(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning OFF the AudioDetectionSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is True

    await switch.async_turn_off()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, audio_detection_enabled=False
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is False


async def test_switch_availability_and_specific_keys(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch availability based on general coordinator status and specific data keys."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    sense_switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    audio_switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert sense_switch.available is True
    assert audio_switch.available is True

    mock_coordinator_switch_fixture.last_update_success = False
    sense_switch._handle_coordinator_update()
    audio_switch._handle_coordinator_update()
    assert sense_switch.available is False
    assert audio_switch.available is False
    mock_coordinator_switch_fixture.last_update_success = True

    mock_coordinator_switch_fixture.data = {"devices": []}
    sense_switch._handle_coordinator_update()
    audio_switch._handle_coordinator_update()
    assert sense_switch.available is False
    assert audio_switch.available is False

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING]}
    sense_switch_key_missing = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING
    )
    assert sense_switch_key_missing.available is False

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING]}
    audio_switch_key_missing = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING
    )
    assert audio_switch_key_missing.available is False

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NOT_DICT]}
    audio_switch_not_dict = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NOT_DICT
    )
    assert audio_switch_not_dict.available is False

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED]}
    audio_switch_no_enabled_key = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED
    )
    assert audio_switch_no_enabled_key.available is False


async def test_switch_handles_unexpected_coord_data(mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch handling of unexpected or missing data for state calculation."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_CAMERA_DEVICE_INFO_BASE]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]

    sense_switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert sense_switch.is_on is False

    audio_switch = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert audio_switch.is_on is False

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED]}
    device_data_malformed_audio = mock_coordinator_switch_fixture.data["devices"][0]
    audio_switch_malformed = await setup_switch_entity(
        mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data_malformed_audio
    )
    assert audio_switch_malformed.is_on is False
