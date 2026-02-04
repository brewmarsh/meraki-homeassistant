"""Tests for the Network Endpoints."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.api.endpoints.network import NetworkEndpoints


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.run_sync = AsyncMock()
    client.run_with_semaphore = AsyncMock(side_effect=lambda x: x)
    return client


@pytest.fixture
def network(mock_client):
    """Fixture for the NetworkEndpoints."""
    return NetworkEndpoints(mock_client)


async def test_get_group_policies(network, mock_client):
    """Test get_group_policies."""
    mock_data = [{"groupPolicyId": "gp1"}]
    mock_client.run_sync.return_value = mock_data

    result = await network.get_group_policies("net1")

    assert result == mock_data
    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    assert kwargs["networkId"] == "net1"


@pytest.mark.asyncio
async def test_get_network_events_filters_none(network, mock_client):
    """Test that get_network_events filters out None values from arguments."""
    # Arrange
    mock_client.dashboard.networks.getNetworkEvents.return_value = {"events": []}
    mock_client.run_sync.return_value = {"events": []}
    network_id = "N_123"

    # Act
    await network.get_network_events(network_id)

    # Assert
    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    # First arg to run_sync is function, second is network_id
    assert args[0] == mock_client.dashboard.networks.getNetworkEvents
    assert args[1] == network_id
    # Ensure no None values in kwargs
    for key, value in kwargs.items():
        assert value is not None, f"Found None value for key: {key}"
    # Specifically check that productType is not in kwargs
    assert "productType" not in kwargs


@pytest.mark.asyncio
async def test_get_network_events_passes_values(network, mock_client):
    """Test that get_network_events passes non-None values correctly."""
    # Arrange
    mock_client.dashboard.networks.getNetworkEvents.return_value = {"events": []}
    mock_client.run_sync.return_value = {"events": []}
    network_id = "N_123"
    product_type = "appliance"

    # Act
    await network.get_network_events(network_id, product_type=product_type)

    # Assert
    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    assert kwargs.get("productType") == product_type
