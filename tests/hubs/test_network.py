"""Tests for the NetworkHub."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.hubs.network import NetworkHub
from tests.const import MOCK_NETWORK, MOCK_DEVICE

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    device_in_network = MOCK_DEVICE.copy()
    device_in_network["networkId"] = MOCK_NETWORK["id"]
    device_other_network = MOCK_DEVICE.copy()
    device_other_network["serial"] = "other_serial"
    device_other_network["networkId"] = "other_network"

    ssid_in_network = {"networkId": MOCK_NETWORK["id"], "name": "SSID in network"}
    ssid_other_network = {"networkId": "other_network", "name": "SSID in other network"}

    coordinator.data = {
        "networks": [MOCK_NETWORK],
        "devices": [device_in_network, device_other_network],
        "ssids": [ssid_in_network, ssid_other_network],
    }
    coordinator.get_network.return_value = MOCK_NETWORK
    return coordinator

def test_network_hub_init(mock_coordinator):
    """Test the initialization of the NetworkHub."""
    hub = NetworkHub(mock_coordinator, MOCK_NETWORK["id"])
    assert hub._coordinator is mock_coordinator
    assert hub.network_id == MOCK_NETWORK["id"]

def test_network_info_property(mock_coordinator):
    """Test the network_info property."""
    hub = NetworkHub(mock_coordinator, MOCK_NETWORK["id"])
    assert hub.network_info == MOCK_NETWORK
    mock_coordinator.get_network.assert_called_once_with(MOCK_NETWORK["id"])

def test_devices_property(mock_coordinator):
    """Test the devices property filters correctly."""
    hub = NetworkHub(mock_coordinator, MOCK_NETWORK["id"])
    devices = hub.devices
    assert len(devices) == 1
    assert devices[0]["networkId"] == MOCK_NETWORK["id"]

def test_ssids_property(mock_coordinator):
    """Test the ssids property filters correctly."""
    hub = NetworkHub(mock_coordinator, MOCK_NETWORK["id"])
    ssids = hub.ssids
    assert len(ssids) == 1
    assert ssids[0]["networkId"] == MOCK_NETWORK["id"]

@pytest.mark.asyncio
async def test_async_update_data(mock_coordinator):
    """Test the async_update_data method."""
    hub = NetworkHub(mock_coordinator, MOCK_NETWORK["id"])
    # This method is a placeholder, so we just call it to ensure no errors
    await hub.async_update_data()
