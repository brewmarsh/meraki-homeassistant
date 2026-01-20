
"""Tests for the Meraki SSID connected clients sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.sensor.ssid.connected_clients import (
    MerakiSsidConnectedClientsSensor,
)


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": [
            {
                "number": 0,
                "name": "My SSID 1",
                "enabled": True,
                "networkId": "net1",
            },
            {
                "number": 1,
                "name": "My SSID 2",
                "enabled": True,
                "networkId": "net1",
            },
        ],
        "clients": [
            # Client 1: Online, on SSID 1, net1
            {
                "networkId": "net1",
                "ssid": "My SSID 1",
                "status": "Online",
            },
            # Client 2: Online, on SSID 1, net1
            {
                "networkId": "net1",
                "ssid": "My SSID 1",
                "status": "Online",
            },
            # Client 3: Offline, on SSID 1, net1
            {
                "networkId": "net1",
                "ssid": "My SSID 1",
                "status": "Offline",
            },
            # Client 4: Online, on SSID 2, net1
            {
                "networkId": "net1",
                "ssid": "My SSID 2",
                "status": "Online",
            },
            # Client 5: Online, on SSID 1, but on another network
            {
                "networkId": "net2",
                "ssid": "My SSID 1",
                "status": "Online",
            },
        ],
        "devices": [
            {
                "serial": "dev_wireless",
                "name": "Access Point",
                "model": "MR52",
                "productType": "wireless",
                "networkId": "net1",
            }
        ],
        "networks": [
            {"id": "net1", "name": "Network 1"},
            {"id": "net2", "name": "Network 2"},
        ],
    }
    def get_ssid(network_id, ssid_number):
        for ssid in coordinator.data["ssids"]:
            if ssid["networkId"] == network_id and ssid["number"] == ssid_number:
                return ssid
        return None
    coordinator.get_ssid.side_effect = get_ssid
    return coordinator


def test_ssid_connected_clients_sensor(mock_data_coordinator):
    """Test the connected clients sensor for an SSID."""
    network_id = "net1"
    ssid_data = mock_data_coordinator.data["ssids"][0]  # My SSID 1
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiSsidConnectedClientsSensor(
        mock_data_coordinator, network_id, ssid_data, config_entry
    )
    sensor._handle_coordinator_update()
    # Expects 2: the two online clients on "My SSID 1" and "net1"
    assert sensor.native_value == 2
    assert sensor.name == "Connected clients"
    assert sensor.device_info["identifiers"] == {(DOMAIN, "net1_0")}
