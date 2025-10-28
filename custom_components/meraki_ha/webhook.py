"""Webhook handling for the Meraki integration."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .const import DOMAIN
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

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The ID of the webhook.
        secret: The secret for the webhook.
        api_client: The Meraki API client.
        entry: The config entry.

    """
    try:
        webhook_url_from_entry = entry.data.get("webhook_url") if entry else None
        webhook_url = get_webhook_url(hass, webhook_id, webhook_url_from_entry)
        await api_client.register_webhook(webhook_url, secret)
    except Exception as err:
        _LOGGER.error("Failed to register webhook: %s", err)


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


async def async_handle_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    request: web.Request,
) -> None:
    """
    Handle a webhook from the Meraki API.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The ID of the webhook.
        request: The request object.

    """
    try:
        data = await request.json()
        _LOGGER.debug("Webhook %s received: %s", webhook_id, data)
    except ValueError:
        _LOGGER.warning("Received invalid JSON in webhook %s", webhook_id)
        return

    entry_data = hass.data.get(DOMAIN, {}).get(webhook_id)
    if not entry_data:
        _LOGGER.warning("Received webhook for unknown config entry: %s", webhook_id)
        return

    secret = entry_data.get("secret")
    if not secret or data.get("sharedSecret") != secret:
        _LOGGER.warning("Received webhook with invalid secret: %s", webhook_id)
        return

    coordinator = entry_data.get("coordinator")
    if not coordinator:
        _LOGGER.warning("Coordinator not found for webhook: %s", webhook_id)
        return

    alert_type = data.get("alertType")
    if alert_type == "APs went down":
        device_serial = data.get("deviceSerial")
        if device_serial and coordinator.data:
            for i, device in enumerate(coordinator.data.get("devices", [])):
                if device.get("serial") == device_serial:
                    _LOGGER.info(
                        "Device %s reported as down via webhook",
                        device_serial,
                    )
                    coordinator.data["devices"][i]["status"] = "offline"
                    coordinator.async_update_listeners()
                    break
    elif alert_type == "Client connectivity changed":
        alert_data = data.get("alertData", {})
        client_mac = alert_data.get("mac")
        if client_mac and coordinator.data:
            for i, client in enumerate(coordinator.data.get("clients", [])):
                if client.get("mac") == client_mac:
                    _LOGGER.info(
                        "Client %s connectivity changed via webhook",
                        client_mac,
                    )
                    coordinator.data["clients"][i]["status"] = (
                        "Online" if alert_data.get("connected") else "Offline"
                    )
                    coordinator.async_update_listeners()
                    break
    else:
        _LOGGER.debug("Ignoring webhook alert type: %s", alert_type)
