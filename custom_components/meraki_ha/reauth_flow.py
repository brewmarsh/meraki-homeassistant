"""Reauthentication flow for the Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import aiohttp
import voluptuous as vol

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
from .core.errors import InvalidOrgID, MerakiAuthenticationError

if TYPE_CHECKING:
    from .config_flow import MerakiConfigFlow

_LOGGER = logging.getLogger(__name__)


def _get_entry(flow: MerakiConfigFlow) -> config_entries.ConfigEntry | None:
    """Retrieve existing config entry for reauth."""
    if hasattr(flow, "_get_reauth_entry"):
        try:
            return flow._get_reauth_entry()
        except Exception:
            pass
    entry_id = flow.context.get("entry_id")
    if entry_id:
        return flow.hass.config_entries.async_get_entry(entry_id)
    return None


async def async_step_reauth(
    self: MerakiConfigFlow,
    user_input: dict[str, Any] | None = None,
) -> config_entries.ConfigFlowResult:
    """Handle reauthentication for the Meraki integration."""
    errors: dict[str, str] = {}
    existing_entry = _get_entry(self)
    if not existing_entry:
        return self.async_abort(reason="unknown_entry")

    # If user_input matches initial entry data passed during async_init, show form
    is_submission = user_input is not None and user_input != existing_entry.data

    if user_input is not None and is_submission:
        auth_type = user_input.get(CONF_AUTH_TYPE, AUTH_TYPE_API_KEY)
        key = user_input.get(CONF_MERAKI_API_KEY)
        token = user_input.get(CONF_OAUTH_TOKEN)

        if auth_type == AUTH_TYPE_OAUTH and not token:
            return await self.async_step_pick_implementation()

        credential = token if auth_type == AUTH_TYPE_OAUTH else key
        org_id = user_input.get(
            CONF_MERAKI_ORG_ID, existing_entry.data.get(CONF_MERAKI_ORG_ID, "")
        )

        try:
            await validate_meraki_credentials(self.hass, str(credential), str(org_id))

            updated_data = {
                **existing_entry.data,
                CONF_AUTH_TYPE: auth_type,
                CONF_MERAKI_API_KEY: credential,
                CONF_MERAKI_ORG_ID: org_id,
            }
            self.hass.config_entries.async_update_entry(
                existing_entry, data=updated_data
            )
            await self.hass.config_entries.async_reload(existing_entry.entry_id)
            _LOGGER.info("Meraki reauthentication successful.")
            return self.async_abort(reason="reauth_successful")

        except (ConfigEntryAuthFailed, MerakiAuthenticationError):
            errors["base"] = "invalid_auth"
        except (InvalidOrgID, ValueError):
            errors["base"] = "invalid_org_id"
        except aiohttp.ClientError:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected error during reauth")
            errors["base"] = "unknown"

    org_id = existing_entry.data.get(CONF_MERAKI_ORG_ID, "")
    return self.async_show_form(
        step_id="reauth",
        data_schema=vol.Schema(
            {
                vol.Required(CONF_MERAKI_API_KEY): str,
                vol.Required(CONF_MERAKI_ORG_ID, default=org_id): str,
            }
        ),
        errors=errors,
        description_placeholders={"org_id": org_id},
    )
