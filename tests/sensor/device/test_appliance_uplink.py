"""Tests for the Meraki appliance uplink sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.setup_helpers import async_setup_sensors
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    mock_device_data = {
        "serial": "dev1",
        "name": "Test Appliance",
        "model": "MX64",
            "productType": "appliance",
        "networkId": "net1",
    }
    coordinator.data = {
        "devices": [mock_device_data],
        "appliance_uplink_statuses": [
            {
                "serial": "dev1",
                "uplinks": [
                    {
                        "interface": "wan1",
                        "status": "active",
                        "ip": "1.2.3.4",
                    },
                    {
                        "interface": "wan2",
                        "status": "failed",
                        "ip": "5.6.7.8",
                    },
                    {
                        "interface": "cellular",
                        "status": "ready",
                        "ip": "9.10.11.12",
                    },
                ],
            }
        ],
        # Add other required data structures for setup_helpers
        "clients": [],
        "ssids": [],
        "vlans": {},
    }
    coordinator.get_device.return_value = MerakiDevice.from_dict(mock_device_data)
    return coordinator


def test_appliance_uplink_sensor_creation(mock_coordinator):
    """Test that appliance uplink sensors are created correctly."""
    hass = MagicMock()
    config_entry = MagicMock()
    camera_service = MagicMock()

    # Run the setup
    sensors = async_setup_sensors(hass, config_entry, mock_coordinator, camera_service)

    # Filter for just the uplink sensors
    uplink_sensors = [s for s in sensors if "Uplink" in s.__class__.__name__]

    # We expect 3 sensors, one for each uplink interface
    assert len(uplink_sensors) == 3

    # Find the specific sensors
    wan1_sensor = next(s for s in uplink_sensors if s.unique_id == "dev1_uplink_wan1")
    wan2_sensor = next(s for s in uplink_sensors if s.unique_id == "dev1_uplink_wan2")
    cellular_sensor = next(
        s for s in uplink_sensors if s.unique_id == "dev1_uplink_cellular"
    )

    # Assertions for WAN1 Sensor
    assert wan1_sensor.name == "Uplink WAN1"
    assert wan1_sensor.native_value == "active"
    assert wan1_sensor.extra_state_attributes["ip"] == "1.2.3.4"

    # Assertions for WAN2 Sensor
    assert wan2_sensor.name == "Uplink WAN2"
    assert wan2_sensor.native_value == "failed"
    assert wan2_sensor.extra_state_attributes["ip"] == "5.6.7.8"

    # Assertions for Cellular Sensor
    assert cellular_sensor.name == "Uplink CELLULAR"
    assert cellular_sensor.native_value == "ready"
    assert cellular_sensor.extra_state_attributes["ip"] == "9.10.11.12"
