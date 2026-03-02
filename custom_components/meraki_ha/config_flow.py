"""Config flow for the Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import callback

try:
    from homeassistant.helpers.service_info.dhcp import DhcpServiceInfo
except ImportError:
    from homeassistant.components.dhcp import (  # type: ignore[attr-defined]
        DhcpServiceInfo,  # type: ignore[no-redef, attr-defined]
    )

from .const import DOMAIN
from .const_conf import (
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)

if TYPE_CHECKING:
    from .coordinators import MerakiMainCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Handle a config flow for Meraki."""

    VERSION = 1
    DOMAIN = DOMAIN
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}
        self.options: dict[str, Any] = {}

    async def async_step_dhcp(
        self,
        discovery_info: DhcpServiceInfo,
    ) -> ConfigFlowResult:
        """Handle DHCP discovery."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        return await self.async_step_user()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        from .schemas import CONFIG_SCHEMA

        errors: dict[str, str] = {}
        if user_input is not None:
            from .helpers.flow_utils import validate_credentials

            errors, validation_result = await validate_credentials(self.hass, user_input)

            if not errors and validation_result:
                org_id = user_input[CONF_MERAKI_ORG_ID]
                org_name = validation_result.get("org_name", org_id)

                await self.async_set_unique_id(org_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=org_name,
                    data={
                        CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                        CONF_MERAKI_ORG_ID: org_id,
                        CONF_ENABLE_VPN_MANAGEMENT: False,
                        CONF_ENABLE_FIREWALL_RULES: False,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow handler."""
        from .options_flow import MerakiOptionsFlowHandler

        return MerakiOptionsFlowHandler(config_entry)

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
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

        coordinator: MerakiMainCoordinator = self.hass.data[DOMAIN][
            entry.entry_id
        ]["coordinator"]

        from .helpers.flow_utils import get_network_options
        from .helpers.schema import get_filtered_schema, populate_schema_defaults
        from .schemas import OPTIONS_SCHEMA_GENERAL

        network_options = get_network_options(coordinator.data)

        # Reconfigure uses the GENERAL schema as a baseline
        filtered_schema = get_filtered_schema(
            coordinator.data.get("devices", []),
            OPTIONS_SCHEMA_GENERAL,
        )

        schema_with_defaults = populate_schema_defaults(
            filtered_schema,
            dict(entry.options),
            network_options,
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema_with_defaults,
        )
