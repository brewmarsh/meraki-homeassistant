"""Test the enabled networks logic."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import CONF_ENABLED_NETWORKS
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator


@pytest.fixture
def coordinator_enabled_networks(hass):
    """Fixture for a MerakiDataCoordinator instance."""
    mock_api_client = MagicMock()
    entry = MagicMock()
    # Initially, no enabled networks option set (or empty list)
    entry.options = {CONF_ENABLED_NETWORKS: []}

    coordinator = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    # Manually set config_entry as it might not be set by super().__init__ if not passed
    coordinator.config_entry = entry
    return coordinator


def test_filter_enabled_networks_empty_enables_all(coordinator_enabled_networks):
    """Test that empty enabled_networks list enables all networks."""
    # Arrange
    data = {
        "networks": [
            {"id": "N_1", "name": "Network 1"},
            {"id": "N_2", "name": "Network 2"},
        ],
        "devices": [
            {"serial": "D1", "networkId": "N_1"},
            {"serial": "D2", "networkId": "N_2"},
        ],
    }

    # Act
    coordinator_enabled_networks._filter_enabled_networks(data)

    # Assert
    # Both networks should be enabled
    assert data["networks"][0]["is_enabled"] is True
    assert data["networks"][1]["is_enabled"] is True

    # Both devices should be present
    assert len(data["devices"]) == 2


def test_filter_enabled_networks_specific_list(coordinator_enabled_networks):
    """Test that specific enabled_networks list filters correctly."""
    # Arrange
    # Update options to have specific network enabled
    coordinator_enabled_networks.config_entry.options = {CONF_ENABLED_NETWORKS: ["N_1"]}

    data = {
        "networks": [
            {"id": "N_1", "name": "Network 1"},
            {"id": "N_2", "name": "Network 2"},
        ],
        "devices": [
            {"serial": "D1", "networkId": "N_1"},
            {"serial": "D2", "networkId": "N_2"},
        ],
    }

    # Act
    coordinator_enabled_networks._filter_enabled_networks(data)

    # Assert
    # Network 1 should be enabled, Network 2 disabled
    assert data["networks"][0]["is_enabled"] is True
    assert data["networks"][1]["is_enabled"] is False

    # Only devices from enabled networks should remain
    assert len(data["devices"]) == 1
    assert data["devices"][0]["serial"] == "D1"
