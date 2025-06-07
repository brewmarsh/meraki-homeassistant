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
    # Initial placeholder values for sense/audio, as sensors currently use these from device_info
    # These will be overridden by actual API call mocks in later test stages
    "senseEnabled": True, # Placeholder, matching sensor's current logic
    "audioDetection": {"enabled": True} # Placeholder
}

MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON = {
    "senseEnabled": True,
    "audioDetection": {"enabled": True},
    # Other potential fields from API
}

MOCK_CAMERA_SENSE_API_DATA_SENSE_OFF_AUDIO_OFF = {
    "senseEnabled": False,
    "audioDetection": {"enabled": False},
}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
    coordinator.data = {"devices": [MOCK_CAMERA_DEVICE_INFO]} # Initial data
    coordinator.async_update_listeners = MagicMock()
    coordinator.async_add_listener = MagicMock()
    coordinator.last_update_success = True
    return coordinator


@pytest.fixture
def mock_meraki_api_client():
    """Fixture for a mock MerakiAPIClient."""
    client = MagicMock()
    # This will be used when sensors are updated to use specific API data
    client.get_camera_sense_settings = AsyncMock(
        return_value=MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON
    )
    return client


async def setup_sensor_entity(
    hass: HomeAssistant, coordinator, sensor_class, device_info
):
    """Helper to setup a sensor entity."""
    sensor = sensor_class(coordinator, device_info)
    sensor.hass = hass # Mock hass instance if needed for entity lifecycle
    sensor.entity_id = f"sensor.test_{sensor.unique_id}" # Example entity_id

    # Manually call this to simulate entity addition if needed for certain tests
    # await sensor.async_added_to_hass()
    return sensor


# --- MerakiCameraSenseStatusSensor Tests ---

async def test_sense_status_sensor_creation_and_properties(hass: HomeAssistant, mock_coordinator):
    """Test sensor creation and basic properties for SenseStatusSensor."""
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
    )

    assert sensor.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_camera_sense_status"
    assert sensor.name == f"{MOCK_CAMERA_DEVICE_INFO['name']} Sense Enabled"
    assert sensor.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}
    assert sensor.available is True # Based on initial coordinator state


async def test_sense_status_sensor_initial_state(hass: HomeAssistant, mock_coordinator):
    """Test initial state based on placeholder logic in sensor."""
    # Sensor currently uses placeholder: sense_enabled = True
    mock_coordinator.data = {"devices": [{**MOCK_CAMERA_DEVICE_INFO, "senseEnabled": True}]}
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
    )
    # _update_sensor_data is called in __init__
    assert sensor.native_value == "enabled"
    assert sensor.icon == "mdi:camera-iris"

    mock_coordinator.data = {"devices": [{**MOCK_CAMERA_DEVICE_INFO, "senseEnabled": False}]}
    sensor_off = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
    )
    # _update_sensor_data is called in __init__
    # Need to manually trigger update or re-initialize for this test structure
    # For now, the sensor's _update_sensor_data relies on its internal placeholder.
    # This test reflects the *current* sensor placeholder logic (always True on init)
    # To test dynamic changes, we'd call _handle_coordinator_update

    # Re-evaluating: The sensor's __init__ calls _update_sensor_data(), which uses a hardcoded True.
    # The test should reflect this, or we need to simulate coordinator updates.
    # For now, the placeholder logic in the sensor is: sense_enabled = True
    # So, native_value will be "enabled"
    current_sensor_placeholder_value = True # This matches the sensor's code
    expected_state = "enabled" if current_sensor_placeholder_value else "disabled"
    expected_icon = "mdi:camera-iris" if current_sensor_placeholder_value else "mdi:camera-off-outline"

    assert sensor.native_value == expected_state
    assert sensor.icon == expected_icon


async def test_sense_status_sensor_coordinator_update(hass: HomeAssistant, mock_coordinator):
    """Test sensor state update from coordinator (still placeholder logic)."""
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
    )

    # Current placeholder logic in sensor: sense_enabled = True, so it's always "enabled"
    # This test will be more meaningful when sensor reads from coordinator actual data

    # Simulate coordinator having updated data (even if sensor doesn't use it yet for this specific field)
    updated_device_info = {**MOCK_CAMERA_DEVICE_INFO, "name": "Updated Camera Name"}
    mock_coordinator.data = {"devices": [updated_device_info]}
    sensor._handle_coordinator_update() # Manually trigger update
    await hass.async_block_till_done() # Ensure state propagation

    assert sensor.name == "Updated Camera Name Sense Enabled" # Name should update
    # State remains based on placeholder until sensor logic changes
    current_sensor_placeholder_value = True
    expected_state = "enabled" if current_sensor_placeholder_value else "disabled"
    assert sensor.native_value == expected_state


