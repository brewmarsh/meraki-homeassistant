"""The Meraki Home Assistant integration."""

from __future__ import annotations

import logging
import secrets
import string

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api.websocket import async_setup_websocket_api
from .const import DOMAIN, WEBHOOK_ID_FORMAT
from .const_conf import CONF_MERAKI_ORG_ID
from .const_platform import PLATFORMS
from .coordinators import (
    MerakiApplianceCoordinator,
    MerakiCameraCoordinator,
    MerakiClientCoordinator,
    MerakiMainCoordinator,
    MerakiSensorCoordinator,
    MerakiSwitchCoordinator,
    MerakiWirelessCoordinator,
)
from .core.repositories.camera_repository import CameraRepository
from .core.repository import MerakiRepository
from .discovery.service import DeviceDiscoveryService
from .frontend import async_register_frontend, async_remove_frontend
from .helpers.migrations import async_cleanup_ghost_devices, async_migrate_entities
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

    # Register the static path for the custom panel
    if hass.http:
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    "/meraki_ha_static",
                    hass.config.path(f"custom_components/{DOMAIN}/www"),
                    cache_headers=True,
                )
            ]
        )

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
    await async_register_frontend(hass, entry)
    async_setup_websocket_api(hass)
    # Perform migrations before coordinator refresh
    await async_migrate_entities(hass, entry.entry_id)
    await async_cleanup_ghost_devices(hass, entry.entry_id)

    # Initialize specialized coordinators
    main_coordinator = MerakiMainCoordinator(hass, entry)
    switch_coordinator = MerakiSwitchCoordinator(hass, entry)
    camera_coordinator = MerakiCameraCoordinator(hass, entry)
    sensor_coordinator = MerakiSensorCoordinator(hass, entry)
    wireless_coordinator = MerakiWirelessCoordinator(hass, entry)
    appliance_coordinator = MerakiApplianceCoordinator(hass, entry)
    client_coordinator = MerakiClientCoordinator(hass, entry)

    # Initial refresh for organization data
    await main_coordinator.async_config_entry_first_refresh()

    # Other coordinators can refresh lazily or be refreshed now
    # We'll do a first refresh for all to ensure discovery has full data
    await switch_coordinator.async_config_entry_first_refresh()
    await camera_coordinator.async_config_entry_first_refresh()
    await sensor_coordinator.async_config_entry_first_refresh()
    await wireless_coordinator.async_config_entry_first_refresh()
    await appliance_coordinator.async_config_entry_first_refresh()
    await client_coordinator.async_config_entry_first_refresh()

    api_client = main_coordinator.api
    repo = MerakiRepository(api_client)
    device_control_service = DeviceControlService(repo)
    switch_port_service = SwitchPortService(repo)
    camera_repo = CameraRepository(api_client, entry.data[CONF_MERAKI_ORG_ID])
    camera_service = CameraService(camera_repo)
    network_control_service = NetworkControlService(api_client, main_coordinator)

    discovery_service: DeviceDiscoveryService = DeviceDiscoveryService(
        main_coordinator=main_coordinator,
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

    await async_register_webhook(hass, webhook_id, secret, api_client, entry=entry)

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
        await async_remove_frontend(hass)

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
