"""Tests for the Meraki connected clients sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.connected_clients import (
    MerakiDeviceConnectedClientsSensor,
)


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
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
        "clients_by_serial": {
            # Appliance gets 2 clients
            "dev_appliance": [
                {"id": "client1"},
                {"id": "client2"},
            ],
            # Switch gets 1 client
            "dev_switch": [
                {"id": "client3"},
            ],
            # Wireless AP gets 3 clients
            "dev_wireless": [
                {"id": "client4"},
                {"id": "client5"},
                {"id": "client6"},
            ],
        },
        "networks": [
            {"id": "net1", "name": "Network 1"},
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
    # The get_device_clients API returns a list of clients. The sensor just counts them.
    assert sensor.native_value == 2
    assert sensor.device_info["name"] == "[Appliance] Appliance"


def test_connected_clients_sensor_switch(mock_data_coordinator):
    """Test the connected clients sensor for a switch."""
    device = mock_data_coordinator.data["devices"][1]  # The switch
    config_entry = mock_data_coordinator.config_entry
    mock_data_coordinator.config_entry.options = {"device_name_format": "prefix"}
    sensor = MerakiDeviceConnectedClientsSensor(
        mock_data_coordinator, device, config_entry
    )
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
    assert sensor.native_value == 3
    assert sensor.device_info["name"] == "[Wireless] Access Point"