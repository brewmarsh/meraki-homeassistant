"""The Meraki Home Assistant integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const.integration import DOMAIN
from .const.platform import PLATFORMS
from .coordinators import MerakiMainCoordinator
from .core.api.factory import create_meraki_client
from .core.errors import MerakiAuthError, MerakiConnectionError
from .discovery.service import DiscoveryService
from .services import async_setup_services
from .services.guest_key_service import GuestKeyService
from .services.switch_port_service import SwitchPortService
from .setup_helpers import async_setup_frontend, async_setup_webhook_lifecycle
from .webhook import async_unregister_webhook

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    _LOGGER.debug("Setting up Meraki config entry: %s", entry.entry_id)

    # 1. Initialize API Client
    try:
        api_client = create_meraki_client(hass, entry)
        await api_client.async_setup()
    except MerakiAuthError as err:
        _LOGGER.error("Authentication failed: %s", err)
        raise ConfigEntryAuthFailed(err) from err
    except MerakiConnectionError as err:
        _LOGGER.error("Connection failed: %s", err)
        return False

    # 2. Initialize Discovery & Main Coordinator
    # We fetch static data once at startup to use across all coordinators
    static_data = {}
    main_coordinator = MerakiMainCoordinator(hass, entry, api_client, static_data)

    # 3. Setup Discovery Service
    discovery_service = DiscoveryService(hass, entry, api_client, main_coordinator)

    # 4. Initialize Services
    guest_key_service = GuestKeyService(api_client, main_coordinator)
    switch_port_service = SwitchPortService(api_client, main_coordinator)
    await async_setup_services(hass)

    # Store for platforms and cleanup
    hass.data[DOMAIN][entry.entry_id] = {
        "api_client": api_client,
        "main_coordinator": main_coordinator,
        "discovery_service": discovery_service,
        "guest_key_service": guest_key_service,
        "switch_port_service": switch_port_service,
    }

    # 5. Handle Webhook Lifecycle (Registration/Unregistration)
    await async_setup_webhook_lifecycle(hass, entry, api_client, main_coordinator)

    # 6. Initialize Static Paths and Frontend
    await async_setup_frontend(hass)

    # 7. Perform initial discovery and platform setup
    # We do this after storing data so platforms can access it immediately
    await main_coordinator.async_config_entry_first_refresh()
    await discovery_service.async_setup_platforms()

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Meraki config entry: %s", entry.entry_id)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)

        # Unregister webhook if configured
        if "webhook_id" in data:
            await async_unregister_webhook(hass, data["webhook_id"], data["api_client"])

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
