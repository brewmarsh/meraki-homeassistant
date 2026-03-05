"""Tests for the Meraki AP client count sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.sensor.device.ap_client_count import (
    MerakiAPClientCountSensor,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}

    device = MerakiDevice.from_dict({
        "serial": "test_serial",
        "name": "Test AP",
        "model": "MR52",
        "productType": "wireless",
    })

    coordinator.data = {
        "clients": [
            {"recentDeviceSerial": "test_serial"},
            "invalid_client_string",  # This should no longer cause the AttributeError
            {"recentDeviceSerial": "other_serial"},
            {"recentDeviceSerial": "test_serial"},
        ]
    }

    coordinator.get_device.return_value = device
    return coordinator, device


def test_ap_client_count_sensor_no_attribute_error(mock_coordinator):
    """Test that the sensor handles invalid client data in the coordinator."""
    coordinator, device = mock_coordinator
    config_entry = coordinator.config_entry

    sensor = MerakiAPClientCountSensor(coordinator, device, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    # This should no longer raise AttributeError
    sensor._update_state()

    # Expected value is 2 (two clients with 'test_serial')
    assert sensor.native_value == 2


def test_ap_client_count_sensor_empty_clients(mock_coordinator):
    """Test the sensor with empty clients list."""
    coordinator, device = mock_coordinator
    coordinator.data["clients"] = []
    config_entry = coordinator.config_entry

    sensor = MerakiAPClientCountSensor(coordinator, device, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    sensor._update_state()
    assert sensor.native_value == 0
