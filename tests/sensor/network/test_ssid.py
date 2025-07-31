"""Tests for the Meraki SSID sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid import create_ssid_sensors
from custom_components.meraki_ha.sensor.network.ssid_availability import (
    MerakiSSIDAvailabilitySensor,
)
from custom_components.meraki_ha.sensor.network.ssid_channel import MerakiSSIDChannelSensor
from custom_components.meraki_ha.sensor.network.ssid_client_count import (
    MerakiSSIDClientCountSensor,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiNetworkCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssids": [
            {
                "number": 0,
                "name": "Test SSID",
                "enabled": True,
                "ipAssignmentMode": "NAT",
                "authMode": "psk",
                "channel": 6,
                "client_count": 10,
                "unique_id": "ssid_0",
            }
        ]
    }
    return coordinator


def test_create_ssid_sensors(mock_coordinator):
    """Test the create_ssid_sensors factory function."""
    ssid_data = mock_coordinator.data["ssids"][0]
    sensors = create_ssid_sensors(mock_coordinator, {}, ssid_data)
    assert len(sensors) == 3
    assert isinstance(sensors[0], MerakiSSIDAvailabilitySensor)
    assert isinstance(sensors[1], MerakiSSIDChannelSensor)
    assert isinstance(sensors[2], MerakiSSIDClientCountSensor)

    assert sensors[0].unique_id == "ssid_0_availability"
    assert sensors[0].is_on is True

    assert sensors[1].unique_id == "ssid_0_channel"
    assert sensors[1].native_value == 6

    assert sensors[2].unique_id == "ssid_0_client_count"
    assert sensors[2].native_value == 10
