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
            MerakiDevice(
                serial="dev1",
                name="Switch",
                model="MS220-8P",
                product_type="switch",
                ports_statuses=[
                    {"portId": 1, "powerUsageInWh": 252},
                    {"portId": 2, "powerUsageInWh": 124.8},
                    {"portId": 3, "powerUsageInWh": 0},
                ],
            )
        ]
    }
    coordinator.get_device.return_value = coordinator.data["devices"][0]
    return coordinator


def test_poe_usage_sensor(mock_device_coordinator):
    """Test the PoE usage sensor."""
    from datetime import timedelta

    # Set update interval to 1 hour (3600 seconds)
    mock_device_coordinator.update_interval = timedelta(hours=1)

    device = mock_device_coordinator.data["devices"][0]
    sensor = MerakiPoeUsageSensor(mock_device_coordinator, device)
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()

    assert sensor.unique_id == "dev1_poe_usage"
    assert sensor.name == "PoE Usage"
    # Total usage = 252 + 124.8 = 376.8 Wh
    # The sensor implementation divides by 24 (assuming daily usage), regardless
    # of update interval
    # 376.8 / 24 = 15.7 W
    assert sensor.native_value == 15.7
    assert sensor.extra_state_attributes["port_1_power_usage_wh"] == 252
    assert sensor.extra_state_attributes["port_2_power_usage_wh"] == 124.8
    assert sensor.extra_state_attributes["port_3_power_usage_wh"] == 0
