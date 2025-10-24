"""Tests for the Meraki config flow."""

import sys
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.config_flow import MerakiAuthenticationError
from custom_components.meraki_ha.const import (
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DOMAIN,
)

# Mock the hass_frontend module
sys.modules["hass_frontend"] = MagicMock()


@pytest.mark.asyncio
async def test_async_step_user_success(hass: HomeAssistant, mocker) -> None:
    """Test the user step of the config flow with valid credentials."""
    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        return_value={"valid": True, "org_name": "Test Org"},
    ):
        # Initial step
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user"}
        )
        assert result["type"] == "form"
        assert result["step_id"] == "user"

        # Provide credentials
        user_input = {
            CONF_MERAKI_API_KEY: "test-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
        }
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input
        )
        assert result["type"] == "form"
        assert result["step_id"] == "init"

        # Provide combined options
        options_input = {
            CONF_SCAN_INTERVAL: 120,
            CONF_ENABLE_DEVICE_TRACKER: True,
            CONF_IGNORED_NETWORKS: "Guest Network, Temp Network",
            "enable_vlan_management": False,
        }
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], options_input
        )
        await hass.async_block_till_done()

        # Final assertions
        assert result["type"] == "create_entry"
        assert result["title"] == "Meraki"
        assert result["data"][CONF_MERAKI_API_KEY] == user_input[CONF_MERAKI_API_KEY]
        assert result["data"][CONF_MERAKI_ORG_ID] == user_input[CONF_MERAKI_ORG_ID]

        assert result["options"] == options_input


@pytest.mark.asyncio
async def test_async_step_user_invalid_auth(hass: HomeAssistant, mocker) -> None:
    """Test the user step of the config flow with invalid credentials."""
    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=MerakiAuthenticationError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user"}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_MERAKI_API_KEY: "test-api-key",
                CONF_MERAKI_ORG_ID: "test-org-id",
            },
        )
        assert result["type"] == "form"
        assert result["errors"] == {"base": "invalid_auth"}
