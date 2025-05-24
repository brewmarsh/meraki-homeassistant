"""Custom exceptions for the Meraki Home Assistant integration's API interactions.

This module defines a hierarchy of custom exception classes to handle various
errors that can occur when communicating with the Meraki Dashboard API.
These exceptions provide more specific error information than generic
Python exceptions.
"""
from typing import Optional # For status_code in MerakiApiException


class MerakiApiException(Exception): # Renamed from MerakiApiError for clarity as a base
    """Base class for exceptions raised by the Meraki API client.

    This exception serves as a generic base for more specific API-related errors.
    It can optionally store an HTTP status code associated with the error.

    Attributes:
        message: A human-readable message describing the error.
        status_code: (Optional) The HTTP status code from the API response, if applicable.
    """

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        """Initialize the MerakiApiException.

        Args:
            message: A human-readable message describing the error.
            status_code: (Optional) The HTTP status code from the API response.
        """
        super().__init__(message)
        self.message: str = message
        self.status_code: Optional[int] = status_code

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        if self.status_code:
            return f"Meraki API Error (Status {self.status_code}): {self.message}"
        return f"Meraki API Error: {self.message}"


# Define more specific exceptions that inherit from MerakiApiException

class MerakiApiConnectionError(MerakiApiException):
    """Exception raised for errors when connecting to the Meraki API.

    This typically indicates network issues (e.g., DNS failure, connection timeout)
    or problems reaching the API endpoint.
    """
    pass # No additional logic needed, inherits all from MerakiApiException


class MerakiApiAuthError(MerakiApiException): # More specific than just "InvalidApiKey"
    """Exception raised for authentication or authorization errors with the Meraki API.

    This occurs if the API key is invalid, has insufficient permissions for the
    requested operation, or if authentication otherwise fails (e.g., HTTP 401/403).
    """
    pass


class MerakiApiNotFoundError(MerakiApiException):
    """Exception raised when a requested resource is not found (HTTP 404)."""
    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(message, status_code)


class MerakiApiRateLimitError(MerakiApiException):
    """Exception raised when API rate limits are exceeded (HTTP 429)."""
    def __init__(self, message: str, status_code: int = 429) -> None:
        super().__init__(message, status_code)

class MerakiApiServerError(MerakiApiException):
    """Exception raised for server-side errors on the Meraki API (HTTP 5xx)."""
    pass


# Alias MerakiApiError to MerakiApiException for backward compatibility if needed,
# or update all usages to MerakiApiException.
# For this task, I'll assume we want to refine the hierarchy, so MerakiApiError
# becomes the more generic MerakiApiException.
MerakiApiError = MerakiApiException

__all__ = [
    "MerakiApiException",
    "MerakiApiError", # Keep alias if used extensively elsewhere
    "MerakiApiConnectionError",
    "MerakiApiAuthError",
    "MerakiApiNotFoundError",
    "MerakiApiRateLimitError",
    "MerakiApiServerError",
]
