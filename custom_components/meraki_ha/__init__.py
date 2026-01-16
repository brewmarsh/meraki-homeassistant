"""The Meraki Home Assistant integration."""

import logging
import random
import string
import json
from pathlib import Path
import aiofiles

from homeassistant.components import frontend as hass_frontend
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
    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, encoding="utf-8") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    # Register the custom panel if not already registered
    panel_registered_key = f"{DOMAIN}_{entry.entry_id}_panel_registered"
    if not hass.data.get(panel_registered_key):
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
                },
                "config_entry_id": entry.entry_id,
            },
            require_admin=True,
        )
        hass.data[panel_registered_key] = True
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
    hass_frontend.async_remove_panel(hass, "meraki")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        # Clean up the panel registration flag
        panel_registered_key = f"{DOMAIN}_{entry.entry_id}_panel_registered"
        if panel_registered_key in hass.data:
            hass.data.pop(panel_registered_key)

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
