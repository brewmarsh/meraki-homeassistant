"""Tests for the Meraki options flow."""

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_DEVICE_NAME_FORMAT,
    CONF_AUTO_ENABLE_RTSP,
    CONF_WEBHOOK_URL,
    CONF_USE_LAN_IP_FOR_RTSP,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
)


@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the options flow."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={
            "meraki_api_key": "test-api-key",
            "meraki_org_id": "test-org-id",
        },
        options={
            CONF_SCAN_INTERVAL: 60,
            CONF_DEVICE_NAME_FORMAT: "prefix",
            CONF_AUTO_ENABLE_RTSP: False,
            CONF_WEBHOOK_URL: "",
        },
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] == "form"
    assert result["step_id"] == "init"

    user_input = {
        CONF_SCAN_INTERVAL: 120,
        CONF_DEVICE_NAME_FORMAT: "suffix",
        CONF_AUTO_ENABLE_RTSP: True,
        CONF_USE_LAN_IP_FOR_RTSP: False,
        CONF_WEBHOOK_URL: "http://example.com/webhook",
        CONF_ENABLE_DEVICE_TRACKER: True,
        CONF_ENABLE_WEB_UI: False,
        CONF_WEB_UI_PORT: 8080,
    }
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input=user_input
    )
    await hass.async_block_till_done()

    assert result["type"] == "create_entry"
    assert config_entry.options == user_input
