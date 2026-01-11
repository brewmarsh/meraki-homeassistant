"""The Meraki Home Assistant integration."""

from __future__ import annotations

import logging
import secrets
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady

from .api.websocket import async_setup_websocket_api
from .const import (
    CONF_ENABLE_MQTT,
    CONF_ENABLE_SCANNING_API,
    CONF_ENABLE_WEB_UI,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_MQTT_RELAY_DESTINATIONS,
    CONF_SCAN_INTERVAL,
    CONF_WEB_UI_PORT,
    DATA_CLIENT,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SCANNING_API,
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


def _cleanup_orphaned_devices(
    hass: HomeAssistant,
    entry: ConfigEntry,
    meraki_device_macs: set[str] | None = None,
) -> None:
    """Clean up orphaned devices from previous versions.

    Removes:
    1. Device type group devices (devicetype_*) - no longer used
    2. Client devices that are actually Meraki hardware (APs, switches, etc.)
    3. Duplicate client devices where entity now links to existing device

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    entry : ConfigEntry
        The config entry for this integration.
    meraki_device_macs : set[str] | None
        Set of Meraki device MAC addresses (normalized lowercase).
        Used to identify client devices that are actually Meraki hardware.

    """
    from homeassistant.helpers import device_registry as dr
    from homeassistant.helpers import entity_registry as er
    from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

    from .const import DOMAIN

    try:
        device_registry = dr.async_get(hass)
        entity_registry = er.async_get(hass)
    except (AttributeError, TypeError) as err:
        _LOGGER.debug("Could not get registries for cleanup: %s", err)
        return

    devices_to_remove: list[str] = []
    meraki_macs = meraki_device_macs or set()

    try:
        all_devices = list(device_registry.devices.values())
    except (AttributeError, TypeError):
        # Device registry may not be fully initialized in tests
        _LOGGER.debug("Device registry not available for cleanup")
        return

    for device in all_devices:
        # Skip devices not from our integration
        if entry.entry_id not in device.config_entries:
            continue

        # Track if this device should be removed
        should_remove = False
        remove_reason = ""

        for domain, identifier in device.identifiers:
            if domain != DOMAIN:
                continue

            # Remove device type group devices (no longer used)
            if identifier.startswith("devicetype_"):
                should_remove = True
                remove_reason = f"orphaned device type group: {identifier}"
                break

            # Check for client devices
            if identifier.startswith("client_"):
                # Extract MAC from identifier (client_XX:XX:XX:XX:XX:XX)
                mac = identifier.replace("client_", "").lower().replace("-", ":")

                # Check if this "client" is actually a Meraki device
                if mac in meraki_macs:
                    should_remove = True
                    remove_reason = f"client is actually a Meraki device (MAC {mac})"
                    break

                # Check if there's another (non-Meraki) device with this MAC
                for other_device in all_devices:
                    if other_device.id == device.id:
                        continue
                    if not other_device.connections:
                        continue

                    for conn_type, conn_id in other_device.connections:
                        if conn_type == CONNECTION_NETWORK_MAC:
                            other_mac = conn_id.lower().replace("-", ":")
                            if other_mac == mac:
                                # Found another device with same MAC
                                # Check if it's not a Meraki client device
                                is_meraki_client = any(
                                    d == DOMAIN and i.startswith("client_")
                                    for d, i in other_device.identifiers
                                )
                                if not is_meraki_client:
                                    # This is a duplicate - entity should
                                    # be on the other device
                                    should_remove = True
                                    remove_reason = (
                                        f"duplicate - MAC {mac} exists on "
                                        f"'{other_device.name}'"
                                    )
                                    break
                    if should_remove:
                        break

        if should_remove:
            _LOGGER.info(
                "Removing client device '%s': %s",
                device.name,
                remove_reason,
            )
            devices_to_remove.append(device.id)

    # Remove orphaned devices
    for device_id in devices_to_remove:
        # First remove any entities linked to this device
        entities = er.async_entries_for_device(entity_registry, device_id)
        for entity in entities:
            _LOGGER.debug("Removing orphaned entity: %s", entity.entity_id)
            entity_registry.async_remove(entity.entity_id)

        # Then remove the device
        device_registry.async_remove_device(device_id)

    if devices_to_remove:
        _LOGGER.info("Cleaned up %d orphaned devices", len(devices_to_remove))


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
    # Note: Device type groups (Access Points, Switches, etc.) are not registered
    # as separate devices since HA doesn't support collapsible hierarchy in the UI.
    # The via_device relationship only shows "Connected via" text.
    if coordinator.data:
        org_id = entry.data[CONF_MERAKI_ORG_ID]
        org_name = entry.data.get("org_name", f"Meraki Org {org_id}")
        _register_organization_device(hass, entry, org_id, org_name)

    # Clean up orphaned devices from previous versions
    # This removes device type groups, Meraki devices that were created as clients,
    # and duplicate client devices
    meraki_device_macs: set[str] = set()
    if coordinator.data:
        for device in coordinator.data.get("devices", []):
            device_mac = device.get("mac")
            if device_mac:
                meraki_device_macs.add(device_mac.lower().replace("-", ":"))
    _cleanup_orphaned_devices(hass, entry, meraki_device_macs)

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

    # Register webhooks for legacy alerts if enabled
    # Note: Scanning API does not use programmatic registration
    if "webhook_id" not in entry.data and not entry.options.get(
        CONF_ENABLE_SCANNING_API, DEFAULT_ENABLE_SCANNING_API
    ):
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
