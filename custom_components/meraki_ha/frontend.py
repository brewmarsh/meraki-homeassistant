<<<<<<< HEAD
"""Starting setup task: Frontend."""
=======
"""Frontend registration."""
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

from __future__ import annotations

import json
<<<<<<< HEAD
import logging
from pathlib import Path

import aiofiles  # type: ignore[import-untyped]
from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
=======
from pathlib import Path

import aiofiles
from homeassistant.components import frontend
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

<<<<<<< HEAD
_LOGGER = logging.getLogger(__name__)


async def async_register_static_path(hass: HomeAssistant) -> None:
    """Register the static path for the frontend."""
    _LOGGER.debug("Registering static path for Meraki HA frontend")
    static_path = str(Path(__file__).parent / "www")
    _LOGGER.debug("Frontend static path: %s", static_path)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=f"/api/panel_custom/{DOMAIN}",
                path=static_path,
                cache_headers=False,
            ),
        ],
    )


async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the panel for the frontend."""
    # Register panel
=======

async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend panel."""
    # Load version from manifest to bust browser cache
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, encoding="utf-8") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    version = manifest.get("version", "0.0.0")
<<<<<<< HEAD
    module_url = f"/api/panel_custom/{DOMAIN}/meraki-panel.js?v={version}"
    _LOGGER.debug("Frontend module URL: %s", module_url)
=======

    # The custom panel will be served at `/meraki_ha_static/meraki-panel.js`.
    # We manually register the static path in `__init__.py` to serve files
    # from `/meraki_ha_static/` which points to `custom_components/meraki_ha/www`.
    module_url = f"/meraki_ha_static/meraki-panel.js?v={version}"

    # Register a custom panel using the modern `module_url` approach
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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


<<<<<<< HEAD
def async_unregister_frontend(hass: HomeAssistant) -> None:
    """
    Unregister the Meraki panel from the Home Assistant frontend.

    Args:
    ----
        hass: The Home Assistant instance.

    """
=======
async def async_remove_frontend(hass: HomeAssistant) -> None:
    """Remove the frontend panel."""
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    frontend.async_remove_panel(hass, "meraki")
