"""Validation utilities for Meraki configuration."""

from __future__ import annotations

import re

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_API_KEY, CONF_NAME

from ...const import (
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)

VALID_MERAKI_API_KEY = re.compile(r"^[0-9a-f]{40}$")
VALID_MERAKI_ORG_ID = re.compile(r"^[0-9]{6,12}$")


def validate_api_key(value: str) -> str:
    """
    Validate Meraki API key format.

    Args:
    ----
        value: The API key to validate.

    Returns
    -------
        The validated API key.

    Raises
    ------
        vol.Invalid: If API key format is invalid.

    """
    if not VALID_MERAKI_API_KEY.match(value):
        raise vol.Invalid("Invalid Meraki API key format")
    return value


def validate_org_id(value: str) -> str:
    """
    Validate Meraki organization ID format.

    Args:
    ----
        value: The org ID to validate.

    Returns
    -------
        The validated org ID.

    Raises
    ------
        vol.Invalid: If org ID format is invalid.

    """
    if not VALID_MERAKI_ORG_ID.match(value):
        raise vol.Invalid("Invalid Meraki organization ID format")
    return value


# Main config schema
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): validate_api_key,
        vol.Required(CONF_MERAKI_ORG_ID): validate_org_id,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            cv.positive_int,
            vol.Range(min=30),
        ),
    },
)

# Options schema
OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            cv.positive_int,
            vol.Range(min=30),
        ),
    },
)
