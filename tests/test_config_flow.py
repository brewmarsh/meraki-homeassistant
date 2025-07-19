"""Tests for the Meraki config flow."""

from unittest.mock import patch

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN


async def test_async_step_user_success(hass: HomeAssistant) -> None:
    """Test the user step of the config flow with valid credentials."""
    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        return_value={"valid": True, "org_name": "Test Org"},
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user"}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
                "scan_interval": 60,
                "device_name_format": "prefix",
            },
        )
        assert result["type"] == "create_entry"
        assert result["title"] == "Test Org [test-org-id]"
        assert result["data"] == {
            "meraki_api_key": "test-api-key",
            "meraki_org_id": "test-org-id",
        }
        assert result["options"] == {
            "scan_interval": 60,
            "device_name_format": "prefix",
        }


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the options flow."""
    entry = await hass.config_entries.async_add(
        {
            "entry_id": "test_entry_id",
            "domain": DOMAIN,
            "title": "Test Org",
            "data": {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
            "options": {
                "scan_interval": 60,
                "device_name_format": "prefix",
            },
        }
    )

    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            "scan_interval": 120,
            "device_name_format": "suffix",
        },
    )

    assert result["type"] == "create_entry"
    assert result["data"] == {
        "scan_interval": 120,
        "device_name_format": "suffix",
    }
