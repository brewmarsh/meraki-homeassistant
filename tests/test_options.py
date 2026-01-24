"""Test the Meraki options flow."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DOMAIN,
)


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test options flow handles MerakiNetwork objects."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key", CONF_MERAKI_ORG_ID: "test-org-id"},
        options={},
    )
    entry.add_to_hass(hass)

    # Mock coordinator and data
    coordinator = MagicMock()
    mock_network = MagicMock()
    mock_network.id = "net1"
    mock_network.name = "Network 1"
    mock_network.__getitem__ = MagicMock(side_effect=TypeError("Not subscriptable"))

    coordinator.data = {"networks": [mock_network]}

    hass.data[DOMAIN] = {entry.entry_id: {"coordinator": coordinator}}

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"
