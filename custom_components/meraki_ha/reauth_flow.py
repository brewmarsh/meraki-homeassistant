"""Reauthentication flow for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

import aiohttp
from homeassistant.exceptions import ConfigEntryAuthFailed

from .authentication import validate_meraki_credentials
from .const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID
from .schemas import CONFIG_SCHEMA

_LOGGER = logging.getLogger(__name__)


async def async_step_reauth(self, user_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle reauthentication for the Meraki integration."""
    errors: Dict[str, str] = {}

    if user_input is not None:
        try:
            await validate_meraki_credentials(
                user_input[CONF_MERAKI_API_KEY],
                user_input[CONF_MERAKI_ORG_ID],
            )

            existing_entry = self.hass.config_entries.async_get_entry(
                self.context["entry_id"]
            )
            if not existing_entry:
                return self.async_abort(reason="unknown_entry")

            updated_data: Dict[str, Any] = {
                CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
            }

            self.hass.config_entries.async_update_entry(
                existing_entry, data=updated_data
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

    return self.async_show_form(
        step_id="reauth", data_schema=CONFIG_SCHEMA, errors=errors
    )
