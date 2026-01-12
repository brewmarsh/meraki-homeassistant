"""The Meraki Home Assistant integration."""

from __future__ import annotations

import secrets
from collections.abc import Awaitable, Callable
from datetime import timedelta
from typing import Any

from homeassistant.components import webhook as ha_webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .api.websocket import async_setup_websocket_api
from .const import (
    CONF_ENABLE_MQTT,
    CONF_ENABLE_SCANNING_API,
    CONF_ENABLE_WEB_UI,
    CONF_ENABLE_WEBHOOKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_MQTT_RELAY_DESTINATIONS,
    CONF_SCAN_INTERVAL,
    CONF_SCANNING_API_VALIDATOR,
    CONF_WEB_UI_PORT,
    CONF_WEBHOOK_SHARED_SECRET,
    DATA_CLIENT,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SCANNING_API,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_ENABLE_WEBHOOKS,
    DEFAULT_MQTT_RELAY_DESTINATIONS,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCANNING_API_VALIDATOR,
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
from .helpers.logging_helper import MerakiLoggers

# sync_helper is used by services/sync_client_names
from .services.camera_service import CameraService
from .services.device_control_service import DeviceControlService
from .services.mqtt_relay import MqttRelayManager
from .services.mqtt_service import MerakiMqttService
from .services.network_control_service import NetworkControlService
from .web_api import async_setup_api
from .web_server import MerakiWebServer
from .webhook import (
    async_handle_scanning_api,
    async_handle_webhook,
    async_unregister_webhook,
)
from .webhook import (
    async_register_webhook as _async_register_webhook,
)
from .webhook_manager import WebhookManager

_LOGGER = MerakiLoggers.MAIN
async_register_webhook = (
    _async_register_webhook  # re-export for backward compatibility/tests
)


def _create_scanning_api_handler(
    config_entry_id: str,
) -> Callable[[HomeAssistant, str, Any], Awaitable[Any]]:
    """Create a webhook handler closure for the Scanning API.

    This creates a handler function that captures the config_entry_id,
    allowing proper routing of webhook requests to the correct integration instance.
    """
    from aiohttp import web  # pylint: disable=import-outside-toplevel

    async def handler(
        hass: HomeAssistant,
        _webhook_id: str,  # Required by HA webhook API, not used here
        request: web.Request,
    ) -> web.Response:
        """Handle incoming Scanning API webhook requests."""
        return await async_handle_scanning_api(hass, config_entry_id, request)

    return handler


def _register_organization_device(
    hass: HomeAssistant,
    entry: ConfigEntry,
    org_id: str,
    org_name: str,
) -> None:
    """Register the organization device as the top-level hub."""
    # pylint: disable=import-outside-toplevel
    # Deferred imports to avoid blocking startup
    from homeassistant.helpers import device_registry as dr

    from .const import DOMAIN

    # pylint: enable=import-outside-toplevel

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
    # Deferred imports to avoid blocking startup
    # pylint: disable=import-outside-toplevel
    from homeassistant.helpers import device_registry as dr
    from homeassistant.helpers import entity_registry as er
    from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

    from .const import DOMAIN
    # pylint: enable=import-outside-toplevel

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

    # Apply user-configured log levels for feature loggers
    # pylint: disable-next=import-outside-toplevel
    from .helpers.logging_helper import apply_log_levels

    apply_log_levels(dict(entry.options))

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
        # pylint: disable-next=import-outside-toplevel
        from .meraki_data_coordinator import MerakiDataCoordinator

        entry_data["coordinator"] = MerakiDataCoordinator(
            hass=hass,
            api_client=api_client,
            entry=entry,
        )
        # Let ConfigEntryNotReady propagate to signal HA to retry setup
        await entry_data["coordinator"].async_config_entry_first_refresh()
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

    async def async_sync_client_names(_call: ServiceCall) -> None:
        """Service call to sync client names from HA to Meraki Dashboard.

        This finds all Meraki clients that have matching Home Assistant devices
        (by MAC address) and updates their names in the Meraki Dashboard to
        match the HA device names.
        """
        # pylint: disable-next=import-outside-toplevel
        from .helpers.sync_helper import get_sync_candidates

        if not coordinator.data or "clients" not in coordinator.data:
            _LOGGER.warning("No client data available for sync")
            return

        # Get candidates using config entry options for include_model/include_version
        clients_to_update = get_sync_candidates(
            hass, coordinator.data["clients"], entry
        )

        if not clients_to_update:
            _LOGGER.info("No clients need name sync - all names are current")
            return

        _LOGGER.info(
            "Syncing %d client names to Meraki Dashboard", len(clients_to_update)
        )

        # Group by network and update
        networks = {c["networkId"] for c in clients_to_update if c.get("networkId")}
        for network_id in networks:
            network_clients = [
                {"mac": c["mac"], "name": c["name"]}
                for c in clients_to_update
                if c.get("networkId") == network_id
            ]
            if network_clients:
                try:
                    await api_client.network.provision_network_clients(
                        network_id, network_clients
                    )
                    _LOGGER.info(
                        "Synced %d clients to network %s",
                        len(network_clients),
                        network_id,
                    )
                except (TimeoutError, OSError) as e:
                    _LOGGER.error(
                        "Failed to sync clients to network %s: %s", network_id, e
                    )

    hass.services.async_register(DOMAIN, "sync_client_names", async_sync_client_names)

    discovered_entities = await discovery_service.discover_entities()
    entry_data["entities"] = discovered_entities

    # Register frontend panel and WebSocket API
    await async_register_static_path(hass)
    await async_register_panel(hass, entry)
    async_setup_api(hass)
    async_setup_websocket_api(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register webhooks (alerts + optional Scanning API)
    scanning_api_enabled = entry.options.get(
        CONF_ENABLE_SCANNING_API, DEFAULT_ENABLE_SCANNING_API
    )
    enable_webhooks = entry.options.get(CONF_ENABLE_WEBHOOKS, DEFAULT_ENABLE_WEBHOOKS)

    # Determine shared secret once and persist for stability across reloads
    webhook_secret = entry.options.get(CONF_WEBHOOK_SHARED_SECRET) or entry.data.get(
        "secret"
    )
    if not webhook_secret:
        webhook_secret = secrets.token_hex(16)

    if enable_webhooks:
        # Use unique webhook ID for alerts to prevent conflicts with scanning API
        webhook_id = f"{entry.entry_id}_alerts"

        # Unregister any existing webhook before registering to handle reloads
        try:
            ha_webhook.async_unregister(hass, webhook_id)
        except ValueError:
            pass  # Webhook wasn't registered, which is fine

        ha_webhook.async_register(
            hass,
            DOMAIN,
            "Meraki Alerts",
            webhook_id,
            async_handle_webhook,
        )
        entry_data["webhook_id"] = webhook_id

        webhook_manager = WebhookManager(hass, api_client, entry)
        entry_data["webhook_manager"] = webhook_manager

        # Persist secret for future reloads
        if "webhook_id" not in entry.data or entry.data.get("secret") != webhook_secret:
            hass.config_entries.async_update_entry(
                entry,
                data={**entry.data, "webhook_id": webhook_id, "secret": webhook_secret},
            )

        registered = await webhook_manager.async_register_webhooks()
        if registered:
            _LOGGER.info("Registered alerts webhook for config entry %s", webhook_id)
        else:
            _LOGGER.warning(
                "Alerts webhook registration with Meraki Dashboard failed for %s. "
                "Webhook will still receive alerts if manually configured.",
                webhook_id,
            )

        # If Scanning API is also enabled, register with a separate unique ID
        if scanning_api_enabled:
            validator = entry.options.get(
                CONF_SCANNING_API_VALIDATOR, DEFAULT_SCANNING_API_VALIDATOR
            )
            if validator:
                # Use unique webhook ID for scanning API
                scanning_webhook_id = f"{entry.entry_id}_scanning"

                # Unregister any existing webhook before registering
                try:
                    ha_webhook.async_unregister(hass, scanning_webhook_id)
                except ValueError:
                    pass

                ha_webhook.async_register(
                    hass,
                    DOMAIN,
                    "Meraki Scanning API",
                    scanning_webhook_id,
                    _create_scanning_api_handler(entry.entry_id),
                    allowed_methods=["GET", "POST"],
                )
                entry_data["scanning_webhook_id"] = scanning_webhook_id
                _LOGGER.info(
                    "Registered Scanning API webhook (with alerts): "
                    "/api/webhook/%s/{validator}",
                    scanning_webhook_id,
                )
            else:
                _LOGGER.warning(
                    "Scanning API enabled but no validator configured for %s",
                    entry.entry_id,
                )
    else:
        # Ensure alerts webhook is not registered when disabled
        existing_webhook_id = entry.data.get("webhook_id")
        if existing_webhook_id:
            try:
                ha_webhook.async_unregister(hass, existing_webhook_id)
            except ValueError:
                pass
            await async_unregister_webhook(hass, entry.entry_id, api_client)

        if scanning_api_enabled:
            # Register Scanning API webhook with validator path when alerts are disabled
            validator = entry.options.get(
                CONF_SCANNING_API_VALIDATOR, DEFAULT_SCANNING_API_VALIDATOR
            )
            if validator:
                # Use unique webhook ID for scanning API
                scanning_webhook_id = f"{entry.entry_id}_scanning"

                # Unregister any existing webhook before registering
                try:
                    ha_webhook.async_unregister(hass, scanning_webhook_id)
                except ValueError:
                    pass

                ha_webhook.async_register(
                    hass,
                    DOMAIN,
                    "Meraki Scanning API",
                    scanning_webhook_id,
                    _create_scanning_api_handler(entry.entry_id),
                    allowed_methods=["GET", "POST"],
                )
                entry_data["scanning_webhook_id"] = scanning_webhook_id
                _LOGGER.info(
                    "Registered Scanning API webhook: /api/webhook/%s/{validator}",
                    scanning_webhook_id,
                )
            else:
                _LOGGER.warning(
                    "Scanning API enabled but no validator configured for %s",
                    entry.entry_id,
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

        # Unregister Scanning API webhook
        if "scanning_webhook_id" in entry_data:
            try:
                ha_webhook.async_unregister(hass, entry_data["scanning_webhook_id"])
                _LOGGER.info(
                    "Unregistered Scanning API webhook: %s",
                    entry_data["scanning_webhook_id"],
                )
            except ValueError:
                _LOGGER.debug(
                    "Scanning API webhook already unregistered: %s",
                    entry_data["scanning_webhook_id"],
                )

        # Unregister alerts webhook and clean up Meraki HTTP servers
        webhook_id = entry_data.get("webhook_id") or entry.data.get("webhook_id")
        if webhook_id:
            try:
                ha_webhook.async_unregister(hass, webhook_id)
                _LOGGER.info("Unregistered alerts webhook: %s", webhook_id)
            except ValueError:
                _LOGGER.debug("Alerts webhook already unregistered: %s", webhook_id)
            api_client = entry_data[DATA_CLIENT]
            if "webhook_manager" in entry_data:
                await entry_data["webhook_manager"].async_unregister_webhooks()
            else:
                await async_unregister_webhook(hass, entry.entry_id, api_client)

        async_unregister_frontend(hass)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok
