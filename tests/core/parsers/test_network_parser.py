"""Tests for the Meraki Network Parser."""

import pytest

from custom_components.meraki_ha.core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)
from custom_components.meraki_ha.core.models.network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)
from custom_components.meraki_ha.core.parsers.network import parse_network_data


@pytest.fixture
def mock_networks():
    """Fixture for mock networks."""
    return [
        MerakiNetwork(id="N_1", name="Network 1", product_types=["appliance"]),
        MerakiNetwork(id="N_2", name="Network 2", product_types=["wireless"]),
    ]


def test_parse_network_data_success(mock_networks):
    """Test successful parsing of all data types."""
    detail_data = {
        "traffic_N_1": {"sent": 100, "recv": 200},
        "vlans_N_1": [
            {
                "id": 10,
                "name": "VLAN 10",
                "subnet": "192.168.10.0/24",
                "applianceIp": "192.168.10.1",
            }
        ],
        "l3_firewall_rules_N_1": {
            "rules": [
                {
                    "comment": "Allow all",
                    "policy": "allow",
                    "protocol": "any",
                    "srcPort": "Any",
                    "srcCidr": "Any",
                    "destPort": "Any",
                    "destCidr": "Any",
                    "syslogEnabled": False,
                }
            ]
        },
        "traffic_shaping_N_1": {"rules": []},
        "vpn_status_N_1": {"mode": "hub"},
        "content_filtering_N_1": {"blockedUrlCategories": []},
        "rf_profiles_N_2": [{"id": "rf_1", "name": "Profile 1"}],
    }
    disabled_features = set()
    previous_data = {}

    result = parse_network_data(
        detail_data, mock_networks, previous_data, disabled_features
    )

    assert result["appliance_traffic"]["N_1"] == {"sent": 100, "recv": 200}

    vlans = result["vlans"]["N_1"]
    assert len(vlans) == 1
    assert isinstance(vlans[0], MerakiVlan)
    assert vlans[0].id == 10

    fw_rules = result["l3_firewall_rules"]["N_1"]
    assert len(fw_rules) == 1
    assert isinstance(fw_rules[0], MerakiFirewallRule)

    assert isinstance(result["traffic_shaping"]["N_1"], MerakiTrafficShaping)
    assert isinstance(result["vpn_status"]["N_1"], MerakiVpn)

    assert result["rf_profiles"]["N_2"] == [{"id": "rf_1", "name": "Profile 1"}]
    assert result["content_filtering"]["N_1"] == {"blockedUrlCategories": []}


def test_parse_traffic_analysis_disabled(mock_networks):
    """Test handling of disabled traffic analysis."""
    error = MerakiTrafficAnalysisError("Traffic analysis is not enabled")
    detail_data = {
        "traffic_N_1": error,
    }
    disabled_features = set()
    previous_data = {}

    result = parse_network_data(
        detail_data, mock_networks, previous_data, disabled_features
    )

    assert "traffic_N_1" in disabled_features
    assert result["appliance_traffic"]["N_1"]["error"] == "disabled"
    assert result["appliance_traffic"]["N_1"]["reason"] == str(error)


def test_parse_vlans_disabled(mock_networks):
    """Test handling of disabled VLANs."""
    error = MerakiVlansDisabledError("VLANs are not enabled")
    detail_data = {
        "vlans_N_1": error,
    }
    disabled_features = set()
    previous_data = {}

    result = parse_network_data(
        detail_data, mock_networks, previous_data, disabled_features
    )

    assert "vlans_N_1" in disabled_features
    assert result["vlans"]["N_1"] == []


def test_parse_vlans_informational_error(mock_networks):
    """Test handling of informational error for VLANs."""
    error = MerakiInformationalError("VLANs are not enabled")
    detail_data = {
        "vlans_N_1": error,
    }
    disabled_features = set()
    previous_data = {}

    result = parse_network_data(
        detail_data, mock_networks, previous_data, disabled_features
    )

    assert "vlans_N_1" in disabled_features
    assert result["vlans"]["N_1"] == []


def test_parse_use_previous_data(mock_networks):
    """Test using previous data when API call fails or is missing."""
    detail_data = {}
    disabled_features = set()
    previous_data = {
        "traffic_N_1": {"sent": 50, "recv": 50},
        "vlans": {"N_1": [{"id": 5, "name": "Old VLAN"}]},
    }

    result = parse_network_data(
        detail_data, mock_networks, previous_data, disabled_features
    )

    assert result["appliance_traffic"]["N_1"] == {"sent": 50, "recv": 50}
    # Vlan objects might not be re-hydrated from dicts if previous data was raw dicts?
    # The current implementation checks:
    # `if prev_vlans: vlan_by_network[network_id] = prev_vlans`.
    # Let's assume previous_data has objects for this test.
    vlan_obj = MerakiVlan(
        id=5, name="Old VLAN", subnet="1.1.1.0/24", appliance_ip="1.1.1.1"
    )
    previous_data["vlans"]["N_1"] = [vlan_obj]

    result = parse_network_data(
        detail_data, mock_networks, previous_data, disabled_features
    )

    assert result["vlans"]["N_1"] == [vlan_obj]
