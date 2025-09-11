"""The Meraki Home Assistant integration."""

import logging
import secrets

from yarl import URL
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.network import get_url
from homeassistant.components.frontend import (
    async_register_built_in_panel,
    async_remove_panel,
)

from .api.websocket import async_setup_websocket_api
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
from .core.coordinators.switch_port_status_coordinator import (
    SwitchPortStatusCoordinator,
)
from .core.coordinators.ssid_firewall_coordinator import SsidFirewallCoordinator
from .core.repository import MerakiRepository
from .web_server import MerakiWebServer
from .webhook import async_register_webhook, async_unregister_webhook
from .core.repositories.camera_repository import CameraRepository
from .services.device_control_service import DeviceControlService
from .services.camera_service import CameraService
from .services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    async_setup_websocket_api(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    _LOGGER.debug("Setting up Meraki entry: %s", entry.entry_id)
    try:
        api_client = MerakiAPIClient(
            hass=hass,
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
    }

    # Create switch port status coordinator
    repository = MerakiRepository(api_client)
    switch_port_coordinator = SwitchPortStatusCoordinator(
        hass=hass,
        repository=repository,
        main_coordinator=coordinator,
        config_entry=entry,
    )
    await switch_port_coordinator.async_refresh()
    hass.data[DOMAIN][entry.entry_id]["switch_port_coordinator"] = (
        switch_port_coordinator
    )

    # Create content filtering and firewall coordinators
    hass.data[DOMAIN][entry.entry_id]["ssid_firewall_coordinators"] = {}
    if coordinator.data:
        # Create per-SSID coordinators
        for ssid in coordinator.data.get("ssids", []):
            if "networkId" in ssid and "number" in ssid:
                # L7 Firewall Coordinator
                ssid_fw_coordinator = SsidFirewallCoordinator(
                    hass=hass,
                    api_client=api_client,
                    scan_interval=scan_interval,
                    network_id=ssid["networkId"],
                    ssid_number=ssid["number"],
                )
                await ssid_fw_coordinator.async_refresh()
                hass.data[DOMAIN][entry.entry_id]["ssid_firewall_coordinators"][
                    f"{ssid['networkId']}_{ssid['number']}"
                ] = ssid_fw_coordinator

    # Start the web server and register the panel if enabled
    if entry.options.get(CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI):
        port = entry.options.get(CONF_WEB_UI_PORT, DEFAULT_WEB_UI_PORT)
        server = MerakiWebServer(hass, coordinator, port)
        await server.start()
        hass.data[DOMAIN][entry.entry_id]["web_server"] = server

        # Register the panel
        _LOGGER.debug("Attempting to register Meraki web UI panel.")
        hass_url = URL(get_url(hass, require_current_request=False))
        panel_url = str(hass_url.with_port(port))
        _LOGGER.debug("Calculated panel URL: %s", panel_url)
        async_register_built_in_panel(
            hass,
            component_name="meraki",
            sidebar_title="Meraki",
            sidebar_icon="mdi:cisco-webex",
            frontend_url_path="meraki",
            config={
                "_panel_custom": {
                    "name": "ha-panel-iframe",
                    "embed_iframe": True,
                    "trust_external_script": True,
                    "url": panel_url,
                }
            },
            require_admin=True,
        )

    # Initialize repositories and services for the new architecture
    meraki_repository = MerakiRepository(api_client)
    control_service = DeviceControlService(meraki_repository)
    camera_repository = CameraRepository(api_client, api_client.organization_id)
    camera_service = CameraService(camera_repository)
    network_control_service = NetworkControlService(api_client, coordinator)

    # Defer import to avoid circular dependencies and blocking startup
    from .discovery.service import DeviceDiscoveryService

    # New discovery service setup. We now pass both the control and camera services.
    discovery_service = DeviceDiscoveryService(
        coordinator=coordinator,
        config_entry=entry,
        meraki_client=api_client,
        switch_port_coordinator=switch_port_coordinator,
        camera_service=camera_service,
        control_service=control_service,
        network_control_service=network_control_service,
    )
    # The discover_entities method is asynchronous and must be awaited
    discovered_entities = await discovery_service.discover_entities()
    hass.data[DOMAIN][entry.entry_id]["entities"] = discovered_entities

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if "webhook_http_server_id" not in entry.data:
        # The webhook_id for Home Assistant is the config entry id
        webhook_id = entry.entry_id
        secret = secrets.token_hex(16)
        webhook = await async_register_webhook(
            hass, webhook_id, secret, api_client, entry
        )
        if webhook and "id" in webhook:
            hass.config_entries.async_update_entry(
                entry,
                data={
                    **entry.data,
                    "webhook_http_server_id": webhook["id"],
                    "secret": secret,
                },
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    if hass.data.get(DOMAIN) and entry.entry_id in hass.data[DOMAIN]:
        if "webhook_http_server_id" in entry.data:
            api_client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
            await async_unregister_webhook(
                hass, entry.data["webhook_http_server_id"], api_client
            )

        if "web_server" in hass.data[DOMAIN][entry.entry_id]:
            server = hass.data[DOMAIN][entry.entry_id]["web_server"]
            await server.stop()
            async_remove_panel(hass, "meraki")

    try:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    except ValueError:
        _LOGGER.debug("Ignoring 'Config entry was never loaded!' error during unload.")
        unload_ok = True

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
