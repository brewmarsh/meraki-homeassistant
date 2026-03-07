"""Tests for the Data Fetch Manager."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client._disabled_features = set()
    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)


@pytest.mark.asyncio
async def test_get_sensor_data_includes_switch_ports(data_fetch_manager, mock_client):
    """Test that get_sensor_data returns switch ports statuses."""
    # Arrange - Using the cleaner 'beta' naming
    switch_device_dict = {"serial": "Q123", "productType": "switch"}
    data_fetch_manager._async_fetch_batch_data = AsyncMock(
        return_value={
            "networks": [],
            "devices": [switch_device_dict],
            "switch_ports": [{"serial": "Q123", "portId": "1", "status": "Connected"}]
        }
    )
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        return_value=[]
    )
    data_fetch_manager.client_fetcher.async_fetch_device_clients = AsyncMock(
        return_value={}
    )

    # Simulate detailed switch ports response
    async def mock_build_strategy_tasks(data):
        data["switch_ports_Q123"] = [{"portId": "1", "status": "Connected"}]

    data_fetch_manager._build_strategy_tasks = AsyncMock(
        side_effect=mock_build_strategy_tasks
    )

    with (
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"
        ),
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"
        ),
    ):
        # Act
        result = await data_fetch_manager.get_sensor_data()

    # Assert - Verifying that the strategy correctly injected data
    # into the device object
    assert result["devices"][0].switch_ports == [{"portId": "1", "status": "Connected"}]


@pytest.mark.asyncio
async def test_get_device_data_excludes_switch_ports(data_fetch_manager, mock_client):
    """Test that get_device_data does not fetch switch ports."""
    # Arrange
    switch_device_dict = {"serial": "Q123", "productType": "switch"}
    data_fetch_manager._async_fetch_batch_data = AsyncMock(
        return_value={
            "networks": [],
            "devices": [switch_device_dict],
        }
    )
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock()

    with (
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"
        ),
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"
        ),
    ):
        # Act
        result = await data_fetch_manager.get_device_data()

    # Assert
    data_fetch_manager._async_fetch_batch_data.assert_called_with(fast_only=True)
    assert not hasattr(result["devices"][0], "switch_ports") or not result["devices"][0].switch_ports


@pytest.mark.asyncio
async def test_async_gather_with_timeout_batching(data_fetch_manager):
    """Test that tasks are executed in batches."""
    # Create 12 tasks
    tasks = {f"task_{i}": AsyncMock(return_value={"id": i})() for i in range(12)}

    # We want to verify that there are sleeps between batches
    # BATCH_SIZE = 5, so 12 tasks = 3 batches (5, 5, 2)
    # Expected sleeps: 2 (one after batch 1, one after batch 2)

    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import (
            async_gather_with_timeout,
        )
        results = await async_gather_with_timeout(
            tasks, label="Test Batching"
        )

        assert len(results) == 12
        for i in range(12):
            assert results[f"task_{i}"] == {"id": i}

        # Verify batching logic
        assert mock_sleep.call_count == 2
        mock_sleep.assert_called_with(1.0)

@pytest.mark.asyncio
async def test_async_gather_with_timeout_custom_batching(data_fetch_manager):
    """Test that tasks are executed with custom batch size and cooldown."""
    tasks = {f"task_{i}": AsyncMock(return_value={"id": i})() for i in range(12)}

    # batch_size=10, so 12 tasks = 2 batches (10, 2)
    # Expected sleeps: 1 (one after batch 1)

    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import (
            async_gather_with_timeout,
        )
        results = await async_gather_with_timeout(
            tasks, label="Test Custom Batching", batch_size=10, cooldown=0.5
        )

        assert len(results) == 12
        assert mock_sleep.call_count == 1
        mock_sleep.assert_called_with(0.5)
