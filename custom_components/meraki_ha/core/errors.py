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

<<<<<<< HEAD

class MerakiTrafficAnalysisError(MerakiInformationalError):
    """Error to indicate that traffic analysis is not enabled."""


class MerakiVlansDisabledError(MerakiInformationalError):
    """Error to indicate that VLANs are not enabled for a network."""
=======
    pass
>>>>>>> origin/beta
