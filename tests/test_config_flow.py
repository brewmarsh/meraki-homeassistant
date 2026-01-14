"""Test the Meraki HA config flow."""

from unittest.mock import patch

from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
)


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        return_value={"valid": True, "org_name": "Test Org"},
    ), patch(
        "custom_components.meraki_ha.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )
        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "init"

        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {},
        )
        await hass.async_block_till_done()

<<<<<<< HEAD
=======
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.FORM
>>>>>>> 12342c48 (fix(ci): resolve config flow test failures)
    assert result3["type"] == FlowResultType.CREATE_ENTRY
    assert result3["title"] == "Test Org"
    assert result3["data"] == {
        "meraki_api_key": "test-api-key",
        "meraki_org_id": "test-org-id",
        "org_name": "Test Org",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass: HomeAssistant) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=MerakiAuthenticationError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=MerakiConnectionError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> d778955d (test(config_flow): Add tests for API error handling)
=======


async def test_reconfigure_flow(hass: HomeAssistant) -> None:
    """Test the reconfiguration flow."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    mock_options = {
        "scan_interval": 60,
        "enable_device_tracker": True,
        "enable_vlan_management": False,
        "enabled_networks": [],
    }
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test-key", "meraki_org_id": "test-org"},
        options=mock_options,
    )
    mock_entry.add_to_hass(hass)

    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": mock_entry.entry_id,
        },
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    new_scan_interval = 120
    with patch(
        "custom_components.meraki_ha.async_setup_entry", return_value=True
    ), patch("custom_components.meraki_ha.async_unload_entry", return_value=True):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                "scan_interval": new_scan_interval,
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reconfigure_successful"

    assert mock_entry.options["scan_interval"] == new_scan_interval
    assert mock_entry.options["enable_device_tracker"] is True
>>>>>>> 00a5566c (fix: Resolve CI failures in config flow and dependencies)
=======
>>>>>>> b654416b (fix(tests): Address PR feedback)
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
