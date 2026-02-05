"""Tests for get_vlan_data in Network Endpoints."""

from unittest.mock import AsyncMock, MagicMock
import pytest
import meraki
from custom_components.meraki_ha.core.api.endpoints.network import NetworkEndpoints
from custom_components.meraki_ha.core.errors import MerakiVlansDisabledError

@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.organization = MagicMock()
    client.organization.get_organization_networks = AsyncMock()
    client.run_sync = AsyncMock()
    return client

@pytest.fixture
def network_endpoints(mock_client):
    """Fixture for the NetworkEndpoints."""
    return NetworkEndpoints(mock_client)

@pytest.mark.asyncio
async def test_get_vlan_data_supported_appliance(network_endpoints, mock_client):
    """Test get_vlan_data with a supported appliance network."""
    network_id = "net123"
    mock_client.organization.get_organization_networks.return_value = [
        {"id": network_id, "productTypes": ["appliance"]}
    ]
    mock_vlan_data = [{"id": "vlan1"}]
    mock_client.run_sync.return_value = mock_vlan_data

    result = await network_endpoints.get_vlan_data(network_id)

    assert result == mock_vlan_data
    mock_client.run_sync.assert_called_with(
        mock_client.dashboard.appliance.getNetworkApplianceVlans,
        networkId=network_id
    )

@pytest.mark.asyncio
async def test_get_vlan_data_unsupported_network(network_endpoints, mock_client):
    """Test get_vlan_data with a network that does not support appliance."""
    network_id = "net123"
    mock_client.organization.get_organization_networks.return_value = [
        {"id": network_id, "productTypes": ["wireless"]}
    ]

    result = await network_endpoints.get_vlan_data(network_id)

    assert result == []
    mock_client.run_sync.assert_not_called()

@pytest.mark.asyncio
async def test_get_vlan_data_no_appliance_attr(network_endpoints, mock_client):
    """Test get_vlan_data when appliance attribute is missing on dashboard."""
    network_id = "net123"
    mock_client.organization.get_organization_networks.return_value = [
        {"id": network_id, "productTypes": ["appliance"]}
    ]
    # Specifically set appliance to None to trigger the safe attribute check
    type(mock_client.dashboard).appliance = property(lambda x: None)

    result = await network_endpoints.get_vlan_data(network_id)

    assert result == []

@pytest.mark.asyncio
async def test_get_vlan_data_vlan_disabled_fallback(network_endpoints, mock_client):
    """Test get_vlan_data fallback when VLANs are disabled."""
    network_id = "net123"
    mock_client.organization.get_organization_networks.return_value = [
        {"id": network_id, "productTypes": ["appliance"]}
    ]

    # First call raises MerakiVlansDisabledError
    # Second call (fallback) returns data
    mock_client.run_sync.side_effect = [
        MerakiVlansDisabledError("VLANs are not enabled"),
        [{"id": "vlan_fallback"}]
    ]

    result = await network_endpoints.get_vlan_data(network_id)

    assert result == [{"id": "vlan_fallback"}]
    assert mock_client.run_sync.call_count == 2
    # Verify both calls used the appliance endpoint
    mock_client.run_sync.assert_called_with(
        mock_client.dashboard.appliance.getNetworkApplianceVlans,
        networkId=network_id
    )
