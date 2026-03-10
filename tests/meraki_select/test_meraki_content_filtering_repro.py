"""Reproduction test for Meraki content filtering dictionary response."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.core.models.network import MerakiNetwork

TEST_ORG_ID = "fake_org"
TEST_NETWORK_ID = "N_12345"
TEST_NETWORK = MerakiNetwork.from_dict(
    {
        "id": TEST_NETWORK_ID,
        "organizationId": TEST_ORG_ID,
        "name": "Main Office",
        "productTypes": ["appliance", "switch", "wireless", "cellularGateway"],
        "tags": "e2e-test",
    }
)


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"api_key": "fake_key", "organization_id": TEST_ORG_ID},
        options={},
        entry_id="test_entry",
    )


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiApiClientProtocol."""
    client = MagicMock()
    client.organization_id = TEST_ORG_ID
    client.appliance = MagicMock()
    client.appliance.update_network_appliance_content_filtering = AsyncMock()
    client.unregister_webhook = AsyncMock(return_value=None)
    client.async_setup = AsyncMock()
    client.has_dashboard = True
    return client


@pytest.fixture
def mock_data_fetch_manager() -> AsyncMock:
    """Fixture for a mocked DataFetchManager."""
    manager = AsyncMock()
    from custom_components.meraki_ha.types import MerakiDevice

    # Mocking blockedUrlCategories as a list of dictionaries to trigger the bug
    data = {
        "devices": [
            MerakiDevice(
                serial="Q234-ABCD-CF", model="MX64", name="Filtering Appliance"
            )
        ],
        "networks": [TEST_NETWORK],
        "content_filtering": {
            TEST_NETWORK.id: {
                "networkId": TEST_NETWORK.id,
                "blockedUrlCategories": [
                    {"id": "meraki:contentFiltering/category/8", "name": "Malware"},
                    {"id": "meraki:contentFiltering/category/9", "name": "Phishing"},
                    {"id": "meraki:contentFiltering/category/11", "name": "Botnets"},
                ],
            }
        },
        "ssids": [],
        "clients": [],
        "vlans": {},
        "appliance_uplink_statuses": [],
        "rf_profiles": {},
        "appliance_traffic": {},
    }
    manager.get_all_data = AsyncMock(return_value=data)
    manager.get_device_data = AsyncMock(return_value=data)
    manager.get_sensor_data = AsyncMock(return_value=data)
    return manager


async def test_content_filtering_select_dict_response(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
    mock_data_fetch_manager: AsyncMock,
) -> None:
    """Test that the content filtering select entity handles dictionary responses."""
    assert await async_setup_component(hass, "http", {})
    mock_config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.create_api_client",
            return_value=mock_meraki_client,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.base.DataFetchManager",
            return_value=mock_data_fetch_manager,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
        patch("homeassistant.components.camera.img_util.TurboJPEG", create=True),
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Find the entity
        from homeassistant.helpers import entity_registry as er

        entity_registry = er.async_get(hass)
        entries = list(entity_registry.entities.values())

        target_entity_id = None
        for e in entries:
            if "content-filtering" in str(e.unique_id) and e.domain == "select":
                target_entity_id = e.entity_id
                break

        assert target_entity_id is not None

        # This access should trigger the TypeError if the bug exists
        state = hass.states.get(target_entity_id)
        assert state is not None
        # Once fixed, this should match 'Security'
        assert state.state == "Security"
