"""Tests for the appliance uplink fallback logic."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.core.api.endpoints.appliance import ApplianceEndpoints
from tests.const import MOCK_NETWORK

@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    # Mock run_sync to just call the function passed to it
    async def side_effect(func, *args, **kwargs):
        if callable(func):
            return func(*args, **kwargs)
        return func
    client.run_sync.side_effect = side_effect
    return client

@pytest.fixture
def appliance_endpoints(mock_api_client):
    """Fixture for an ApplianceEndpoints instance."""
    return ApplianceEndpoints(mock_api_client, MagicMock())

@pytest.mark.asyncio
async def test_get_uplink_performance_tries_all_names(appliance_endpoints, mock_api_client):
    """Test that it tries all three SDK method names and returns empty list if none found."""
    # Setup mock dashboard with none of the methods
    mock_appliance = MagicMock(spec=[]) # Ensure no attributes exist

    mock_api_client.dashboard.appliance = mock_appliance

    # Call the method
    result = await appliance_endpoints.get_network_appliance_uplinks_performance(MOCK_NETWORK.id)

    assert result == []

@pytest.mark.asyncio
async def test_get_uplink_performance_uses_first_available(appliance_endpoints, mock_api_client):
    """Test that it uses the first available SDK method."""
    mock_appliance = MagicMock(spec=["getNetworkApplianceUplinksLossAndLatency"])

    # Mock the second one
    mock_method = MagicMock(return_value=[{"test": "data"}])
    mock_appliance.getNetworkApplianceUplinksLossAndLatency = mock_method

    mock_api_client.dashboard.appliance = mock_appliance

    # Call the method
    result = await appliance_endpoints.get_network_appliance_uplinks_performance(MOCK_NETWORK.id)

    assert result == [{"test": "data"}]
    # Note: run_sync is called with (method, networkId=network_id)
    # Our side_effect calls method(networkId=network_id)
    mock_method.assert_called_once_with(networkId=MOCK_NETWORK.id)

@pytest.mark.asyncio
async def test_get_uplink_performance_prefers_usage_history(appliance_endpoints, mock_api_client):
    """Test that it prefers UsageHistory and passes timespan=60."""
    mock_appliance = MagicMock(spec=[
        "getNetworkApplianceUplinksUsageHistory",
        "getNetworkApplianceUplinksLossAndLatency"
    ])

    mock_method1 = MagicMock(return_value=[{"variant": "history"}])
    mock_method2 = MagicMock(return_value=[{"variant": "loss_latency"}])

    mock_appliance.getNetworkApplianceUplinksUsageHistory = mock_method1
    mock_appliance.getNetworkApplianceUplinksLossAndLatency = mock_method2

    mock_api_client.dashboard.appliance = mock_appliance

    result = await appliance_endpoints.get_network_appliance_uplinks_performance(MOCK_NETWORK.id)

    assert result == [{"variant": "history"}]
    mock_method1.assert_called_once_with(networkId=MOCK_NETWORK.id, timespan=60)
    mock_method2.assert_not_called()

@pytest.mark.asyncio
async def test_get_uplink_performance_falls_back_from_usage_history(appliance_endpoints, mock_api_client):
    """Test that it falls back from UsageHistory if it's missing."""
    mock_appliance = MagicMock(spec=["getNetworkApplianceUplinksLossAndLatency"])

    mock_method = MagicMock(return_value=[{"variant": "loss_latency"}])
    mock_appliance.getNetworkApplianceUplinksLossAndLatency = mock_method

    mock_api_client.dashboard.appliance = mock_appliance

    result = await appliance_endpoints.get_network_appliance_uplinks_performance(MOCK_NETWORK.id)

    assert result == [{"variant": "loss_latency"}]
    mock_method.assert_called_once()
