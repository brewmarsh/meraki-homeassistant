"""The Meraki Home Assistant integration."""

from __future__ import annotations

import logging
import secrets
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady

if TYPE_CHECKING:
    from .meraki_data_coordinator import MerakiDataCoordinator

from .api.websocket import async_setup_websocket_api
from .const import (
    CONF_ENABLE_MQTT,
    CONF_ENABLE_WEB_UI,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_MQTT_RELAY_DESTINATIONS,
    CONF_SCAN_INTERVAL,
    CONF_WEB_UI_PORT,
    DATA_CLIENT,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_MQTT_RELAY_DESTINATIONS,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEB_UI_PORT,
    DOMAIN,
    PLATFORMS,
)
from .core.api.client import MerakiAPIClient
from .core.coordinators.ssid_firewall_coordinator import SsidFirewallCoordinator
from .core.coordinators.switch_port_status_coordinator import (
    SwitchPortStatusCoordinator,
)
from .core.repositories.camera_repository import CameraRepository
from .core.repository import MerakiRepository
from .core.timed_access_manager import TimedAccessManager
from .discovery.service import DeviceDiscoveryService
from .frontend import (
    async_register_panel,
    async_register_static_path,
    async_unregister_frontend,
)
from .services.camera_service import CameraService
from .services.device_control_service import DeviceControlService
from .services.mqtt_relay import MqttRelayManager
from .services.mqtt_service import MerakiMqttService
from .services.network_control_service import NetworkControlService
from .web_api import async_setup_api
from .web_server import MerakiWebServer
from .webhook import (
    async_register_webhook,
    async_unregister_webhook,
)

_LOGGER = logging.getLogger(__name__)


def _register_organization_device(
    hass: HomeAssistant,
    entry: ConfigEntry,
    org_id: str,
    org_name: str,
) -> None:
    """Register the organization device as the top-level hub."""
    from homeassistant.helpers import device_registry as dr

    from .const import DOMAIN

    try:
        device_registry = dr.async_get(hass)
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, f"org_{org_id}")},
            name=org_name,
            manufacturer="Cisco Meraki",
            model="Organization",
        )
        _LOGGER.debug("Registered organization device: %s", org_name)
    except (AttributeError, TypeError) as err:
        _LOGGER.debug("Could not register organization device: %s", err)


def _register_device_type_groups(
    hass: HomeAssistant,
    entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
) -> None:
    """Register device type grouping devices for each network.

    Creates hierarchy: Organization → Network → Device Type Group → Device
    """
    from homeassistant.helpers import device_registry as dr

    from .const import DOMAIN
    from .helpers.device_info_helpers import (
        DEVICE_TYPE_DISPLAY_NAMES,
        DEVICE_TYPE_MODELS,
    )

    try:
        device_registry = dr.async_get(hass)
    except (AttributeError, TypeError) as err:
        _LOGGER.debug("Could not get device registry: %s", err)
        return

    # Get all networks, devices, clients, VLANs, and SSIDs
    networks = coordinator.data.get("networks", [])
    devices = coordinator.data.get("devices", [])
    clients = coordinator.data.get("clients", [])
    vlans_by_network = coordinator.data.get("vlans", {})  # Dict: {network_id: [vlans]}
    ssids_list = coordinator.data.get("ssids", [])  # List of all SSIDs (flat)

    # Group devices by network and product type
    network_product_types: dict[str, set[str]] = {}
    network_names: dict[str, str] = {}
    networks_with_clients: set[str] = set()
    networks_with_vlans: set[str] = set()
    networks_with_ssids: set[str] = set()

    for network in networks:
        network_id = network.get("id")
        if network_id:
            network_names[network_id] = network.get("name", f"Network {network_id}")
            network_product_types[network_id] = set()

    for device in devices:
        network_id = device.get("networkId")
        product_type = device.get("productType")
        if network_id and product_type:
            if network_id not in network_product_types:
                network_product_types[network_id] = set()
            network_product_types[network_id].add(product_type)

    # Track networks that have clients
    for client in clients:
        network_id = client.get("networkId")
        if network_id:
            networks_with_clients.add(network_id)

    # Track networks that have VLANs
    for network_id, vlans in vlans_by_network.items():
        if vlans and isinstance(vlans, list) and len(vlans) > 0:
            networks_with_vlans.add(network_id)

    # Track networks that have SSIDs (ssids is a flat list with networkId field)
    for ssid in ssids_list:
        network_id = ssid.get("networkId")
        if network_id:
            networks_with_ssids.add(network_id)

    # Register device type groups for each network
    for network_id, product_types in network_product_types.items():
        network_name = network_names.get(network_id, f"Network {network_id}")
        for product_type in product_types:
            display_name = DEVICE_TYPE_DISPLAY_NAMES.get(
                product_type, product_type.title()
            )
            model_name = DEVICE_TYPE_MODELS.get(product_type, "Meraki Devices")

            try:
                device_registry.async_get_or_create(
                    config_entry_id=entry.entry_id,
                    identifiers={(DOMAIN, f"devicetype_{network_id}_{product_type}")},
                    name=f"{network_name} {display_name}",
                    manufacturer="Cisco Meraki",
                    model=model_name,
                    via_device=(DOMAIN, f"network_{network_id}"),
                )
            except (AttributeError, TypeError) as err:
                _LOGGER.debug(
                    "Could not register device type group %s for network %s: %s",
                    product_type,
                    network_id,
                    err,
                )

    # Register Clients group for networks that have clients
    for network_id in networks_with_clients:
        network_name = network_names.get(network_id, f"Network {network_id}")
        try:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, f"devicetype_{network_id}_clients")},
                name=f"{network_name} Clients",
                manufacturer="Cisco Meraki",
                model="Network Clients",
                via_device=(DOMAIN, f"network_{network_id}"),
            )
        except (AttributeError, TypeError) as err:
            _LOGGER.debug(
                "Could not register Clients group for network %s: %s",
                network_id,
                err,
            )

    # Register VLANs group for networks that have VLANs
    for network_id in networks_with_vlans:
        network_name = network_names.get(network_id, f"Network {network_id}")
        try:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, f"devicetype_{network_id}_vlans")},
                name=f"{network_name} VLANs",
                manufacturer="Cisco Meraki",
                model="Network VLANs",
                via_device=(DOMAIN, f"network_{network_id}"),
            )
        except (AttributeError, TypeError) as err:
            _LOGGER.debug(
                "Could not register VLANs group for network %s: %s",
                network_id,
                err,
            )

    # Register SSIDs group for networks that have SSIDs
    for network_id in networks_with_ssids:
        network_name = network_names.get(network_id, f"Network {network_id}")
        try:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, f"devicetype_{network_id}_ssids")},
                name=f"{network_name} SSIDs",
                manufacturer="Cisco Meraki",
                model="Wireless SSIDs",
                via_device=(DOMAIN, f"network_{network_id}"),
            )
        except (AttributeError, TypeError) as err:
            _LOGGER.debug(
                "Could not register SSIDs group for network %s: %s",
                network_id,
                err,
            )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
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
        from .meraki_data_coordinator import MerakiDataCoordinator

        entry_data["coordinator"] = MerakiDataCoordinator(
            hass=hass,
            api_client=api_client,
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

    # Register the organization device as the top-level hub in the hierarchy
    # Hierarchy: Organization → Network → Device Type Group → Devices
    if coordinator.data:
        org_id = entry.data[CONF_MERAKI_ORG_ID]
        org_name = entry.data.get("org_name", f"Meraki Org {org_id}")
        _register_organization_device(hass, entry, org_id, org_name)
        # Register device type groups (Access Points, Switches, Cameras, etc.)
        _register_device_type_groups(hass, entry, coordinator)

    if "meraki_repository" not in entry_data:
        entry_data["meraki_repository"] = MerakiRepository(api_client)
    meraki_repository = entry_data["meraki_repository"]

    # Create switch port status coordinator
    switch_port_coordinator = SwitchPortStatusCoordinator(
        hass=hass,
        repository=meraki_repository,
        main_coordinator=coordinator,
        config_entry=entry,
    )
    await switch_port_coordinator.async_refresh()
    entry_data["switch_port_coordinator"] = switch_port_coordinator

    # Create content filtering and firewall coordinators
    entry_data["ssid_firewall_coordinators"] = {}
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
                entry_data["ssid_firewall_coordinators"][
                    f"{ssid['networkId']}_{ssid['number']}"
                ] = ssid_fw_coordinator

    # Start the web server if enabled
    if entry.options.get(CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI):
        port = entry.options.get(CONF_WEB_UI_PORT, DEFAULT_WEB_UI_PORT)
        server = MerakiWebServer(hass, coordinator, port)
        await server.start()
        entry_data["web_server"] = server

    # Initialize MQTT service if enabled
    if entry.options.get(CONF_ENABLE_MQTT, DEFAULT_ENABLE_MQTT):
        # Set up the relay manager for forwarding messages
        relay_destinations = entry.options.get(
            CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
        )
        relay_manager = None
        if relay_destinations:
            relay_manager = MqttRelayManager(relay_destinations)
            await relay_manager.async_start()
            entry_data["mqtt_relay_manager"] = relay_manager

        # Set up the MQTT service for receiving sensor data
        mqtt_service = MerakiMqttService(
            hass=hass,
            coordinator=coordinator,
            relay_manager=relay_manager,
        )
        if await mqtt_service.async_start():
            entry_data["mqtt_service"] = mqtt_service
            coordinator.set_mqtt_enabled(True)
            _LOGGER.info("MQTT service started for MT sensor real-time updates")
        else:
            _LOGGER.warning(
                "Failed to start MQTT service - ensure Mosquitto broker is running"
            )

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

    # Initialize Timed Access Manager
    if "timed_access_manager" not in entry_data:
        entry_data["timed_access_manager"] = TimedAccessManager(api_client)

    # Register service
    async def handle_create_timed_access(call: ServiceCall) -> None:
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

    discovered_entities = await discovery_service.discover_entities()
    entry_data["entities"] = discovered_entities

    # Register frontend panel and WebSocket API
    await async_register_static_path(hass)
    await async_register_panel(hass, entry)
    async_setup_api(hass)
    async_setup_websocket_api(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if "webhook_id" not in entry.data:
        webhook_id = entry.entry_id
        secret = secrets.token_hex(16)
        await async_register_webhook(
            hass, webhook_id, secret, api_client, entry, entry.entry_id
        )
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
        if DATA_CLIENT in entry_data:
            client = entry_data[DATA_CLIENT]
            await client.async_close()
            _LOGGER.debug("Meraki API client session closed")

        # Stop MQTT service and relay manager
        if "mqtt_service" in entry_data:
            mqtt_service = entry_data["mqtt_service"]
            await mqtt_service.async_stop()
            _LOGGER.info("MQTT service stopped")

        if "mqtt_relay_manager" in entry_data:
            relay_manager = entry_data["mqtt_relay_manager"]
            await relay_manager.async_stop()
            _LOGGER.info("MQTT relay manager stopped")

        if "web_server" in entry_data:
            server = entry_data["web_server"]
            await server.stop()

        if "webhook_id" in entry.data:
            api_client = entry_data[DATA_CLIENT]
            await async_unregister_webhook(hass, entry.entry_id, api_client)

        async_unregister_frontend(hass)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok
