from unittest.mock import AsyncMock, patch

from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN


async def test_reauth_flow(hass: HomeAssistant) -> None:
    """Test the reauthentication flow."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_MERAKI_API_KEY: "old-api-key",
            CONF_MERAKI_ORG_ID: "old-org-id"
        },
        entry_id="test_reauth_entry_id",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_REAUTH, "entry_id": entry.entry_id},
        data=entry.data,
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reauth"

    with patch(
        "custom_components.meraki_ha.reauth_flow.validate_meraki_credentials",
        new_callable=AsyncMock,
        return_value=True
    ), patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        new_callable=AsyncMock,
        return_value=True
    ) as mock_reload:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_MERAKI_API_KEY: "new-api-key",
                CONF_MERAKI_ORG_ID: "new-org-id",
            },
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reauth_successful"

    assert entry.data[CONF_MERAKI_API_KEY] == "new-api-key"
    assert entry.data[CONF_MERAKI_ORG_ID] == "new-org-id"
    mock_reload.assert_called_once_with(entry.entry_id)
