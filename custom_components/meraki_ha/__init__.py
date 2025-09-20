"""The Meraki Home Assistant integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    PLATFORMS,
    WEBHOOK_ID_FORMAT,
)
from .coordinator import MerakiDataUpdateCoordinator
from .webhook import async_register_webhook
from .core.api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    coordinator = MerakiDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up webhook
    webhook_id = WEBHOOK_ID_FORMAT.format(entry_id=entry.entry_id)
    hass.data[DOMAIN][entry.entry_id]["webhook_id"] = webhook_id
    if not entry.data.get("webhook_secret"):
        secret = "".join(
            __import__("random").choice(__import__("string").ascii_letters)
            for _ in range(32)
        )
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_secret": secret}
        )
    else:
        secret = entry.data["webhook_secret"]

    await async_register_webhook(
        hass, webhook_id, secret, coordinator.api, entry=entry
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
