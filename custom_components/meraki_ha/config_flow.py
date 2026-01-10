"""Config flow for the Meraki Home Assistant integration."""

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow
from homeassistant.helpers import selector

from .authentication import validate_meraki_credentials
from .const import (
    CONF_ENABLED_NETWORKS,
    CONF_INTEGRATION_TITLE,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DOMAIN,
)
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .options_flow import MerakiOptionsFlowHandler
from .schemas import CONFIG_SCHEMA, SCHEMA_NETWORK_SELECTION

_LOGGER = logging.getLogger(__name__)


class MerakiConfigFlow(ConfigFlow, domain="meraki_ha"):  # type: ignore[call-arg]
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = "cloud_poll"

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}
        self.options: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                validation_result = await validate_meraki_credentials(
                    self.hass,
                    user_input[CONF_MERAKI_API_KEY],
                    user_input[CONF_MERAKI_ORG_ID],
                )
                self.data[CONF_MERAKI_API_KEY] = user_input[CONF_MERAKI_API_KEY]
                self.data[CONF_MERAKI_ORG_ID] = user_input[CONF_MERAKI_ORG_ID]
                self.data["org_name"] = validation_result.get(
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
                )

                await self.async_set_unique_id(user_input[CONF_MERAKI_ORG_ID])
                self._abort_if_unique_id_configured()

                return await self.async_step_init()

            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
            except AbortFlow:
                return self.async_abort(reason="already_configured")
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the general settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=self.data.get("org_name", CONF_INTEGRATION_TITLE),
                data=self.data,
                options=self.options,
            )

        return self.async_show_form(
            step_id="init", data_schema=SCHEMA_NETWORK_SELECTION
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler.

        Note: As of Home Assistant 2025.x, we should NOT pass config_entry
        to the OptionsFlow constructor. The framework sets up config_entry
        after initialization via the handler property.
        """
        return MerakiOptionsFlowHandler()

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a reconfiguration flow."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if not entry:
            return self.async_abort(reason="unknown_entry")

        if user_input is not None:
            new_options = {**entry.options, **user_input}
            self.hass.config_entries.async_update_entry(entry, options=new_options)
            await self.hass.config_entries.async_reload(entry.entry_id)
            return self.async_abort(reason="reconfigure_successful")

        network_options = []
        if (
            DOMAIN in self.hass.data
            and entry.entry_id in self.hass.data[DOMAIN]
            and "coordinator" in self.hass.data[DOMAIN][entry.entry_id]
        ):
            coordinator = self.hass.data[DOMAIN][entry.entry_id]["coordinator"]
            if coordinator.data and coordinator.data.get("networks"):
                network_options = [
                    {"label": network["name"], "value": network["id"]}
                    for network in coordinator.data["networks"]
                ]

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_NETWORK_SELECTION, entry.options, network_options
        )

        return self.async_show_form(
            step_id="reconfigure", data_schema=schema_with_defaults
        )

    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: Mapping[str, Any],
        network_options: list[dict[str, str]] | None = None,
    ) -> vol.Schema:
        """Populate a schema with default values from a dictionary."""
        new_schema_keys = {}
        if network_options is None:
            network_options = []

        # Convert to dict for easier handling
        defaults_dict = dict(defaults)

        for key, value in schema.schema.items():
            key_name = key.schema
            target_key = key

            if key_name in defaults_dict:
                target_key = type(key)(key.schema, default=defaults_dict[key.schema])

            if key_name == CONF_ENABLED_NETWORKS and isinstance(
                value, selector.SelectSelector
            ):
                current_values = defaults_dict.get(CONF_ENABLED_NETWORKS, [])
                existing_option_values = {opt["value"] for opt in network_options}

                combined_options = list(network_options)
                for val in current_values:
                    if val not in existing_option_values:
                        combined_options.append({"label": val, "value": val})

                new_config = value.config.copy()
                # Use selector.SelectOptionDict for proper typing
                new_config["options"] = [
                    selector.SelectOptionDict(label=opt["label"], value=opt["value"])
                    for opt in combined_options
                ]
                value = selector.SelectSelector(new_config)

            new_schema_keys[target_key] = value
        return vol.Schema(new_schema_keys)
