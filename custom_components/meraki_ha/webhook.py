"""Webhook handling for the Meraki integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from aiohttp import web

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.webhooks import EVENT_MERAKI_WEBHOOK_ALERT
from homeassistant.components import webhook
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import NoURLAvailableError, get_url

from .core.errors import MerakiConnectionError

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from .core.api import MerakiApiClientProtocol


_LOGGER = logging.getLogger(__name__)


def _get_base_webhook_url(
    hass: HomeAssistant,
    entry_webhook_url: str | None = None,
) -> str | None:
    """Get the base webhook URL, falling back to internal if external unavailable."""
    if entry_webhook_url:
        return entry_webhook_url

    try:
        return get_url(hass, allow_internal=False, prefer_external=True)
    except NoURLAvailableError:
        _LOGGER.warning(
            "Could not determine external URL for Meraki webhooks. "
            "Trying internal URL as a fallback."
        )
        try:
            return get_url(hass, allow_internal=True, prefer_external=False)
        except NoURLAvailableError:
            _LOGGER.warning(
                "Could not determine internal URL for Meraki webhooks. "
                "Please configure an 'external_url' in Home Assistant or "
                "provide a manual override in the integration options."
            )
            return None


def _is_local_hostname(hostname: str | None) -> bool:
    """Check if the given hostname is a local network address."""
    if not hostname:
        return False
    return (
        hostname.startswith("192.168.")
        or hostname.startswith("10.")
        or hostname.startswith("172.")
        or hostname == "localhost"
        or hostname.endswith(".local")
    )


def _validate_webhook_url(base_url: str) -> bool:
    """Validate that the webhook URL meets Meraki's requirements."""
    if not base_url.startswith("https://"):
        _LOGGER.warning(
            "Meraki webhooks require HTTPS. Webhook registration skipped. "
            "The integration will run in polling-only mode."
        )
        return False

    parsed = urlparse(base_url)
    if _is_local_hostname(parsed.hostname):
        raise MerakiConnectionError(
            "Meraki webhooks require a public URL, but the current URL "
            "appears to be a local address. Please configure a public HTTPS URL.",
        )

    return True


def get_webhook_url(
    hass: HomeAssistant,
    webhook_id: str,
    entry_webhook_url: str | None = None,
) -> str | None:
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
        The full webhook URL, or None if it cannot be determined.

    Raises
    ------
        MerakiConnectionError: If the URL doesn't meet Meraki's requirements.

    """
    base_url = _get_base_webhook_url(hass, entry_webhook_url)

    if not base_url or not _validate_webhook_url(base_url):
        return None

    # Remove trailing slash if present
    base_url = base_url.rstrip("/")

    return f"{base_url}/api/webhook/{webhook_id}"


def _resolve_registration_params(
    hass: HomeAssistant,
    webhook_id: str,
    entry: ConfigEntry | None = None,
    config_entry_id: str | None = None,
) -> tuple[str | None, str | None]:
    """Resolve webhook URL and config entry ID for registration."""
    webhook_url_from_entry = entry.data.get("webhook_url") if entry else None
    webhook_url = get_webhook_url(hass, webhook_id, webhook_url_from_entry)
    resolved_id = config_entry_id or (entry.entry_id if entry else None)
    return webhook_url, resolved_id


async def async_register_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    secret: str,
    api_client: MerakiApiClientProtocol,
    entry: ConfigEntry | None = None,
    config_entry_id: str | None = None,
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
        webhook.async_register(hass, DOMAIN, "Meraki", webhook_id, async_handle_webhook)
        webhook_url, resolved_id = _resolve_registration_params(
            hass, webhook_id, entry, config_entry_id
        )
        if webhook_url and resolved_id:
            await api_client.register_webhook(webhook_url, secret, resolved_id)
    except Exception:
        _LOGGER.error("Failed to register webhook", exc_info=True)


async def async_unregister_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    api_client: MerakiApiClientProtocol,
) -> None:
    """
    Unregister a webhook with the Meraki API.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The httpServerId from Meraki.
        api_client: The Meraki API client.

    """
    webhook.async_unregister(hass, webhook_id)
    await api_client.unregister_webhook(webhook_id)


def _handle_ap_went_down_alert(data: dict, coordinator: Any) -> None:
    """Handle the 'APs went down' alert type."""
    device_serial = data.get("deviceSerial")
    if not device_serial or not coordinator.data:
        return

    devices = coordinator.data.get("devices", [])
    if not isinstance(devices, list):
        return

    for i, device in enumerate(devices):
        if not hasattr(device, "serial"):
            continue
        if device.serial == device_serial:
            _LOGGER.info(
                "Device %s reported as down via webhook",
                device_serial,
            )
            coordinator.data["devices"][i].status = "offline"
            coordinator.async_update_listeners()
            break


def _handle_client_connectivity_changed_alert(data: dict, coordinator: Any) -> None:
    """Handle the 'Client connectivity changed' alert type."""
    alert_data = data.get("alertData", {})
    client_mac = alert_data.get("mac")
    if not client_mac or not coordinator.data:
        return

    clients = coordinator.data.get("clients", [])
    if not isinstance(clients, list):
        return

    for i, client in enumerate(clients):
        if not isinstance(client, dict):
            continue
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


async def _parse_webhook_request(
    webhook_id: str,
    request: web.Request,
) -> dict[str, Any] | None:
    """Parse the JSON payload from a webhook request."""
    try:
        data = await request.json()
        _LOGGER.debug("Webhook %s received: %s", webhook_id, data)
        return data
    except ValueError:
        _LOGGER.warning("Received invalid JSON in webhook %s", webhook_id)
        return None


def _validate_webhook_payload(
    hass: HomeAssistant,
    webhook_id: str,
    data: dict[str, Any],
) -> dict[str, Any] | None:
    """Validate webhook payload and return entry data if valid."""
    entry_data = hass.data.get(DOMAIN, {}).get(webhook_id)
    if not entry_data:
        _LOGGER.warning("Received webhook for unknown config entry: %s", webhook_id)
        return None

    secret = entry_data.get("secret")
    if not secret or data.get("sharedSecret") != secret:
        _LOGGER.warning("Received webhook with invalid secret: %s", webhook_id)
        return None

    return entry_data


def _dispatch_webhook_alert(data: dict[str, Any], coordinator: Any) -> None:
    """Dispatch webhook alert to the appropriate handler."""
    alert_type = data.get("alertType")
    if alert_type == "APs went down":
        _handle_ap_went_down_alert(data, coordinator)
    elif alert_type == "Client connectivity changed":
        _handle_client_connectivity_changed_alert(data, coordinator)
    else:
        _LOGGER.debug("Ignoring webhook alert type: %s", alert_type)


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
    data = await _parse_webhook_request(webhook_id, request)
    if not data:
        return

    entry_data = _validate_webhook_payload(hass, webhook_id, data)
    if not entry_data:
        return

    # Fire event for automation triggers
    hass.bus.async_fire(EVENT_MERAKI_WEBHOOK_ALERT, data)

    coordinator = entry_data.get("coordinator")
    if not coordinator:
        _LOGGER.warning("Coordinator not found for webhook: %s", webhook_id)
        return

    _dispatch_webhook_alert(data, coordinator)
