"""Test the Meraki VPN select entity."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import CONF_ENABLE_VPN_MANAGEMENT, DOMAIN
from custom_components.meraki_ha.types import MerakiVpn
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={CONF_ENABLE_VPN_MANAGEMENT: True},
        entry_id="test_entry",
    )


@pytest.fixture
def mock_meraki_client() -> AsyncMock:
    """Fixture for a mocked MerakiAPIClient."""
    client = AsyncMock()
    # Ensure network data is consistent
    network_id = MOCK_NETWORK.id

    client.get_all_data = AsyncMock(
        return_value={
            "devices": [],
            "networks": [MOCK_NETWORK],
            "vpn_status": {
                network_id: MerakiVpn(mode="spoke", hubs=[], subnets=[])
            },
            "ssids": [],
            "clients": [],
            "vlans": {},
            "appliance_uplink_statuses": [],
            "rf_profiles": {},
            "appliance_traffic": {},
            "content_filtering": {},
        }
    )
    client.unregister_webhook = AsyncMock(return_value=None)
    # Mock the update method
    client.appliance = AsyncMock()
    client.appliance.update_vpn_status = AsyncMock()

    return client


async def test_vpn_select_entity(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
) -> None:
    """Test the VPN select entity is created and functional."""
    assert await async_setup_component(hass, "http", {})
    mock_config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinator.ApiClient",
            return_value=mock_meraki_client,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Find the entity by searching the registry
        from homeassistant.helpers import entity_registry as er

        entity_registry = er.async_get(hass)
        entries = list(entity_registry.entities.values())

        # Look for the entity
        target_entity = None
        for e in entries:
            if "vpn" in str(e.unique_id):
                target_entity = e
                break

        assert target_entity is not None
        assert target_entity.domain == "select"

        # Verify state
        state = hass.states.get(target_entity.entity_id)
        assert state is not None
        assert state.state == "spoke"

        # Test selection
        await hass.services.async_call(
            "select",
            "select_option",
            {"entity_id": target_entity.entity_id, "option": "hub"},
            blocking=True,
        )

        # Verify API called
        mock_meraki_client.appliance.update_vpn_status.assert_called_with(
            network_id=MOCK_NETWORK.id,
            mode="hub",
        )
