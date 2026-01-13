"""Starting setup task: Frontend."""

from __future__ import annotations

import json
<<<<<<< HEAD
<<<<<<< HEAD
from pathlib import Path

import aiofiles
=======
<<<<<<< HEAD
from pathlib import Path

import aiofiles
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
import logging
from pathlib import Path

import aiofiles  # type: ignore[import-untyped]
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

<<<<<<< HEAD
<<<<<<< HEAD

async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend."""
    # Setup panel
=======
<<<<<<< HEAD

async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend."""
    # Setup panel
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
_LOGGER = logging.getLogger(__name__)


async def async_register_static_path(hass: HomeAssistant) -> None:
    """Register the static path for the frontend."""
    _LOGGER.debug("Registering static path for Meraki HA frontend")
    static_path = str(Path(__file__).parent / "www")
    _LOGGER.debug("Frontend static path: %s", static_path)
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=f"/api/panel_custom/{DOMAIN}",
<<<<<<< HEAD
<<<<<<< HEAD
                path=str(Path(__file__).parent / "www"),
=======
<<<<<<< HEAD
                path=str(Path(__file__).parent / "www"),
=======
                path=static_path,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
                path=static_path,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
                cache_headers=False,
            ),
        ],
    )

<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the panel for the frontend."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======

async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the panel for the frontend."""
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    # Register panel
    manifest_path = Path(__file__).parent / "manifest.json"
    async with aiofiles.open(manifest_path, encoding="utf-8") as f:
        manifest_data = await f.read()
        manifest = json.loads(manifest_data)
    version = manifest.get("version", "0.0.0")
    module_url = f"/api/panel_custom/{DOMAIN}/meraki-panel.js?v={version}"
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    _LOGGER.debug("Frontend module URL: %s", module_url)
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    _LOGGER.debug("Frontend module URL: %s", module_url)
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)


def async_unregister_frontend(hass: HomeAssistant) -> None:
    """
    Unregister the Meraki panel from the Home Assistant frontend.

    Args:
    ----
        hass: The Home Assistant instance.

    """
    frontend.async_remove_panel(hass, "meraki")
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
