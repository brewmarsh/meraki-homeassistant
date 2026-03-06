"""Factory for creating Meraki API clients."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .client import MerakiApiClientProtocol as MerakiAPIClient
from .protocol import MerakiApiClientProtocol as MerakiApiClientProtocolType
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.devices import DevicesEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.sensor import SensorEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints


def create_api_client(
    hass: HomeAssistant,
    api_key: str,
    org_id: str,
    base_url: str = "https://api.meraki.com/api/v1",
) -> MerakiApiClientProtocolType:
    """
    Create a new Meraki API client with all endpoints configured.

    Args:
        hass: The Home Assistant instance.
        api_key: The Meraki API key.
        org_id: The organization ID.
        base_url: The base URL for the Meraki API.

    Returns
    -------
        The configured Meraki API client.

    """
    client = MerakiAPIClient(hass, api_key, org_id, base_url)

    # Initialize endpoint handlers
    client.appliance = ApplianceEndpoints(client, hass)
    client.camera = CameraEndpoints(client)
    client.devices = DevicesEndpoints(client)
    client.network = NetworkEndpoints(client)
    client.organization = OrganizationEndpoints(client)
    client.switch = SwitchEndpoints(client)
    client.wireless = WirelessEndpoints(client)
    client.sensor = SensorEndpoints(client)

    return client
