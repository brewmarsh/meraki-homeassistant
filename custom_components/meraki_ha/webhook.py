"""Webhook handling for the Meraki integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .const import CONF_WEBHOOK_URL
from .core.api import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


def get_webhook_url(
    hass: HomeAssistant, webhook_id: str, entry_webhook_url: Optional[str] = None
) -> str:
    """Get the URL for a webhook.

    Meraki requires HTTPS URLs that are publicly accessible.
    Raises MerakiConnectionError if the URL doesn't meet Meraki's requirements.

    Args:
        hass: The Home Assistant instance
        webhook_id: The ID of the webhook
        entry_webhook_url: Optional base webhook URL from config entry
    """
    from urllib.parse import urlparse
    from .core.errors import MerakiConnectionError

    # Use configured webhook URL if provided, otherwise fall back to HA's external URL
    base_url = (
        entry_webhook_url
        if entry_webhook_url
        else get_url(hass, allow_internal=False, prefer_external=True)
    )

    if not base_url:
        raise MerakiConnectionError(
            "No webhook URL configured. Please either configure an external URL in the "
            "integration options or in your Home Assistant configuration."
        )

    # Ensure the URL uses HTTPS
    if not base_url.startswith("https://"):
        raise MerakiConnectionError(
            "Meraki webhooks require HTTPS. Please configure an HTTPS URL."
        )

    # Parse the URL to check if it's a local address
    parsed = urlparse(base_url)
    hostname = parsed.hostname
    if hostname and (
        hostname.startswith("192.168.")
        or hostname.startswith("10.")
        or hostname.startswith("172.")
        or hostname == "localhost"
        or hostname.endswith(".local")
    ):
        raise MerakiConnectionError(
            "Meraki webhooks require a public URL. Your current URL appears to be a local address. "
            "Please configure a public HTTPS URL."
        )

    # Remove trailing slash if present
    base_url = base_url.rstrip("/")

    return f"{base_url}/api/webhook/{webhook_id}"


async def async_register_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    secret: str,
    api_client: "MerakiAPIClient",
    entry=None,
) -> None:
    """Register a webhook with the Meraki API.

    Args:
        hass: The Home Assistant instance
        webhook_id: The ID of the webhook
        secret: The webhook secret
        api_client: The Meraki API client
        entry: Optional config entry containing webhook URL configuration

    Raises:
        MerakiConnectionError: If the webhook cannot be registered due to URL requirements
            or other API errors.
    """
    try:
        webhook_url = get_webhook_url(
            hass, webhook_id, entry.data.get(CONF_WEBHOOK_URL) if entry else None
        )
        await api_client.register_webhook(webhook_url, secret)
    except Exception as err:
        _LOGGER.error("Failed to register webhook: %s", err)
        raise


async def async_unregister_webhook(
    hass: HomeAssistant, webhook_id: str, api_client: "MerakiAPIClient"
) -> None:
    """Unregister a webhook with the Meraki API."""
    await api_client.unregister_webhook(webhook_id)


async def async_handle_webhook(
    hass: HomeAssistant, webhook_id: str, request: Any
) -> Dict[str, Any]:
    """Handle a webhook from the Meraki API."""
    # TODO: Implement webhook handling
    return {}
