"""Test the API utility functions."""

import asyncio
from json import JSONDecodeError
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientError
from meraki.exceptions import APIError  # type: ignore

from custom_components.meraki_ha.core.utils.api_utils import handle_meraki_errors
from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiInformationalError,
    MerakiNetworkError,
)

@pytest.fixture
def mock_api_client():
    client = MagicMock()
    client.mark_feature_disabled = MagicMock()
    return client

@pytest.fixture
def mock_instance(mock_api_client):
    instance = MagicMock()
    instance._api_client = mock_api_client
    return instance

@pytest.mark.asyncio
async def test_handle_meraki_errors_rate_limit_retry():
    """Test that the handle_meraki_errors decorator retries on 429 errors."""
    mock_api_call = AsyncMock()
    metadata = {
        "tags": ["rate-limit"],
        "operation": "getDevice",
        "errors": ["Rate limit hit"],
    }
    response_mock = MagicMock()
    response_mock.status_code = 429
    response_mock.headers = {"Retry-After": "2"}

    api_error = APIError(metadata, response=response_mock)
    mock_api_call.side_effect = [api_error, api_error, "Success"]

    decorated_func = handle_meraki_errors(mock_api_call)

    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        result = await decorated_func()

        assert result == "Success"
        assert mock_api_call.call_count == 3
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(2)

@pytest.mark.asyncio
async def test_handle_connection_error_safe_return_dict():
    """Test handling JSONDecodeError returns safe dict."""
    async def api_call() -> dict:
        raise JSONDecodeError("msg", "doc", 0)

    decorated = handle_meraki_errors(api_call)
    result = await decorated()
    assert result == {}

@pytest.mark.asyncio
async def test_handle_connection_error_safe_return_list():
    """Test handling JSONDecodeError returns safe list."""
    async def api_call() -> list:
        raise JSONDecodeError("msg", "doc", 0)

    decorated = handle_meraki_errors(api_call)
    result = await decorated()
    assert result == []

@pytest.mark.asyncio
async def test_feature_disabled_traffic_analysis(mock_instance):
    """Test handling Traffic Analysis disabled error."""
    async def api_call(self, network_id: str) -> dict:
        response = MagicMock()
        response.json.return_value = {"errors": ["Traffic Analysis with Hostname Visibility is not enabled"]}
        raise APIError(
            {"errors": ["Traffic Analysis with Hostname Visibility is not enabled"], "tags": ["tag"], "operation": "op"},
            response=response
        )

    decorated = handle_meraki_errors(api_call)

    with patch("custom_components.meraki_ha.core.utils.api_utils._LOGGER") as mock_logger:
        result = await decorated(mock_instance, "net-123")

        assert result == {}
        mock_instance._api_client.mark_feature_disabled.assert_called_with("traffic", "net-123")
        mock_logger.debug.assert_called()

@pytest.mark.asyncio
async def test_feature_disabled_vlan(mock_instance):
    """Test handling VLAN disabled error."""
    async def api_call(self, network_id: str) -> list:
        response = MagicMock()
        response.json.return_value = {"errors": ["VLANs are not enabled for this network"]}
        raise APIError(
            {"errors": ["VLANs are not enabled for this network"], "tags": ["tag"], "operation": "op"},
            response=response
        )

    decorated = handle_meraki_errors(api_call)

    result = await decorated(mock_instance, "net-123")

    assert result == []
    mock_instance._api_client.mark_feature_disabled.assert_called_with("vlans", "net-123")

@pytest.mark.asyncio
async def test_auth_error():
    """Test handling authentication error."""
    async def api_call():
        raise APIError(
            {"errors": ["Invalid API key"], "tags": ["tag"], "operation": "op"},
            response=MagicMock(status_code=401)
        )

    decorated = handle_meraki_errors(api_call)

    with pytest.raises(MerakiAuthenticationError):
        await decorated()

@pytest.mark.asyncio
async def test_client_error():
    """Test handling aiohttp ClientError."""
    async def api_call():
        raise ClientError("Connection failed")

    decorated = handle_meraki_errors(api_call)

    with pytest.raises(MerakiConnectionError):
        await decorated()

@pytest.mark.asyncio
async def test_unexpected_error():
    """Test handling unexpected error."""
    async def api_call():
        raise ValueError("Unexpected")

    decorated = handle_meraki_errors(api_call)

    with pytest.raises(MerakiConnectionError) as excinfo:
        await decorated()
    assert "Unexpected error" in str(excinfo.value)
