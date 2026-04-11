"""Tests for the Meraki SSID Availability sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.network.ssid_availability import (
    MerakiSSIDAvailabilitySensor,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": {
            0: {"number": 0, "name": "Test SSID", "enabled": True, "networkId": "net1"}
        }
    }
    return coordinator


def test_ssid_availability_sensor(mock_coordinator):
    """Test the SSID Availability sensor."""
    ssid_data = {"number": 0, "name": "Test SSID", "enabled": True, "networkId": "net1"}

    sensor = MerakiSSIDAvailabilitySensor(
        mock_coordinator, mock_coordinator.config_entry, ssid_data
    )

    assert sensor.native_value is True
    assert sensor.icon == "mdi:check-circle-outline"
