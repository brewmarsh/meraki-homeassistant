"""Webhook handling for the Meraki integration."""

import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN, WEBHOOK_ID_FORMAT

_LOGGER = logging.getLogger(__name__)


def get_webhook_url(hass: HomeAssistant, webhook_id: str) -> str:
    """Get the URL for a webhook."""
    return f"{hass.config.internal_url}/api/webhook/{webhook_id}"


async def async_register_webhook(
    hass: HomeAssistant, webhook_id: str, secret: str, api_client: "MerakiAPIClient"
) -> None:
    """Register a webhook with the Meraki API."""
    webhook_url = get_webhook_url(hass, webhook_id)
    await api_client.register_webhook(webhook_url, secret)


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
