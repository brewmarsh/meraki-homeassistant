"""Tests for the Data Fetch Manager timeouts."""

import asyncio
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
    client.has_dashboard = True
    client.run_with_semaphore = AsyncMock()
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
        side_effect=asyncio.TimeoutError,
    ):
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(asyncio.TimeoutError):
                await data_fetch_manager._async_fetch_initial_data()
            mock_log_error.assert_called_with(
                "Timeout during %s. Potential semaphore deadlock.", "Initial Batch"
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
        side_effect=asyncio.TimeoutError,
    ):
        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(asyncio.TimeoutError):
                await data_fetch_manager.get_all_data()
            # It might be called for detailed data first
            mock_log_error.assert_any_call(
                "Timeout during %s. Potential semaphore deadlock.",
                "Detailed Device Data",
            )


@pytest.mark.asyncio
async def test_get_all_data_client_timeout(data_fetch_manager, mock_client):
    """Test that get_all_data logs error and raises TimeoutError on client timeout."""
    data_fetch_manager._async_fetch_initial_data = AsyncMock(return_value={})

    # We need to bypass the first wait_for (detailed data)
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.asyncio.wait_for"
    ) as mock_wait_for:
        # First call returns empty dict (detail data results)
        mock_wait_for.side_effect = asyncio.TimeoutError

        with patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher._LOGGER.error"
        ) as mock_log_error:
            with pytest.raises(asyncio.TimeoutError):
                await data_fetch_manager.get_all_data()
            mock_log_error.assert_called_with(
                "Timeout during %s. Potential semaphore deadlock.", "Client Data"
            )
