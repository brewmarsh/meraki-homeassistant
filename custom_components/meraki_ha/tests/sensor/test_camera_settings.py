"""Tests for Meraki camera settings sensors."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.sensor.camera_settings import (
    MerakiCameraSenseStatusSensor,
    MerakiCameraAudioDetectionSensor,
)
from custom_components.meraki_ha.coordinators import MerakiDataUpdateCoordinator

# Mock device data as it would appear in the coordinator for a camera
MOCK_CAMERA_DEVICE_SERIAL = "Q234-ABCD-5678"
MOCK_CAMERA_DEVICE_INFO = {
    "serial": MOCK_CAMERA_DEVICE_SERIAL,
    "name": "Test Camera",
    "model": "MV12",
    "productType": "camera",
    "mac": "00:11:22:33:44:55",
    # These keys are now expected to be populated by DataAggregationCoordinator
    "senseEnabled": True,
    "audioDetection": {"enabled": True}
}

# Variations of device data for testing different states and availability
MOCK_DEVICE_SENSE_ON_AUDIO_ON = {
    **MOCK_CAMERA_DEVICE_INFO,
    "senseEnabled": True,
    "audioDetection": {"enabled": True},
}

MOCK_DEVICE_SENSE_OFF_AUDIO_OFF = {
    **MOCK_CAMERA_DEVICE_INFO,
    "name": "Camera Sense Off", # Different name for clarity in tests
    "senseEnabled": False,
    "audioDetection": {"enabled": False},
}

MOCK_DEVICE_SENSE_MISSING_KEY = { # Missing 'senseEnabled'
    **MOCK_CAMERA_DEVICE_INFO,
    "name": "Camera Sense Key Missing",
    "audioDetection": {"enabled": True},
}
# Remove senseEnabled from this mock, it should not be present
del MOCK_DEVICE_SENSE_MISSING_KEY["senseEnabled"]


MOCK_DEVICE_AUDIO_MISSING_KEY = { # Missing 'audioDetection' entirely
    **MOCK_CAMERA_DEVICE_INFO,
    "name": "Camera Audio Key Missing",
    "senseEnabled": True,
}
del MOCK_DEVICE_AUDIO_MISSING_KEY["audioDetection"]

MOCK_DEVICE_AUDIO_MALFORMED = { # 'audioDetection' is not a dict
    **MOCK_CAMERA_DEVICE_INFO,
    "name": "Camera Audio Malformed",
    "senseEnabled": True,
    "audioDetection": "not_a_dict",
}


@pytest.fixture
def mock_coordinator(hass: HomeAssistant): # Add hass for coordinator if it needs it
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    # Initialize with some default data, tests can override coordinator.data as needed
    coordinator = MerakiDataUpdateCoordinator(
        hass=hass,
        logger=MagicMock(),
        name="test_meraki_coordinator",
        meraki_client=MagicMock(spec=AsyncMock), # Mock the API client
        org_id="test_org_id" # Add org_id
    )
    # Set scan_interval if its absence causes issues, though not directly used by these sensor tests' logic
    coordinator.scan_interval = timedelta(seconds=30) # Example
    coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]} # Default to sense on, audio on
    # coordinator.async_update_listeners = MagicMock() # Already part of DataUpdateCoordinator
    # coordinator.async_add_listener = MagicMock() # Already part of DataUpdateCoordinator
    coordinator.last_update_success = True
    return coordinator


@pytest.fixture
def mock_meraki_api_client():
    """Fixture for a mock MerakiAPIClient."""
    client = MagicMock()
    # The mock_meraki_api_client is not directly used by sensors, but by the coordinator.
    # It's here if we were testing the coordinator's interaction with it.
    # For sensor tests, we primarily care about the data *already in* the coordinator.
    client = MagicMock(spec=AsyncMock)
    return client


async def setup_sensor_entity(
    hass: HomeAssistant, coordinator: MerakiDataUpdateCoordinator, sensor_class, device_info: dict
):
    """Helper to setup a sensor entity."""
    sensor = sensor_class(coordinator, device_info) # device_info is the specific dict for this device
    sensor.hass = hass
    sensor.entity_id = f"sensor.test_{sensor.unique_id.lower()}"

    # Simulate entity being added to HA for full lifecycle, if necessary for some tests
    # await sensor.async_added_to_hass()
    return sensor


# --- MerakiCameraSenseStatusSensor Tests ---

async def test_sense_status_sensor_creation_and_properties(hass: HomeAssistant, mock_coordinator):
    """Test sensor creation and basic properties for SenseStatusSensor."""
    # Coordinator data is defaulted to MOCK_DEVICE_SENSE_ON_AUDIO_ON
    device_data = mock_coordinator.data["devices"][0]
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, device_data
    )

    assert sensor.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_camera_sense_status"
    assert sensor.name == "Sense Enabled" # Should be from EntityDescription
    assert sensor.state_class is None
    assert sensor.options is None
    assert sensor.native_unit_of_measurement is None
    assert sensor.suggested_unit_of_measurement is None
    assert sensor.suggested_display_precision is None # Verify suggested display precision
    assert sensor.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert sensor.available is True # Initial data has senseEnabled


async def test_sense_status_sensor_state_reflects_coordinator_data(hass: HomeAssistant, mock_coordinator):
    """Test sensor state reflects coordinator data for SenseStatusSensor."""
    # Case 1: senseEnabled is True
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]}
    device_data_on = mock_coordinator.data["devices"][0]
    sensor_on = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, device_data_on
    )
    # _update_sensor_data is called in __init__, then _handle_coordinator_update can be called
    # For initial state right after setup:
    assert sensor_on.native_value == "enabled"
    assert sensor_on.icon == "mdi:camera-iris"

    # Case 2: senseEnabled is False
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_OFF_AUDIO_OFF]}
    device_data_off = mock_coordinator.data["devices"][0]
    sensor_off = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, device_data_off
    )
    assert sensor_off.native_value == "disabled"
    assert sensor_off.icon == "mdi:camera-off-outline"

    # Case 3: Update coordinator data and call _handle_coordinator_update
    # Start with sensor_on (senseEnabled: True)
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_OFF_AUDIO_OFF]} # Change data to False
    sensor_on._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor_on.native_value == "disabled"
    assert sensor_on.icon == "mdi:camera-off-outline"
    # The entity's own .name property should remain "Sense Enabled"
    assert sensor_on.name == "Sense Enabled" # Name is from EntityDescription


async def test_sense_status_sensor_availability(hass: HomeAssistant, mock_coordinator):
    """Test sensor availability changes for SenseStatusSensor."""
    # Initial state: Available (senseEnabled is True in MOCK_DEVICE_SENSE_ON_AUDIO_ON)
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator.data["devices"][0]
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, device_data
    )
    assert sensor.available is True

    # Scenario 1: Coordinator update fails
    mock_coordinator.last_update_success = False
    # Data might still be there, but super().available will be False
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available is False

    # Scenario 2: Coordinator successful, but device data missing from coordinator
    mock_coordinator.last_update_success = True
    mock_coordinator.data = {"devices": []}
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available is False

    # Scenario 3: Device data present, but 'senseEnabled' key is missing
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_MISSING_KEY]}
    # Need to re-init or ensure the specific device_data is passed if setup_sensor_entity doesn't re-fetch from coordinator
    device_data_missing_key = mock_coordinator.data["devices"][0]
    sensor_missing_key = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, device_data_missing_key
    )
    # _update_sensor_data and available are called during init
    assert sensor_missing_key.available is False
    assert sensor_missing_key.native_value is None # Reflects missing data
    assert sensor_missing_key.icon == "mdi:camera-question"


# --- MerakiCameraAudioDetectionSensor Tests ---

async def test_audio_sensor_creation_and_properties(hass: HomeAssistant, mock_coordinator):
    """Test sensor creation and basic properties for AudioDetectionSensor."""
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator.data["devices"][0]
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data
    )

    assert sensor.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_camera_audio_detection_status"
    assert sensor.name == "Audio Detection" # Should be from EntityDescription
    assert sensor.state_class is None
    assert sensor.options is None
    assert sensor.native_unit_of_measurement is None
    assert sensor.suggested_unit_of_measurement is None
    assert sensor.suggested_display_precision is None # Verify suggested display precision
    assert sensor.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert sensor.available is True # Initial data has audioDetection.enabled


async def test_audio_sensor_state_reflects_coordinator_data(hass: HomeAssistant, mock_coordinator):
    """Test sensor state reflects coordinator data for AudioDetectionSensor."""
    # Case 1: audioDetection.enabled is True
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]}
    device_data_on = mock_coordinator.data["devices"][0]
    sensor_on = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data_on
    )
    assert sensor_on.native_value == "enabled"
    assert sensor_on.icon == "mdi:microphone"

    # Case 2: audioDetection.enabled is False
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_OFF_AUDIO_OFF]}
    device_data_off = mock_coordinator.data["devices"][0]
    sensor_off = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data_off
    )
    assert sensor_off.native_value == "disabled"
    assert sensor_off.icon == "mdi:microphone-off"

    # Case 3: Update coordinator data and call _handle_coordinator_update
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]} # Back to True
    sensor_off._handle_coordinator_update() # sensor_off was previously False
    await hass.async_block_till_done()
    assert sensor_off.native_value == "enabled"
    assert sensor_off.icon == "mdi:microphone"
    # The entity's own .name property should remain "Audio Detection"
    assert sensor_off.name == "Audio Detection"


async def test_audio_sensor_availability_and_malformed_data(hass: HomeAssistant, mock_coordinator):
    """Test sensor availability for AudioDetectionSensor, including malformed data."""
    mock_coordinator.data = {"devices": [MOCK_DEVICE_SENSE_ON_AUDIO_ON]}
    device_data = mock_coordinator.data["devices"][0]
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data
    )
    assert sensor.available is True

    # Scenario 1: 'audioDetection' key entirely missing
    mock_coordinator.data = {"devices": [MOCK_DEVICE_AUDIO_MISSING_KEY]}
    device_data_key_missing = mock_coordinator.data["devices"][0]
    sensor_key_missing = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data_key_missing
    )
    assert sensor_key_missing.available is False
    assert sensor_key_missing.native_value is None
    assert sensor_key_missing.icon == "mdi:microphone-question"

    # Scenario 2: 'audioDetection' is present but not a dictionary (malformed)
    mock_coordinator.data = {"devices": [MOCK_DEVICE_AUDIO_MALFORMED]}
    device_data_malformed = mock_coordinator.data["devices"][0]
    sensor_malformed = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data_malformed
    )
    assert sensor_malformed.available is False
    assert sensor_malformed.native_value is None
    assert sensor_malformed.icon == "mdi:microphone-question"

    # Scenario 3: 'audioDetection' is a dict, but 'enabled' key is missing
    malformed_audio_no_enabled_key = {**MOCK_CAMERA_DEVICE_INFO, "audioDetection": {"not_enabled_key": True}}
    mock_coordinator.data = {"devices": [malformed_audio_no_enabled_key]}
    device_data_malformed_inner = mock_coordinator.data["devices"][0]
    sensor_malformed_inner = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, device_data_malformed_inner
    )
    assert sensor_malformed_inner.available is False
    assert sensor_malformed_inner.native_value is None
    assert sensor_malformed_inner.icon == "mdi:microphone-question"

# The note about future tests can be removed or updated as the tests now reflect
# that the sensor reads from enriched coordinator data.
# The `mock_meraki_api_client` is not strictly needed for *these specific sensor tests*
# because we are directly manipulating `mock_coordinator.data`.
# It would be used if we were testing the coordinator's own `_async_update_data` method
# where it calls `get_camera_sense_settings`.
# The `test_sensor_api_error_scenario` would also apply to how the *coordinator* handles API errors,
# and how that reflects in `coordinator.last_update_success` or `coordinator.data`, which then
# affects sensor availability. The current availability tests cover `last_update_success = False`
# and missing data in the coordinator.
from datetime import timedelta # Add timedelta to imports at the top
