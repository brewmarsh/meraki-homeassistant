"""Network-related utility functions."""
from __future__ import annotations

import ipaddress
from typing import Any
from urllib.parse import urlparse


def calculate_network_health(data: dict[str, Any]) -> float:
    """
    Calculate the overall health score for a network.

    This calculates a health score from 0-100 based on:
    - Device status
    - Alert severity
    - Client connectivity
    - Network usage

    Args:
    ----
        data: Network data dictionary containing status metrics.

    Returns:
    -------
        A float between 0-100 representing network health.

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


def get_active_vlans(network_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Get list of active VLANs in the network.

    Args:
    ----
        network_data: Network data dictionary.

    Returns:
    -------
        List of active VLAN dictionaries with id and subnet info.

    """
    vlans = []
    for vlan in network_data.get("vlans", []):
        if vlan.get("enabled"):
            vlans.append(
                {
                    "id": vlan.get("id"),
                    "name": vlan.get("name"),
                    "subnet": vlan.get("subnet"),
                    "applianceIp": vlan.get("applianceIp"),
                },
            )
    return vlans


def get_ssid_status(network_data: dict[str, Any], ssid_number: int) -> str | None:
    """
    Get the status of a specific SSID.

    Args:
    ----
        network_data: Network data dictionary.
        ssid_number: The SSID number to check.

    Returns:
    -------
        Status string or None if SSID not found.

    """
    ssids = network_data.get("wireless", {}).get("ssids", [])
    for ssid in ssids:
        if ssid.get("number") == ssid_number:
            return "enabled" if ssid.get("enabled") else "disabled"
    return None


def is_private_ip(url_or_ip: str | None) -> bool:
    """
    Check if the given string is a private IP address.

    Extracts the hostname from a URL if necessary.

    Args:
    ----
        url_or_ip: The URL or IP address to check.

    Returns:
    -------
        True if the IP is private, False otherwise.

    """
    if not url_or_ip:
        return False
    try:
        # Assume it's a full URL and parse it
        hostname = urlparse(url_or_ip).hostname
        # If parsing results in a hostname, use that.
        # Otherwise, assume the original string was the IP.
        ip_to_check = hostname or url_or_ip
        return ipaddress.ip_address(ip_to_check).is_private
    except ValueError:
        # This can happen if the input is not a valid IP or URL,
        # or if the hostname is not an IP.
        return False


def construct_rtsp_url(ip_address: str) -> str:
    """
    Construct an RTSP URL from an IP address.

    Args:
    ----
        ip_address: The IP address of the camera.

    Returns:
    -------
        The RTSP URL.

    """
    # The exact path can vary, but for many cameras, the root path is sufficient.
    # This can be expanded if specific models require a different path.
    return f"rtsp://{ip_address}:9000/live"
