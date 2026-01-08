"""Tests for the Meraki PoE usage sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.poe_usage import MerakiPoeUsageSensor


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Switch",
                "model": "MS220-8P",
                "productType": "switch",
                "ports_statuses": [
                    {"portId": 1, "powerUsageInWh": 252},
                    {"portId": 2, "powerUsageInWh": 124.8},
                    {"portId": 3, "powerUsageInWh": 0},
                ],
            }
        ]
    }
    return coordinator


def test_poe_usage_sensor(mock_device_coordinator):
    """Test the PoE usage sensor."""
    device = mock_device_coordinator.data["devices"][0]
    sensor = MerakiPoeUsageSensor(mock_device_coordinator, device)
    assert sensor.unique_id == "dev1_poe_usage"
    # Name is the device name (format_entity_name with default NONE format)
    assert sensor.name == "Switch"
    assert sensor.native_value == 15.7
    assert sensor.extra_state_attributes["port_1_power_usage_wh"] == 252
    assert sensor.extra_state_attributes["port_2_power_usage_wh"] == 124.8
    assert sensor.extra_state_attributes["port_3_power_usage_wh"] == 0
