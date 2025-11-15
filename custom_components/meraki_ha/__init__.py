"""The Meraki Home Assistant integration."""

import logging
import secrets
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ENABLE_WEB_UI,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_WEB_UI_PORT,
    DATA_CLIENT,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEB_UI_PORT,
    DOMAIN,
    PLATFORMS,
)
from .core.api.client import MerakiAPIClient
from .core.repositories.camera_repository import CameraRepository
from .core.repository import MerakiRepository
from .discovery.service import DeviceDiscoveryService
from .meraki_data_coordinator import MerakiDataCoordinator
from .services.camera_service import CameraService
from .services.device_control_service import DeviceControlService
from .services.network_control_service import NetworkControlService
from .web_server import MerakiWebServer
from .webhook import async_register_webhook, async_unregister_webhook

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_or_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up or update Meraki from a config entry."""
    _LOGGER.debug("Setting up or updating Meraki entry: %s", entry.entry_id)

    entry_data = hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {})

    try:
        if DATA_CLIENT not in entry_data:
            entry_data[DATA_CLIENT] = MerakiAPIClient(
                hass,
                api_key=entry.data[CONF_MERAKI_API_KEY],
                org_id=entry.data[CONF_MERAKI_ORG_ID],
            )
        api_client = entry_data[DATA_CLIENT]
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

    if "coordinator" not in entry_data:
        entry_data["coordinator"] = MerakiDataCoordinator(
            hass=hass,
            api_client=api_client,
            scan_interval=scan_interval,
            entry=entry,
        )
        await entry_data["coordinator"].async_config_entry_first_refresh()
    else:
        entry_data["coordinator"].update_interval = timedelta(seconds=scan_interval)
        await entry_data["coordinator"].async_refresh()
    coordinator = entry_data["coordinator"]

    if "meraki_repository" not in entry_data:
        entry_data["meraki_repository"] = MerakiRepository(api_client)
    meraki_repository = entry_data["meraki_repository"]

    # Handle web server
    web_ui_enabled = entry.options.get(CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI)
    web_server = entry_data.get("web_server")
    if web_ui_enabled:
        if not web_server:
            port = entry.options.get(CONF_WEB_UI_PORT, DEFAULT_WEB_UI_PORT)
            server = MerakiWebServer(hass, coordinator, port)
            await server.start()
            entry_data["web_server"] = server
        else:
            # Check if port changed
            new_port = entry.options.get(CONF_WEB_UI_PORT, DEFAULT_WEB_UI_PORT)
            if web_server.port != new_port:
                await web_server.stop()
                server = MerakiWebServer(hass, coordinator, new_port)
                await server.start()
                entry_data["web_server"] = server
    elif web_server:
        # Web UI was disabled
        await web_server.stop()
        entry_data.pop("web_server", None)

    # Initialize repositories and services for the new architecture
    if "control_service" not in entry_data:
        entry_data["control_service"] = DeviceControlService(meraki_repository)
    control_service = entry_data["control_service"]

    if "camera_repository" not in entry_data:
        entry_data["camera_repository"] = CameraRepository(
            api_client, api_client.organization_id
        )
    camera_repository = entry_data["camera_repository"]

    if "camera_service" not in entry_data:
        entry_data["camera_service"] = CameraService(camera_repository)
    camera_service = entry_data["camera_service"]

    if "network_control_service" not in entry_data:
        entry_data["network_control_service"] = NetworkControlService(
            api_client, coordinator
        )
    network_control_service = entry_data["network_control_service"]

    # New discovery service setup.
    if "discovery_service" not in entry_data:
        entry_data["discovery_service"] = DeviceDiscoveryService(
            coordinator=coordinator,
            config_entry=entry,
            meraki_client=api_client,
            camera_service=camera_service,
            control_service=control_service,
            network_control_service=network_control_service,
        )
    discovery_service = entry_data["discovery_service"]

    discovered_entities = await discovery_service.discover_entities()
    entry_data["entities"] = discovered_entities

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if "webhook_id" not in entry.data:
        webhook_id = entry.entry_id
        secret = secrets.token_hex(16)
        await async_register_webhook(hass, webhook_id, secret, api_client, entry)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_id": webhook_id, "secret": secret}
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    if not await async_setup_or_update_entry(hass, entry):
        return False

    entry.async_on_unload(entry.add_update_listener(async_update_entry))
    return True


async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update a given config entry."""
    await async_setup_or_update_entry(hass, entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    entry_data = hass.data[DOMAIN].get(entry.entry_id)
    if entry_data:
        if "webhook_id" in entry.data:
            api_client = entry_data[DATA_CLIENT]
            await async_unregister_webhook(hass, entry.data["webhook_id"], api_client)

        if "web_server" in entry_data:
            server = entry_data["web_server"]
            await server.stop()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok
