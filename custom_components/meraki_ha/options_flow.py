"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import DOMAIN
from .const_conf import CONF_INTEGRATION_TITLE
from .coordinator import MerakiDataUpdateCoordinator
from .helpers.schema import get_filtered_schema, populate_schema_defaults
from .schemas import (
    OPTIONS_SCHEMA_ADVANCED,
    OPTIONS_SCHEMA_CAMERAS,
    OPTIONS_SCHEMA_GENERAL,
    OPTIONS_SCHEMA_SENSORS,
)


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.options = dict(config_entry.options)
        self._coordinator_instance: MerakiDataUpdateCoordinator | None = None

    @property
    def coordinator(self) -> MerakiDataUpdateCoordinator:
        """Get the coordinator."""
        if self._coordinator_instance is None:
            self._coordinator_instance = self.hass.data[DOMAIN][
                self.config_entry.entry_id
            ]["coordinator"]
        return self._coordinator_instance

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Manage the options flow menu."""
        from .helpers.flow_utils import has_cameras

        menu_options = ["general", "sensors"]
        if has_cameras(self.coordinator.data):
            menu_options.append("cameras")
        menu_options.append("advanced")

        return self.async_show_menu(step_id="init", menu_options=menu_options)

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage general settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        from .helpers.flow_utils import get_network_options

        schema = populate_schema_defaults(
            OPTIONS_SCHEMA_GENERAL,
            self.options,
            get_network_options(self.coordinator.data),
        )
        return self.async_show_form(step_id="general", data_schema=schema)

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage sensor settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema = populate_schema_defaults(
            OPTIONS_SCHEMA_SENSORS,
            self.options,
        )
        return self.async_show_form(step_id="sensors", data_schema=schema)

    async def async_step_cameras(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage camera settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        # Filter schema in case we somehow got here without cameras
        # (though menu handles it)
        # But also get_filtered_schema handles filtering specific options if needed.
        filtered_schema = get_filtered_schema(
            self.coordinator.data.get("devices", []),
            OPTIONS_SCHEMA_CAMERAS,
        )

        schema = populate_schema_defaults(
            filtered_schema,
            self.options,
        )
        return self.async_show_form(step_id="cameras", data_schema=schema)

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage advanced settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        filtered_schema = get_filtered_schema(
            self.coordinator.data.get("devices", []),
            OPTIONS_SCHEMA_ADVANCED,
        )

        schema = populate_schema_defaults(
            filtered_schema,
            self.options,
        )
        return self.async_show_form(step_id="advanced", data_schema=schema)
