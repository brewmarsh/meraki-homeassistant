"""The Meraki Home Assistant integration."""

import logging
import secrets
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
<<<<<<< HEAD
    CONF_ENABLE_WEB_UI,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_WEB_UI_PORT,
    DATA_CLIENT,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEB_UI_PORT,
=======
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DATA_CLIENT,
    DEFAULT_SCAN_INTERVAL,
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    DOMAIN,
    PLATFORMS,
)
from .core.api.client import MerakiAPIClient
from .core.repositories.camera_repository import CameraRepository
from .core.repository import MerakiRepository
<<<<<<< HEAD
<<<<<<< HEAD
=======
from .core.timed_access_manager import TimedAccessManager
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
from .core.timed_access_manager import TimedAccessManager
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
<<<<<<< HEAD
<<<<<<< HEAD
from .web_server import MerakiWebServer
from .webhook import (
    async_register_webhook,
    async_unregister_webhook,
    get_webhook_url,
=======
from .webhook import (
    async_register_webhook,
    async_unregister_webhook,
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
from .webhook import (
    async_register_webhook,
    async_unregister_webhook,
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
<<<<<<< HEAD
<<<<<<< HEAD
    """Set up Meraki from a config entry."""
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    """
    Set up Meraki from a config entry.

    This function initializes the API client, data coordinator, and various
    services/repositories required for the integration. It also handles the
    setup of the optional local web server and the custom frontend panel.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry.

    Returns
    -------
        True if setup is successful, False otherwise.

    Raises
    ------
        ConfigEntryNotReady: If the coordinator fails to fetch initial data.
    """
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    hass.data.setdefault(DOMAIN, {})
    entry_data = hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {})

    try:
        if DATA_CLIENT not in entry_data:
            client = MerakiAPIClient(
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
                hass,
                api_key=entry.data[CONF_MERAKI_API_KEY],
                org_id=entry.data[CONF_MERAKI_ORG_ID],
            )
            await client.async_setup()
<<<<<<< HEAD
=======
                api_key=entry.data[CONF_MERAKI_API_KEY],
                org_id=entry.data[CONF_MERAKI_ORG_ID],
            )
            # await client.async_setup() # Removed as MerakiAPIClient doesn't have async_setup in this version
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
<<<<<<< HEAD
<<<<<<< HEAD
            scan_interval=scan_interval,
=======
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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

<<<<<<< HEAD
<<<<<<< HEAD
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

=======
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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

<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    # Initialize Timed Access Manager
    if "timed_access_manager" not in entry_data:
        manager = TimedAccessManager(hass)
        await manager.async_setup()
        entry_data["timed_access_manager"] = manager

    # Register service
    async def handle_create_timed_access(call):
        ssid_number = call.data["ssid_number"]
        duration = call.data["duration"]
        name = call.data.get("name")
        passphrase = call.data.get("passphrase")
        group_policy_id = call.data.get("group_policy_id")
        network_id = call.data.get("network_id")

        if not network_id:
            _LOGGER.error(
                "Missing required parameter 'network_id' for timed access creation"
            )
            return

        manager = entry_data["timed_access_manager"]
        await manager.create_key(
            config_entry_id=entry.entry_id,
            network_id=network_id,
            ssid_number=str(ssid_number),
            duration_minutes=duration,
            name=name,
            passphrase=passphrase,
            group_policy_id=group_policy_id,
        )

    hass.services.async_register(
        DOMAIN, "create_timed_access", handle_create_timed_access
    )

<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
<<<<<<< HEAD
<<<<<<< HEAD
        await async_register_webhook(hass, webhook_id, secret, api_client, entry)
=======
        await async_register_webhook(
            hass, webhook_id, secret, api_client, entry, entry.entry_id
        )
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
        await async_register_webhook(
            hass, webhook_id, secret, api_client, entry, entry.entry_id
        )
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_id": webhook_id, "secret": secret}
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when it has changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    entry_data = hass.data[DOMAIN].get(entry.entry_id)
    if entry_data:
        if "webhook_id" in entry.data:
            api_client = entry_data[DATA_CLIENT]
<<<<<<< HEAD
<<<<<<< HEAD
            webhook_url = get_webhook_url(hass, entry.data["webhook_id"])
            await async_unregister_webhook(hass, webhook_url, api_client)

        if "web_server" in entry_data:
            server = entry_data["web_server"]
            await server.stop()
=======
            await async_unregister_webhook(hass, entry.entry_id, api_client)

>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
            await async_unregister_webhook(hass, entry.entry_id, api_client)

>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        async_unregister_frontend(hass)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok
