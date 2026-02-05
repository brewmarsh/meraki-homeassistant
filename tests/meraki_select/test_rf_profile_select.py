"""Test the Meraki RF Profile select entity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.const_conf import CONF_ENABLE_SSID_SENSORS
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={CONF_ENABLE_SSID_SENSORS: True},
        entry_id="test_entry",
    )


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    # Mock the wireless object
    client.wireless = MagicMock()
    client.wireless.update_network_wireless_ssid = AsyncMock()
    client.unregister_webhook = AsyncMock(return_value=None)
    client.appliance.get_network_appliance_content_filtering_categories = AsyncMock(
        return_value={"categories": []}
    )

    return client


@pytest.fixture
def mock_data_fetch_manager() -> AsyncMock:
    """Fixture for a mocked DataFetchManager."""
    manager = AsyncMock()
    manager.get_all_data = AsyncMock(
        return_value={
            "devices": [],
            "networks": [MOCK_NETWORK],
            "ssids": [
                {
                    "networkId": MOCK_NETWORK.id,
                    "number": 1,
                    "name": "Test SSID",
                    "rfProfileId": "p1",
                }
            ],
            "rf_profiles": {
                MOCK_NETWORK.id: [
                    {"id": "p1", "name": "Profile 1"},
                    {"id": "p2", "name": "Profile 2"},
                ]
            },
            "vpn_status": {},
            "clients": [],
            "vlans": {},
            "appliance_uplink_statuses": [],
            "appliance_traffic": {},
            "content_filtering": {},
        }
    )
    return manager


async def test_rf_profile_select_entity(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
    mock_data_fetch_manager: AsyncMock,
) -> None:
    """Test the RF Profile select entity is created and functional."""
    assert await async_setup_component(hass, "http", {})
    mock_config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinator.ApiClient",
            return_value=mock_meraki_client,
        ),
        patch(
            "custom_components.meraki_ha.coordinator.DataFetchManager",
            return_value=mock_data_fetch_manager,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Find the entity by searching the registry
        entity_registry = er.async_get(hass)
        entity_id = entity_registry.async_get_entity_id(
            "select", DOMAIN, f"meraki-ssid-{MOCK_NETWORK.id}-1-rf-profile"
        )

        assert entity_id is not None

        # Verify state
        state = hass.states.get(entity_id)
        assert state is not None
        assert state.state == "Profile 1"
        assert "Profile 1" in state.attributes["options"]
        assert "Profile 2" in state.attributes["options"]
        assert "None" in state.attributes["options"]

        # Test selection
        await hass.services.async_call(
            "select",
            "select_option",
            {"entity_id": entity_id, "option": "Profile 2"},
            blocking=True,
        )

        # Verify API called
        mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_with(
            network_id=MOCK_NETWORK.id,
            number=1,
            rfProfileId="p2",
        )

        # Test selection of "None"
        await hass.services.async_call(
            "select",
            "select_option",
            {"entity_id": entity_id, "option": "None"},
            blocking=True,
        )

        # Verify API called with None
        mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_with(
            network_id=MOCK_NETWORK.id,
            number=1,
            rfProfileId=None,
        )
