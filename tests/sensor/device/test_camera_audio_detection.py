"""Tests for the Meraki Camera Audio Detection sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.const import EntityCategory

from custom_components.meraki_ha.sensor.device.camera_audio_detection import (
    MerakiCameraAudioDetectionSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    # Ensure data is truthy for availability check
    coordinator.data = {"status": "online"}
    return coordinator


def test_camera_audio_detection_sensor(mock_coordinator):
    """Test the camera audio detection sensor."""
    hass = MagicMock()

    # Create a mock device with audio detection enabled
    device = MerakiDevice(
        serial="test_serial",
        name="Test Camera",
        model="MV2",
        mac="00:11:22:33:44:55",
        network_id="net1",
        product_type="camera",
        sense_settings={"audioDetection": {"enabled": True}},
    )
    # Ensure device is online for availability
    device.status = "online"

    mock_coordinator.get_device.return_value = device

    sensor = MerakiCameraAudioDetectionSensor(
        mock_coordinator, device, mock_coordinator.config_entry
    )

    assert sensor.unique_id == "test_serial_camera_audio_detection_status"
    # Note: Name format checks are good to keep
    assert "Audio Detection" in sensor.name
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == "enabled"
    assert sensor.icon == "mdi:microphone"

    # Mock hass for the sensor
    sensor.hass = hass
    sensor.async_write_ha_state = MagicMock()

    # Update with enabled audio
    device.sense_settings = {"audioDetection": {"enabled": True}}
    sensor._handle_coordinator_update()

    assert sensor.native_value == "enabled"
    assert sensor.icon == "mdi:microphone"

    # Update with missing audio detection data
    # Action 4: Clear the dictionary entirely to properly simulate removal of audio detection
    device.sense_settings = {}
    sensor._handle_coordinator_update()

    assert sensor.native_value is None
    assert sensor.icon == "mdi:microphone-question"

    # Also test with sense_settings being None
    device.sense_settings = None
    sensor._handle_coordinator_update()
    assert sensor.native_value is None
    assert sensor.icon == "mdi:microphone-question"
