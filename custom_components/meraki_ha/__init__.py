"""The Meraki Home Assistant integration."""

import logging
import json
from pathlib import Path
import aiofiles  # type: ignore[import-untyped]
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import config_validation as cv
from homeassistant.components import frontend

from .const import (
    DOMAIN,
    PLATFORMS,
    WEBHOOK_ID_FORMAT,
    CONF_MERAKI_ORG_ID,
)
from .coordinator import MerakiDataUpdateCoordinator
from .webhook import async_register_webhook
from .web_api import async_setup_api
from .core.repositories.camera_repository import CameraRepository
from .services.camera_service import CameraService
from .core.repository import MerakiRepository
from .services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.deprecated(cv.empty_config_schema(DOMAIN))


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    hass.http.register_static_path(
        f"/api/panel_custom/{DOMAIN}",
        str(Path(__file__).parent / "www"),
        cache_headers=False,
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
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
        secret = "".join(
            __import__("random").choice(__import__("string").ascii_letters)
            for _ in range(32)
        )
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_secret": secret}
        )
    else:
        secret = entry.data["webhook_secret"]

    await async_register_webhook(hass, webhook_id, secret, coordinator.api, entry=entry)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, mode="r") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    version = manifest.get("version", "0.0.0")
    module_url = f"/api/panel_custom/{DOMAIN}/meraki-panel.js?v={version}"
    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title=entry.title,
        sidebar_icon="mdi:router-network",
        frontend_url_path="meraki",
        config={
            "_panel_custom": {
                "name": "meraki-panel",
                "module_url": module_url,
                "embed_iframe": False,
                "trust_external_script": True,
            },
            "config_entry_id": entry.entry_id,
        },
        require_admin=True,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    frontend.async_remove_panel(hass, "meraki")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
