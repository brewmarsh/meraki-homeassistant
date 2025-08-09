"""Tests for the Meraki connected clients sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "devices": [
            {
                "serial": "dev_appliance",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "networkId": "net1",
            },
            {
                "serial": "dev_switch",
                "name": "Switch",
                "model": "MS220",
                "productType": "switch",
                "networkId": "net1",
            },
            {
                "serial": "dev_wireless",
                "name": "Access Point",
                "model": "MR52",
                "productType": "wireless",
                "networkId": "net1",
            },
        ],
        "clients": [
            # Client 1: Wireless, on AP, on net1, Online
            {
                "networkId": "net1",
                "recentDeviceSerial": "dev_wireless",
                "status": "Online",
                "recentDeviceConnection": "Wireless",
            },
            # Client 2: Wired, on net1, Online
            {
                "networkId": "net1",
                "recentDeviceSerial": "dev_switch", # This might be the switch, or something else
                "status": "Online",
                "recentDeviceConnection": "Wired",
            },
            # Client 3: Offline, on net1
            {
                "networkId": "net1",
                "recentDeviceSerial": "dev_wireless",
                "status": "Offline",
                "recentDeviceConnection": "Wireless",
            },
            # Client 4: Online, but on another network
            {
                "networkId": "net2",
                "status": "Online",
            },
        ],
        "networks": [
            {"id": "net1", "name": "Network 1"},
            {"id": "net2", "name": "Network 2"},
        ]
    }
    return coordinator


def test_connected_clients_sensor_appliance(mock_data_coordinator):
    """Test the connected clients sensor for an appliance. Should count all online clients on its network."""
    device = mock_data_coordinator.data["devices"][0]  # The appliance
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDeviceConnectedClientsSensor(mock_data_coordinator, device, config_entry)
    # Expects 2: the online wireless client and the online wired client on net1
    assert sensor.native_value == 2


def test_connected_clients_sensor_switch(mock_data_coordinator):
    """Test the connected clients sensor for a switch. Should count only wired online clients on its network."""
    device = mock_data_coordinator.data["devices"][1]  # The switch
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDeviceConnectedClientsSensor(mock_data_coordinator, device, config_entry)
    # Expects 1: the online wired client on net1
    assert sensor.native_value == 1


def test_connected_clients_sensor_wireless(mock_data_coordinator):
    """Test the connected clients sensor for a wireless device. Should count only clients connected to it."""
    device = mock_data_coordinator.data["devices"][2]  # The wireless AP
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDeviceConnectedClientsSensor(mock_data_coordinator, device, config_entry)
    # Expects 1: the online wireless client connected to this specific AP
    assert sensor.native_value == 1
