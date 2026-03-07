"""Integration-level tests for the Meraki HA component."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.types import MerakiNetwork  # Combined import
from tests.const import (  # Combined import
    MOCK_DEVICE,
    MOCK_GX_DEVICE,
    MOCK_MX_DEVICE,
    MOCK_NETWORK,
)


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={},
        entry_id="test_entry",
    )


@pytest.fixture
def mock_meraki_client() -> AsyncMock:
    """Fixture for a mocked MerakiApiClientProtocol."""
    client = MagicMock(spec=AsyncMock)
    client.async_setup = AsyncMock(return_value=None)
    client.unregister_webhook = AsyncMock(return_value=None)
    client.appliance = AsyncMock()
    client.appliance.get_network_appliance_content_filtering_categories = AsyncMock(
        return_value={"categories": []}
    )
    return client


@pytest.fixture
def mock_data_fetch_manager() -> AsyncMock:
    """Fixture for a mocked DataFetchManager."""
    manager = AsyncMock()
    manager.get_device_data = AsyncMock(
        return_value={
            "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
            "networks": [  # Using MerakiNetwork directly
                MerakiNetwork(
                    id=MOCK_NETWORK.id,
                    name="Test Network",
                    product_types=["wireless", "appliance"],
                    organization_id="fake_org",
                ),
            ],
            "ssids": [
                {
                    "number": 0,
                    "name": "Test SSID",
                    "enabled": True,
                    "networkId": MOCK_NETWORK.id,
                },
            ],
            "clients": [],
            "vlans": {},
            "appliance_uplink_statuses": [],
            "rf_profiles": {},
            "appliance_traffic": {},
        },
    )
    manager.get_sensor_data = AsyncMock(
        return_value={
            "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
            "networks": [  # Using MerakiNetwork directly
                MerakiNetwork(
                    id=MOCK_NETWORK.id,
                    name="Test Network",
                    product_types=["wireless", "appliance"],
                    organization_id="fake_org",
                ),
            ],
            "ssids": [
                {
                    "number": 0,
                    "name": "Test SSID",
                    "enabled": True,
                    "networkId": MOCK_NETWORK.id,
                },
            ],
            "clients": [],
            "vlans": {},
            "appliance_uplink_statuses": [],
            "rf_profiles": {},
            "appliance_traffic": {},
        },
    )
    return manager


@pytest.mark.enable_socket
async def test_ssid_device_creation_and_unification(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
    mock_data_fetch_manager: AsyncMock,
) -> None:
    """
    Test that entities are attached to the Virtual Controller (Network Device).

    Args:
    ----
        hass: The Home Assistant instance.
        mock_config_entry: The config entry.
        mock_meraki_client: The mocked Meraki API client.
        mock_data_fetch_manager: The mocked DataFetchManager.

    """
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
    ):
        # Set up the component
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Get the device and entity registries
        device_registry = async_get_device_registry(hass)
        entity_registry = async_get_entity_registry(hass)

        # Refactor: Find devices related to the Network (Virtual Controller)
        network_device_identifier = (DOMAIN, f"network_{MOCK_NETWORK.id}")
        network_device = device_registry.async_get_device({network_device_identifier})

        # Assert that a device was created
        assert network_device is not None

        # Assert that the device has the correct name (Virtual Controller format)
        assert network_device.name == "[Network] Test Network"

        # Find all entities associated with this device by querying the entity registry
        entities = [
            entity.entity_id
            for entity in entity_registry.entities.values()
            if entity.device_id == network_device.id
        ]

        # Assert that multiple entities have been created for this one device
        # Should include SSID entities, Network Status, etc.
        assert len(entities) > 0


@pytest.mark.enable_socket
async def test_integration_reload(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_meraki_client: AsyncMock,
    mock_data_fetch_manager: AsyncMock,
) -> None:
    """
    Test that the integration reloads successfully.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_config_entry: The config entry.
        mock_meraki_client: The mocked Meraki API client.
        mock_data_fetch_manager: The mocked DataFetchManager.

    """
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
    ):
        # Set up the component
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Reload the integration
        assert await hass.config_entries.async_reload(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        # Check that the coordinator is still there, indicating a successful reload
        assert DOMAIN in hass.data
        assert mock_config_entry.entry_id in hass.data[DOMAIN]
        assert "main_coordinator" in hass.data[DOMAIN][mock_config_entry.entry_id]
