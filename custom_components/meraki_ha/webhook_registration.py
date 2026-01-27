"""Webhook registration and unregistration for the Meraki integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from homeassistant.components import cloud
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .core.errors import MerakiConnectionError

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from .core.api import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


def get_webhook_url(
    hass: HomeAssistant,
    webhook_id: str,
    entry_webhook_url: str | None = None,
) -> str:
    """
    Get the URL for a webhook.

    Meraki requires HTTPS URLs that are publicly accessible.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The ID of the webhook.
        entry_webhook_url: Optional base webhook URL from config entry.

    Returns
    -------
        The full webhook URL.

    Raises
    ------
        MerakiConnectionError: If the URL doesn't meet Meraki's requirements.

    """
    # Use configured webhook URL if provided, otherwise fall back to HA's external URL
    base_url = (
        entry_webhook_url
        if entry_webhook_url
        else get_url(hass, allow_internal=False, prefer_external=True)
    )

    if not base_url:
        raise MerakiConnectionError(
            "No webhook URL configured. Please either configure an external URL in the "
            "integration options or in your Home Assistant configuration.",
        )

    # Ensure the URL uses HTTPS
    if not base_url.startswith("https://"):
        raise MerakiConnectionError(
            "Meraki webhooks require HTTPS. Please configure an HTTPS URL.",
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
            "Meraki webhooks require a public URL, but the current URL "
            "appears to be a local address. Please configure a public HTTPS URL.",
        )

    # Remove trailing slash if present
    base_url = base_url.rstrip("/")

    return f"{base_url}/api/webhook/{webhook_id}"


async def async_register_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    secret: str,
    api_client: MerakiAPIClient,
    entry: ConfigEntry | None = None,
) -> None:
    """
    Register a webhook with the Meraki API.

    This function determines the correct public URL for the webhook, which is a
    requirement for the Meraki API. The URL is selected based on the following
    priority:
    1. A specific webhook URL provided in the integration's configuration entry.
    2. The Home Assistant Cloud URL (Nabu Casa), if the user is logged in.
    3. The external URL configured in the main Home Assistant settings.

    The function will only attempt registration if the user is logged into Home
    Assistant Cloud. If a valid, public HTTPS URL cannot be determined, a
    `MerakiConnectionError` will be raised by the underlying `get_webhook_url`
    function, and this function will log a warning.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The ID of the webhook to register.
        secret: The secret required by the Meraki API for this webhook.
        api_client: An instance of the Meraki API client used to make the call.
        entry: The configuration entry associated with this integration instance.

    """
    if "cloud" in hass.config.components and cloud.async_is_logged_in(hass):
        try:
            webhook_url_from_entry = entry.data.get("webhook_url") if entry else None
            webhook_url = get_webhook_url(hass, webhook_id, webhook_url_from_entry)
            await api_client.register_webhook(webhook_url, secret)
        except Exception as e:
            _LOGGER.warning("Failed to register webhook: %s", e)
    else:
        _LOGGER.debug(
            "Home Assistant Cloud not connected. Skipping Cloudhook registration."
        )


async def async_unregister_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    api_client: MerakiAPIClient,
) -> None:
    """
    Unregister a webhook with the Meraki API.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The httpServerId from Meraki.
        api_client: The Meraki API client.

    """
    await api_client.unregister_webhook(webhook_id)
