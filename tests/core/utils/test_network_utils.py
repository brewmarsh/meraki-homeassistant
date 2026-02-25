"""Tests for network utils."""
import pytest
from custom_components.meraki_ha.core.utils.network_utils import get_active_vlans
from custom_components.meraki_ha.core.models.network import MerakiVlan

def test_get_active_vlans_with_dicts():
    """Test get_active_vlans with dictionaries (legacy)."""
    network_data = {
        "vlans": [
            {
                "id": "1",
                "name": "VLAN 1",
                "subnet": "192.168.1.0/24",
                "applianceIp": "192.168.1.1",
                "enabled": True,
            },
            {
                "id": "2",
                "name": "VLAN 2",
                "enabled": False,
            },
            {
                "id": "3",
                "name": "VLAN 3",
                "subnet": "192.168.3.0/24",
                "applianceIp": "192.168.3.1",
                "enabled": True,
            },
        ]
    }

    active = get_active_vlans(network_data)
    assert len(active) == 2
    assert active[0]["id"] == "1"
    assert active[1]["id"] == "3"
    assert active[0]["applianceIp"] == "192.168.1.1"

def test_get_active_vlans_with_objects():
    """Test get_active_vlans with MerakiVlan objects."""
    vlan1 = MerakiVlan(
        id="10",
        name="VLAN 10",
        subnet="10.0.10.0/24",
        appliance_ip="10.0.10.1",
    )
    vlan2 = MerakiVlan(
        id="20",
        name="VLAN 20",
        subnet="10.0.20.0/24",
        appliance_ip="10.0.20.1",
    )

    network_data = {
        "vlans": [vlan1, vlan2]
    }

    # This should handle objects and assume they are active
    active = get_active_vlans(network_data)

    assert len(active) == 2
    assert active[0]["id"] == "10"
    assert active[0]["name"] == "VLAN 10"
    assert active[0]["subnet"] == "10.0.10.0/24"
    assert active[0]["applianceIp"] == "10.0.10.1"

    assert active[1]["id"] == "20"
