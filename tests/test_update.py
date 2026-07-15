"""Tests for the Meraki update platform."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.update import MerakiUpdateEntity
from homeassistant.exceptions import HomeAssistantError


@pytest.fixture
def mock_device():
    """Mock Meraki device."""
    device = MagicMock()
    device.serial = "ABC-123"
    device.firmware = "wired-15-44"
    device.network_id = "N_123"
    device.product_type = "switch"
    device.firmware_upgrades = {
        "availableVersions": [
            {
                "firmware": "wired-16-1",
                "releaseNotes": "Bug fixes and stability improvements.",
            }
        ]
    }
    return device


@pytest.fixture
def mock_coordinator(mock_device):
    """Mock Meraki coordinator."""
    coordinator = MagicMock()
    coordinator.api = MagicMock()
    coordinator.api.network = MagicMock()
    coordinator.api.network.create_network_firmware_upgrades_rollout = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    coordinator.data = {"devices": [mock_device]}
    return coordinator


@pytest.mark.asyncio
async def test_update_entity_properties(hass, mock_coordinator, mock_device):
    """Test update entity properties."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, entry_id="test_entry")
    entity = MerakiUpdateEntity(mock_coordinator, mock_device, entry)

    assert entity.installed_version == "wired-15-44"
    assert entity.latest_version == "wired-16-1"
    assert entity.release_notes == "Bug fixes and stability improvements."
    assert entity.unique_id == "ABC-123_update"
    assert entity.name == "Firmware Update"


@pytest.mark.asyncio
async def test_update_entity_install(hass, mock_coordinator, mock_device):
    """Test update entity install."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, entry_id="test_entry")
    entity = MerakiUpdateEntity(mock_coordinator, mock_device, entry)

    await entity.async_install(version="wired-16-1", backup=False)

    mock_coordinator.api.network.create_network_firmware_upgrades_rollout.assert_called_once_with(
        network_id="N_123",
        product_type="switch",
    )
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_update_entity_install_failure(hass, mock_coordinator, mock_device):
    """Test update entity install failure."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, entry_id="test_entry")
    entity = MerakiUpdateEntity(mock_coordinator, mock_device, entry)

    mock_coordinator.api.network.create_network_firmware_upgrades_rollout.side_effect = Exception(
        "API Error"
    )

    with pytest.raises(
        HomeAssistantError, match="Failed to trigger firmware upgrade: API Error"
    ):
        await entity.async_install(version="wired-16-1", backup=False)
