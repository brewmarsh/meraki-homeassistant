"""The Meraki Home Assistant integration."""

import logging
import secrets

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
    DATA_CLIENT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_WEB_UI_PORT,
    DOMAIN,
    PLATFORMS,
)
from .core.api.client import MerakiAPIClient
from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .core.coordinators.content_filtering_coordinator import ContentFilteringCoordinator
from .core.coordinators.client_firewall_coordinator import ClientFirewallCoordinator
from .web_server import MerakiWebServer
from .webhook import async_register_webhook, async_unregister_webhook

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    _LOGGER.debug("Setting up Meraki entry: %s", entry.entry_id)
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
        "content_filtering_coordinators": {},
    }

    # Create content filtering coordinators for each network with an appliance
    if coordinator.data and coordinator.data.get("networks"):
        for network in coordinator.data["networks"]:
            if "appliance" in network.get("productTypes", []):
                cf_coordinator = ContentFilteringCoordinator(
                    hass=hass,
                    api_client=api_client,
                    scan_interval=scan_interval,
                    network_id=network["id"],
                )
                await cf_coordinator.async_refresh()
                hass.data[DOMAIN][entry.entry_id]["content_filtering_coordinators"][
                    network["id"]
                ] = cf_coordinator

    # Create client firewall coordinators for each network with an appliance
    if coordinator.data and coordinator.data.get("networks"):
        hass.data[DOMAIN][entry.entry_id]["client_firewall_coordinators"] = {}
        for network in coordinator.data["networks"]:
            if "appliance" in network.get("productTypes", []):
                cfw_coordinator = ClientFirewallCoordinator(
                    hass=hass,
                    api_client=api_client,
                    scan_interval=scan_interval,
                    network_id=network["id"],
                )
                await cfw_coordinator.async_refresh()
                hass.data[DOMAIN][entry.entry_id]["client_firewall_coordinators"][
                    network["id"]
                ] = cfw_coordinator

    # Start the web server if enabled
    if entry.options.get(CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI):
        port = entry.options.get(CONF_WEB_UI_PORT, DEFAULT_WEB_UI_PORT)
        server = MerakiWebServer(hass, coordinator, port)
        await server.start()
        hass.data[DOMAIN][entry.entry_id]["web_server"] = server

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

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

        if "web_server" in hass.data[DOMAIN][entry.entry_id]:
            server = hass.data[DOMAIN][entry.entry_id]["web_server"]
            await server.stop()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

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
