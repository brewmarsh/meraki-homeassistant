"""Test DataFetchManager feature flags."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.models.network import MerakiNetwork


@pytest.mark.asyncio
async def test_appliance_features_fetching_behavior() -> None:
    """
    Test that appliance features are fetched according to configuration.

    This test verifies that:
    1. When disabled (default), tasks are NOT created.
    2. When enabled, tasks ARE created.
    """
    # Mock Client
    mock_client = MagicMock()
    # Mock semaphores - just return the coroutine passed to it
    async def mock_run_with_semaphore(coro: Any) -> Any:
        return await coro

    mock_client.run_with_semaphore.side_effect = lambda x: x
    mock_client._disabled_features = set()

    # Mock appliance endpoint methods
    mock_client.appliance.get_l3_firewall_rules = AsyncMock(return_value={})
    mock_client.appliance.get_traffic_shaping = AsyncMock(return_value={})
    mock_client.network.get_vlan_data = AsyncMock(return_value=[])
    mock_client.appliance.get_network_vlans = AsyncMock(return_value=[])
    mock_client.appliance.get_vpn_status = AsyncMock(return_value={})
    mock_client.appliance.get_appliance_ports = AsyncMock(return_value=[])
    mock_client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value={}
    )
    mock_client.appliance.get_network_appliance_uplinks_loss_and_latency = AsyncMock(
        return_value=[]
    )
    mock_client.network.get_network_traffic = AsyncMock(return_value=[])

    mock_network = MerakiNetwork(id="net1", product_types=["appliance"])

    # Case 1: Disabled (Default)
    manager_disabled = DataFetchManager(
        client=mock_client,
        enable_firewall_rules=False,
        enable_traffic_shaping=False,
    )
    with patch("asyncio.create_task", side_effect=lambda x: x):
        tasks_disabled = manager_disabled._build_detail_tasks([mock_network], [])

    assert "l3_firewall_rules_net1" not in tasks_disabled
    assert "traffic_shaping_net1" not in tasks_disabled

    # Cleanup coroutines to avoid RuntimeWarning
    for task in tasks_disabled.values():
        await task

    # Case 2: Enabled
    manager_enabled = DataFetchManager(
        client=mock_client,
        enable_firewall_rules=True,
        enable_traffic_shaping=True,
    )
    with patch("asyncio.create_task", side_effect=lambda x: x):
        tasks_enabled = manager_enabled._build_detail_tasks([mock_network], [])

    assert "l3_firewall_rules_net1" in tasks_enabled
    assert "traffic_shaping_net1" in tasks_enabled

    # Cleanup coroutines to avoid RuntimeWarning
    for task in tasks_enabled.values():
        await task
