"""Reauthentication flow for the Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import aiohttp
import voluptuous as vol
from homeassistant import data_entry_flow
from homeassistant.exceptions import ConfigEntryAuthFailed

from .authentication import validate_meraki_credentials
from .const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID

if TYPE_CHECKING:
<<<<<<< HEAD
    from .config_flow import ConfigFlowHandler
=======
    from .config_flow import MerakiConfigFlow
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)


_LOGGER = logging.getLogger(__name__)


async def async_step_reauth(
<<<<<<< HEAD
    self: ConfigFlowHandler,
=======
    self: MerakiConfigFlow,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
    user_input: dict[str, Any] | None = None,
) -> data_entry_flow.FlowResult:
    """
    Handle reauthentication for the Meraki integration.

    Args:
    ----
        self: The config flow handler.
        user_input: The user input.

    Returns
    -------
        The flow result.

    """
    errors: dict[str, str] = {}
    existing_entry = self.hass.config_entries.async_get_entry(
        self.context["entry_id"],
    )
    if not existing_entry:
        return self.async_abort(reason="unknown_entry")

    if user_input is not None:
        try:
            await validate_meraki_credentials(
                self.hass,
                user_input[CONF_MERAKI_API_KEY],
                user_input[CONF_MERAKI_ORG_ID],
            )

            updated_data = {
                **existing_entry.data,
                CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
            }

            self.hass.config_entries.async_update_entry(
                existing_entry,
                data=updated_data,
            )
            await self.hass.config_entries.async_reload(existing_entry.entry_id)
            _LOGGER.info("Meraki reauthentication successful.")
            return self.async_abort(reason="reauth_successful")

        except ConfigEntryAuthFailed:
            _LOGGER.warning("Reauthentication failed: Invalid credentials.")
            errors["base"] = "invalid_auth"
        except ValueError:
            _LOGGER.warning("Reauthentication failed: Invalid Organization ID.")
            errors["base"] = "invalid_org_id"
        except aiohttp.ClientError:
            _LOGGER.error("Reauthentication failed: Cannot connect to Meraki API.")
            errors["base"] = "cannot_connect"
        except Exception as e:
            _LOGGER.error("An unexpected error occurred during reauth: %s", e)
            errors["base"] = "unknown"

    org_id = existing_entry.data.get(CONF_MERAKI_ORG_ID, "")

    return self.async_show_form(
        step_id="reauth",
        data_schema=vol.Schema(
            {
                vol.Required(CONF_MERAKI_API_KEY): str,
                vol.Required(CONF_MERAKI_ORG_ID, default=org_id): str,
            },
        ),
        errors=errors,
    )
