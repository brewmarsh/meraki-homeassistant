"""Tests for the NetworkHub."""

<<<<<<< HEAD
=======
import dataclasses
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.hubs.network import NetworkHub
from tests.const import MOCK_DEVICE, MOCK_NETWORK


@pytest.fixture
def mock_coordinator_with_devices_and_ssids(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataCoordinator with devices and SSIDs."""
    device_in_network = MOCK_DEVICE.copy()
    device_in_network["networkId"] = MOCK_NETWORK["id"]
    device_other_network = MOCK_DEVICE.copy()
    device_other_network["serial"] = "other_serial"
    device_other_network["networkId"] = "other_network"

    ssid_in_network = {"networkId": MOCK_NETWORK["id"], "name": "SSID in network"}
=======
    """Fixture for a mocked MerakiDataUpdateCoordinator with devices and SSIDs."""
    device_in_network = dataclasses.replace(MOCK_DEVICE, network_id=MOCK_NETWORK.id)
    device_other_network = dataclasses.replace(
        MOCK_DEVICE, serial="other_serial", network_id="other_network"
    )

    ssid_in_network = {"networkId": MOCK_NETWORK.id, "name": "SSID in network"}
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    ssid_other_network = {
        "networkId": "other_network",
        "name": "SSID in other network",
    }

    mock_coordinator.data = {
        "networks": [MOCK_NETWORK],
        "devices": [device_in_network, device_other_network],
        "ssids": [ssid_in_network, ssid_other_network],
    }
    mock_coordinator.get_network.return_value = MOCK_NETWORK
    return mock_coordinator


def test_network_hub_init(mock_coordinator_with_devices_and_ssids: MagicMock) -> None:
    """Test the initialization of the NetworkHub."""
<<<<<<< HEAD
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK["id"])
    assert hub._coordinator is mock_coordinator_with_devices_and_ssids
    assert hub.network_id == MOCK_NETWORK["id"]
=======
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK.id)
    assert hub._coordinator is mock_coordinator_with_devices_and_ssids
    assert hub.network_id == MOCK_NETWORK.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


def test_network_info_property(
    mock_coordinator_with_devices_and_ssids: MagicMock,
) -> None:
    """Test the network_info property."""
<<<<<<< HEAD
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK["id"])
    assert hub.network_info == MOCK_NETWORK
    mock_coordinator_with_devices_and_ssids.get_network.assert_called_once_with(
        MOCK_NETWORK["id"]
=======
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK.id)
    assert hub.network_info == MOCK_NETWORK
    mock_coordinator_with_devices_and_ssids.get_network.assert_called_once_with(
        MOCK_NETWORK.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    )


def test_devices_property(mock_coordinator_with_devices_and_ssids: MagicMock) -> None:
    """Test the devices property filters correctly."""
<<<<<<< HEAD
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK["id"])
    devices = hub.devices
    assert len(devices) == 1
    assert devices[0]["networkId"] == MOCK_NETWORK["id"]
=======
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK.id)
    devices = hub.devices
    assert len(devices) == 1
    assert devices[0].network_id == MOCK_NETWORK.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


def test_ssids_property(mock_coordinator_with_devices_and_ssids: MagicMock) -> None:
    """Test the ssids property filters correctly."""
<<<<<<< HEAD
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK["id"])
    ssids = hub.ssids
    assert len(ssids) == 1
    assert ssids[0]["networkId"] == MOCK_NETWORK["id"]
=======
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK.id)
    ssids = hub.ssids
    assert len(ssids) == 1
    assert ssids[0]["networkId"] == MOCK_NETWORK.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


@pytest.mark.asyncio
async def test_async_update_data(
    mock_coordinator_with_devices_and_ssids: MagicMock,
) -> None:
    """Test the async_update_data method."""
<<<<<<< HEAD
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK["id"])
=======
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, MOCK_NETWORK.id)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    # This method is a placeholder, so we just call it to ensure no errors
    await hub.async_update_data()
