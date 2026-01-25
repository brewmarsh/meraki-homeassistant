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
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}

    # Create a mock device
    mock_device = MerakiDevice(
        serial="Q234-5678-90AB",
        name="Test Camera",
        model="MV2",
        network_id="net1",
        product_type="camera",
        sense_settings={"audioDetection": {"enabled": True}},
    )

    coordinator.data = {
        "devices": [mock_device],
    }
    # Mock get_device to return the device
    coordinator.get_device.return_value = mock_device

    return coordinator


def test_camera_audio_detection_sensor(mock_coordinator):
    """Test Camera Audio Detection sensor creation and state."""
    hass = MagicMock()

    device_data = mock_coordinator.data["devices"][0]

    sensor = MerakiCameraAudioDetectionSensor(
        mock_coordinator, device_data, mock_coordinator.config_entry
    )

    assert sensor.unique_id == "Q234-5678-90AB_camera_audio_detection_status"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.available is True
    assert sensor.native_value == "enabled"
    assert sensor.icon == "mdi:microphone"

    # Mock hass for the sensor
    sensor.hass = hass
    sensor.async_write_ha_state = MagicMock()

    # Test update with disabled
    device_data.sense_settings["audioDetection"]["enabled"] = False
    sensor._handle_coordinator_update()
    assert sensor.native_value == "disabled"
    assert sensor.icon == "mdi:microphone-off"

    # Test unavailable/missing data
    mock_coordinator.get_device.return_value = None
    sensor._handle_coordinator_update()
    assert sensor.native_value is None
