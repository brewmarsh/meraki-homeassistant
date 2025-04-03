"""Custom exceptions for the meraki_ha integration's Meraki API interactions."""


class MerakiApiError(Exception):
    """Exception to indicate a Meraki API error.

    This exception is raised when there is an issue communicating with the
    Meraki API, such as network errors, invalid requests, or API rate limits.
    """

    def __init__(self, message: str) -> None:
        """Initialize the MerakiApiError with a custom message."""
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        return f"Meraki API Error: {self.message}"
