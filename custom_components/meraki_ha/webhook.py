"""Webhook handling for the Meraki integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiohttp import web
from homeassistant.core import HomeAssistant

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


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
                if device.serial == device_serial:
                    _LOGGER.info(
                        "Device %s reported as down via webhook",
                        device_serial,
                    )
                    coordinator.data["devices"][i].status = "offline"
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
