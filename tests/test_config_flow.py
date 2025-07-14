"""Tests for the Meraki config flow."""
from unittest.mock import patch

import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN


@pytest.fixture(autouse=True)
def mock_validate_meraki_credentials():
    """Mock `validate_meraki_credentials`."""
    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        return_value={"org_name": "Test Org"},
    ) as mock:
        yield mock


async def test_user_step(hass: HomeAssistant) -> None:
    """Test the user step."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "custom_components.meraki_ha.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == "Test Org [test-org-id]"
    assert result["data"] == {
        "meraki_api_key": "test-api-key",
        "meraki_org_id": "test-org-id",
    }
    assert result["options"] == {
        "scan_interval": 300,
        "device_name_format": "omitted",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_reauth(hass: HomeAssistant) -> None:
    """Test the reauth flow."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test-api-key", "meraki_org_id": "test-org-id"},
    )
    mock_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_REAUTH,
            "entry_id": mock_entry.entry_id,
        },
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "reauth"

    with patch(
        "custom_components.meraki_ha.async_setup_entry",
        return_value=True,
    ), patch(
        "custom_components.meraki_ha.async_unload_entry",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "new-api-key",
                "meraki_org_id": "new-org-id",
            },
        )

    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"

    assert mock_entry.data["meraki_api_key"] == "new-api-key"
    assert mock_entry.data["meraki_org_id"] == "new-org-id"


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the options flow."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test-api-key", "meraki_org_id": "test-org-id"},
        options={"scan_interval": 300, "device_name_format": "omitted"},
    )
    mock_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(mock_entry.entry_id)

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"scan_interval": 60, "device_name_format": "prefix"},
    )

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert mock_entry.options == {
        "scan_interval": 60,
        "device_name_format": "prefix",
    }