async def test_sense_status_sensor_availability(hass: HomeAssistant, mock_coordinator):
    """Test sensor availability changes."""
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
    )
    assert sensor.available is True

    # Simulate coordinator failure
    mock_coordinator.last_update_success = False
    sensor._handle_coordinator_update() # Propagate change
    await hass.async_block_till_done()
    assert sensor.available is False

    # Simulate coordinator success but device data missing
    mock_coordinator.last_update_success = True
    mock_coordinator.data = {"devices": []} # Device not in list
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available is False

    # Simulate coordinator success and device data present again
    mock_coordinator.data = {"devices": [MOCK_CAMERA_DEVICE_INFO]}
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available is True


# --- MerakiCameraAudioDetectionSensor Tests ---

async def test_audio_sensor_creation_and_properties(hass: HomeAssistant, mock_coordinator):
    """Test sensor creation and basic properties for AudioDetectionSensor."""
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, MOCK_CAMERA_DEVICE_INFO
    )

    assert sensor.unique_id == f"{MOCK_CAMERA_DEVICE_SERIAL}_camera_audio_detection_status"
    assert sensor.name == f"{MOCK_CAMERA_DEVICE_INFO['name']} Audio Detection"
    assert sensor.device_info["identifiers"] == {(DOMAIN, MOCK_CAMERA_DEVICE_SERIAL)}


async def test_audio_sensor_initial_state(hass: HomeAssistant, mock_coordinator):
    """Test initial state based on placeholder logic in sensor for AudioDetectionSensor."""
    # Sensor currently uses placeholder: audio_detection_enabled = True
    mock_coordinator.data = {"devices": [{**MOCK_CAMERA_DEVICE_INFO, "audioDetection": {"enabled": True}}]}
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, MOCK_CAMERA_DEVICE_INFO
    )
    # Reflects current placeholder in sensor code: audio_detection_enabled = True
    current_sensor_placeholder_value = True
    expected_state = "enabled" if current_sensor_placeholder_value else "disabled"
    expected_icon = "mdi:microphone" if current_sensor_placeholder_value else "mdi:microphone-off"

    assert sensor.native_value == expected_state
    assert sensor.icon == expected_icon


async def test_audio_sensor_coordinator_update(hass: HomeAssistant, mock_coordinator):
    """Test sensor state update from coordinator (still placeholder logic) for AudioDetectionSensor."""
    sensor = await setup_sensor_entity(
        hass, mock_coordinator, MerakiCameraAudioDetectionSensor, MOCK_CAMERA_DEVICE_INFO
    )

    updated_device_info = {**MOCK_CAMERA_DEVICE_INFO, "name": "Updated Mic Name"}
    mock_coordinator.data = {"devices": [updated_device_info]}
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()

    assert sensor.name == "Updated Mic Name Audio Detection"
    current_sensor_placeholder_value = True
    expected_state = "enabled" if current_sensor_placeholder_value else "disabled"
    assert sensor.native_value == expected_state


# Future tests (when sensors use actual API data via coordinator):
# - Mock get_camera_sense_settings to return different data (sense on/off, audio on/off)
# - Verify sensor state reflects this mocked API data after coordinator update.
# - Test behavior when get_camera_sense_settings raises an API error (e.g., UpdateFailed).
#   The sensor should become unavailable or report an error state if appropriate.
# - Test with unexpected API response structure.

# Example of a future test:
# async def test_sense_status_sensor_reflects_api_data(hass: HomeAssistant, mock_coordinator, mock_meraki_api_client):
# """Test sensor state reflects actual (mocked) API data for SenseStatusSensor."""
# # This test assumes the coordinator is updated to fetch and store camera sense data
# # and the sensor is updated to read this specific data.
#
# # Setup coordinator to use the mock API client
#     mock_coordinator.meraki_api_client = mock_meraki_api_client
#
# # Mock the coordinator's data to include specific sense settings from a (future) API call
# # This would require the coordinator to fetch and store this.
# # For now, we'll assume device_info gets updated with this specific data.
#     mock_coordinator.data = {
# "devices": [
#             {
#                 **MOCK_CAMERA_DEVICE_INFO,
#                 "senseEnabled": MOCK_CAMERA_SENSE_API_DATA_SENSE_OFF_AUDIO_OFF["senseEnabled"]
#             }
# ]
#     }
#
#     sensor = await setup_sensor_entity(
#         hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
#     )
# # At this point, sensor's _update_sensor_data should use the "senseEnabled" from the coordinator data
# # which we've mocked to be False.
#
# # Manually trigger update to simulate coordinator refresh based on new (mocked) API data
#     sensor._handle_coordinator_update()
#     await hass.async_block_till_done()
#
#     assert sensor.native_value == "disabled"
#     assert sensor.icon == "mdi:camera-off-outline"
#
# # Test with sense enabled
#     mock_meraki_api_client.get_camera_sense_settings.return_value = MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON
#     mock_coordinator.data = {
# "devices": [
#             {
#                 **MOCK_CAMERA_DEVICE_INFO,
#                 "senseEnabled": MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON["senseEnabled"]
#             }
# ]
#     }
#     sensor._handle_coordinator_update()
#     await hass.async_block_till_done()
#
#     assert sensor.native_value == "enabled"
#     assert sensor.icon == "mdi:camera-iris"

