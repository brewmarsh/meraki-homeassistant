"""Tests for the API utils."""

from __future__ import annotations

from typing import Any

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
    _is_list_return_type,
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


# Test functions for _is_list_return_type with string annotations
# (due to from __future__ import annotations at top of file)
async def func_returning_list_of_dicts() -> list[dict[str, Any]]:
    """Return a list of dicts (string annotation due to __future__)."""
    return []


async def func_returning_list_of_strings() -> list[str]:
    """Return a list of strings (string annotation due to __future__)."""
    return []


async def func_returning_dict() -> dict[str, Any]:
    """Return a dict (string annotation due to __future__)."""
    return {}


async def func_returning_plain_list() -> list:
    """Return a plain list (string annotation due to __future__)."""
    return []


async def func_returning_no_annotation():
    """Return without annotation."""
    return {}


class TestIsListReturnType:
    """Tests for the _is_list_return_type helper function."""

    def test_list_of_dicts_with_string_annotation(self):
        """Test that list[dict[str, Any]] is detected as a list return type.

        This is the critical test case - with 'from __future__ import annotations',
        the annotation is a string at runtime.
        """
        assert _is_list_return_type(func_returning_list_of_dicts) is True

    def test_list_of_strings_with_string_annotation(self):
        """Test that list[str] is detected as a list return type."""
        assert _is_list_return_type(func_returning_list_of_strings) is True

    def test_plain_list_with_string_annotation(self):
        """Test that plain list is detected as a list return type."""
        assert _is_list_return_type(func_returning_plain_list) is True

    def test_dict_is_not_list_type(self):
        """Test that dict[str, Any] is NOT detected as a list return type."""
        assert _is_list_return_type(func_returning_dict) is False

    def test_no_annotation_is_not_list_type(self):
        """Test that a function with no return annotation is NOT a list type."""
        assert _is_list_return_type(func_returning_no_annotation) is False


@handle_meraki_errors
async def decorated_func_list_return() -> list[dict[str, Any]]:
    """Test function that should return [] on error (uses string annotation)."""
    raise MerakiConnectionError("test error")


@handle_meraki_errors
async def decorated_func_dict_return() -> dict[str, Any]:
    """Test function that should return {} on error (uses string annotation)."""
    raise MerakiConnectionError("test error")


@pytest.mark.asyncio
async def test_handle_meraki_errors_with_future_annotations():
    """Test decorator returns correct empty type with __future__ annotations.

    This test verifies the fix for the bug where functions using
    'from __future__ import annotations' would incorrectly return {}
    instead of [] for list-returning functions.
    """
    # list[dict[str, Any]] should return []
    result_list = await decorated_func_list_return()
    assert result_list == [], f"Expected [], got {result_list}"
    assert isinstance(result_list, list)

    # dict[str, Any] should return {}
    result_dict = await decorated_func_dict_return()
    assert result_dict == {}, f"Expected {{}}, got {result_dict}"
    assert isinstance(result_dict, dict)
