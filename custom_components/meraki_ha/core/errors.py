"""Custom exceptions for the Meraki HA integration."""


class MerakiHAException(Exception):
    """Base exception for Meraki HA."""


class ApiClientCommunicationError(MerakiHAException):
    """Exception to indicate a communication error with the Meraki API."""


class MerakiInformationalError(MerakiHAException):
    """An informational 'error' from the Meraki API."""


class MerakiTrafficAnalysisError(MerakiInformationalError):
    """Exception for when traffic analysis is not enabled on the Meraki dashboard."""


class MerakiAuthenticationError(MerakiHAException):
    """Exception to indicate an authentication error with the Meraki API."""


class MerakiConnectionError(MerakiHAException):
    """Exception to indicate a connection error with the Meraki API."""


class MerakiDeviceError(MerakiHAException):
    """Exception to indicate a device-specific error with the Meraki API."""


class MerakiNetworkError(MerakiHAException):
    """Exception to indicate a network-specific error with the Meraki API."""
