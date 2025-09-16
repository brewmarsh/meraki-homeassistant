"""Utility functions for generating unique entity IDs."""


def get_vlan_entity_id(network_id: str, vlan_id: str, sensor_type: str) -> str:
    """Generate a unique ID for a VLAN sensor."""
    return f"meraki_vlan_{network_id}_{vlan_id}_{sensor_type}"


def get_firewall_rule_entity_id(network_id: str, rule_index: int) -> str:
    """Generate a unique ID for a firewall rule entity."""
    return f"meraki_firewall_rule_{network_id}_{rule_index}"
