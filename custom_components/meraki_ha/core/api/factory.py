"""Factory for creating Meraki API clients."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...const.config import (
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from .client import MerakiClient
from .protocol import MerakiApiClientProtocol as MerakiApiClientProtocolType


def create_api_client(
    hass: HomeAssistant,
    api_key: str,
    org_id: str | None = None,
    base_url: str = "https://api.meraki.com/api/v1",
    enabled_networks: list[str] | None = None,
) -> MerakiApiClientProtocolType:
    """
    Create a new Meraki API client with all endpoints configured.

    Args:
        hass: The Home Assistant instance.
        api_key: The Meraki API key.
        org_id: The organization ID.
        base_url: The base URL for the Meraki API.
        enabled_networks: The list of enabled networks.

    Returns
    -------
        The configured Meraki API client.

    """
    return MerakiClient(hass, api_key, org_id, base_url, enabled_networks)


def create_meraki_client(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> MerakiApiClientProtocolType:
    """
    Create a Meraki API client from a config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns
    -------
        The configured Meraki API client.

    """
    api_key = entry.data[CONF_MERAKI_API_KEY]
    org_id = entry.data.get(CONF_MERAKI_ORG_ID)

    # Prioritize enabled networks from options, fall back to data
    enabled_networks = entry.options.get(
        CONF_ENABLED_NETWORKS, entry.data.get(CONF_ENABLED_NETWORKS, [])
    )

    return create_api_client(
        hass,
        api_key,
        org_id,
        enabled_networks=enabled_networks,
    )
