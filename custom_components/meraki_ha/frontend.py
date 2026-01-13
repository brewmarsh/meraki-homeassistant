"""Starting setup task: Frontend."""

from __future__ import annotations

import json
<<<<<<< HEAD
from pathlib import Path

import aiofiles
=======
import logging
from pathlib import Path

import aiofiles  # type: ignore[import-untyped]
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

<<<<<<< HEAD

async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend."""
    # Setup panel
=======
_LOGGER = logging.getLogger(__name__)


async def async_register_static_path(hass: HomeAssistant) -> None:
    """Register the static path for the frontend."""
    _LOGGER.debug("Registering static path for Meraki HA frontend")
    static_path = str(Path(__file__).parent / "www")
    _LOGGER.debug("Frontend static path: %s", static_path)
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=f"/api/panel_custom/{DOMAIN}",
<<<<<<< HEAD
                path=str(Path(__file__).parent / "www"),
=======
                path=static_path,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
                cache_headers=False,
            ),
        ],
    )

<<<<<<< HEAD
=======

async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the panel for the frontend."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
    # Register panel
    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, encoding="utf-8") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    version = manifest.get("version", "0.0.0")
    module_url = f"/api/panel_custom/{DOMAIN}/meraki-panel.js?v={version}"
<<<<<<< HEAD
=======
    _LOGGER.debug("Frontend module URL: %s", module_url)
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
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
=======


def async_unregister_frontend(hass: HomeAssistant) -> None:
    """
    Unregister the Meraki panel from the Home Assistant frontend.

    Args:
    ----
        hass: The Home Assistant instance.

    """
    frontend.async_remove_panel(hass, "meraki")
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
