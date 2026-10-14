"""Test user-friendly logging in MerakiClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.api.client import (
    FRIENDLY_FEATURE_NAMES,
    MerakiClient,
)
from homeassistant.core import HomeAssistant


@pytest.mark.asyncio
async def test_run_sync_friendly_logging(hass: HomeAssistant) -> None:
    """Test that run_async logs friendly error messages for 400 errors."""
    client = MerakiClient(hass, "api_key", "org_id")

    # Patch clientsession during async_setup to avoid aiodns issues
    with (
        patch(
            "custom_components.meraki_ha.core.api.client.async_get_clientsession"
        ) as mock_get_session,
        patch("meraki.aio.AsyncDashboardAPI"),
    ):
        mock_get_session.return_value = MagicMock()
        await client.async_setup()

    try:
        # Mock dashboard and an endpoint as AsyncMock
        mock_func = AsyncMock()
        mock_func.__name__ = "getNetworkTraffic"

        # Create a real APIError
        metadata = {"tags": ["test"], "operation": "getNetworkTraffic"}
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {
            "errors": ["Traffic analysis is not enabled for this network"]
        }
        response.headers = {"X-Cisco-Meraki-API-Request-Id": "req_id"}
        error = APIError(metadata, response)

        mock_func.side_effect = error

        with patch(
            "custom_components.meraki_ha.core.api.client._LOGGER"
        ) as mock_logger:
            # We need to provide a networkId to trigger the logging properly
            result = await client.run_async(mock_func, networkId="N_123")

            assert result == []
            assert client.is_feature_disabled("getNetworkTraffic", "N_123")

            # Verify the log message
            friendly_name = FRIENDLY_FEATURE_NAMES["getNetworkTraffic"]

            mock_logger.warning.assert_any_call(
                "%s is not enabled for network %s and will not be checked until the integration restarts. "
                "To add %s support, enable it on the Cisco Meraki dashboard.",
                friendly_name.capitalize(),
                "N_123",
                friendly_name.lower(),
            )
    finally:
        if client._worker_tasks:
            for task in client._worker_tasks:
                task.cancel()


@pytest.mark.asyncio
async def test_run_sync_fallback_logging(hass: HomeAssistant) -> None:
    """Test that run_async falls back to raw endpoint name if not in FRIENDLY_FEATURE_NAMES."""
    client = MerakiClient(hass, "api_key", "org_id")

    # Patch clientsession during async_setup to avoid aiodns issues
    with (
        patch(
            "custom_components.meraki_ha.core.api.client.async_get_clientsession"
        ) as mock_get_session,
        patch("meraki.aio.AsyncDashboardAPI"),
    ):
        mock_get_session.return_value = MagicMock()
        await client.async_setup()

    try:
        # Mock dashboard and an unknown endpoint as AsyncMock
        mock_func = AsyncMock()
        mock_func.__name__ = "unknownEndpoint"

        # Create a real APIError
        metadata = {"tags": ["test"], "operation": "unknownEndpoint"}
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {"errors": ["this feature must be enabled"]}
        response.headers = {}
        error = APIError(metadata, response)

        mock_func.side_effect = error

        with patch(
            "custom_components.meraki_ha.core.api.client._LOGGER"
        ) as mock_logger:
            result = await client.run_async(mock_func, networkId="N_456")

            assert result == []

            mock_logger.warning.assert_any_call(
                "%s is not enabled for network %s and will not be checked until the integration restarts. "
                "To add %s support, enable it on the Cisco Meraki dashboard.",
                "Unknownendpoint",  # capitalize() makes only first letter uppercase
                "N_456",
                "unknownendpoint",
            )
    finally:
        if client._worker_tasks:
            for task in client._worker_tasks:
                task.cancel()
