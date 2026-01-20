"""Frontend registration."""

from __future__ import annotations

import json
from pathlib import Path

import aiofiles
from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend panel."""
    # Load version from manifest to bust browser cache
    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, encoding="utf-8") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    version = manifest.get("version", "0.0.0")

    # The custom panel will be served at `/local/meraki_ha/meraki-panel.js`.
    # Note: As of HA 2026.1, the `www` folder is no longer automatically mapped.
    # We manually register the static path in `__init__.py` to serve files
    # from `/local/meraki_ha/` which points to `custom_components/meraki_ha/www`.
    module_url = f"/local/{DOMAIN}/meraki-panel.js?v={version}"

    # Register a custom panel using the modern `module_url` approach
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


async def async_remove_frontend(hass: HomeAssistant) -> None:
    """Remove the frontend panel."""
    frontend.async_remove_panel(hass, "meraki")
