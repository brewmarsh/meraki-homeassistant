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
def mock_meraki_api_client_switch_fixture(): # Renamed to avoid conflict
    """Fixture for a mock MerakiAPIClient for switch tests."""
    client = MagicMock(spec=MerakiAPIClient)
    client.get_camera_sense_settings = AsyncMock(return_value={"senseEnabled": True, "audioDetection": {"enabled": True}})
    client.update_camera_sense_settings = AsyncMock(return_value={})
    return client

@pytest.fixture
def mock_coordinator_switch_fixture(hass: HomeAssistant, mock_meraki_api_client_switch_fixture: MagicMock):
    """Fixture for a mock MerakiDataUpdateCoordinator for switches."""
    coordinator = MerakiDataUpdateCoordinator(
        hass=hass,
        logger=MagicMock(),
        name="test_meraki_switch_coordinator",
        meraki_client=mock_meraki_api_client_switch_fixture,
        org_id="test_org_id_switch"
    )
    coordinator.scan_interval = timedelta(seconds=30)
    coordinator.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]} # Default
    coordinator.last_update_success = True
    return coordinator


async def setup_switch_entity(
    hass: HomeAssistant, coordinator: MerakiDataUpdateCoordinator,
    api_client: MerakiAPIClient, switch_class, device_info: dict
):
    """Helper to setup a switch entity."""
    switch = switch_class(coordinator, api_client, device_info)
    switch.hass = hass
    switch.entity_id = f"switch.test_{switch.unique_id.lower()}" # Lowercase for consistency
    return switch

# --- MerakiCameraSenseSwitch Tests ---

