"""Helper functions for setting up the Meraki integration."""

from __future__ import annotations

import logging
import secrets
import string
from typing import Any

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const.integration import DOMAIN
from .const.webhooks import WEBHOOK_ID_FORMAT
from .webhook import async_register_webhook

_LOGGER = logging.getLogger(__name__)


async def async_setup_frontend(hass: HomeAssistant) -> None:
    """Register static paths and frontend assets."""
    if "frontend" in hass.config.components:
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    url_path="/meraki_ha_static",
                    path=hass.config.path("custom_components/meraki_ha/www"),
                    cache_headers=False,
                )
            ]
        )
        add_extra_js_url(hass, "/meraki_ha_static/meraki-card.js")


async def async_setup_webhook_lifecycle(
    hass: HomeAssistant,
    entry: ConfigEntry,
    api_client: Any,
    main_coordinator: Any,
) -> str:
    """Initialize and register webhooks for the config entry."""
    webhook_id = WEBHOOK_ID_FORMAT.format(entry_id=entry.entry_id)
    hass.data[DOMAIN][entry.entry_id]["webhook_id"] = webhook_id

    new_data = {**entry.data}
    changed = False

    if not entry.data.get("webhook_secret"):
        new_data["webhook_secret"] = "".join(
            secrets.choice(string.ascii_letters) for _ in range(32)
        )
        changed = True

    if not entry.data.get("webhook_validator"):
        new_data["webhook_validator"] = "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(32)
        )
        changed = True

    if changed:
        hass.config_entries.async_update_entry(entry, data=new_data)

    secret = new_data["webhook_secret"]
    validator = new_data["webhook_validator"]

    # Store in hass.data for the webhook handler
    hass.data[DOMAIN][webhook_id] = {
        "secret": secret,
        "validator": validator,
        "coordinator": main_coordinator,
    }

    try:
        await async_register_webhook(
            hass, webhook_id, secret, api_client, validator=validator, entry=entry
        )
    except Exception as e:
        _LOGGER.error(
            "Failed to register webhook. Fast updates disabled, "
            "falling back to polling. Error: %s",
            e,
        )

    return webhook_id
