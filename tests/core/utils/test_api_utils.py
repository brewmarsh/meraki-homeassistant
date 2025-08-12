"""Tests for the API utils."""

import pytest
from aiohttp import ClientError
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)
from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiNetworkError,
)


@handle_meraki_errors
async def dummy_api_call():
    """A dummy API call that can be used to test the decorator."""
    return {"status": "ok"}


class MockResponse:
    def __init__(self, status_code, reason, json_data):
        self.status_code = status_code
        self.reason = reason
        self._json_data = json_data

    def json(self):
        return self._json_data


@handle_meraki_errors
async def dummy_api_call_auth_error():
    """A dummy API call that raises an auth error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(401, "Unauthorized", {"errors": ["invalid api key"]}),
    )


@handle_meraki_errors
async def dummy_api_call_device_error():
    """A dummy API call that raises a device error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(500, "Internal Server Error", {"errors": ["device not found"]}),
    )


@handle_meraki_errors
async def dummy_api_call_network_error():
    """A dummy API call that raises a network error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(500, "Internal Server Error", {"errors": ["network not found"]}),
    )


@handle_meraki_errors
async def dummy_api_call_rate_limit_error():
    """A dummy API call that raises a rate limit error."""
    raise APIError(
        {"tags": ["test"], "operation": "test"},
        MockResponse(429, "Too Many Requests", {"errors": ["rate limit exceeded"]}),
    )


@handle_meraki_errors
async def dummy_api_call_client_error():
    """A dummy API call that raises a client error."""
    raise ClientError("test")


@handle_meraki_errors
async def dummy_api_call_generic_error():
    """A dummy API call that raises a generic error."""
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


def test_validate_response():
    """Test the validate_response function."""
    with pytest.raises(MerakiConnectionError):
        validate_response(None)
    with pytest.raises(MerakiConnectionError):
        validate_response({})
    assert validate_response({"key": "value"}) == {"key": "value"}
    assert validate_response([1, 2, 3]) == [1, 2, 3]
    assert validate_response("string") == {"value": "string"}
    assert validate_response(123) == {"value": 123}
    assert validate_response(1.23) == {"value": 1.23}
    assert validate_response(True) == {"value": True}
