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
)
from custom_components.meraki_ha.config_flow import MerakiAuthenticationError

@pytest.mark.asyncio
async def test_async_step_user_success(hass: HomeAssistant) -> None:
    """Test the user step of the config flow with valid credentials."""
    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        return_value={"valid": True, "org_name": "Test Org"},
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user"}
        )
        assert result["type"] == "form"
        assert result["step_id"] == "user"

        user_input = {
            CONF_MERAKI_API_KEY: "test-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
            CONF_SCAN_INTERVAL: 120,
            CONF_DEVICE_NAME_FORMAT: "suffix",
            CONF_AUTO_ENABLE_RTSP: True,
            CONF_WEBHOOK_URL: "http://example.com",
        }

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input
        )
        await hass.async_block_till_done()

        assert result["type"] == "create_entry"
        assert result["title"] == "Test Org"
        assert result["data"] == user_input


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
