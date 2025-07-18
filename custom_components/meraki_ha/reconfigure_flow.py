"""Reconfiguration flow for the Meraki Home Assistant integration."""

from typing import Any, Dict, Optional

from .schemas import RECONFIGURE_SCHEMA


async def async_step_reconfigure(self, user_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle a reconfiguration flow."""
    entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
    assert entry

    if user_input is not None:
        return self.async_update_reload_and_abort(
            entry,
            options={
                **entry.options,
                "scan_interval": user_input["scan_interval"],
                "device_name_format": user_input["device_name_format"],
            },
        )

    return self.async_show_form(
        step_id="reconfigure",
        data_schema=RECONFIGURE_SCHEMA,
    )
