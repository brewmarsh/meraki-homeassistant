"""Factory for creating Meraki API clients."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .client import MerakiClient
from .protocol import MerakiApiClientProtocol as MerakiApiClientProtocolType


def create_api_client(
    hass: HomeAssistant,
    api_key: str,
    org_id: str | None = None,
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
    return MerakiClient(hass, api_key, org_id, base_url)
