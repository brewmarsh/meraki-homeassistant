<<<<<<< HEAD
<<<<<<< HEAD
"""Core errors and exceptions for the Meraki integration."""


class MerakiError(Exception):
    """Base exception for Meraki integration."""

    def __init__(self, message: str = "") -> None:
        """Initialize the exception."""
        super().__init__(message)
        self.message = message


class MerakiConnectionError(MerakiError):
    """Error to indicate a connection problem."""

    pass


class MerakiAuthenticationError(MerakiError):
    """Error to indicate an authentication problem."""

    pass


class MerakiConfigError(MerakiError):
    """Error to indicate a configuration problem."""

    pass


class MerakiDeviceError(MerakiError):
    """Error to indicate a device-specific problem."""

    pass


class MerakiNetworkError(MerakiError):
    """Error to indicate a network-specific problem."""

    pass


class MerakiInformationalError(MerakiError):
    """Error to indicate an informational/non-critical problem."""


class MerakiTrafficAnalysisError(MerakiInformationalError):
    """Error to indicate that traffic analysis is not enabled."""


class MerakiVlansDisabledError(MerakiInformationalError):
    """Error to indicate that VLANs are not enabled for a network."""
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
"""Custom exceptions for the Meraki HA integration."""


class MerakiHAException(Exception):
    """Base exception for Meraki HA."""


class ApiClientCommunicationError(MerakiHAException):
    """Exception to indicate a communication error with the Meraki API."""


class MerakiInformationalError(MerakiHAException):
    """An informational 'error' from the Meraki API."""


class MerakiTrafficAnalysisError(MerakiInformationalError):
    """Exception for when traffic analysis is not enabled on the Meraki dashboard."""


class MerakiVlanError(MerakiInformationalError):
    """Exception for when VLANs are not enabled on the Meraki dashboard."""


class MerakiAuthenticationError(MerakiHAException):
    """Exception to indicate an authentication error with the Meraki API."""


class MerakiConnectionError(MerakiHAException):
    """Exception to indicate a connection error with the Meraki API."""


class MerakiDeviceError(MerakiHAException):
    """Exception to indicate a device-specific error with the Meraki API."""


class MerakiNetworkError(MerakiHAException):
    """Exception to indicate a network-specific error with the Meraki API."""
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
