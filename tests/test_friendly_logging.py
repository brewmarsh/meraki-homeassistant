"""Test user-friendly logging in MerakiClient."""

import pytest
from unittest.mock import MagicMock, patch
import meraki
from custom_components.meraki_ha.core.api.client import MerakiClient, FRIENDLY_FEATURE_NAMES

class FakeAPIError(meraki.APIError):
    def __init__(self, message, status, headers=None):
        self.message = message
        self.status = status
        self.response = MagicMock()
        self.response.headers = headers or {}
    def __str__(self):
        return self.message

@pytest.mark.asyncio
async def test_run_sync_friendly_logging(hass):
    """Test that run_sync logs friendly error messages for 400 errors."""
    client = MerakiClient(hass, "api_key", "org_id")
    await client.async_setup()

    # Mock dashboard and an endpoint
    mock_func = MagicMock()
    mock_func.__name__ = "getNetworkTraffic"

    # Create a fake APIError
    error = FakeAPIError(
        "Traffic analysis is not enabled for this network",
        400,
        {"X-Cisco-Meraki-API-Request-Id": "req_id"}
    )

    # Use patch to mock loop.run_in_executor
    with patch("asyncio.get_event_loop") as mock_loop, \
         patch("custom_components.meraki_ha.core.api.client._LOGGER") as mock_logger:

        mock_loop.return_value.run_in_executor.side_effect = error

        # We need to provide a networkId to trigger the logging properly
        result = await client.run_sync(mock_func, networkId="N_123")

        assert result == []
        assert client.is_feature_disabled("getNetworkTraffic", "N_123")

        # Verify the log message
        friendly_name = FRIENDLY_FEATURE_NAMES["getNetworkTraffic"]

        mock_logger.warning.assert_any_call(
            "%s is not enabled for network %s and will not be checked until the integration restarts. "
            "To add %s support, enable it on the Cisco Meraki dashboard.",
            friendly_name.capitalize(),
            "N_123",
            friendly_name.lower()
        )

@pytest.mark.asyncio
async def test_run_sync_fallback_logging(hass):
    """Test that run_sync falls back to raw endpoint name if not in FRIENDLY_FEATURE_NAMES."""
    client = MerakiClient(hass, "api_key", "org_id")
    await client.async_setup()

    # Mock dashboard and an unknown endpoint
    mock_func = MagicMock()
    mock_func.__name__ = "unknownEndpoint"

    # Create a fake APIError
    error = FakeAPIError(
        "this feature must be enabled",
        400
    )

    with patch("asyncio.get_event_loop") as mock_loop, \
         patch("custom_components.meraki_ha.core.api.client._LOGGER") as mock_logger:

        mock_loop.return_value.run_in_executor.side_effect = error

        result = await client.run_sync(mock_func, networkId="N_456")

        assert result == []

        mock_logger.warning.assert_any_call(
            "%s is not enabled for network %s and will not be checked until the integration restarts. "
            "To add %s support, enable it on the Cisco Meraki dashboard.",
            "Unknownendpoint", # capitalize() makes only first letter uppercase
            "N_456",
            "unknownendpoint"
        )
