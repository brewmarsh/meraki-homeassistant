"""API error categorization and custom exceptions."""

from meraki.exceptions import APIError  # type: ignore


class RetryRequest(Exception):
    """Internal exception to trigger a retry."""


def is_rate_limit_error(err: APIError) -> bool:
    """Check if error is due to rate limiting."""
    return getattr(err, "status", None) == 429 or "rate limit" in str(err).lower()


def is_auth_error(err: APIError) -> bool:
    """Check if error is an authentication error."""
    return getattr(err, "status", None) in (401, 403) or any(
        msg in str(err).lower()
        for msg in (
            "unauthorized",
            "forbidden",
            "invalid api key",
            "authentication failed",
        )
    )


def is_device_error(err: APIError) -> bool:
    """Check if error is device-related."""
    return any(
        msg in str(err).lower()
        for msg in (
            "device not found",
            "invalid serial",
            "device error",
            "device offline",
        )
    )


def is_network_error(err: APIError) -> bool:
    """Check if error is network-related."""
    return any(
        msg in str(err).lower()
        for msg in (
            "network not found",
            "invalid network",
            "network error",
            "network offline",
        )
    )


def is_informational_error(err: APIError) -> bool:
    """Check if error is informational (e.g., feature not enabled)."""
    error_msg = str(err)
    return (
        "VLANs are not enabled for this network" in error_msg
        or "Traffic Analysis with Hostname Visibility" in error_msg
        or "historical viewing is not supported" in error_msg
    )
