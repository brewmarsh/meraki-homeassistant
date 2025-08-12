"""Utility functions for generating unique entity IDs."""


def get_vlan_entity_id(network_id: str, vlan_id: int, sensor_type: str) -> str:
    """Generate a unique ID for a VLAN sensor."""
    return f"meraki_vlan_{network_id}_{vlan_id}_{sensor_type}"