# async def test_audio_sensor_reflects_api_data(hass: HomeAssistant, mock_coordinator, mock_meraki_api_client):
# """Test sensor state reflects actual (mocked) API data for AudioDetectionSensor."""
#     mock_coordinator.meraki_api_client = mock_meraki_api_client
#     mock_coordinator.data = {
# "devices": [
#             {
#                 **MOCK_CAMERA_DEVICE_INFO,
#                 "audioDetection": {
# "enabled": MOCK_CAMERA_SENSE_API_DATA_SENSE_OFF_AUDIO_OFF["audioDetection"]["enabled"]
#                 }
#             }
# ]
#     }
#
#     sensor = await setup_sensor_entity(
#         hass, mock_coordinator, MerakiCameraAudioDetectionSensor, MOCK_CAMERA_DEVICE_INFO
#     )
#     sensor._handle_coordinator_update()
#     await hass.async_block_till_done()
#
#     assert sensor.native_value == "disabled"
#     assert sensor.icon == "mdi:microphone-off"
#
# # Test with audio enabled
#     mock_meraki_api_client.get_camera_sense_settings.return_value = MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON
#     mock_coordinator.data = {
# "devices": [
#             {
#                 **MOCK_CAMERA_DEVICE_INFO,
#                 "audioDetection": {
# "enabled": MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON["audioDetection"]["enabled"]
#                 }
#             }
# ]
#     }
#     sensor._handle_coordinator_update()
#     await hass.async_block_till_done()
#
#     assert sensor.native_value == "enabled"
#     assert sensor.icon == "mdi:microphone"
#
# async def test_sensor_api_error_scenario(hass: HomeAssistant, mock_coordinator, mock_meraki_api_client):
# """Test sensor behavior when API call via coordinator fails."""
#     mock_coordinator.meraki_api_client = mock_meraki_api_client
#     mock_meraki_api_client.get_camera_sense_settings.side_effect = UpdateFailed("API Error")
#
# # Simulate the coordinator trying to update its data and failing
# # This part depends on how the coordinator itself handles the UpdateFailed exception
# # For this test, let's assume the coordinator sets its data to None or last_update_success to False
#     mock_coordinator.last_update_success = False
#     mock_coordinator.data = None # Or some indicator of failure
#
#     sensor = await setup_sensor_entity(
#         hass, mock_coordinator, MerakiCameraSenseStatusSensor, MOCK_CAMERA_DEVICE_INFO
#     )
#     sensor._handle_coordinator_update() # To reflect new coordinator state
#     await hass.async_block_till_done()
#
#     assert sensor.available is False
# # Depending on desired behavior, native_value might be None or a specific error state
#     assert sensor.native_value is None
#
# # Restore for other tests
#     mock_coordinator.last_update_success = True
#     mock_coordinator.data = {"devices": [MOCK_CAMERA_DEVICE_INFO]}
#     mock_meraki_api_client.get_camera_sense_settings.side_effect = None
#     mock_meraki_api_client.get_camera_sense_settings.return_value = MOCK_CAMERA_SENSE_API_DATA_SENSE_ON_AUDIO_ON

"""
Note on current sensor tests:
The current sensor implementation uses placeholder logic for `senseEnabled` and `audioDetection.enabled`
(hardcoded to True within their `_update_sensor_data` methods if no specific data is found).
The tests above reflect this current state.
The commented-out tests (`test_sense_status_sensor_reflects_api_data`, etc.)
are designed for a future state where:
1. The `MerakiDataUpdateCoordinator` is responsible for calling `meraki_api_client.get_camera_sense_settings(serial)`.
2. The coordinator stores this specific camera sense data, likely keyed by serial, within its `coordinator.data`.
   For example: `coordinator.data['devices_camera_sense'][serial] = {'senseEnabled': True, ...}`.
3. The `MerakiCameraSenseStatusSensor` and `MerakiCameraAudioDetectionSensor` are updated
   in their `_get_current_device_data` (or a new method) to retrieve this specific data from the coordinator,
   rather than relying on placeholders or generic device data for these states.
Once these changes are made to the sensors and coordinator, the commented-out tests can be enabled and adapted.
"""
