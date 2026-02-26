"""Tests for the Data Fetch Manager timeouts."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.models.network import MerakiNetwork


async def clean_exit_wait_for(coro, timeout=None):
    """Raise TimeoutError but ensure coro is closed."""
    if hasattr(coro, "close"):
        coro.close()
    elif hasattr(coro, "cancel"):
        coro.cancel()
        try:
            await coro
        except (asyncio.CancelledError, Exception):
            pass
    raise asyncio.TimeoutError()


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client._disabled_features = set()
    client.has_dashboard = True

    def run_with_semaphore_side_effect(coro):
        """Side effect to return a completed future and close input coroutine."""
        if asyncio.iscoroutine(coro):
            coro.close()
        f = asyncio.Future()
        f.set_result({})
        return f

    client.run_with_semaphore = MagicMock(side_effect=run_with_semaphore_side_effect)
    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)


@pytest.mark.asyncio
async def test_fetch_initial_data_timeout(data_fetch_manager, mock_client):
    """Test that _async_fetch_initial_data logs error and raises TimeoutError."""
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.asyncio.wait_for",
        side_effect=clean_exit_wait_for,
    ):
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(asyncio.TimeoutError):
                await data_fetch_manager._async_fetch_initial_data()
            mock_log_error.assert_called_with(
                "Timeout during %s. Potential semaphore deadlock.", "Initial batch"
            )


@pytest.mark.asyncio
async def test_get_all_data_detailed_timeout(data_fetch_manager, mock_client):
    """Test that get_all_data logs error and raises TimeoutError on detailed timeout."""
    # Provide data to ensure detail tasks are built
    data_fetch_manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [{"id": "n1", "productTypes": ["appliance"]}],
            "devices": [],
        }
    )

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.asyncio.wait_for",
        side_effect=clean_exit_wait_for,
    ):
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(UpdateFailed):
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
    MerakiNetwork(id="n1", product_types=["appliance"])
    data_fetch_manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [{"id": "n1", "productTypes": ["appliance"]}], # Raw data
            "devices": [],
        }
    )

    # We also need detail batch to succeed (or return empty) so we reach client fetch.
    # But wait_for is patched globally to fail!
    # So the first wait_for (Detail batch) will fail and raise TimeoutError.
    # And we won't reach Client data timeout.

    # We need to make the first wait_for SUCCEED, and second one FAIL.

    async def side_effect(coro, timeout=None):
        # Inspect coro to guess which call it is?
        # Or use side_effect iterable.
        pass

    # Using side_effect iterator
    async def success_wait_for(coro, timeout=None):
        return await coro

    # But wait_for wraps _execute_batches or client fetcher.
    # _execute_batches returns list.

    # If we mock wait_for, we must return what it expects.
    # Detail batch returns dict (from _process_batch_results inside _async_gather_with_timeout).
    # Wait, _async_gather_with_timeout calls wait_for.

    # Let's mock _async_gather_with_timeout to succeed.
    data_fetch_manager._async_gather_with_timeout = AsyncMock(return_value={})

    # Now get_all_data proceeds to client fetch.

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.ClientFetcher.async_fetch_network_clients",
        new_callable=MagicMock,
    ):
        asyncio.Future()
        # The future hangs or we mock wait_for to raise.

        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.asyncio.wait_for",
            side_effect=clean_exit_wait_for,
        ):
            with patch(
                "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
            ) as mock_log_error:
                # Client timeout is suppressed, so no exception raised
                await data_fetch_manager.get_all_data()

                # Verify error was logged - message changed slightly in implementation
                mock_log_error.assert_called_with(
                    "Timeout during client data fetch"
                )
