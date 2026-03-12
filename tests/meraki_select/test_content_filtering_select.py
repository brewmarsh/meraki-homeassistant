"""Test the Meraki content filtering select entity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "fake_key", CONF_MERAKI_ORG_ID: "fake_org"},
        options={},
        entry_id="test_entry",
    )


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiApiClientProtocol."""
    client = MagicMock()
    client.organization_id = "fake_org"

    # Mock the appliance object
    client.appliance = MagicMock()
    client.appliance.update_network_appliance_content_filtering = AsyncMock()
    client.appliance.get_network_appliance_content_filtering_categories = AsyncMock(
        return_value={
            "categories": [
                {
                    "id": "meraki:contentFiltering/category/1",
                    "name": "Adult and Pornography",
                },
                {"id": "meraki:contentFiltering/category/2", "name": "Nudity"},
                {"id": "meraki:contentFiltering/category/8", "name": "Malware Sites"},
                {
                    "id": "meraki:contentFiltering/category/9",
                    "name": "Phishing and Other Frauds",
                },
                {"id": "meraki:contentFiltering/category/11", "name": "Bot Nets"},
                {
                    "id": "meraki:contentFiltering/category/12",
                    "name": "Spyware and Adware",
                },
                {
                    "id": "meraki:contentFiltering/category/15",
                    "name": "Proxy Avoidance and Anonymizers",
                },
            ]
        }
    )

    client.organization = MagicMock()
    client.organization.get_organization_networks = AsyncMock(return_value=[])

    client.unregister_webhook = AsyncMock(return_value=None)
    client.async_setup = AsyncMock()
    client.has_dashboard = True

    return client


@pytest.fixture
def mock_data_fetch_manager() -> AsyncMock:
    """Fixture for a mocked DataFetchManager."""
    manager = AsyncMock()
    from custom_components.meraki_ha.types import MerakiDevice

    mock_data = {
        "devices": [
            MerakiDevice(
                serial="Q234-ABCD-CF", model="MX64", name="Filtering Appliance"
            )
        ],
        "networks": [MOCK_NETWORK],
        "content_filtering": {
            MOCK_NETWORK.id: {
                "networkId": MOCK_NETWORK.id,
                "blockedUrlCategories": [
                    {"id": "meraki:contentFiltering/category/8"},
                    {"id": "meraki:contentFiltering/category/9"},
                    {"id": "meraki:contentFiltering/category/11"},
                    {"id": "meraki:contentFiltering/category/12"},
                    {"id": "meraki:contentFiltering/category/15"},
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
    manager.get_all_data = AsyncMock(return_value=mock_data)
    manager.get_device_data = AsyncMock(return_value=mock_data)
    manager.get_sensor_data = AsyncMock(return_value=mock_data)
    return manager


async def test_content_filtering_select_entity(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
    mock_data_fetch_manager: AsyncMock,
) -> None:
    """Test the content filtering select entity is created and functional."""
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

        # Find the entity by searching the registry
        from homeassistant.helpers import entity_registry as er

        entity_registry = er.async_get(hass)
        entries = list(entity_registry.entities.values())

        # Look for the entity
        target_entity = None
        for e in entries:
            if "content-filtering" in str(e.unique_id) and e.domain == "select":
                target_entity = e
                break

        assert target_entity is not None
        assert target_entity.domain == "select"

        # Verify state
        state = hass.states.get(target_entity.entity_id)
        assert state is not None
        assert state.state == "Security"

        # Test selection
        await hass.services.async_call(
            "select",
            "select_option",
            {"entity_id": target_entity.entity_id, "option": "Family"},
            blocking=True,
        )

        # Verify API called with Family categories (URN format)
        mock_meraki_client.appliance.update_network_appliance_content_filtering.assert_called_with(
            network_id=MOCK_NETWORK.id,
            blockedUrlCategories=[
                "meraki:contentFiltering/category/1",
                "meraki:contentFiltering/category/2",
                "meraki:contentFiltering/category/8",
            ],
        )
