"""Tests for the Data Fetch Manager sanitization logic."""

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
    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)


@pytest.mark.asyncio
async def test_async_gather_with_timeout_sanitization(data_fetch_manager):
    """Test that _async_gather_with_timeout sanitizes exceptions and types."""

    async def success_coro():
        return {"data": "ok"}

    async def error_coro():
        raise ValueError("API Error")

    async def invalid_type_coro():
        return "not a dict or list"

    tasks = {
        "success": success_coro(),
        "error": error_coro(),
        "invalid": invalid_type_coro(),
        "none": asyncio.sleep(0, result=None),
    }

    # Act
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import (
            async_gather_with_timeout,
        )

        results = await async_gather_with_timeout(tasks, label="Test Batch")

    # Assert
    assert results["success"] == {"data": "ok"}
    assert results["error"] is None
    assert results["invalid"] is None
    assert results["none"] is None

    # Verify logging
    mock_logger.error.assert_called()
    mock_logger.debug.assert_called()


@pytest.mark.asyncio
async def test_get_all_data_resilience_to_none(data_fetch_manager, mock_client):
    """Test that get_all_data handles None values for networks and devices."""
    # Simulate sanitization returning None for networks and devices
    data_fetch_manager._async_fetch_batch_data = AsyncMock(
        return_value={
            "networks": None,
            "devices": None,
            "organization": {"name": "Test Org"},
            "statuses": [],
        }
    )

    # Use regular MagicMock to return a string/None instead of a coroutine
    # since we'll mock _async_gather_with_timeout anyway.
    data_fetch_manager.client_fetcher.async_fetch_network_clients = MagicMock(
        return_value="mock_task"
    )

    data_fetch_manager.client_fetcher.derive_device_clients = MagicMock(return_value={})

    # Act
    with (
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"
        ),
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"
        ),
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.async_gather_with_timeout",
            new_callable=AsyncMock,
        ) as mock_gather,
    ):
        # We need mock_gather to return a dict for the client_results call
        mock_gather.return_value = {}

        result = await data_fetch_manager.get_all_data()

    # Assert
    assert result["org_name"] == "Test Org"
    assert result["networks"] == []
    assert result["devices"] == []
    assert result["clients"] == []
