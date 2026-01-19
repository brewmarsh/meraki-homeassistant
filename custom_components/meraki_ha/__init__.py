"""The Meraki Home Assistant integration."""

import logging
<<<<<<< HEAD
import random
import string
from pathlib import Path

from homeassistant import config_entries
from homeassistant.components import frontend as hass_frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api.websocket import async_setup_websocket_api
from .const import (
    CONF_MERAKI_ORG_ID,
    DOMAIN,
    PLATFORMS,
    WEBHOOK_ID_FORMAT,
)
from .coordinator import MerakiDataUpdateCoordinator
from .core.repositories.camera_repository import CameraRepository
from .core.repository import MerakiRepository
from .services.camera_service import CameraService
from .services.device_control_service import DeviceControlService
from .web_api import async_setup_api
from .webhook import async_register_webhook

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """
    Set up the Meraki integration.

    Args:
        hass: The Home Assistant instance.
        config: The configuration.

    Returns
    -------
        Whether the setup was successful.

    """
    from . import config_flow

    config_entries.HANDLERS.register(DOMAIN)(config_flow.ConfigFlowHandler)
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up Meraki from a config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns
    -------
        Whether the setup was successful.

    """
    # Modern, async-safe asset registration
    path_to_www = Path(__file__).parent / "www"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(f"/local/{DOMAIN}", str(path_to_www), False)]
    )

    # Sidebar registration with a guard
    if "meraki" not in hass.data.get("frontend_panels", {}):
        try:
            hass_frontend.async_register_built_in_panel(
                hass,
                component_name="custom",
                sidebar_title=entry.title,
                sidebar_icon="mdi:router-network",
                frontend_url_path="meraki",
                config={
                    "config_entry_id": entry.entry_id,
                    "_panel_custom": {
                        "name": "meraki-panel",
                        "module_url": f"/local/{DOMAIN}/meraki-panel.js",
                        "embed_iframe": False,
                        "trust_external_script": True,
                    },
                },
                require_admin=True,
            )
        except Exception:
            _LOGGER.exception("Failed to register sidebar")

    async_setup_api(hass)
    async_setup_websocket_api(hass)  # Added from incoming branch
    coordinator = MerakiDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    repo = MerakiRepository(coordinator.api)
    device_control_service = DeviceControlService(repo)
    camera_repo = CameraRepository(coordinator.api, entry.data[CONF_MERAKI_ORG_ID])
    camera_service = CameraService(camera_repo)

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "meraki_client": coordinator.api,
        "device_control_service": device_control_service,
        "camera_service": camera_service,
    }

    # Set up webhook
    webhook_id = WEBHOOK_ID_FORMAT.format(entry_id=entry.entry_id)
    hass.data[DOMAIN][entry.entry_id]["webhook_id"] = webhook_id
    if not entry.data.get("webhook_secret"):
        secret = "".join(random.choice(string.ascii_letters) for _ in range(32))
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, "webhook_secret": secret},
        )
    else:
        secret = entry.data["webhook_secret"]

    await async_register_webhook(hass, webhook_id, secret, coordinator.api, entry=entry)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

=======
import secrets
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

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
from .frontend import (
    async_register_panel,
    async_register_static_path,
    async_unregister_frontend,
)
from .meraki_data_coordinator import MerakiDataCoordinator
from .services.camera_service import CameraService
from .services.device_control_service import DeviceControlService
from .services.network_control_service import NetworkControlService
from .web_api import async_setup_api
from .web_server import MerakiWebServer
from .webhook import (
    async_register_webhook,
    async_unregister_webhook,
    get_webhook_url,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    entry_data = hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {})

    try:
        if DATA_CLIENT not in entry_data:
            client = MerakiAPIClient(
                hass,
                api_key=entry.data[CONF_MERAKI_API_KEY],
                org_id=entry.data[CONF_MERAKI_ORG_ID],
            )
            await client.async_setup()
            entry_data[DATA_CLIENT] = client
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
        try:
            await entry_data["coordinator"].async_config_entry_first_refresh()
        except ConfigEntryNotReady:
            raise
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

    # Register frontend panel
    await async_register_static_path(hass)
    await async_register_panel(hass, entry)
    async_setup_api(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if "webhook_id" not in entry.data:
        webhook_id = entry.entry_id
        secret = secrets.token_hex(16)
        await async_register_webhook(hass, webhook_id, secret, api_client, entry)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_id": webhook_id, "secret": secret}
        )

>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


<<<<<<< HEAD
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload a Meraki config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns
    -------
        Whether the unload was successful.

    """
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        hass_frontend.async_remove_panel(hass, "meraki")

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """
    Reload Meraki config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    """
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
=======
async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when it has changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    entry_data = hass.data[DOMAIN].get(entry.entry_id)
    if entry_data:
        if "webhook_id" in entry.data:
            api_client = entry_data[DATA_CLIENT]
            webhook_url = get_webhook_url(hass, entry.data["webhook_id"])
            await async_unregister_webhook(hass, webhook_url, api_client)

        if "web_server" in entry_data:
            server = entry_data["web_server"]
            await server.stop()
        async_unregister_frontend(hass)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
