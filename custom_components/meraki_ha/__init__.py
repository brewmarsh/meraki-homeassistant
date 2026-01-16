"""The Meraki Home Assistant integration."""

import logging
import random
import string
from pathlib import Path

from homeassistant.components import frontend as hass_frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

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
        hass_frontend.async_register_built_in_panel(
            hass,
            component_name="custom",
            sidebar_title=entry.title,
            sidebar_icon="mdi:router-network",
            frontend_url_path="meraki",
            config={
                "_panel_custom": {
                    "name": "meraki-panel",
                    "module_url": f"/local/{DOMAIN}/meraki-panel.js",
                    "embed_iframe": False,
                    "trust_external_script": True,
                }
            },
            require_admin=True,
        )

    async_setup_api(hass)
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

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

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
