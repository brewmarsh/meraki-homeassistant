"""Test the Meraki VPN select entity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import CONF_ENABLE_VPN_MANAGEMENT
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.types import MerakiVpn
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
    client.organization_id = "fake_org"
    client.async_setup = AsyncMock()
    client.has_dashboard = True
    client.unregister_webhook = AsyncMock()

    # Mock the appliance object (must be MagicMock for attribute access)
    client.appliance = MagicMock()
    client.appliance.update_vpn_status = AsyncMock()
    client.appliance.get_network_appliance_content_filtering_categories = AsyncMock(
        return_value={"categories": []}
    )

    client.organization = MagicMock()
    client.organization.get_organization_networks = AsyncMock(return_value=[])

    client.network = MagicMock()
    client.network.unregister_webhook = AsyncMock()
    client.unregister_webhook = AsyncMock()

    async def mock_run_with_semaphore(coro):
        return await coro

    async def mock_run_with_cache(cache_key, func, ttl=None):
        return await func()

    client.run_with_semaphore = AsyncMock(side_effect=mock_run_with_semaphore)
    client.run_with_cache = AsyncMock(side_effect=mock_run_with_cache)

    return client


@pytest.fixture
def mock_data_fetch_manager() -> AsyncMock:
    """Fixture for a mocked DataFetchManager."""
    from custom_components.meraki_ha.types import MerakiDevice

    manager = AsyncMock()
    mock_data = {
        "devices": [
            MerakiDevice(serial="Q234-ABCD-VPN", model="MX6", name="VPN Appliance")
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
    # Action 1: Remove mock_http and mock_frontend fixtures to allow real http component setup
    assert await async_setup_component(hass, "http", {})
    mock_config_entry.add_to_hass(hass)

    # Action 2: Provide an explicit AsyncMock for the nested network call
    mock_meraki_client.appliance.update_vpn_status = AsyncMock()

    with (
        patch(
            "custom_components.meraki_ha.__init__.create_api_client",
            return_value=mock_meraki_client,
        ),
        patch(
            "custom_components.meraki_ha.create_api_client",
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
        assert target_entity.unique_id == f"meraki-network-{MOCK_NETWORK.id}-vpn"

        # Verify state
        state = hass.states.get(target_entity.entity_id)
        assert state is not None
        assert state.state == "spoke"
        assert state.attributes["options"] == ["none", "spoke", "hub"]

        # Test selection
        await hass.services.async_call(
            "select",
            "select_option",
            {"entity_id": target_entity.entity_id, "option": "hub"},
            blocking=True,
        )

        await hass.async_block_till_done()

        # Verify API called
        mock_meraki_client.appliance.update_vpn_status.assert_called_with(
            network_id=MOCK_NETWORK.id,
            mode="hub",
        )

        # Ensure integration unloads while mocks are still active
        assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
        await hass.async_block_till_done()
