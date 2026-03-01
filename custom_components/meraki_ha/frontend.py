"""Frontend registration."""

from __future__ import annotations

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.loader import async_get_loaded_integration


async def async_register_frontend(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register the frontend panel."""
    # Check if the panel is already registered
    if "meraki" in hass.data.get("frontend_panels", {}):
        return

    # Load version from integration to bust browser cache
    integration = async_get_loaded_integration(hass, entry.domain)
    version = integration.version

    # The custom panel will be served at `/meraki_ha_static/meraki-panel.js`.
    # We manually register the static path in `__init__.py` to serve files
    # from `/meraki_ha_static/` which points to `custom_components/meraki_ha/www`.
    module_url = f"/meraki_ha_static/meraki-panel.js?v={version}"

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
        # Allow updating the panel registration to prevent conflicts on reload
        update=True,
    )


async def async_remove_frontend(hass: HomeAssistant) -> None:
    """Remove the frontend panel."""
    frontend.async_remove_panel(hass, "meraki")
