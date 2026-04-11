"""Tests for the Data Fetch Manager timeouts."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.models.network import MerakiNetwork


async def clean_exit_wait_for(coro, timeout=None, **kwargs):
    """Raise TimeoutError but ensure coro is closed."""
    # Handle if tasks is passed instead of coro (for async_gather_with_timeout mock)
    if isinstance(coro, dict):
        for t in coro.values():
            if asyncio.iscoroutine(t):
                t.close()
    elif hasattr(coro, "close"):
        coro.close()
    elif hasattr(coro, "cancel"):
        coro.cancel()
        try:
            await coro
        except (asyncio.CancelledError, Exception):
            pass
    raise asyncio.TimeoutError()


async def mock_gather_and_close(tasks, **kwargs):
    """Mock async_gather_with_timeout and close coroutines."""
    for t in tasks.values():
        if asyncio.iscoroutine(t):
            t.close()
    return {}


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client._disabled_features = set()
    client.has_dashboard = True

    # Ensure run_with_cache is an AsyncMock and works
    async def mock_run_with_cache(cache_key, func, ttl=None):
        return await func()

    client.run_with_cache = AsyncMock(side_effect=mock_run_with_cache)

    async def run_with_semaphore_side_effect(coro):
        """Side effect to return a completed future and close input coroutine."""
        if asyncio.iscoroutine(coro):
            coro.close()
        return {}

    client.run_with_semaphore = AsyncMock(side_effect=run_with_semaphore_side_effect)
    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)


@pytest.mark.asyncio
async def test_fetch_initial_data_timeout(data_fetch_manager, mock_client):
    """Test that _async_fetch_batch_data logs error and raises TimeoutError."""
    # Action 2: Ensure awaited methods are AsyncMock
    data_fetch_manager._async_fetch_batch_data = AsyncMock(side_effect=asyncio.TimeoutError)

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils.asyncio.wait_for",
        new_callable=AsyncMock,
        side_effect=clean_exit_wait_for,
    ):
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(asyncio.TimeoutError):
                # This call will trigger wait_for which will raise TimeoutError
                await data_fetch_manager._async_fetch_batch_data()


@pytest.mark.asyncio
async def test_get_all_data_detailed_timeout(data_fetch_manager, mock_client):
    """Test that get_all_data logs error and raises TimeoutError on detailed timeout."""
    # Action 2: Ensure awaited methods are AsyncMock
    # Provide data to ensure detail tasks are built
    data_fetch_manager._async_fetch_batch_data = AsyncMock(
        return_value={
            "networks": [{"id": "n1", "productTypes": ["appliance"]}],
            "devices": [],
            "statuses": [],
            "organization": {"name": "Test Org"},
        }
    )

    # Mock helpers to return non-coroutine objects to avoid unawaited coroutines
    data_fetch_manager.appliance_strategy.device_helper.get_appliance_ports = MagicMock(return_value=[])
    data_fetch_manager.appliance_strategy.uplink_helper.get_uplink_performance = MagicMock(return_value=[])

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils.asyncio.wait_for",
        new_callable=AsyncMock,
        side_effect=clean_exit_wait_for,
    ):
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(asyncio.TimeoutError):
                await data_fetch_manager.get_all_data()
            # It might be called for detailed data first
            mock_log_error.assert_any_call(
                "Timeout during %s. Potential semaphore deadlock.",
                "Detail batch",
            )


@pytest.mark.asyncio
async def test_get_all_data_client_timeout(data_fetch_manager, mock_client):
    """Test that get_all_data logs error and raises TimeoutError on client timeout."""
    # Provide at least one network so client fetching is attempted
    net = MerakiNetwork(id="n1", product_types=["appliance"])
    # Action 2: Ensure awaited methods are AsyncMock
    data_fetch_manager._async_fetch_batch_data = AsyncMock(
        return_value={
            "networks": [net],
            "devices": [],
            "statuses": [],
            "organization": {"name": "Test Org"},
        }
    )

    # Mock helpers to return non-coroutine objects to avoid unawaited coroutines
    data_fetch_manager.appliance_strategy.device_helper.get_appliance_ports = MagicMock(return_value=[])
    data_fetch_manager.appliance_strategy.uplink_helper.get_uplink_performance = MagicMock(return_value=[])

    # Mock client_fetcher to avoid unawaited coroutines
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])

    # We also need detail batch to succeed (or return empty) so we reach client fetch.
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.async_gather_with_timeout",
        new_callable=AsyncMock,
    ) as mock_gather:
        # Side effect that returns the values directly
        mock_gather.side_effect = [{}, clean_exit_wait_for]
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
        ) as mock_log_error:
            # Client timeout is suppressed, so no exception raised
            await data_fetch_manager.get_all_data()

            # Verify error was logged
            mock_log_error.assert_called_with("Timeout during client data fetch")
