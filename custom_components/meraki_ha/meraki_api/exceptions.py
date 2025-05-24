"""Defines custom exceptions for Meraki API interactions within the integration.

This module contains the `MerakiApiError` class, a specialized exception
used throughout the Meraki API client to indicate various issues encountered
while communicating with the Meraki Dashboard API.
"""


class MerakiApiError(Exception):
    """Custom exception for errors related to the Meraki API.

    This exception is raised when there are issues during communication with
    the Meraki API. This can include network problems, authentication failures
    (though `aiohttp.ClientResponseError` might be more specific for HTTP status
    codes), API rate limiting, or other API-specific errors.

    Attributes:
        message (str): A human-readable message describing the error.
    """

    def __init__(self, message: str) -> None:
        """Initializes the MerakiApiError.

        Args:
            message (str): A descriptive message explaining the nature of the API error.
        """
        super().__init__(message)
        self.message = message  # Store the message for direct access if needed.

    def __str__(self) -> str:
        """Returns the string representation of the MerakiApiError.

        Overrides the default `__str__` method to provide a more informative
        error message, prefixed with "Meraki API Error:".

        Returns:
            str: The formatted error message.
        """
        return f"Meraki API Error: {self.message}"
