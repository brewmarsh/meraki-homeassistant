"""Network-related utility functions."""

from typing import Any, Dict, List, Optional


def calculate_network_health(data: Dict[str, Any]) -> float:
    """Calculate the overall health score for a network.

    This calculates a health score from 0-100 based on:
    - Device status
    - Alert severity
    - Client connectivity
    - Network usage

    Args:
        data: Network data dictionary containing status metrics

    Returns:
        A float between 0-100 representing network health
    """
    score = 100.0

    # Check device status
    devices = data.get("devices", [])
    if devices:
        online_devices = sum(1 for d in devices if d.get("status") == "online")
        device_ratio = online_devices / len(devices)
        score *= device_ratio

    # Check alerts
    alerts = data.get("alerts", [])
    if alerts:
        critical = sum(1 for a in alerts if a.get("severity") == "critical")
        warning = sum(1 for a in alerts if a.get("severity") == "warning")
        score -= critical * 10 + warning * 5

    # Check client health
    clients = data.get("clients", [])
    if clients:
        healthy_clients = sum(1 for c in clients if c.get("status") == "healthy")
        client_ratio = healthy_clients / len(clients)
        score *= client_ratio

    return max(0.0, min(100.0, score))


def get_active_vlans(network_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get list of active VLANs in the network.

    Args:
        network_data: Network data dictionary

    Returns:
        List of active VLAN dictionaries with id and subnet info
    """
    vlans = []
    for vlan in network_data.get("vlans", []):
        if vlan.get("enabled", False):
            vlans.append(
                {
                    "id": vlan.get("id"),
                    "name": vlan.get("name"),
                    "subnet": vlan.get("subnet"),
                    "applianceIp": vlan.get("applianceIp"),
                }
            )
    return vlans


def get_ssid_status(network_data: Dict[str, Any], ssid_number: int) -> Optional[str]:
    """Get the status of a specific SSID.

    Args:
        network_data: Network data dictionary
        ssid_number: The SSID number to check

    Returns:
        Status string or None if SSID not found
    """
    ssids = network_data.get("wireless", {}).get("ssids", [])
    for ssid in ssids:
        if ssid.get("number") == ssid_number:
            if ssid.get("enabled"):
                return "enabled"
            return "disabled"
    return None
