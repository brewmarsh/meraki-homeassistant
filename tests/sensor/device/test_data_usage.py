"""Tests for the Meraki data usage sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.data_usage import MerakiDataUsageSensor
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "devices": [
            MerakiDevice.from_dict(
                {
                    "serial": "dev1",
                    "name": "Appliance",
                    "model": "MX64",
                    "productType": "appliance",
                    "networkId": "net-123",
                }
            )
        ],
        "appliance_traffic": {
            "net-123": [
                {"sent": 1024, "recv": 4096},
                {"sent": 1024, "recv": 4096},
            ]
        },
    }

    def get_device(serial):
        for d in coordinator.data["devices"]:
            if d.serial == serial:
                return d
        return None

    coordinator.get_device.side_effect = get_device
    return coordinator


def test_data_usage_sensor(mock_data_coordinator):
    """Test the data usage sensor."""
    device = mock_data_coordinator.data["devices"][0]
    # Explicitly set usage_metrics for micro-targeted remediation
    mock_metrics = MagicMock()
    mock_metrics.total = 10.0
    mock_metrics.sent = 2.0
    mock_metrics.received = 8.0
    device.usage_metrics = mock_metrics

    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDataUsageSensor(mock_data_coordinator, device, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.unique_id == "dev1_data_usage"
    assert sensor.name == "Data Usage"
    assert sensor.native_value == 10.0  # (1+1) + (4+4) = 10 MB
    assert sensor.extra_state_attributes["sent_mb"] == 2.0
    assert sensor.extra_state_attributes["received_mb"] == 8.0


def test_data_usage_sensor_disabled(mock_data_coordinator):
    """Test the data usage sensor when traffic analysis is disabled."""
    # Overwrite the traffic data with the disabled marker
    mock_data_coordinator.data["appliance_traffic"]["net-123"] = {"error": "disabled"}

    device = mock_data_coordinator.data["devices"][0]
    # Explicitly set state for micro-targeted remediation
    device.traffic_analysis_enabled = False

    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDataUsageSensor(mock_data_coordinator, device, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()

    assert sensor.native_value == "Disabled"
    assert (
        sensor.extra_state_attributes["reason"]
        == "Traffic analysis is not enabled for this network."
    )
