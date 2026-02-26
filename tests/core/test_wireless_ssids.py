"""Tests for Wireless SSIDs fetching and processing."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)


@pytest.fixture
def mock_client():
    """Mock Meraki API client."""
    client = MagicMock()
    client._disabled_features = set()
    client.has_dashboard = True

    # Mock run_with_semaphore to be a simple pass-through for tests
    async def run_with_sem(coro):
        return await coro
    client.run_with_semaphore = run_with_sem

    return client

@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)

@pytest.mark.asyncio
async def test_wireless_ssids_processing(data_fetch_manager, mock_client):
    """Test that wireless SSIDs are correctly processed and added to data."""
    # Mock initial data return
    data_fetch_manager._async_fetch_initial_data = AsyncMock(return_value={
        "networks": [{"id": "N_123", "name": "Test Network", "productTypes": ["wireless"]}],
        "devices": [],
    })

    # Mock client fetcher to avoid errors
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    data_fetch_manager.client_fetcher.derive_device_clients = MagicMock(return_value={})

    # Mock the strategy to add a task that returns SSIDs
    # This simulates what build_network_tasks does (adding a task to the dict)
    async def mock_ssid_task():
        return [{"number": 1, "name": "Test SSID", "enabled": True}]

    # We need to ensure that when _build_strategy_tasks runs, it populates 'ssids_N_123'
    # The real implementation calls strategy.build_network_tasks.
    # We can mock strategy.build_network_tasks to add our mock task.

    data_fetch_manager.wireless_strategy.build_network_tasks = MagicMock(
        side_effect=lambda nid, pts, tks: tks.update({f"ssids_{nid}": mock_ssid_task()})
    )

    # Act
    data = await data_fetch_manager.get_all_data()

    # Assert
    assert "ssids" in data
    ssids = data["ssids"]
    assert len(ssids) == 1
    assert ssids[0]["name"] == "Test SSID"
    assert ssids[0]["networkId"] == "N_123"
    assert ssids[0]["number"] == 1

    assert "wireless_settings" in data
    assert "N_123" in data["wireless_settings"]
    assert len(data["wireless_settings"]["N_123"]) == 1
