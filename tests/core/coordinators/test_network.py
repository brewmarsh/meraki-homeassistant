"""Tests for the Meraki network coordinator."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.meraki_ha.core.coordinators.network import MerakiNetworkCoordinator

@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_networks = AsyncMock(return_value=[
        {'id': 'net1', 'name': 'Network 1', 'productTypes': ['wireless']},
        {'id': 'net2', 'name': 'Network 2', 'productTypes': ['switch']},
    ])
    client.get_network_clients = AsyncMock(return_value=[{'mac': 'client1'}])
    client.get_ssids = AsyncMock(return_value=[{'number': 0, 'name': 'SSID 1'}])
    return client

@pytest.fixture
async def network_coordinator(mock_api_client):
    """Fixture for a MerakiNetworkCoordinator with a mocked API client."""
    coordinator = MerakiNetworkCoordinator(
        hass=MagicMock(),
        api_client=mock_api_client,
        name='network_coordinator',
        update_interval=MagicMock(),
    )
    await coordinator.async_config_entry_first_refresh()
    return coordinator

async def test_network_coordinator_data(network_coordinator):
    """Test that the network coordinator fetches and processes data correctly."""
    assert network_coordinator.data is not None
    assert len(network_coordinator.data['networks']) == 2
    assert len(network_coordinator.data['clients']) == 2
    assert len(network_coordinator.data['ssids']) == 1
    assert network_coordinator.data['networks'][0]['id'] == 'net1'
    assert network_coordinator.data['clients'][0]['mac'] == 'client1'
    assert network_coordinator.data['ssids'][0]['name'] == 'SSID 1'

async def test_get_network_by_id(network_coordinator):
    """Test getting a network by its ID."""
    network = network_coordinator.get_network_by_id('net1')
    assert network is not None
    assert network['id'] == 'net1'
    assert network_coordinator.get_network_by_id('net3') is None

async def test_ssid_filtering(mock_api_client):
    """Test that disabled SSIDs are filtered out."""
    mock_api_client.get_ssids.return_value = [
        {'number': 0, 'name': 'Enabled SSID', 'enabled': True},
        {'number': 1, 'name': 'Disabled SSID', 'enabled': False},
    ]
    coordinator = MerakiNetworkCoordinator(
        hass=MagicMock(),
        api_client=mock_api_client,
        name='network_coordinator',
        update_interval=MagicMock(),
    )
    await coordinator.async_config_entry_first_refresh()
    assert len(coordinator.data['ssids']) == 1
    assert coordinator.data['ssids'][0]['name'] == 'Enabled SSID'
