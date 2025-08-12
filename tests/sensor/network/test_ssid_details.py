"""Tests for the Meraki SSID detail sensors."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid import create_ssid_sensors


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": [
            {
                "number": 0,
                "name": "Test SSID",
                "networkId": "net1",
                "walledGardenEnabled": True,
                "walledGardenRanges": ["example.com"],
                "perSsidBandwidthLimitUp": 1000,
                "perSsidBandwidthLimitDown": 5000,
                "mandatoryDhcpEnabled": True,
            }
        ],
        "rf_profiles": {
            "net1": [
                {
                    "id": "1234",
                    "name": "Main Office",
                    "twoFourGhzSettings": {"minBitrate": 11},
                    "fiveGhzSettings": {"minBitrate": 24},
                }
            ]
        },
    }
    return coordinator


def test_ssid_detail_sensor_creation(mock_coordinator):
    """Test that the new SSID detail sensors are created correctly."""
    config_entry = MagicMock()
    ssid_data = mock_coordinator.data["ssids"][0]

    # Run the factory function
    sensors = create_ssid_sensors(mock_coordinator, config_entry, ssid_data)

    # Filter for just the new detail sensors
    from custom_components.meraki_ha.sensor.network.ssid_details import (
        MerakiSSIDDetailSensor,
    )

    detail_sensors = {
        s.name: s for s in sensors if isinstance(s, MerakiSSIDDetailSensor)
    }

    assert len(detail_sensors) == 6

    # --- Assertions for each sensor ---

    walled_garden = detail_sensors["Walled Garden"]
    assert walled_garden.native_value == "enabled"
    assert walled_garden.extra_state_attributes["ranges"] == ["example.com"]

    upload_limit = detail_sensors["Total Upload Limit"]
    assert upload_limit.native_value == 1000

    download_limit = detail_sensors["Total Download Limit"]
    assert download_limit.native_value == 5000

    mandatory_dhcp = detail_sensors["Mandatory DHCP"]
    assert mandatory_dhcp.native_value == "enabled"

    min_bitrate_24 = detail_sensors["Minimum Bitrate 2.4GHz"]
    assert min_bitrate_24.native_value == 11

    min_bitrate_5 = detail_sensors["Minimum Bitrate 5GHz"]
    assert min_bitrate_5.native_value == 24
