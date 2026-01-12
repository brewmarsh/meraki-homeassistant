"""Webhook handling for the Meraki integration."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .const import (
    CONF_SCANNING_API_SECRET,
    CONF_SCANNING_API_VALIDATOR,
    CONF_WEBHOOK_SHARED_SECRET,
    DOMAIN,
)
from .core.errors import MerakiConnectionError
from .handlers import (
    client_alerts,
    device_alerts,
    network_alerts,
    security_alerts,
    sensor_alerts,
)
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
) -> bool:
    """
    Register a webhook with the Meraki API.

    Args:
    ----
        hass: The Home Assistant instance.
        webhook_id: The ID of the webhook.
        secret: The secret for the webhook.
        api_client: The Meraki API client.
        entry: The config entry.
        config_entry_id: The config entry ID (used in webhook name).

    Returns
    -------
        True if registration was successful, False otherwise.

    """
    if not config_entry_id:
        _LOGGER_ALERTS.error("Cannot register webhook without config_entry_id")
        return False

    try:
        webhook_url_from_entry = entry.data.get("webhook_url") if entry else None
        webhook_url = get_webhook_url(hass, webhook_id, webhook_url_from_entry)
        await api_client.register_webhook(webhook_url, secret, config_entry_id)
        _LOGGER_ALERTS.info(
            "Successfully registered webhook with Meraki Dashboard: %s", webhook_url
        )
        return True
    except (MerakiConnectionError, ValueError, TypeError) as err:
        _LOGGER_ALERTS.error("Failed to register webhook: %s", err)
        return False


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


async def _validate_shared_secret(
    request_secret: str | None,
    config_entry: ConfigEntry,
) -> bool:
    """Validate the shared secret from the webhook request.

    The secret can be stored in two places:
    1. config_entry.options[CONF_WEBHOOK_SHARED_SECRET] - user-configured
    2. config_entry.data["secret"] - auto-generated during registration

    We check both locations for flexibility.
    """
    # First, check user-configured secret in options
    configured_secret = config_entry.options.get(CONF_WEBHOOK_SHARED_SECRET)

    # If not in options, check auto-generated secret in data
    if not configured_secret:
        configured_secret = config_entry.data.get("secret")

    if not configured_secret:
        _LOGGER_ALERTS.warning(
            "No webhook shared secret is configured. "
            "Please configure a shared secret in the integration options."
        )
        return False

    if request_secret != configured_secret:
        _LOGGER_ALERTS.warning(
            "Webhook shared secret mismatch. "
            "Received secret does not match configured secret."
        )
        return False

    return True


async def _route_by_alert_type(
    coordinator: MerakiDataCoordinator,
    alert_type: str,
    data: dict,
) -> None:
    """Route webhook data to the appropriate handler based on alertType.

    This function also marks the webhook as received to enable polling reduction.

    Alert type categories:
    - Device: AP/Switch/Gateway/Camera/Sensor up/down, rebooted
    - Client: connectivity changed, new client, blocked
    - Network: settings changed (SSID, VLAN, firewall)
    - Security: rogue AP, intrusion, malware
    - Sensor: temperature, humidity, water, door, power thresholds
    """
    # Track processing start time for metrics
    start_time = datetime.now()

    # Mark that we received a valid webhook - enables polling reduction
    # Also handles deduplication via alertId
    alert_id = data.get("alertId")
    is_new = coordinator.mark_webhook_received(alert_type, alert_id)
    if not is_new:
        # This is a duplicate alert, skip processing
        return

    # Track webhook count by alert type (for metrics)
    webhook_counts = getattr(coordinator, "_webhook_counts_by_type", {})
    webhook_counts[alert_type] = webhook_counts.get(alert_type, 0) + 1
    coordinator._webhook_counts_by_type = webhook_counts

    alert_lower = alert_type.lower()

    # Device alerts: status changes and reboots
    if (
        alert_type.startswith("APs")
        or alert_type.startswith("Switches")
        or alert_type.startswith("Gateways")
        or alert_type.startswith("Cameras")
        or alert_type.startswith("Sensors")
        or "went down" in alert_lower
        or "came up" in alert_lower
        or "went offline" in alert_lower
        or "came online" in alert_lower
        or "rebooted" in alert_lower
    ):
        await device_alerts.async_handle_device_alert(coordinator, alert_type, data)

    # Client alerts: connectivity, new clients, blocked
    elif (
        "client" in alert_lower
        or "connectivity" in alert_lower
        or "new client" in alert_lower
        or "blocked" in alert_lower
    ):
        await client_alerts.async_handle_client_alert(coordinator, alert_type, data)

    # Network/configuration alerts
    elif (
        "settings changed" in alert_lower
        or "ssid" in alert_lower
        or "vlan" in alert_lower
        or "firewall" in alert_lower
        or "configuration" in alert_lower
    ):
        await network_alerts.async_handle_network_alert(coordinator, alert_type, data)

    # Security alerts
    elif (
        "rogue" in alert_lower
        or "intrusion" in alert_lower
        or "malware" in alert_lower
        or "security" in alert_lower
        or "threat" in alert_lower
    ):
        await security_alerts.async_handle_security_alert(coordinator, alert_type, data)

    # MT Sensor alerts: environmental thresholds
    elif (
        "temperature" in alert_lower
        or "humidity" in alert_lower
        or "water" in alert_lower
        or "door" in alert_lower
        or "power" in alert_lower
        or "threshold" in alert_lower
        or "sensor" in alert_lower
    ):
        await sensor_alerts.async_handle_sensor_alert(coordinator, alert_type, data)

    else:
        _LOGGER_ALERTS.debug("No handler for webhook alert type: %s", alert_type)

    # Track processing duration for metrics
    duration_ms = (datetime.now() - start_time).total_seconds() * 1000
    durations = getattr(coordinator, "_webhook_processing_durations", [])
    durations.append(duration_ms)
    # Keep only last 1000 samples to avoid memory growth
    if len(durations) > 1000:
        durations = durations[-1000:]
    coordinator._webhook_processing_durations = durations


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

    # Differentiate between Scanning API and alerts webhook
    if "type" in data and "secret" in data:
        return await _handle_scanning_api_data(hass, webhook_id, data)

    # --- Alerts Webhook Handling ---
    _LOGGER_ALERTS.debug("Alerts webhook %s received: %s", webhook_id, data)

    config_entry = hass.config_entries.async_get_entry(webhook_id)
    if not config_entry:
        _LOGGER_ALERTS.warning(
            "Received webhook for unknown config entry: %s", webhook_id
        )
        return web.Response(status=404)

    if not await _validate_shared_secret(data.get("sharedSecret"), config_entry):
        return web.Response(status=401)

    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][webhook_id]["coordinator"]
    alert_type = data.get("alertType")

    if alert_type:
        await _route_by_alert_type(coordinator, alert_type, data)
    else:
        _LOGGER_ALERTS.warning("Webhook received with no alertType: %s", data)

    return web.Response(status=200)
