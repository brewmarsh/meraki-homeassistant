"""Tests for the appliance uplink fallback logic."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.api.endpoints.appliance import (
    ApplianceEndpoints,
)


@pytest.fixture
def mock_dashboard():
    """Fixture for a mocked meraki.DashboardAPI instance."""
    with patch("meraki.DashboardAPI") as mock_dashboard_class:
        dashboard = mock_dashboard_class.return_value
        # Ensure the appliance attribute is a MagicMock so we can attach methods to it
        dashboard.appliance = MagicMock()
        yield dashboard


@pytest.fixture
def hass():
    """Fixture for a mocked Home Assistant instance."""
    return MagicMock()


@pytest.fixture
def api_client(hass, mock_dashboard):
    """Fixture for a MerakiAPIClient instance."""
    client = MerakiAPIClient(hass=hass, api_key="test-key", org_id="test-org")
    client.dashboard = mock_dashboard

    # Mock run_sync to execute the function directly
    async def mock_run_sync(func, *args, **kwargs):
        return func(*args, **kwargs)

    client.run_sync = MagicMock(side_effect=mock_run_sync)
    return client


@pytest.fixture
def appliance_endpoints(api_client, hass):
    """Fixture for an ApplianceEndpoints instance."""
    return ApplianceEndpoints(api_client, hass)


@pytest.mark.asyncio
async def test_uplink_fallback_usage_history(appliance_endpoints, mock_dashboard):
    """Test fallback to getNetworkApplianceUplinksUsageHistory."""
    # Setup the method existence
    mock_method = MagicMock(return_value=[{"serial": "Q234", "uplinks": []}])

    # 1. UsageHistory
    mock_dashboard.appliance = MagicMock(
        spec=["getNetworkApplianceUplinksUsageHistory"]
    )
    mock_dashboard.appliance.getNetworkApplianceUplinksUsageHistory = mock_method

    result = await appliance_endpoints.get_network_appliance_uplinks_performance("N123")

    assert result == [{"serial": "Q234", "uplinks": []}]
    mock_dashboard.appliance.getNetworkApplianceUplinksUsageHistory.assert_called_with(
        networkId="N123", timespan=60
    )


@pytest.mark.asyncio
async def test_uplink_fallback_loss_latency(appliance_endpoints, mock_dashboard):
    """Test fallback to getNetworkApplianceUplinksLossAndLatency."""
    mock_method = MagicMock(return_value=[])

    # Only have the second method
    mock_dashboard.appliance = MagicMock(
        spec=["getNetworkApplianceUplinksLossAndLatency"]
    )
    mock_dashboard.appliance.getNetworkApplianceUplinksLossAndLatency = mock_method

    await appliance_endpoints.get_network_appliance_uplinks_performance("N123")

    mock_dashboard.appliance.getNetworkApplianceUplinksLossAndLatency.assert_called_with(
        networkId="N123"
    )


@pytest.mark.asyncio
async def test_uplink_fallback_uplinks_loss_latency(
    appliance_endpoints, mock_dashboard
):
    """Test fallback to getNetworkApplianceUplinksUplinksLossAndLatency."""
    mock_method = MagicMock(return_value=[])

    # Only have the third method
    mock_dashboard.appliance = MagicMock(
        spec=["getNetworkApplianceUplinksUplinksLossAndLatency"]
    )
    mock_dashboard.appliance.getNetworkApplianceUplinksUplinksLossAndLatency = (
        mock_method
    )

    await appliance_endpoints.get_network_appliance_uplinks_performance("N123")

    mock_dashboard.appliance.getNetworkApplianceUplinksUplinksLossAndLatency.assert_called_with(
        networkId="N123"
    )


@pytest.mark.asyncio
async def test_uplink_fallback_none(appliance_endpoints, mock_dashboard):
    """Test when no method is found."""
    mock_dashboard.appliance = MagicMock(spec=[])

    result = await appliance_endpoints.get_network_appliance_uplinks_performance("N123")

    assert result == []
