"""Starting setup task: Frontend."""

from __future__ import annotations

import json
from pathlib import Path

import aiofiles
from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend."""
    # Setup panel
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=f"/api/panel_custom/{DOMAIN}",
                path=str(Path(__file__).parent / "www"),
                cache_headers=False,
            ),
        ],
    )

    # Register panel
    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, encoding="utf-8") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    version = manifest.get("version", "0.0.0")
    module_url = f"/api/panel_custom/{DOMAIN}/meraki-panel.js?v={version}"

    # Dual-registration logic
    if MAJOR_VERSION > 2026 or (MAJOR_VERSION == 2026 and MINOR_VERSION >= 1):
        # New dashboard registration for HA version 2026.1 and newer
        frontend.async_register_built_in_panel(
            hass=hass,
            component_name="custom",
            sidebar_title="Meraki",
            sidebar_icon="mdi:lan-check",
            frontend_url_path="meraki-dashboard",
            config={
                "version": version,
                "entry_id": entry.entry_id,
            },
            require_admin=False,
        )
    else:
        # Legacy panel_custom registration for older HA versions
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
