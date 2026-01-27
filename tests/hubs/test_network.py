"""Tests for the NetworkHub."""

import dataclasses
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.hubs.network import NetworkHub
from tests.const import MOCK_DEVICE, MOCK_NETWORK


@pytest.fixture
def mock_coordinator_with_devices_and_ssids(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with devices and SSIDs."""
    device_in_network = dataclasses.replace(MOCK_DEVICE, network_id=MOCK_NETWORK.id)
    device_other_network = dataclasses.replace(
        MOCK_DEVICE, serial="other_serial", network_id="other_network"
    )

    ssid_in_network = {"networkId": MOCK_NETWORK.id, "name": "SSID in network"}
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
    network_id: str = MOCK_NETWORK.id or "test_network"
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, network_id)
    assert hub._coordinator is mock_coordinator_with_devices_and_ssids
    assert hub.network_id == network_id


def test_network_info_property(
    mock_coordinator_with_devices_and_ssids: MagicMock,
) -> None:
    """Test the network_info property."""
    network_id: str = MOCK_NETWORK.id or "test_network"
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, network_id)
    assert hub.network_info == MOCK_NETWORK
    mock_coordinator_with_devices_and_ssids.get_network.assert_called_once_with(
        network_id
    )


def test_devices_property(mock_coordinator_with_devices_and_ssids: MagicMock) -> None:
    """Test the devices property filters correctly."""
    network_id: str = MOCK_NETWORK.id or "test_network"
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, network_id)
    devices = hub.devices
    assert len(devices) == 1
    assert devices[0].network_id == network_id


def test_ssids_property(mock_coordinator_with_devices_and_ssids: MagicMock) -> None:
    """Test the ssids property filters correctly."""
    network_id: str = MOCK_NETWORK.id or "test_network"
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, network_id)
    ssids = hub.ssids
    assert len(ssids) == 1
    assert ssids[0]["networkId"] == network_id


@pytest.mark.asyncio
async def test_async_update_data(
    mock_coordinator_with_devices_and_ssids: MagicMock,
) -> None:
    """Test the async_update_data method."""
    network_id: str = MOCK_NETWORK.id or "test_network"
    hub = NetworkHub(mock_coordinator_with_devices_and_ssids, network_id)
    # This method is a placeholder, so we just call it to ensure no errors
    await hub.async_update_data()