async def test_sense_switch_creation_and_properties(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch creation and basic properties for SenseSwitch."""
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    # Name generation relies on hass.states.async_entity_category_for_device,
    # which is hard to mock here. Unique ID and device info are more critical.
    assert switch.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_sense_enabled_switch"
    assert switch.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert switch.available is True # Based on default coordinator data


async def test_sense_switch_initial_state_on(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test SenseSwitch initial state when sense is ON."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is True

async def test_sense_switch_initial_state_off(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test SenseSwitch initial state when sense is OFF."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is False


async def test_sense_switch_turn_on(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning ON the SenseSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is False

    await switch.async_turn_on()
    await hass.async_block_till_done()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, sense_enabled=True # Corrected: sense_enabled
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is True


async def test_sense_switch_turn_off(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning OFF the SenseSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is True

    await switch.async_turn_off()
    await hass.async_block_till_done()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, sense_enabled=False # Corrected: sense_enabled
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is False


async def test_sense_switch_update_from_coordinator(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test SenseSwitch state updates from coordinator."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is True

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    switch._handle_coordinator_update()
    await hass.async_block_till_done()
    assert switch.is_on is False
    # Switch has an explicit name property: device_name + entity_description.name
    assert switch.name == f"{MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF['name']} MV Sense"


async def test_sense_switch_api_error_on_update(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test API error during SenseSwitch update."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert switch.is_on is False

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.side_effect = MerakiApiError("API Update Failed")

    await switch.async_turn_on()
    await hass.async_block_till_done()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, sense_enabled=True
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is True # Optimistic update

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    switch._handle_coordinator_update()
    await hass.async_block_till_done()
    assert switch.is_on is False


# --- MerakiCameraAudioDetectionSwitch Tests ---

async def test_audio_switch_creation_and_properties(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch creation and basic properties for AudioDetectionSwitch."""
    device_data = mock_coordinator_switch_fixture.data["devices"][0] # Default is SENSE_ON_AUDIO_ON
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_audio_detection_switch"
    # Switch has an explicit name property: device_name + entity_description.name
    assert switch.name == f"{device_data['name']} Audio Detection"
    assert switch.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert switch.available is True


async def test_audio_switch_initial_state_on(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test AudioDetectionSwitch initial state when audio is ON."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is True


async def test_audio_switch_initial_state_off(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test AudioDetectionSwitch initial state when audio is OFF."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is False


async def test_audio_switch_turn_on(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning ON the AudioDetectionSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_OFF_AUDIO_OFF]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is False

    await switch.async_turn_on()
    await hass.async_block_till_done()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, audio_detection_enabled=True # Corrected: audio_detection_enabled
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is True


async def test_audio_switch_turn_off(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test turning OFF the AudioDetectionSwitch."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert switch.is_on is True

    await switch.async_turn_off()
    await hass.async_block_till_done()

    mock_meraki_api_client_switch_fixture.update_camera_sense_settings.assert_called_once_with(
        serial=MOCK_CAMERA_DEVICE_SERIAL, audio_detection_enabled=False # Corrected: audio_detection_enabled
    )
    mock_coordinator_switch_fixture.async_request_refresh.assert_called_once()
    assert switch.is_on is False


async def test_switch_availability_and_specific_keys(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch availability based on general coordinator status and specific data keys."""
    # Default: Sense switch with SENSE_ON_AUDIO_ON data should be available
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator_switch_fixture.data["devices"][0]
    sense_switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    audio_switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert sense_switch.available is True
    assert audio_switch.available is True

    # Coordinator update fails
    mock_coordinator_switch_fixture.last_update_success = False
    sense_switch._handle_coordinator_update()
    audio_switch._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sense_switch.available is False
    assert audio_switch.available is False
    mock_coordinator_switch_fixture.last_update_success = True # Reset for next test

    # Device missing from coordinator
    mock_coordinator_switch_fixture.data = {"devices": []}
    sense_switch._handle_coordinator_update() # This will cause _get_current_device_data to return None
    audio_switch._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sense_switch.available is False
    assert audio_switch.available is False

    # Test Sense switch availability when 'senseEnabled' key is missing
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING]}
    sense_switch_key_missing = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, MOCK_DEVICE_SWITCH_SENSE_KEY_MISSING
    )
    assert sense_switch_key_missing.available is False

    # Test Audio switch availability when 'audioDetection' key is missing entirely
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING]}
    audio_switch_key_missing = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, MOCK_DEVICE_SWITCH_AUDIO_KEY_MISSING
    )
    assert audio_switch_key_missing.available is False

    # Test Audio switch availability when 'audioDetection' is not a dict
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NOT_DICT]}
    audio_switch_not_dict = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NOT_DICT
    )
    assert audio_switch_not_dict.available is False

    # Test Audio switch availability when 'audioDetection.enabled' key is missing
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED]}
    audio_switch_no_enabled_key = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED
    )
    assert audio_switch_no_enabled_key.available is False


async def test_switch_handles_unexpected_coord_data(hass: HomeAssistant, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture):
    """Test switch handling of unexpected or missing data for state calculation."""
    mock_coordinator_switch_fixture.data = {"devices": [MOCK_CAMERA_DEVICE_INFO_BASE]} # Base, no senseEnabled or audioDetection
    device_data = mock_coordinator_switch_fixture.data["devices"][0]

    sense_switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraSenseSwitch, device_data
    )
    assert sense_switch.is_on is False # Defaults to False if key missing

    audio_switch = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data
    )
    assert audio_switch.is_on is False # Defaults to False

    mock_coordinator_switch_fixture.data = {"devices": [MOCK_DEVICE_SWITCH_AUDIO_MALFORMED_NO_ENABLED]}
    device_data_malformed_audio = mock_coordinator_switch_fixture.data["devices"][0]
    audio_switch_malformed = await setup_switch_entity(
        hass, mock_coordinator_switch_fixture, mock_meraki_api_client_switch_fixture, MerakiCameraAudioDetectionSwitch, device_data_malformed_audio
    )
    assert audio_switch_malformed.is_on is False

"""
Note on current switch tests:
The tests assume that the coordinator's data (`coordinator.data['devices']`) will be structured
such that each device entry directly contains `senseEnabled` (boolean) and `audioDetection` (dict with `enabled` boolean)
if those settings are known for the camera. This matches the current implementation of the switches'
`_update_internal_state` which reads these attributes from the device data provided by the coordinator.

The `MerakiCameraSettingSwitchBase`'s `_get_current_device_data` method simply iterates through
`self.coordinator.data["devices"]` to find the matching serial. The tests provide mock coordinator data
that reflects this structure.

If the coordinator were to fetch data from `get_camera_sense_settings` and store it in a *different*
structure within `coordinator.data` (e.g., `coordinator.data['camera_sense_data'][serial]`), then
the switches' `_get_current_device_data` or `_update_internal_state` would need to be adjusted
to look for data in that new location, and these tests would need to be updated accordingly.
The current tests are aligned with the existing switch code.
"""
