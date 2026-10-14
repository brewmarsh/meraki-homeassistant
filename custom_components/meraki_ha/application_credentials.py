"""Application credentials platform for the Cisco Meraki integration."""

from __future__ import annotations

from homeassistant.components.application_credentials import AuthorizationServer
from homeassistant.core import HomeAssistant


async def async_get_authorization_server(
    hass: HomeAssistant,
) -> AuthorizationServer:
    """Return authorization server for Cisco Meraki."""
    return AuthorizationServer(
        authorize_url="https://as.meraki.com/oauth/authorize",
        token_url="https://as.meraki.com/oauth/token",
    )


async def async_get_description_placeholders(
    hass: HomeAssistant,
) -> dict[str, str]:
    """Return description placeholders for credentials dialog."""
    return {
        "oauth_url": "https://as.meraki.com/oauth/authorize",
    }
