"""Tests for the Meraki connected clients sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.connected_clients import (
    MerakiDeviceConnectedClientsSensor,
)


@pytest.fixture
def mock_data_coordinator():
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
=======
    """Fixture for a mocked MerakiDataCoordinator."""
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
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
            {
                "serial": "dev_gateway",
                "name": "Gateway",
                "model": "GX20",
                "productType": "cellularGateway",
                "networkId": "net1",
            },
        ],
        "clients": [
            # Client 1: Online, on net1
            {"networkId": "net1", "status": "Online"},
            # Client 2: Online, on net1
            {"networkId": "net1", "status": "Online"},
            # Client 3: Offline, on net1
            {"networkId": "net1", "status": "Offline"},
            # Client 4: Online, but on another network
            {"networkId": "net2", "status": "Online"},
        ],
        "clients_by_serial": {
            # This data is now only used for switch and wireless
            "dev_switch": [
                {"id": "client_w1"},
            ],
            "dev_wireless": [
                {"id": "client_ap1"},
                {"id": "client_ap2"},
                {"id": "client_ap3"},
            ],
        },
        "networks": [
            {"id": "net1", "name": "Network 1"},
            {"id": "net2", "name": "Network 2"},
        ],
    }
    return coordinator


def test_connected_clients_sensor_appliance(mock_data_coordinator):
    """Test the connected clients sensor for an appliance."""
    device = mock_data_coordinator.data["devices"][0]  # The appliance
    config_entry = mock_data_coordinator.config_entry
    mock_data_coordinator.config_entry.options = {"device_name_format": "prefix"}
    sensor = MerakiDeviceConnectedClientsSensor(
        mock_data_coordinator, device, config_entry
    )
    # Expects 2: the two online clients on net1 from the main `clients` list
    assert sensor.native_value == 2
    assert sensor.device_info["name"] == "[Appliance] Appliance"


def test_connected_clients_sensor_gateway(mock_data_coordinator):
    """Test the connected clients sensor for a cellular gateway."""
    device = mock_data_coordinator.data["devices"][3]  # The gateway
    config_entry = mock_data_coordinator.config_entry
    mock_data_coordinator.config_entry.options = {"device_name_format": "prefix"}
    sensor = MerakiDeviceConnectedClientsSensor(
        mock_data_coordinator, device, config_entry
    )
    # Expects 2: the two online clients on net1 from the main `clients` list
    assert sensor.native_value == 2
    assert sensor.device_info["name"] == "[Cellulargateway] Gateway"


def test_connected_clients_sensor_switch(mock_data_coordinator):
    """Test the connected clients sensor for a switch."""
    device = mock_data_coordinator.data["devices"][1]  # The switch
    config_entry = mock_data_coordinator.config_entry
    mock_data_coordinator.config_entry.options = {"device_name_format": "prefix"}
    sensor = MerakiDeviceConnectedClientsSensor(
        mock_data_coordinator, device, config_entry
    )
    # Expects 1 from the `clients_by_serial` data
    assert sensor.native_value == 1
    assert sensor.device_info["name"] == "[Switch] Switch"


def test_connected_clients_sensor_wireless(mock_data_coordinator):
    """Test the connected clients sensor for a wireless device."""
    device = mock_data_coordinator.data["devices"][2]  # The wireless AP
    config_entry = mock_data_coordinator.config_entry
    mock_data_coordinator.config_entry.options = {"device_name_format": "prefix"}
    sensor = MerakiDeviceConnectedClientsSensor(
        mock_data_coordinator, device, config_entry
    )
    # Expects 3 from the `clients_by_serial` data
    assert sensor.native_value == 3
    assert sensor.device_info["name"] == "[Wireless] Access Point"
