"""Tests for the Meraki Camera Sense Status sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.camera_sense_status import (
    MerakiCameraSenseStatusSensor,
)
from custom_components.meraki_ha.core.models.device import MerakiDevice
from homeassistant.const import EntityCategory


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiCameraCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    # Ensure data is truthy for availability check
    coordinator.data = {"status": "online"}
    return coordinator


def test_camera_sense_status_sensor(mock_coordinator):
    """Test the camera sense status sensor."""
    hass = MagicMock()

    # Create a mock device with sense enabled
    device = MerakiDevice(
        serial="test_serial",
        name="Test Camera",
        model="MV2",
        mac="00:11:22:33:44:55",
        network_id="net1",
        product_type="camera",
        sense_settings={"senseEnabled": True},
    )
    # Ensure device is online for availability
    device.status = "online"

    mock_coordinator.get_device.return_value = device

    sensor = MerakiCameraSenseStatusSensor(
        mock_coordinator, device, mock_coordinator.config_entry
    )

    assert sensor.unique_id == "test_serial_camera_sense_status"
    assert "Sense Enabled" in sensor.name
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == "enabled"
    assert sensor.icon == "mdi:camera-iris"
    assert sensor.available is True

    # Mock hass for the sensor
    sensor.hass = hass
    sensor.async_write_ha_state = MagicMock()

    # Update with disabled sense
    device.sense_settings = {"senseEnabled": False}
    sensor._handle_coordinator_update()

    assert sensor.native_value == "disabled"
    assert sensor.icon == "mdi:camera-off-outline"
    assert sensor.available is True

    # Update with missing senseEnabled data
    device.sense_settings = {}
    sensor._handle_coordinator_update()

    assert sensor.native_value is None
    assert sensor.icon == "mdi:camera-question"
    assert sensor.available is True

    # Test with sense_settings being None
    device.sense_settings = None
    sensor._handle_coordinator_update()
    assert sensor.native_value is None
    assert sensor.icon == "mdi:camera-question"
    assert sensor.available is False

    # Test missing coordinator data
    mock_coordinator.data = None
    assert sensor.available is False
    mock_coordinator.data = {"status": "online"}

    # Test missing device data
    mock_coordinator.get_device.return_value = None
    sensor._handle_coordinator_update()
    assert sensor.native_value is None
    assert sensor.icon == "mdi:help-rhombus"
    assert sensor.available is False


def test_camera_sense_status_missing_serial(mock_coordinator):
    """Test that ValueError is raised if serial is missing."""
    device = MerakiDevice(
        serial=None,
        name="Test Camera",
        model="MV2",
        mac="00:11:22:33:44:55",
        network_id="net1",
        product_type="camera",
    )
    with pytest.raises(ValueError, match="Device serial cannot be None"):
        MerakiCameraSenseStatusSensor(
            mock_coordinator, device, mock_coordinator.config_entry
        )
