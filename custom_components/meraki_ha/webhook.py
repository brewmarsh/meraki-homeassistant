"""Webhook handling for the Meraki integration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .const import (
    CONF_SCANNING_API_SECRET,
    CONF_SCANNING_API_VALIDATOR,
    DOMAIN,
)
from .core.errors import MerakiConnectionError
from .helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from .core.api import MerakiAPIClient
    from .meraki_data_coordinator import MerakiDataCoordinator


# Use feature-specific loggers - can be configured independently via:
# logger:
#   logs:
#     custom_components.meraki_ha.alerts: debug
#     custom_components.meraki_ha.scanning_api: debug
_LOGGER_ALERTS = MerakiLoggers.ALERTS
_LOGGER_SCANNING = MerakiLoggers.SCANNING_API


async def async_handle_scanning_api(
    hass: HomeAssistant,
    config_entry_id: str,
    request: web.Request,
) -> web.Response:
    """Handle a webhook from the Meraki Scanning API.

    This is the direct endpoint handler for Scanning API webhooks.
    It handles both GET (validation) and POST (data) requests.

    URL format: /api/webhook/{config_entry_id}/{validator}
    HA only matches on config_entry_id, so we extract the validator from the path.
    """
    # Extract validator from URL path (format: /api/webhook/{entry_id}/{validator})
    path_parts = request.path.strip("/").split("/")
    url_validator = path_parts[-1] if len(path_parts) >= 4 else None

    _LOGGER_SCANNING.debug(
        "Scanning API webhook received: method=%s, entry=%s, path=%s, url_validator=%s",
        request.method,
        config_entry_id,
        request.path,
        url_validator[:16] + "..." if url_validator else None,
    )

    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    if not config_entry:
        _LOGGER_SCANNING.warning(
            "Scanning API webhook: config entry %s not found", config_entry_id
        )
        return web.Response(status=404)

    configured_validator = config_entry.options.get(CONF_SCANNING_API_VALIDATOR)

    # Verify the validator in the URL matches our configured validator
    if url_validator and configured_validator and url_validator != configured_validator:
        _LOGGER_SCANNING.warning(
            "Scanning API: URL validator mismatch (url=%s, configured=%s)",
            url_validator[:16] + "..." if url_validator else None,
            configured_validator[:16] + "..." if configured_validator else None,
        )
        return web.Response(status=404)

    if request.method == "GET":
        if configured_validator:
            _LOGGER_SCANNING.debug("Scanning API GET validation - returning validator")
            return web.Response(text=configured_validator)
        _LOGGER_SCANNING.warning("Scanning API GET: no validator configured")
        return web.Response(status=404)

    if request.method == "POST":
        try:
            data = await request.json()
        except ValueError:
            _LOGGER_SCANNING.warning("Received invalid JSON in Scanning API webhook")
            return web.Response(status=400)

        _LOGGER_SCANNING.debug(
            "Scanning API POST received, type=%s", data.get("type", "unknown")
        )
        return await _handle_scanning_api_data(hass, config_entry_id, data)

    _LOGGER_SCANNING.warning("Scanning API: unsupported method %s", request.method)
    return web.Response(status=405)


async def _handle_scanning_api_data(
    hass: HomeAssistant,
    config_entry_id: str,
    data: dict,
) -> web.Response:
    """Process Scanning API data.

    This is a helper function that processes already-parsed JSON data.
    It handles secret verification and forwards data to the coordinator.

    Args:
    ----
        hass: The Home Assistant instance.
        config_entry_id: The config entry ID.
        data: The parsed JSON data from the Scanning API.

    Returns
    -------
        An aiohttp web.Response object.

    """
    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    if not config_entry:
        _LOGGER_SCANNING.warning(
            "Scanning API data handler: config entry %s not found", config_entry_id
        )
        return web.Response(status=404)

    secret = config_entry.options.get(CONF_SCANNING_API_SECRET)
    received_secret = data.get("secret")
    if not secret:
        _LOGGER_SCANNING.warning(
            "Scanning API: no secret configured in integration options"
        )
        return web.Response(status=401)
    if received_secret != secret:
        _LOGGER_SCANNING.warning(
            "Scanning API: secret mismatch (received=%s, expected=%s)",
            received_secret[:8] + "..." if received_secret else "None",
            secret[:8] + "...",
        )
        return web.Response(status=401)

    if data.get("type") == "DevicesSeen":
        _LOGGER_SCANNING.debug(
            "Scanning API: processing DevicesSeen with %d observations",
            len(data.get("data", {}).get("observations", [])),
        )
        coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry_id][
            "coordinator"
        ]
        await coordinator.async_handle_scanning_api_data(data["data"])
    else:
        _LOGGER_SCANNING.debug(
            "Scanning API: ignoring message type=%s", data.get("type")
        )

    return web.Response(status=200)


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
        webhook_url_from_entry = entry.data.get("webhook_url") if entry else None
        webhook_url = get_webhook_url(hass, webhook_id, webhook_url_from_entry)
        if config_entry_id:
            await api_client.register_webhook(webhook_url, secret)
    except (MerakiConnectionError, ValueError, TypeError) as err:
        _LOGGER_ALERTS.error("Failed to register webhook: %s", err)


async def async_unregister_webhook(
    _hass: HomeAssistant,
    config_entry_id: str,
    api_client: MerakiAPIClient,
) -> None:
    """
    Unregister a webhook with the Meraki API.

    Args:
    ----
        _hass: The Home Assistant instance (unused, kept for API consistency).
        config_entry_id: The config entry ID.
        api_client: The Meraki API client.

    """
    await api_client.unregister_webhook(config_entry_id)


async def async_handle_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    request: web.Request,
) -> web.Response:
    """
    Handle a webhook from the Meraki API.

    This function acts as a router for different webhook types. It determines
    whether the request is for the legacy alerts webhook or the new Scanning API
    based on the presence of a "type" field in the JSON payload, which is
    unique to the Scanning API.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The ID of the webhook, which corresponds to the config entry ID.
        request: The request object from aiohttp.

    Returns
    -------
        An aiohttp web.Response object.

    """
    try:
        data = await request.json()
    except ValueError:
        _LOGGER_ALERTS.warning("Received invalid JSON in webhook %s", webhook_id)
        return web.Response(status=400)

    # Differentiate between Scanning API and legacy alerts webhook
    # The Scanning API payload has a "type" field (e.g., "DevicesSeen")
    # and a "secret" field, whereas legacy alerts have "sharedSecret".
    if "type" in data and "secret" in data:
        _LOGGER_SCANNING.debug("Scanning API webhook %s received: %s", webhook_id, data)
        # Handle Scanning API data directly (request already parsed above)
        return await _handle_scanning_api_data(hass, webhook_id, data)

    # --- Legacy Alerts Webhook Handling ---
    _LOGGER_ALERTS.debug("Alerts webhook %s received: %s", webhook_id, data)

    entry_data = hass.data.get(DOMAIN, {}).get(webhook_id)
    if not entry_data:
        _LOGGER_ALERTS.warning(
            "Received webhook for unknown config entry: %s", webhook_id
        )
        return web.Response(status=404)

    secret = entry_data.get("secret")
    if not secret or data.get("sharedSecret") != secret:
        _LOGGER_ALERTS.warning("Received webhook with invalid secret: %s", webhook_id)
        return web.Response(status=401)

    coordinator = entry_data.get("coordinator")
    if not coordinator:
        _LOGGER_ALERTS.warning("Coordinator not found for webhook: %s", webhook_id)
        return web.Response(status=500)

    alert_type = data.get("alertType")
    if alert_type == "APs went down":
        device_serial = data.get("deviceSerial")
        if device_serial and coordinator.data:
            for i, device in enumerate(coordinator.data.get("devices", [])):
                if device.get("serial") == device_serial:
                    _LOGGER_ALERTS.info(
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
                    _LOGGER_ALERTS.info(
                        "Client %s connectivity changed via webhook",
                        client_mac,
                    )
                    coordinator.data["clients"][i]["status"] = (
                        "Online" if alert_data.get("connected") else "Offline"
                    )
                    coordinator.async_update_listeners()
                    break
    else:
        _LOGGER_ALERTS.debug("Ignoring webhook alert type: %s", alert_type)

    return web.Response(status=200)
