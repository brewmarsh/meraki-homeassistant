"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Meraki options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["general", "sensors", "cameras", "advanced"],
        )

    async def _handle_step(
        self,
        step_id: str,
        schema_getter: Any,
        user_input: dict[str, Any] | None,
    ) -> ConfigFlowResult:
        """Handle a generic option step."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        return self.async_show_form(
            step_id=step_id,
            data_schema=schema_getter(dict(self.config_entry.options)),
        )

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle general settings."""
        from .schemas import get_options_schema_general

        return await self._handle_step(
            "general", get_options_schema_general, user_input
        )

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle sensor settings."""
        from .schemas import get_options_schema_sensors

        return await self._handle_step(
            "sensors", get_options_schema_sensors, user_input
        )

    async def async_step_cameras(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle camera settings."""
        from .schemas import get_options_schema_cameras

        return await self._handle_step(
            "cameras", get_options_schema_cameras, user_input
        )

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle advanced settings."""
        from .schemas import get_options_schema_advanced

        return await self._handle_step(
            "advanced", get_options_schema_advanced, user_input
        )
