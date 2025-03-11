"""Custom exceptions for the meraki_ha integration's Meraki API interactions."""

class MerakiApiError(Exception):
    """Exception to indicate a Meraki API error.

    This exception is raised when there is an issue communicating with the
    Meraki API, such as network errors, invalid requests, or API rate limits.
    """
    pass