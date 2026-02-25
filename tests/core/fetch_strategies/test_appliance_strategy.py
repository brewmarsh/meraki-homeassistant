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
from custom_components.meraki_ha.core.models.device import (
    MerakiAppliancePort,
    MerakiDevice,
)


@pytest.fixture
def mock_client():
    """Fixture for a mock Meraki API client."""
    client = MagicMock()
    # Mock run_with_semaphore to just return the coroutine/call
    client.run_with_semaphore.side_effect = lambda x: x
    return client


@pytest.fixture
def disabled_features():
    """Fixture for the disabled features set."""
    return set()


@pytest.fixture
def strategy(mock_client, disabled_features):
    """Fixture for the ApplianceFetchStrategy."""
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

    # Patch async methods to avoid unawaited coroutine warnings
    with patch.object(
        strategy, "_async_get_appliance_ports", return_value=MagicMock()
    ), patch.object(
        strategy, "_get_uplink_performance", return_value=MagicMock()
    ):
        strategy.build_network_tasks(network_id, tasks)

    assert f"traffic_{network_id}" not in tasks
    assert f"vlans_{network_id}" not in tasks


def test_build_network_tasks_includes_enabled(strategy, disabled_features):
    """Test that build_network_tasks includes enabled features."""
    network_id = "net1"

    tasks = {}

    # Patch async methods to avoid unawaited coroutine warnings
    with patch.object(
        strategy, "_async_get_appliance_ports", return_value=MagicMock()
    ), patch.object(
        strategy, "_get_uplink_performance", return_value=MagicMock()
    ):
        strategy.build_network_tasks(network_id, tasks)

    assert f"traffic_{network_id}" in tasks
    assert f"vlans_{network_id}" in tasks
    # Verify always-on tasks
    assert f"appliance_ports_{network_id}" in tasks
    assert f"content_filtering_{network_id}" in tasks


def test_build_network_tasks_respects_feature_flags(mock_client, disabled_features):
    """Test that build_network_tasks respects boolean feature flags."""
    network_id = "net1"

    # All enabled
    strategy_enabled = ApplianceFetchStrategy(
        client=mock_client,
        _disabled_features=disabled_features,
        enable_vpn_management=True,
        enable_firewall_rules=True,
        enable_traffic_shaping=True,
    )
    tasks = {}

    # Patch async methods to avoid unawaited coroutine warnings
    with patch.object(
        strategy_enabled, "_async_get_appliance_ports", return_value=MagicMock()
    ), patch.object(
        strategy_enabled, "_get_uplink_performance", return_value=MagicMock()
    ):
        strategy_enabled.build_network_tasks(network_id, tasks)

    assert f"vpn_status_{network_id}" in tasks
    assert f"l3_firewall_rules_{network_id}" in tasks
    assert f"traffic_shaping_{network_id}" in tasks

    # All disabled
    strategy_disabled = ApplianceFetchStrategy(
        client=mock_client,
        _disabled_features=disabled_features,
        enable_vpn_management=False,
        enable_firewall_rules=False,
        enable_traffic_shaping=False,
    )
    tasks = {}

    # Patch async methods to avoid unawaited coroutine warnings
    with patch.object(
        strategy_disabled, "_async_get_appliance_ports", return_value=MagicMock()
    ), patch.object(
        strategy_disabled, "_get_uplink_performance", return_value=MagicMock()
    ):
        strategy_disabled.build_network_tasks(network_id, tasks)

    assert f"vpn_status_{network_id}" not in tasks
    assert f"l3_firewall_rules_{network_id}" not in tasks
    assert f"traffic_shaping_{network_id}" not in tasks


def test_build_device_tasks(strategy):
    """Test that build_device_tasks adds correct tasks."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    mock_device.network_id = "NET1"
    tasks = {}

    strategy.build_device_tasks(mock_device, tasks, capabilities=[])

    assert f"appliance_settings_{mock_device.serial}" in tasks


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


def test_process_network_vlans_disables_on_vlans_disabled_error(
    strategy, disabled_features
):
    """Test that process_network_vlans disables feature on MerakiVlansDisabledError."""
    network_id = "net1"
    key = f"vlans_{network_id}"
    detail_data = {key: MerakiVlansDisabledError("Disabled")}
    vlan_by_network = {}

    strategy.process_network_vlans(network_id, detail_data, {}, vlan_by_network)

    assert key in disabled_features
    assert vlan_by_network[network_id] == []


def test_process_device_details_ports(strategy):
    """Test processing device details for appliance ports."""
    mock_device = MagicMock()
    mock_device.network_id = "net1"
    detail_data = {
        "appliance_ports_net1": [
            {"number": 1, "enabled": True},
            {"number": 2, "enabled": False},
        ]
    }

    strategy.process_device_details(mock_device, detail_data, None)

    assert len(mock_device.appliance_ports) == 2
    assert mock_device.appliance_ports[0].number == 1
    assert mock_device.appliance_ports[1].enabled is False


def test_process_device_details_settings(strategy):
    """Test processing device details for appliance settings."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    detail_data = {
        "appliance_settings_SERIAL1": {
            "dynamicDns": {"enabled": True, "prefix": "test"}
        }
    }

    strategy.process_device_details(mock_device, detail_data, None)

    assert mock_device.dynamic_dns == {"enabled": True, "prefix": "test"}


def test_process_device_details_fallback_to_prev(strategy):
    """Test processing device details falls back to previous data."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    mock_device.network_id = "net1"
    detail_data = {}
    prev_device = MerakiDevice(
        serial="SERIAL1",
        network_id="net1",
        appliance_ports=[MerakiAppliancePort(number=1, enabled=True)],
        dynamic_dns={"enabled": True, "prefix": "prev"},
    )

    strategy.process_device_details(mock_device, detail_data, prev_device)

    assert mock_device.appliance_ports == prev_device.appliance_ports
    assert mock_device.dynamic_dns == prev_device.dynamic_dns
