"""The Meraki Home Assistant integration."""

from __future__ import annotations

import logging
import secrets
import string

from custom_components.meraki_ha.const.config import (
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

    # Initialize shared API client
    api_client = create_api_client(
        hass=hass,
        api_key=entry.data[CONF_MERAKI_API_KEY],
        org_id=entry.data[CONF_MERAKI_ORG_ID],
    )
    await api_client.async_setup()

    # Initialize specialized coordinators
    main_coordinator = MerakiMainCoordinator(hass, entry, api_client)
    device_coordinator = MerakiDeviceCoordinator(hass, entry, api_client)
    switch_coordinator = MerakiSwitchCoordinator(hass, entry, api_client)
    camera_coordinator = MerakiCameraCoordinator(hass, entry, api_client)
    sensor_coordinator = MerakiSensorCoordinator(hass, entry, api_client)
    wireless_coordinator = MerakiWirelessCoordinator(hass, entry, api_client)
    appliance_coordinator = MerakiApplianceCoordinator(hass, entry, api_client)
    client_coordinator = MerakiClientCoordinator(hass, entry, api_client)

    # 1. Block setup until the basic device skeleton is loaded (Tier 1)
    # This is strictly required to populate the Device Registry promptly.
    await device_coordinator.async_config_entry_first_refresh()

    # Seed the specialized coordinators with the basic device data so discovery
    # can proceed without waiting for the heavy full organizational/sensor refresh.
    # We explicitly do NOT use async_set_updated_data() here because that would mark
    # the coordinators as having had a successful first update, making entities
    # prematurely "available" with incomplete data.
    for coord in [
        main_coordinator,
        switch_coordinator,
        camera_coordinator,
        sensor_coordinator,
        wireless_coordinator,
        appliance_coordinator,
        client_coordinator,
    ]:
        coord.data = device_coordinator.data
        coord.devices_by_serial = device_coordinator.devices_by_serial
        coord.networks_by_id = device_coordinator.networks_by_id
        coord.ssids_by_network_and_number = (
            device_coordinator.ssids_by_network_and_number
        )

    # 2. Start heavy fetching for other coordinators in the background.
    # This prevents blocking the Home Assistant UI and avoids setup timeouts.
    for coord, name in [
        (main_coordinator, "meraki_main_init"),
        (switch_coordinator, "meraki_switch_init"),
        (camera_coordinator, "meraki_camera_init"),
        (sensor_coordinator, "meraki_sensor_init"),
        (wireless_coordinator, "meraki_wireless_init"),
        (appliance_coordinator, "meraki_appliance_init"),
        (client_coordinator, "meraki_client_init"),
    ]:
        entry.async_create_background_task(
            hass, coord.async_request_refresh(), name=name
        )

    repo = MerakiRepository(api_client)
    device_control_service = DeviceControlService(repo)
    switch_port_service = SwitchPortService(repo)
    camera_repo = CameraRepository(api_client, entry.data[CONF_MERAKI_ORG_ID])
    camera_service = CameraService(camera_repo)
    network_control_service = NetworkControlService(api_client, main_coordinator)

    discovery_service: DeviceDiscoveryService = DeviceDiscoveryService(
        main_coordinator=main_coordinator,
        device_coordinator=device_coordinator,
        switch_coordinator=switch_coordinator,
        camera_coordinator=camera_coordinator,
        sensor_coordinator=sensor_coordinator,
        wireless_coordinator=wireless_coordinator,
        appliance_coordinator=appliance_coordinator,
        client_coordinator=client_coordinator,
        config_entry=entry,
        meraki_client=api_client,
        camera_service=camera_service,
        control_service=device_control_service,
        network_control_service=network_control_service,
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": main_coordinator,  # Maintain for backward compatibility
        "main_coordinator": main_coordinator,
        "device_coordinator": device_coordinator,
        "switch_coordinator": switch_coordinator,
        "camera_coordinator": camera_coordinator,
        "sensor_coordinator": sensor_coordinator,
        "wireless_coordinator": wireless_coordinator,
        "appliance_coordinator": appliance_coordinator,
        "client_coordinator": client_coordinator,
        "meraki_client": api_client,
        "camera_service": camera_service,
        "device_control_service": device_control_service,
        "switch_port_service": switch_port_service,
        "network_control_service": network_control_service,
        "discovery_service": discovery_service,
    }

    await discovery_service.discover_entities()

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
            "Failed to register webhook. Fast updates disabled, falling back to polling. Error: %s",
            e,
        )

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
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
