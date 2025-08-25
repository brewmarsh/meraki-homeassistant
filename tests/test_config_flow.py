"""Tests for the Meraki config flow."""

from unittest.mock import patch

from homeassistant.core import HomeAssistant
import pytest

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_DEVICE_NAME_FORMAT,
    CONF_AUTO_ENABLE_RTSP,
    CONF_WEBHOOK_URL,
    CONF_USE_LAN_IP_FOR_RTSP,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    CONF_IGNORED_NETWORKS,
)
from custom_components.meraki_ha.config_flow import MerakiAuthenticationError


@pytest.mark.asyncio
async def test_async_step_user_success(hass: HomeAssistant) -> None:
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
        assert result["step_id"] == "general"

        # Provide general options
        general_input = {
            CONF_SCAN_INTERVAL: 120,
            CONF_DEVICE_NAME_FORMAT: "suffix",
        }
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], general_input
        )
        assert result["type"] == "form"
        assert result["step_id"] == "features"

        # Provide features options
        features_input = {
            CONF_AUTO_ENABLE_RTSP: True,
            CONF_USE_LAN_IP_FOR_RTSP: False,
            CONF_ENABLE_DEVICE_TRACKER: True,
            CONF_ENABLE_WEB_UI: False,
            CONF_WEB_UI_PORT: 8080,
            CONF_HIDE_UNCONFIGURED_SSIDS: True,
        }
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], features_input
        )
        assert result["type"] == "form"
        assert result["step_id"] == "advanced"

        # Provide advanced options
        advanced_input = {
            CONF_WEBHOOK_URL: "http://example.com/webhook",
            CONF_IGNORED_NETWORKS: "Guest Network, Temp Network",
        }
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], advanced_input
        )
        await hass.async_block_till_done()

        # Final assertions
        assert result["type"] == "create_entry"
        assert result["title"] == "Test Org"
        assert result["data"][CONF_MERAKI_API_KEY] == user_input[CONF_MERAKI_API_KEY]
        assert result["data"][CONF_MERAKI_ORG_ID] == user_input[CONF_MERAKI_ORG_ID]

        expected_options = {**general_input, **features_input, **advanced_input}
        assert result["options"] == expected_options


@pytest.mark.asyncio
async def test_async_step_user_invalid_auth(hass: HomeAssistant) -> None:
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
