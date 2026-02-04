"""Test DataFetchManager feature flags."""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.types import MerakiNetwork


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

    # Mock appliance endpoint methods
    mock_client.appliance.get_l3_firewall_rules = AsyncMock(return_value={})
    mock_client.appliance.get_traffic_shaping = AsyncMock(return_value={})
    mock_client.appliance.get_network_vlans = AsyncMock(return_value=[])
    mock_client.appliance.get_vpn_status = AsyncMock(return_value={})
    mock_client.appliance.get_appliance_ports = AsyncMock(return_value=[])
    mock_client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value={}
    )
    mock_client.network.get_network_traffic = AsyncMock(return_value=[])

    # Mock Network
    MerakiNetwork(
        id="net1",
        organization_id="org1",
        product_types=["appliance"],
        name="Test Network",
        time_zone="UTC",
        tags=[],
        notes=None,
    )

    # Case 1: Disabled (Default)
    manager_disabled = DataFetchManager(
        client=mock_client,
        enable_firewall_rules=False,
        enable_traffic_shaping=False
    )
    tasks_disabled: dict[str, asyncio.Task[Any]] = {}
    manager_disabled._build_appliance_network_tasks("net1", tasks_disabled)

    assert "l3_firewall_rules_net1" not in tasks_disabled
    assert "traffic_shaping_net1" not in tasks_disabled

    # Cleanup tasks
    for task in tasks_disabled.values():
        task.cancel()

    # Case 2: Enabled
    manager_enabled = DataFetchManager(
        client=mock_client,
        enable_firewall_rules=True,
        enable_traffic_shaping=True
    )
    tasks_enabled: dict[str, asyncio.Task[Any]] = {}
    manager_enabled._build_appliance_network_tasks("net1", tasks_enabled)

    assert "l3_firewall_rules_net1" in tasks_enabled
    assert "traffic_shaping_net1" in tasks_enabled

    # Cleanup tasks
    for task in tasks_enabled.values():
        task.cancel()
