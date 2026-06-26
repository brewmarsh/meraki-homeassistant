"""Test the MerakiClient async implementation."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.api.client import MerakiClient


@pytest.mark.asyncio
async def test_meraki_client_async_setup(hass: HomeAssistant) -> None:
    """Test that MerakiClient.async_setup initializes AsyncDashboardAPI."""
    api_key = "test-api-key"
    client = MerakiClient(hass, api_key)

    with patch("meraki.aio.AsyncDashboardAPI") as mock_async_api:
        await client.async_setup()

        # Verify AsyncDashboardAPI was initialized correctly
        mock_async_api.assert_called_once()
        args, kwargs = mock_async_api.call_args
        assert kwargs["api_key"] == api_key
        assert "aiohttp_session" in kwargs
        assert client.dashboard is not None


@pytest.mark.asyncio
async def test_meraki_client_run_async(hass: HomeAssistant) -> None:
    """Test that MerakiClient.run_async awaits the provided coroutine."""
    api_key = "test-api-key"
    client = MerakiClient(hass, api_key)

    # Mock the dashboard and a sample coroutine
    client.dashboard = AsyncMock()
    mock_coro_func = AsyncMock(return_value={"status": "ok"})

    # Call run_async (it will be renamed from run_sync)
    # Since I haven't renamed it yet, this test should fail if I run it now.
    # But I'll write it with the new name to follow TDD.
    result = await client.run_async(mock_coro_func, param="value")

    assert result == {"status": "ok"}
    mock_coro_func.assert_called_once_with(param="value")
