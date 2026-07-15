"""Test the MerakiClient async implementation."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.api.client import MerakiClient
from homeassistant.core import HomeAssistant


@pytest.mark.asyncio
async def test_meraki_client_async_setup(hass: HomeAssistant) -> None:
    """Test that MerakiClient.async_setup initializes AsyncDashboardAPI."""
    api_key = "test-api-key"
    client = MerakiClient(hass, api_key)

    try:
        with (
            patch(
                "custom_components.meraki_ha.core.api.client.async_get_clientsession"
            ) as mock_get_session,
            patch("meraki.aio.AsyncDashboardAPI") as mock_async_api,
        ):
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session

            await client.async_setup()

            # Verify AsyncDashboardAPI was initialized correctly
            mock_async_api.assert_called_once()
            args, kwargs = mock_async_api.call_args
            assert kwargs["api_key"] == api_key
            assert kwargs["aiohttp_session"] == mock_session
            assert client.dashboard is not None
    finally:
        if client._worker_tasks:
            for task in client._worker_tasks:
                task.cancel()


@pytest.mark.asyncio
async def test_meraki_client_run_async(hass: HomeAssistant) -> None:
    """Test that MerakiClient.run_async awaits the provided coroutine."""
    api_key = "test-api-key"
    client = MerakiClient(hass, api_key)

    # Initialize dashboard and start worker tasks manually
    client.dashboard = AsyncMock()
    client._worker_tasks = [
        asyncio.create_task(client._worker_loop(i)) for i in range(3)
    ]

    try:
        # Mock a sample coroutine
        mock_coro_func = AsyncMock(return_value={"status": "ok"})

        result = await client.run_async(mock_coro_func, param="value")

        assert result == {"status": "ok"}
        mock_coro_func.assert_called_once_with(param="value")
    finally:
        if client._worker_tasks:
            for task in client._worker_tasks:
                task.cancel()
