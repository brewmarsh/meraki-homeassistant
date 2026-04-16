"""Tests for the Discovery Coordinator."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.discovery.coordinator import DiscoveryCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr


@pytest.fixture
def mock_api():
    """Mock Meraki API client."""
    api = MagicMock()
    api.organization.get_organization.return_value = {
        "id": "org123",
        "name": "Test Org",
    }
    api.organization.get_organization_networks.return_value = [
        {"id": "net1", "name": "Network 1"},
        {"id": "net2", "name": "Network 2"},
    ]
    api.enabled_networks = []
    return api


@pytest.fixture
def mock_config_entry():
    """Mock Config Entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    return entry


async def test_discovery_coordinator_registry_update(
    hass: HomeAssistant, mock_api, mock_config_entry
):
    """Test that the coordinator updates the device registry with Orgs and Networks."""
    coordinator = DiscoveryCoordinator(hass, mock_config_entry, mock_api)

    # Run the refresh
    await coordinator.async_refresh()

    dev_reg = dr.async_get(hass)

    # Check Organization device
    org_device = dev_reg.async_get_device(identifiers={(DOMAIN, "org_org123")})
    assert org_device is not None
    assert org_device.name == "Cisco Meraki: Test Org"
    assert org_device.model == "Organization"
    assert org_device.entry_type == dr.DeviceEntryType.SERVICE

    # Check Network devices
    net1_device = dev_reg.async_get_device(identifiers={(DOMAIN, "network_net1")})
    assert net1_device is not None
    assert net1_device.name == "Meraki Network: Network 1"
    assert net1_device.via_device_id == org_device.id

    net2_device = dev_reg.async_get_device(identifiers={(DOMAIN, "network_net2")})
    assert net2_device is not None
    assert net2_device.name == "Meraki Network: Network 2"
    assert net2_device.via_device_id == org_device.id


async def test_discovery_coordinator_selective_networks(
    hass: HomeAssistant, mock_api, mock_config_entry
):
    """Test that the coordinator only creates devices for selected networks."""
    mock_api.enabled_networks = ["net1"]
    coordinator = DiscoveryCoordinator(hass, mock_config_entry, mock_api)

    await coordinator.async_refresh()

    dev_reg = dr.async_get(hass)

    # net1 should exist
    assert dev_reg.async_get_device(identifiers={(DOMAIN, "network_net1")}) is not None
    # net2 should NOT exist
    assert dev_reg.async_get_device(identifiers={(DOMAIN, "network_net2")}) is None
