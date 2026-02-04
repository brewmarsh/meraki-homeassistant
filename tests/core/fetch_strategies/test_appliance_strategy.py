"""Test ApplianceFetchStrategy."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.core.errors import (
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)
from custom_components.meraki_ha.core.fetch_strategies.appliance import (
    ApplianceFetchStrategy,
)


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.run_with_semaphore.side_effect = lambda x: x
    return client

@pytest.fixture
def disabled_features():
    return set()

@pytest.fixture
def strategy(mock_client, disabled_features):
    return ApplianceFetchStrategy(
        client=mock_client,
        _disabled_features=disabled_features,
        enable_vpn_management=False,
        enable_firewall_rules=False,
        enable_traffic_shaping=False,
    )

def test_build_network_tasks_skips_disabled(strategy, disabled_features):
    """Test that build_network_tasks skips disabled features."""
    network_id = "net1"
    disabled_features.add(f"traffic_{network_id}")
    disabled_features.add(f"vlans_{network_id}")

    tasks = {}
    with patch("asyncio.create_task", side_effect=lambda x: x):
        strategy.build_network_tasks(network_id, tasks)

    assert f"traffic_{network_id}" not in tasks
    assert f"vlans_{network_id}" not in tasks

def test_build_network_tasks_includes_enabled(strategy, disabled_features):
    """Test that build_network_tasks includes enabled features."""
    network_id = "net1"

    tasks = {}
    with patch("asyncio.create_task", side_effect=lambda x: x):
        strategy.build_network_tasks(network_id, tasks)

    assert f"traffic_{network_id}" in tasks
    assert f"vlans_{network_id}" in tasks

def test_process_network_traffic_disables_on_error(strategy, disabled_features):
    """Test that process_network_traffic disables the feature on error."""
    network_id = "net1"
    key = f"traffic_{network_id}"
    detail_data = {key: MerakiTrafficAnalysisError("Disabled")}
    appliance_traffic = {}

    strategy.process_network_traffic(network_id, detail_data, {}, appliance_traffic)

    assert key in disabled_features
    assert appliance_traffic[network_id]["error"] == "disabled"

def test_process_network_vlans_disables_on_vlan_error(strategy, disabled_features):
    """Test that process_network_vlans disables the feature on MerakiVlanError."""
    network_id = "net1"
    key = f"vlans_{network_id}"
    detail_data = {key: MerakiVlanError("Disabled")}
    vlan_by_network = {}

    strategy.process_network_vlans(network_id, detail_data, {}, vlan_by_network)

    assert key in disabled_features
    assert vlan_by_network[network_id] == []

def test_process_network_vlans_disables_on_vlans_disabled_error(strategy, disabled_features):
    """Test that process_network_vlans disables the feature on MerakiVlansDisabledError."""
    network_id = "net1"
    key = f"vlans_{network_id}"
    detail_data = {key: MerakiVlansDisabledError("Disabled")}
    vlan_by_network = {}

    strategy.process_network_vlans(network_id, detail_data, {}, vlan_by_network)

    assert key in disabled_features
    assert vlan_by_network[network_id] == []
