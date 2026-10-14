"""Reconfiguration flow for the Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import aiohttp

from homeassistant import config_entries
from homeassistant.exceptions import ConfigEntryAuthFailed

from .authentication import validate_meraki_credentials
from .const.config import (
    AUTH_TYPE_API_KEY,
    AUTH_TYPE_OAUTH,
    CONF_AUTH_TYPE,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_OAUTH_TOKEN,
)
from .core.errors import (
    ApiClientCommunicationError,
    InvalidOrgID,
    MerakiAuthenticationError,
    MerakiConnectionError,
)

if TYPE_CHECKING:
    from .config_flow import MerakiConfigFlow

_LOGGER = logging.getLogger(__name__)


async def _validate_and_reconfigure_key(
    flow: MerakiConfigFlow,
    entry: config_entries.ConfigEntry,
    credential: str,
    auth_type: str,
) -> config_entries.ConfigFlowResult:
    """Validate credentials and update config entry."""
    org_id = entry.data.get(CONF_MERAKI_ORG_ID)
    await validate_meraki_credentials(flow.hass, credential, org_id)

    data_updates = {
        CONF_AUTH_TYPE: auth_type,
        CONF_MERAKI_API_KEY: credential,
    }
    _LOGGER.info("Meraki authentication reconfigured successfully.")
    return flow.async_update_reload_and_abort(
        entry,
        data_updates=data_updates,
        reason="reconfigure_successful",
    )


async def async_step_reconfigure(
    self: MerakiConfigFlow,
    user_input: dict[str, Any] | None = None,
) -> config_entries.ConfigFlowResult:
    """Handle reconfiguration of authentication for the Meraki integration."""
    from .schemas import get_reconfigure_schema

    errors: dict[str, str] = {}
    entry = self._get_reconfigure_entry()

    if user_input is not None:
        auth_type = user_input.get(CONF_AUTH_TYPE, AUTH_TYPE_API_KEY)
        key = user_input.get(CONF_MERAKI_API_KEY)
        token = user_input.get(CONF_OAUTH_TOKEN)

        if auth_type == AUTH_TYPE_OAUTH and not token:
            return await self.async_step_pick_implementation()

        credential = token if auth_type == AUTH_TYPE_OAUTH else key
        if not credential:
            errors["base"] = "invalid_auth"
        else:
            try:
                return await _validate_and_reconfigure_key(
                    self, entry, credential, auth_type
                )
            except (ConfigEntryAuthFailed, MerakiAuthenticationError):
                errors["base"] = "invalid_auth"
            except InvalidOrgID:
                errors["base"] = "invalid_org_id"
            except (
                MerakiConnectionError,
                ApiClientCommunicationError,
                aiohttp.ClientError,
            ):
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during reconfiguration")
                errors["base"] = "cannot_connect"

    current_auth = entry.data.get(CONF_AUTH_TYPE, AUTH_TYPE_API_KEY)
    return self.async_show_form(
        step_id="reconfigure",
        data_schema=get_reconfigure_schema(current_auth),
        errors=errors,
    )
