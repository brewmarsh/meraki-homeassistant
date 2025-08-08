"""Tests for the Meraki data usage sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.data_usage import MerakiDataUsageSensor

@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "traffic": [{"sent": 2048, "received": 8192}],  # 2 MB  # 8 MB
            }
        ]
    }
    return coordinator


def test_data_usage_sensor(mock_data_coordinator):
    """Test the data usage sensor."""
    device = mock_data_coordinator.data["devices"][0]
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDataUsageSensor(mock_data_coordinator, device, config_entry)
    assert sensor.unique_id == "dev1_data_usage"
    assert sensor.name == "Data Usage"
    assert sensor.native_value == 10.0  # 2 + 8
    assert sensor.extra_state_attributes["sent_mb"] == 2.0
    assert sensor.extra_state_attributes["received_mb"] == 8.0
