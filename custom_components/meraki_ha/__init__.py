"""The Meraki Home Assistant integration."""

import logging
import secrets

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DATA_CLIENT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    PLATFORM_DEVICE_TRACKER,
)
from .core.api.client import MerakiAPIClient
from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .webhook import async_register_webhook, async_unregister_webhook

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    try:
        api_client = MerakiAPIClient(
            api_key=entry.data[CONF_MERAKI_API_KEY],
            org_id=entry.data[CONF_MERAKI_ORG_ID],
        )
    except KeyError as err:
        _LOGGER.error("Missing required configuration: %s", err)
        return False

    try:
        scan_interval = int(
            entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        if scan_interval <= 0:
            scan_interval = DEFAULT_SCAN_INTERVAL
    except (ValueError, TypeError):
        scan_interval = DEFAULT_SCAN_INTERVAL

    coordinator = MerakiDataCoordinator(
        hass=hass,
        api_client=api_client,
        scan_interval=scan_interval,
        config_entry=entry,
    )

    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        DATA_CLIENT: api_client,
        "platforms": [],
    }

    platforms_to_load = list(PLATFORMS)
    if not entry.options.get(CONF_ENABLE_DEVICE_TRACKER, True):
        platforms_to_load.remove(PLATFORM_DEVICE_TRACKER)

    hass.data[DOMAIN][entry.entry_id]["platforms"] = platforms_to_load
    await hass.config_entries.async_forward_entry_setups(entry, platforms_to_load)

    if "webhook_id" not in entry.data:
        webhook_id = entry.entry_id
        secret = secrets.token_hex(16)
        await async_register_webhook(hass, webhook_id, secret, api_client, entry)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_id": webhook_id, "secret": secret}
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    if hass.data.get(DOMAIN) and entry.entry_id in hass.data[DOMAIN]:
        if "webhook_id" in entry.data:
            api_client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
            await async_unregister_webhook(hass, entry.data["webhook_id"], api_client)

    platforms_to_unload = hass.data[DOMAIN][entry.entry_id].get("platforms", PLATFORMS)
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, platforms_to_unload
    )

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    unload_ok = await async_unload_entry(hass, entry)
    if unload_ok:
        await async_setup_entry(hass, entry)
