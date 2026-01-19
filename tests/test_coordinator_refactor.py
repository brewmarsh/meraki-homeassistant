"""Tests for the Meraki data coordinator refactor."""

from dataclasses import is_dataclass
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
from tests.const import MOCK_DEVICE, MOCK_NETWORK


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock()
    return client

@pytest.fixture
def coordinator(hass, mock_api_client):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MagicMock()
    entry.options = {}
    return MerakiDataCoordinator(
        hass=hass, api_client=mock_api_client, scan_interval=300, entry=entry
    )

@pytest.mark.asyncio
async def test_coordinator_returns_objects(coordinator, mock_api_client):
    """Test that coordinator converts dicts to objects."""
    # Arrange
    mock_data = {
        "networks": [MOCK_NETWORK],
        "devices": [MOCK_DEVICE],
    }
    mock_api_client.get_all_data.return_value = mock_data

    # Act
    await coordinator._async_update_data()

    # Assert
    # Check device
    device = coordinator.get_device(MOCK_DEVICE.serial)
    assert device is not None
    assert is_dataclass(device)
    assert isinstance(device, MerakiDevice)
    assert device.serial == MOCK_DEVICE.serial
    assert device.name == MOCK_DEVICE.name

    # Check network
    network = coordinator.get_network(MOCK_NETWORK.id)
    assert network is not None
    assert is_dataclass(network)
    assert isinstance(network, MerakiNetwork)
    assert network.id == MOCK_NETWORK.id

@pytest.mark.asyncio
async def test_status_messages_update_objects(coordinator, mock_api_client):
    """Test that status messages are added to objects."""
    # Arrange
    mock_data = {
        "networks": [MOCK_NETWORK],
        "devices": [MOCK_DEVICE],
    }
    mock_api_client.get_all_data.return_value = mock_data
    data = await coordinator._async_update_data()
    coordinator.data = data

    # Act
    coordinator.add_status_message(MOCK_DEVICE.serial, "Test Message")

    # Assert
    device = coordinator.get_device(MOCK_DEVICE.serial)
    assert "Test Message" in device.status_messages

    # Check data dict (which are objects now)
    device_obj = coordinator.data["devices"][0]
    assert "Test Message" in device_obj.status_messages
