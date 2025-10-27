"""Tests for the API utils."""

import pytest
from aiohttp import ClientError
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiNetworkError,
)
from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)


@handle_meraki_errors
async def dummy_api_call():
    """Call a dummy API to test the decorator."""
    return {"status": "ok"}


class MockResponse:

    """Mock response for APIError."""

    def __init__(self, status_code, reason, json_data):
        """Initialize the mock response."""
        self.status_code = status_code
        self.reason = reason
        self._json_data = json_data

    def json(self):
        """Return the json data."""
        return self._json_data


@handle_meraki_errors
async def dummy_api_call_auth_error():
    """Call a dummy API that raises an auth error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(401, "Unauthorized", {"errors": ["invalid api key"]}),
    )


@handle_meraki_errors
async def dummy_api_call_device_error():
    """Call a dummy API that raises a device error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(500, "Internal Server Error", {"errors": ["device not found"]}),
    )


@handle_meraki_errors
async def dummy_api_call_network_error():
    """Call a dummy API that raises a network error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(500, "Internal Server Error", {"errors": ["network not found"]}),
    )


@handle_meraki_errors
async def dummy_api_call_rate_limit_error():
    """Call a dummy API that raises a rate limit error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(429, "Too Many Requests", {"errors": ["rate limit exceeded"]}),
    )


@handle_meraki_errors
async def dummy_api_call_client_error():
    """Call a dummy API that raises a client error."""
    raise ClientError("test")


@handle_meraki_errors
async def dummy_api_call_generic_error():
    """Call a dummy API that raises a generic error."""
    raise Exception("test")


@pytest.mark.asyncio
async def test_handle_meraki_errors():
    """Test the handle_meraki_errors decorator."""
    assert await dummy_api_call() == {"status": "ok"}
    with pytest.raises(MerakiAuthenticationError):
        await dummy_api_call_auth_error()
    with pytest.raises(MerakiDeviceError):
        await dummy_api_call_device_error()
    with pytest.raises(MerakiNetworkError):
        await dummy_api_call_network_error()
    with pytest.raises(MerakiConnectionError):
        await dummy_api_call_client_error()
    with pytest.raises(MerakiConnectionError):
        await dummy_api_call_generic_error()


@handle_meraki_errors
async def dummy_api_call_empty_dict() -> dict[str, str]:
    """Call a dummy API that raises an error and expects a dict."""
    raise MerakiConnectionError("test")


@handle_meraki_errors
async def dummy_api_call_empty_list() -> list[str]:
    """Call a dummy API that raises an error and expects a list."""
    raise MerakiConnectionError("test")


@pytest.mark.asyncio
async def test_handle_meraki_errors_empty_response():
    """Test that the decorator returns a type-safe empty value."""
    assert await dummy_api_call_empty_dict() == {}
    assert await dummy_api_call_empty_list() == []


def test_validate_response():
    """Test the validate_response function."""
    with pytest.raises(MerakiConnectionError):
        validate_response(None)

    # Empty dicts are now allowed, but will log a warning
    assert validate_response({}) == {}
    assert validate_response({"key": "value"}) == {"key": "value"}
    assert validate_response([1, 2, 3]) == [1, 2, 3]
    assert validate_response("string") == {"value": "string"}
    assert validate_response(123) == {"value": 123}
    assert validate_response(1.23) == {"value": 1.23}
    assert validate_response(True) == {"value": True}
