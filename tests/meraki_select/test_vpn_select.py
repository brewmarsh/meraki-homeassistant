"""Test the Meraki VPN select entity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.config import CONF_ENABLE_VPN_MANAGEMENT
from custom_components.meraki_ha.types import MerakiVpn
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.setup import async_setup_component
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"api_key": "fake_key", "organization_id": "fake_org"},
        options={CONF_ENABLE_VPN_MANAGEMENT: True},
        entry_id="test_entry",
    )


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiApiClientProtocol."""
    client = MagicMock()
    # Mock the appliance object (must be MagicMock for attribute access)
    client.appliance = MagicMock()
    client.appliance.update_vpn_status = AsyncMock()
    client.unregister_webhook = AsyncMock(return_value=None)
    client.appliance.get_network_appliance_content_filtering_categories = AsyncMock(
        return_value={"categories": []}
    )

    return client


@pytest.fixture
def mock_data_fetch_manager() -> AsyncMock:
    """Fixture for a mocked DataFetchManager."""
    from custom_components.meraki_ha.types import MerakiDevice

    manager = AsyncMock()
    mock_data = {
        "devices": [
            MerakiDevice(serial="Q234-ABCD-VPN", model="MX64", name="VPN Appliance")
        ],
        "networks": [MOCK_NETWORK],
        "vpn_status": {MOCK_NETWORK.id: MerakiVpn(mode="spoke", hubs=[], subnets=[])},
        "ssids": [],
        "clients": [],
        "vlans": {},
        "appliance_uplink_statuses": [],
        "rf_profiles": {},
        "appliance_traffic": {},
        "content_filtering": {},
    }
    manager.get_all_data = AsyncMock(return_value=mock_data)
    manager.get_device_data = AsyncMock(return_value=mock_data)
    manager.get_sensor_data = AsyncMock(return_value=mock_data)
    return manager


async def test_vpn_select_entity(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
    mock_data_fetch_manager: AsyncMock,
) -> None:
    """Test the VPN select entity is created and functional."""
    assert await async_setup_component(hass, "http", {})
    mock_config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinators.base.ApiClient",
            return_value=mock_meraki_client,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.base.DataFetchManager",
            return_value=mock_data_fetch_manager,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Find the entity by searching the registry
        entity_registry = er.async_get(hass)
        entries = list(entity_registry.entities.values())

        # Look for the entity
        target_entity = None
        for e in entries:
            if e.domain == "select" and "vpn" in str(e.unique_id):
                target_entity = e
                break

        assert target_entity is not None

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
