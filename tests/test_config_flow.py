"""Tests for the Meraki config flow."""
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_KEY

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.config_flow import ConfigFlowHandler


async def test_async_step_user(
    hass: HomeAssistant,
) -> None:
    """Test the async_step_user function."""
    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials"
    ) as mock_validate:
        mock_validate.return_value = {"valid": True, "org_name": "org_name"}
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user", "entry_id": "test_entry_id"}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test_api_key",
                "meraki_org_id": "org_id",
            },
        )
        assert result["type"] == "create_entry"
        assert result["title"] == "org_name [org_id]"
        assert result["data"]["meraki_api_key"] == "test_api_key"
        assert result["data"]["meraki_org_id"] == "org_id"
