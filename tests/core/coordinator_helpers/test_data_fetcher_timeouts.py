"""Tests for the Data Fetch Manager timeouts."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)


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
            with pytest.raises(asyncio.TimeoutError):
                await data_fetch_manager.get_all_data()
            # It might be called for detailed data first
            mock_log_error.assert_any_call(
                "Timeout during %s. Potential semaphore deadlock.",
                "Detailed device data",
            )


@pytest.mark.asyncio
async def test_get_all_data_client_timeout(data_fetch_manager, mock_client):
    """Test that get_all_data logs error and raises TimeoutError on client timeout."""
    data_fetch_manager._async_fetch_initial_data = AsyncMock(return_value={})

    # We need to bypass the first wait_for (detailed data) - wait, if initial
    # data is empty, detail tasks are empty, so wait_for is NOT called for
    # detailed data. So the first call to wait_for IS for client data.
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.ClientFetcher.async_fetch_network_clients",
        new_callable=MagicMock,
    ) as mock_fetch:
        f = asyncio.Future()
        f.set_result([])
        mock_fetch.return_value = f

        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.asyncio.wait_for",
            side_effect=clean_exit_wait_for,
        ) as mock_wait_for:

            with patch(
                "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
            ) as mock_log_error:
                with pytest.raises(asyncio.TimeoutError):
                    await data_fetch_manager.get_all_data()
                mock_log_error.assert_called_with(
                    "Timeout during %s. Potential semaphore deadlock.", "Client data"
                )
                # Verify called once
                assert mock_wait_for.call_count == 1
