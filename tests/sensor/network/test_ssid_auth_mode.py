"""Tests for the Meraki SSID Auth Mode sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.network.ssid_auth_mode import (
    MerakiSSIDAuthModeSensor,
)
from homeassistant.const import EntityCategory


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": {
            0: {"number": 0, "name": "Test SSID", "authMode": "psk", "networkId": "net1"}
        }
    }
    return coordinator


def test_ssid_auth_mode_sensor(mock_coordinator):
    """Test the SSID Auth Mode sensor."""
    ssid_data = {"number": 0, "name": "Test SSID", "authMode": "psk", "networkId": "net1"}

    sensor = MerakiSSIDAuthModeSensor(
        mock_coordinator, mock_coordinator.config_entry, ssid_data
    )

    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == "psk"
    assert sensor.icon == "mdi:lock"
