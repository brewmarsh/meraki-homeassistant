"""Tests for the Network Endpoints."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.api.endpoints.network import NetworkEndpoints


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.dashboard.networks.getNetworkGroupPolicies = AsyncMock()
    return client


@pytest.fixture
def network(mock_client):
    """Fixture for the NetworkEndpoints."""
    return NetworkEndpoints(mock_client)


async def test_get_group_policies(network, mock_client):
    """Test get_group_policies."""
    mock_data = [{"groupPolicyId": "gp1"}]
    mock_client.dashboard.networks.getNetworkGroupPolicies = AsyncMock(
        return_value=mock_data
    )

    result = await network.get_group_policies("net1")

    assert result == mock_data
    mock_client.dashboard.networks.getNetworkGroupPolicies.assert_called_once_with(
        networkId="net1"
    )
