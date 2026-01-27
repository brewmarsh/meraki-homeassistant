"""Tests for the Meraki PoE usage sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.poe_usage import MerakiPoeUsageSensor
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            MerakiDevice.from_dict(
                {
                    "serial": "dev1",
                    "name": "Switch",
                    "model": "MS220-8P",
                    "productType": "switch",
                    "portsStatuses": [
                        {"portId": 1, "powerUsageInWh": 252},
                        {"portId": 2, "powerUsageInWh": 124.8},
                        {"portId": 3, "powerUsageInWh": 0},
                    ],
                }
            )
        ]
    }
    coordinator.get_device.return_value = coordinator.data["devices"][0]
    return coordinator


def test_poe_usage_sensor(mock_device_coordinator):
    """Test the PoE usage sensor."""
    from datetime import timedelta
    mock_device_coordinator.update_interval = timedelta(hours=24)

    device = mock_device_coordinator.data["devices"][0]
    sensor = MerakiPoeUsageSensor(mock_device_coordinator, device)
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()

    assert sensor.unique_id == "dev1_poe_usage"
    assert sensor.name == "PoE Usage"
    assert sensor.native_value == 15.7
    assert sensor.extra_state_attributes["port_1_power_usage_wh"] == 252
    assert sensor.extra_state_attributes["port_2_power_usage_wh"] == 124.8
    assert sensor.extra_state_attributes["port_3_power_usage_wh"] == 0


def test_poe_usage_sensor_with_timespan(mock_device_coordinator):
    """Test the PoE usage sensor with explicit timespan."""
    device = mock_device_coordinator.data["devices"][0]
    # Update device ports to include _timespan
    # Original ports: 252, 124.8, 0 = 376.8 total Wh
    # Add _timespan = 3600 (1 hour)
    for port in device.ports_statuses:
        port["_timespan"] = 3600

    sensor = MerakiPoeUsageSensor(mock_device_coordinator, device)

    # 376.8 Wh / 1 h = 376.8 W
    assert sensor.native_value == 376.8

    # Update timespan to 300s (5 min)
    for port in device.ports_statuses:
        port["_timespan"] = 300

    # 376.8 Wh / (300/3600) = 376.8 * 12 = 4521.6 W
    assert sensor.native_value == 4521.6
