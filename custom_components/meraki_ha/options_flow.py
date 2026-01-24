"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries, data_entry_flow

from .const import CONF_INTEGRATION_TITLE, DOMAIN
from .coordinator import MerakiDataUpdateCoordinator
from .helpers.schema import populate_schema_defaults
from .schemas import OPTIONS_SCHEMA


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """
        Initialize options flow.

        Args:
        ----
            config_entry: The config entry.

        """
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> data_entry_flow.FlowResult:
        """
        Manage the options flow.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE,
                data=self.options,
            )

        coordinator: MerakiDataUpdateCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
        network_options = []
        if coordinator.data and coordinator.data.get("networks"):
            network_options = [
                {"label": network["name"], "value": network["id"]}
                for network in coordinator.data["networks"]
            ]

        # Populate the form with existing values from the config entry.
        schema_with_defaults = populate_schema_defaults(
            OPTIONS_SCHEMA,
            self.options,
            network_options,
        )

        return self.async_show_form(step_id="init", data_schema=schema_with_defaults)
