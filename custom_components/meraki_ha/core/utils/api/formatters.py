"""API response formatting and validation."""

import inspect
import logging
from collections.abc import Callable
from typing import Any

from ...errors import MerakiConnectionError, MerakiInformationalError

_LOGGER = logging.getLogger(__name__)


def get_safe_return_value(
    func: Callable[..., Any], error_msg: str | None = None
) -> Any:
    """Get a safe return value based on the function's return type annotation."""
    sig = inspect.signature(func)
    return_type = sig.return_annotation
    if return_type is list or getattr(return_type, "__origin__", None) is list:
        return []
    if return_type is dict or getattr(return_type, "__origin__", None) is dict:
        return {}
    if error_msg:
        return MerakiInformationalError(error_msg)
    return {}


def validate_response(response: Any) -> Any:
    """
    Validate and normalize an API response.

    Args:
    ----
        response: The API response to validate

    Returns
    -------
        Normalized response dictionary

    Raises
    ------
        MerakiConnectionError: If response is invalid or empty

    """
    if response is None:
        raise MerakiConnectionError("Empty response from API")

    if isinstance(response, dict):
        if not response:
            _LOGGER.warning("Empty response dictionary from API")
        return response

    if isinstance(response, list):
        return response

    if isinstance(response, (str, int, float, bool)):
        return {"value": response}

    raise MerakiConnectionError(
        f"Invalid response format: {type(response)}. Expected dict or list."
    )
