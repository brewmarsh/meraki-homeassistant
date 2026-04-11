"""Tests for ApplianceFetchStrategy uplink performance."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.fetch_strategies.appliance import (
    ApplianceFetchStrategy,
)
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture
def mock_client():
    """Fixture for a mock Meraki API client."""
    client = MagicMock()
    client.run_with_semaphore.side_effect = lambda x: x
    # Mock dashboard.appliance
    client.dashboard = MagicMock()
    client.dashboard.appliance = MagicMock()

    # Mock run_sync to execute the function directly
    async def mock_run_sync(func, *args, **kwargs):
        return func(*args, **kwargs)

    client.run_sync.side_effect = mock_run_sync

    return client


@pytest.fixture
def strategy(mock_client):
    """Fixture for the ApplianceFetchStrategy."""
    return ApplianceFetchStrategy(
        client=mock_client,
        _disabled_features=set(),
        enable_vpn_management=False,
        enable_firewall_rules=False,
        enable_traffic_shaping=False,
    )


@pytest.mark.asyncio
async def test_get_uplink_performance_usage_history(strategy, mock_client):
    """Test fetching uplink performance via UsageHistory."""
    mock_data = [{"serial": "SERIAL1", "interface": "wan1", "lossPercent": 0.1}]
    mock_client.dashboard.appliance.getNetworkApplianceUplinksUsageHistory = MagicMock(
        return_value=mock_data
    )

    result = await strategy.uplink_helper.get_uplink_performance("net1")

    assert result == mock_data
    mock_client.dashboard.appliance.getNetworkApplianceUplinksUsageHistory.assert_called_once_with(
        networkId="net1", timespan=60
    )


@pytest.mark.asyncio
async def test_get_uplink_performance_fallback(strategy, mock_client):
    """Test fetching uplink performance with fallback."""
    # First method fails
    mock_client.dashboard.appliance.getNetworkApplianceUplinksUsageHistory = MagicMock(
        side_effect=Exception("Failed")
    )
    # Second method succeeds
    mock_data = [{"serial": "SERIAL1", "interface": "wan1", "lossPercent": 0.2}]
    mock_client.dashboard.appliance.getNetworkApplianceUplinksLossAndLatency = (
        MagicMock(return_value=mock_data)
    )

    result = await strategy.uplink_helper.get_uplink_performance("net1")

    assert result == mock_data
    mock_client.dashboard.appliance.getNetworkApplianceUplinksLossAndLatency.assert_called_once_with(
        networkId="net1"
    )


@pytest.mark.asyncio
async def test_get_uplink_performance_legacy_fallback(strategy, mock_client):
    """Test fetching uplink performance with legacy fallback."""
    # First and second methods fail
    mock_client.dashboard.appliance.getNetworkApplianceUplinksUsageHistory = MagicMock(
        side_effect=Exception("Failed")
    )
    mock_client.dashboard.appliance.getNetworkApplianceUplinksLossAndLatency = (
        MagicMock(side_effect=Exception("Failed"))
    )
    # Third method succeeds
    mock_data = [{"serial": "SERIAL1", "interface": "wan1", "loss": 0.3}]
    mock_client.dashboard.appliance.getNetworkApplianceUplinksPerformance = MagicMock(
        return_value=mock_data
    )

    result = await strategy.uplink_helper.get_uplink_performance("net1")

    assert result == mock_data
    mock_client.dashboard.appliance.getNetworkApplianceUplinksPerformance.assert_called_once_with(
        networkId="net1"
    )


def test_process_device_details_normalization(strategy):
    """Test that performance data keys are normalized."""
    mock_device = MagicMock(spec=MerakiDevice)
    mock_device.serial = "SERIAL1"
    mock_device.network_id = "net1"
    mock_device.appliance_uplink_statuses = []

    detail_data = {
        "uplink_performance_net1": [
            {
                "serial": "SERIAL1",
                "interface": "wan1",
                "loss": 1.5,
                "latency": 25,
            }
        ]
    }

    strategy.process_device_details(mock_device, detail_data, None)

    # Check that uplinks was updated with normalized keys
    assert len(mock_device.uplinks) == 1
    uplink = mock_device.uplinks[0]
    assert uplink["lossPercent"] == 1.5
    assert uplink["latencyMs"] == 25
    # Original keys should still be there
    assert uplink["loss"] == 1.5
    assert uplink["latency"] == 25
