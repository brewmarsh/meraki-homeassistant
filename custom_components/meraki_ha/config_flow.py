"""Config flow for Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import callback
from homeassistant.helpers import config_entry_oauth2_flow

from .const.config import (
    AUTH_TYPE_API_KEY,
    AUTH_TYPE_OAUTH,
    CONF_AUTH_TYPE,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_OAUTH_TOKEN,
)
from .const.integration import DOMAIN
from .reauth_flow import async_step_reauth
from .reconfigure_flow import async_step_reconfigure

_LOGGER = logging.getLogger(__name__)


class MerakiConfigFlow(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler,
    domain=DOMAIN,
):
    """Handle a config flow for Meraki."""

    DOMAIN = DOMAIN
    VERSION = 3

    async_step_reauth = async_step_reauth
    async_step_reconfigure = async_step_reconfigure

    def __init__(self) -> None:
        """Initialize the config flow."""
        super().__init__()
        self._auth_type: str = AUTH_TYPE_API_KEY
        self._api_key: str | None = None
        self._org_id: str | None = None
        self._orgs: list[dict[str, Any]] = []
        self._oauth_data: dict[str, Any] = {}

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        from .core.api import create_api_client
        from .core.errors import (
            ApiClientCommunicationError,
            InvalidOrgID,
            MerakiAuthenticationError,
            MerakiConnectionError,
        )
        from .schemas import STEP_USER_DATA_SCHEMA

        errors: dict[str, str] = {}
        if user_input is not None:
            auth_type = user_input.get(CONF_AUTH_TYPE, AUTH_TYPE_API_KEY)
            self._auth_type = auth_type
            token = user_input.get(CONF_OAUTH_TOKEN)
            key = user_input.get(CONF_MERAKI_API_KEY)

            if auth_type == AUTH_TYPE_OAUTH and not token:
                return await self.async_step_pick_implementation()

            self._api_key = token if auth_type == AUTH_TYPE_OAUTH else key
            if not self._api_key:
                errors["base"] = "invalid_auth"
            else:
                try:
                    client = create_api_client(self.hass, self._api_key)
                    await client.async_setup()
                    self._orgs = await client.organization.get_organizations()
                    if not self._orgs:
                        errors["base"] = "no_orgs"
                    else:
                        return await self.async_step_org()
                except MerakiAuthenticationError:
                    errors["base"] = "invalid_auth"
                except (MerakiConnectionError, ApiClientCommunicationError):
                    errors["base"] = "cannot_connect"
                except InvalidOrgID:
                    errors["base"] = "invalid_org"
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception("Unexpected exception during config flow")
                    errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> ConfigFlowResult:
        """Create entry or handle reconfigure after OAuth authorization."""
        from .core.api import create_api_client
        from .core.errors import (
            ApiClientCommunicationError,
            InvalidOrgID,
            MerakiAuthenticationError,
            MerakiConnectionError,
        )

        access_token = data["token"]["access_token"]
        self._auth_type = AUTH_TYPE_OAUTH
        self._api_key = access_token
        self._oauth_data = data

        if self.source == config_entries.SOURCE_RECONFIGURE:
            entry = self._get_reconfigure_entry()
            return self.async_update_reload_and_abort(
                entry,
                data_updates={
                    CONF_AUTH_TYPE: AUTH_TYPE_OAUTH,
                    CONF_MERAKI_API_KEY: access_token,
                    **data,
                },
                reason="reconfigure_successful",
            )

        try:
            client = create_api_client(self.hass, access_token)
            await client.async_setup()
            self._orgs = await client.organization.get_organizations()
            if not self._orgs:
                return self.async_abort(reason="no_orgs")
            return await self.async_step_org()
        except MerakiAuthenticationError:
            return self.async_abort(reason="invalid_auth")
        except (MerakiConnectionError, ApiClientCommunicationError):
            return self.async_abort(reason="cannot_connect")
        except InvalidOrgID:
            return self.async_abort(reason="invalid_org")

    async def async_step_org(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
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
    ) -> ConfigFlowResult:
        """Handle network selection."""
        from .core.api import create_api_client
        from .core.errors import (
            ApiClientCommunicationError,
            InvalidOrgID,
            MerakiAuthenticationError,
            MerakiConnectionError,
        )
        from .schemas import get_network_selection_schema

        errors: dict[str, str] = {}
        if user_input is not None:
            config_data = {
                CONF_AUTH_TYPE: self._auth_type,
                CONF_MERAKI_API_KEY: self._api_key,
                CONF_MERAKI_ORG_ID: self._org_id,
                CONF_ENABLED_NETWORKS: user_input[CONF_ENABLED_NETWORKS],
                **self._oauth_data,
            }
            return self.async_create_entry(title="Cisco Meraki", data=config_data)

        try:
            client = create_api_client(self.hass, str(self._api_key), self._org_id)
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
        except (MerakiConnectionError, ApiClientCommunicationError):
            errors["base"] = "cannot_connect"
        except InvalidOrgID:
            errors["base"] = "invalid_org"
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
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        from .options_flow import MerakiOptionsFlowHandler

        return MerakiOptionsFlowHandler(config_entry)
