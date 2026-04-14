"""The Meraki Home Assistant integration."""

from __future__ import annotations

import asyncio
import logging
import secrets
import string
from typing import Any

from custom_components.meraki_ha.const.config import (
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.platform import PLATFORMS
from custom_components.meraki_ha.const.webhooks import WEBHOOK_ID_FORMAT
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api.websocket import async_setup_websocket_api
from .coordinators import (
    MerakiApplianceCoordinator,
    MerakiCameraCoordinator,
    MerakiClientCoordinator,
    MerakiDeviceCoordinator,
    MerakiMainCoordinator,
    MerakiSensorCoordinator,
    MerakiSwitchCoordinator,
    MerakiWirelessCoordinator,
)
from .core.api.factory import create_api_client
from .core.repositories.camera_repository import CameraRepository
from .core.repository import MerakiRepository
from .discovery.coordinator import DiscoveryCoordinator
from .discovery.service import DeviceDiscoveryService
from .helpers.migrations import async_cleanup_ghost_devices, async_migrate_entities
from .services import async_setup_services
from .services.camera_service import CameraService
from .services.device_control_service import DeviceControlService
from .services.ipsk_manager import IPSKManager
from .services.manager import ServicesManager
from .services.network_control_service import NetworkControlService
from .services.switch_port_service import SwitchPortService
from .webhook import async_register_webhook, async_unregister_webhook

_LOGGER = logging.getLogger(__name__)

# Set up logging for the coordinator move to suppress legacy import warnings
# during the transition phase.
logging.getLogger("meraki_ha.coordinator").setLevel(logging.ERROR)

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
    hass.data.setdefault(DOMAIN, {})

    # Initialize the singleton IPSK Manager
    if "ipsk_manager" not in hass.data[DOMAIN]:
        ipsk_manager = IPSKManager(hass)
        await ipsk_manager.async_setup()
        hass.data[DOMAIN]["ipsk_manager"] = ipsk_manager

    # Set up services
    await async_setup_services(hass)

    return True


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", entry.version)

    new_data = {**entry.data}

    if entry.version == 1:
        if "meraki_api_key" in new_data:
            new_data["api_key"] = new_data.pop("meraki_api_key")
        entry.version = 2

    if entry.version == 2:
        # Migration: org_id -> organization_id
        if "org_id" in new_data:
            new_data[CONF_MERAKI_ORG_ID] = new_data.pop("org_id")

        # Ensure we also use the correct constant for api_key if it was something else
        if "meraki_api_key" in new_data:
            new_data[CONF_MERAKI_API_KEY] = new_data.pop("meraki_api_key")

        entry.version = 3

    hass.config_entries.async_update_entry(entry, data=new_data)

    _LOGGER.info("Migration to version %s successful", entry.version)

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
    # Register static path for frontend
    if "frontend" in hass.config.components:
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    url_path="/meraki_ha_static",
                    path=hass.config.path("custom_components/meraki_ha/www"),
                    cache_headers=False,
                )
            ]
        )

        # Register the JavaScript module so it appears in the dashboard
        add_extra_js_url(hass, "/meraki_ha_static/meraki-card.js")

    async_setup_websocket_api(hass)
    # Perform migrations before coordinator refresh
    await async_migrate_entities(hass, entry.entry_id)
    await async_cleanup_ghost_devices(hass, entry.entry_id)

    # Action 2: Safe extraction with legacy fallbacks
    api_key = entry.data.get(CONF_MERAKI_API_KEY) or entry.data.get("meraki_api_key")
    org_id = entry.data.get(CONF_MERAKI_ORG_ID) or entry.data.get("org_id")
    enabled_networks = entry.options.get(CONF_ENABLED_NETWORKS) or entry.data.get(
        CONF_ENABLED_NETWORKS, []
    )

    if not api_key:
        _LOGGER.error("Meraki API Key is missing. Please re-authenticate.")
        raise ConfigEntryAuthFailed("Missing Meraki API Key")
    if not org_id:
        _LOGGER.error("Meraki Organization ID is missing. Please re-authenticate.")
        raise ConfigEntryAuthFailed("Missing Meraki Organization ID")

    # Initialize shared API client
    api_client = create_api_client(
        hass=hass,
        api_key=api_key,
        org_id=org_id,
        enabled_networks=enabled_networks,
    )
    await api_client.async_setup()

    # Initialize discovery coordinator for Orgs and Networks
    discovery_coordinator = DiscoveryCoordinator(hass, entry, api_client)
    await discovery_coordinator.async_config_entry_first_refresh()

    # Shared static data for all coordinators to avoid redundant API calls
    static_data: dict[str, Any] = {}

    # Initialize unified coordinator
    main_coordinator = MerakiMainCoordinator(
        hass, entry, api_client, static_data=static_data
    )

    # All specialized coordinator references now point to the same instance
    device_coordinator = main_coordinator
    switch_coordinator = main_coordinator
    camera_coordinator = main_coordinator
    sensor_coordinator = main_coordinator
    wireless_coordinator = main_coordinator
    appliance_coordinator = main_coordinator
    client_coordinator = main_coordinator

    # 1. Block setup until the unified state is loaded (Tier 1)
    # This is strictly required to populate the Device Registry promptly.
    await main_coordinator.async_config_entry_first_refresh()

    # Perform static initialization (RF Profiles, Group Policies, Sensor Relationships)
    # once at startup using the discovered devices and networks.
    # This avoids redundant API calls in the 30s polling loop.
    _LOGGER.info(
        "Starting static initialization for Meraki coordinator %s", entry.title
    )
    await main_coordinator.async_initialize()

    repo = MerakiRepository(api_client)
    device_control_service = DeviceControlService(repo)
    switch_port_service = SwitchPortService(repo)
    camera_repo = CameraRepository(api_client, org_id)
    camera_service = CameraService(camera_repo)
    network_control_service = NetworkControlService(api_client, main_coordinator)

    discovery_service: DeviceDiscoveryService = DeviceDiscoveryService(
        main_coordinator=main_coordinator,
        config_entry=entry,
        meraki_client=api_client,
        camera_service=camera_service,
        control_service=device_control_service,
        network_control_service=network_control_service,
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": main_coordinator,  # Maintain for backward compatibility
        "main_coordinator": main_coordinator,
        "discovery_coordinator": discovery_coordinator,
        "device_coordinator": main_coordinator,
        "switch_coordinator": main_coordinator,
        "camera_coordinator": main_coordinator,
        "sensor_coordinator": main_coordinator,
        "wireless_coordinator": main_coordinator,
        "appliance_coordinator": main_coordinator,
        "client_coordinator": main_coordinator,
        "meraki_client": api_client,
        "camera_service": camera_service,
        "device_control_service": device_control_service,
        "switch_port_service": switch_port_service,
        "network_control_service": network_control_service,
        "discovery_service": discovery_service,
    }

    # Set up services
    services_manager = ServicesManager(
        hass,
        device_control_service,
        switch_port_service,
        camera_service,
    )
    await services_manager.async_register_services()

    # Set up webhook
    webhook_id = WEBHOOK_ID_FORMAT.format(entry_id=entry.entry_id)
    hass.data[DOMAIN][entry.entry_id]["webhook_id"] = webhook_id
    if not entry.data.get("webhook_secret"):
        secret = "".join(secrets.choice(string.ascii_letters) for _ in range(32))
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, "webhook_secret": secret},
        )
    else:
        secret = entry.data["webhook_secret"]

    try:
        await async_register_webhook(hass, webhook_id, secret, api_client, entry=entry)
    except Exception as e:
        _LOGGER.error(
            "Failed to register webhook. Fast updates disabled, "
            "falling back to polling. Error: %s",
            e,
        )

    # 3. Run discovery ONLY when data is present and services are initialized
    await discovery_service.discover_entities()

    # 4. Finally, forward to platforms (sensor, switch, etc.)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


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
        entry_data = hass.data[DOMAIN].pop(entry.entry_id)
        if "webhook_id" in entry_data:
            await async_unregister_webhook(
                hass, entry_data["webhook_id"], entry_data["meraki_client"]
            )

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """
    Reload Meraki config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    """
    _LOGGER.info("Options updated, reloading integration...")
    await hass.config_entries.async_reload(entry.entry_id)
