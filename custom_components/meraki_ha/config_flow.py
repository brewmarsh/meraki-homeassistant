"""Config flow for Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const.config import (
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from .const.integration import DOMAIN
from .reauth_flow import async_step_reauth

_LOGGER = logging.getLogger(__name__)


class MerakiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meraki."""

    async_step_reauth = async_step_reauth

    VERSION = 3

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._api_key: str | None = None
        self._org_id: str | None = None
        self._orgs: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        from .core.api import create_api_client
        from .core.errors import (
            MerakiAuthenticationError,
            MerakiConnectionError,
        )
        from .schemas import STEP_USER_DATA_SCHEMA

        errors: dict[str, str] = {}
        if user_input is not None:
            self._api_key = user_input[CONF_MERAKI_API_KEY]
            try:
                # Validation logic using the updated Client name
                client = create_api_client(
                    self.hass,
                    self._api_key,
                )
                await client.async_setup()
                self._orgs = await client.get_organizations()
                if not self._orgs:
                    errors["base"] = "no_orgs"
                else:
                    return await self.async_step_org()
            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_org(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle organization selection."""
        from .schemas import get_org_selection_schema

        if user_input is not None:
            self._org_id = user_input[CONF_MERAKI_ORG_ID]
            return await self.async_step_networks()

        return self.async_show_form(
            step_id="org",
            data_schema=get_org_selection_schema(self._orgs),
        )

    async def async_step_networks(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle network selection."""
        from .core.api import create_api_client
        from .core.errors import (
            MerakiAuthenticationError,
            MerakiConnectionError,
        )
        from .schemas import get_network_selection_schema

        errors: dict[str, str] = {}
        if user_input is not None:
            config_data = {
                CONF_MERAKI_API_KEY: self._api_key,
                CONF_MERAKI_ORG_ID: self._org_id,
                CONF_ENABLED_NETWORKS: user_input[CONF_ENABLED_NETWORKS],
            }
            return self.async_create_entry(title="Cisco Meraki", data=config_data)

        try:
            # Fetch networks for the selected organization
            client = create_api_client(self.hass, self._api_key, self._org_id)
            await client.async_setup()
            networks = await client.organization.get_organization_networks()

            if not networks:
                errors["base"] = "no_networks"
                return self.async_show_form(
                    step_id="networks",
                    data_schema=get_network_selection_schema([]),
                    errors=errors,
                )

            return self.async_show_form(
                step_id="networks",
                data_schema=get_network_selection_schema(networks),
                errors=errors,
            )
        except MerakiAuthenticationError:
            errors["base"] = "invalid_auth"
        except MerakiConnectionError:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception during network selection")
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="networks",
            data_schema=get_network_selection_schema([]),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> MerakiOptionsFlowHandler:
        """Get the options flow for this handler."""
        return MerakiOptionsFlowHandler(config_entry)


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Meraki options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["general", "sensors", "cameras", "advanced"],
        )

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle general settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import get_options_schema_general

        return self.async_show_form(
            step_id="general",
            data_schema=get_options_schema_general(self.config_entry.options),
        )

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle sensor settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import get_options_schema_sensors

        return self.async_show_form(
            step_id="sensors",
            data_schema=get_options_schema_sensors(self.config_entry.options),
        )

    async def async_step_cameras(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle camera settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import get_options_schema_cameras

        return self.async_show_form(
            step_id="cameras",
            data_schema=get_options_schema_cameras(self.config_entry.options),
        )

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle advanced settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import get_options_schema_advanced

        return self.async_show_form(
            step_id="advanced",
            data_schema=get_options_schema_advanced(self.config_entry.options),
        )
