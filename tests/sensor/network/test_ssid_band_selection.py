"""Tests for the Meraki SSID Band Selection sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.const import EntityCategory

from custom_components.meraki_ha.sensor.network.ssid_band_selection import (
    MerakiSSIDBandSelectionSensor,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": {
            0: {
                "number": 0,
                "name": "Test SSID",
                "bandSelection": "Dual band operation with Band Steering",
                "networkId": "net1",
            }
        }
    }
    return coordinator


def test_ssid_band_selection_sensor(mock_coordinator):
    """Test the SSID Band Selection sensor."""
    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "bandSelection": "Dual band operation with Band Steering",
        "networkId": "net1",
    }

    sensor = MerakiSSIDBandSelectionSensor(
        mock_coordinator, mock_coordinator.config_entry, ssid_data
    )

    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == "Dual band operation with Band Steering"
    assert sensor.icon == "mdi:wifi-arrow-up-down"
