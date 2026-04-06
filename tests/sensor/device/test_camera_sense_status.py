"""Tests for the Meraki camera sense status sensor."""

from unittest.mock import MagicMock
import pytest

from custom_components.meraki_ha.sensor.device.camera_sense_status import MerakiCameraSenseStatusSensor
from custom_components.meraki_ha.core.models.device import MerakiDevice

@pytest.mark.asyncio
async def test_camera_sense_status_sensor():
    """Test the MerakiCameraSenseStatusSensor."""
    mock_coordinator = MagicMock()

    device_data = MerakiDevice(
        serial="SERIAL123",
        model="MV12",
        name="Test Camera",
        product_type="camera",
        network_id="N_123"
    )
    device_data.sense_settings = {"senseEnabled": True}

    mock_coordinator.get_device.return_value = device_data
    mock_coordinator.data = {"devices_by_serial": {"SERIAL123": device_data}}

    mock_config_entry = MagicMock()
    mock_config_entry.options = {}

    # Instantiate sensor
    sensor = MerakiCameraSenseStatusSensor(mock_coordinator, device_data, mock_config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    # Assert properties
    assert sensor.unique_id == "SERIAL123_camera_sense_status"
    assert sensor.native_value == "enabled"
    assert sensor.available is True

    # Test disabled
    device_data.sense_settings = {"senseEnabled": False}
    sensor._handle_coordinator_update()
    assert sensor.native_value == "disabled"

    # Test missing senseEnabled
    device_data.sense_settings = {}
    sensor._handle_coordinator_update()
    assert sensor.native_value is None

    # Test invalid sense_settings
    device_data.sense_settings = None
    sensor._handle_coordinator_update()
    assert sensor.native_value is None
    assert sensor.available is False

    # Test no device data
    mock_coordinator.get_device.return_value = None
    sensor._handle_coordinator_update()
    assert sensor.native_value is None
    assert sensor.available is False
