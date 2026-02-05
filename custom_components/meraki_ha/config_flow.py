"""Config flow for the Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow

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
    CONF_INTEGRATION_TITLE,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .helpers.schema import populate_schema_defaults
from .schemas import CONFIG_SCHEMA, OPTIONS_SCHEMA

if TYPE_CHECKING:
    from .coordinator import MerakiDataUpdateCoordinator

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
        """
        Handle DHCP discovery.

        Args:
            discovery_info: The discovery info.

        Returns
        -------
            The flow result.

        """
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        return await self.async_step_user()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Handle the initial step.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        errors: dict[str, str] = {}
        if user_input is not None:
            from .authentication import validate_meraki_credentials

            try:
                api_key = user_input[CONF_MERAKI_API_KEY]
                org_id = user_input[CONF_MERAKI_ORG_ID]
                validation_result = await validate_meraki_credentials(
                    self.hass,
                    api_key,
                    org_id,
                )
                org_name = validation_result.get("org_name", org_id)

                await self.async_set_unique_id(org_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=org_name,
                    data={
                        CONF_MERAKI_API_KEY: api_key,
                        CONF_MERAKI_ORG_ID: org_id,
                        CONF_ENABLE_VPN_MANAGEMENT: False,
                        CONF_ENABLE_FIREWALL_RULES: False,
                    },
                )

            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
            except AbortFlow as e:
                raise e
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

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
        """
        Get the options flow for this handler.

        Args:
        ----
            config_entry: The config entry.

        Returns
        -------
            The options flow handler.

        """
        from .options_flow import MerakiOptionsFlowHandler

        return MerakiOptionsFlowHandler(config_entry)

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Handle a reconfiguration flow.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if not entry:
            return self.async_abort(reason="unknown_entry")

        if user_input is not None:
            new_options = {**entry.options, **user_input}
            self.hass.config_entries.async_update_entry(entry, options=new_options)
            await self.hass.config_entries.async_reload(entry.entry_id)
            return self.async_abort(reason="reconfigure_successful")


        coordinator: MerakiDataUpdateCoordinator = self.hass.data[DOMAIN][
            entry.entry_id
        ]["coordinator"]
        network_options = []
        if coordinator.data and coordinator.data.get("networks"):
            for network in coordinator.data["networks"]:
                name = getattr(network, "name", None)
                if name is None and isinstance(network, dict):
                    name = network.get("name")

                net_id = getattr(network, "id", None)
                if net_id is None and isinstance(network, dict):
                    net_id = network.get("id")

                if name and net_id:
                    network_options.append({"label": name, "value": net_id})

        schema_with_defaults = populate_schema_defaults(
            OPTIONS_SCHEMA,
            dict(entry.options),
            network_options,
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema_with_defaults,
        )
