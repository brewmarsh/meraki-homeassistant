"""Tests for network utility functions."""

from typing import Any

from custom_components.meraki_ha.core.utils.network_utils import (
    calculate_network_health,
    construct_rtsp_url,
    get_active_vlans,
    get_ssid_status,
    is_private_ip,
)

# ===== calculate_network_health Tests =====


def test_calculate_network_health_full_score() -> None:
    """Test health score is 100 when all devices online, no alerts, healthy clients."""
    data = {
        "devices": [
            {"status": "online"},
            {"status": "online"},
            {"status": "online"},
        ],
        "alerts": [],
        "clients": [
            {"status": "healthy"},
            {"status": "healthy"},
        ],
    }

    score = calculate_network_health(data)
    assert score == 100.0


def test_calculate_network_health_empty_data() -> None:
    """Test health score is 100 when no data provided."""
    data: dict[str, object] = {}
    score = calculate_network_health(data)
    assert score == 100.0


def test_calculate_network_health_offline_devices() -> None:
    """Test health score decreases with offline devices."""
    data = {
        "devices": [
            {"status": "online"},
            {"status": "offline"},
        ],
        "alerts": [],
        "clients": [],
    }

    score = calculate_network_health(data)
    # 50% devices online, so score should be 50
    assert score == 50.0


def test_calculate_network_health_critical_alerts() -> None:
    """Test health score decreases with critical alerts."""
    data = {
        "devices": [],
        "alerts": [
            {"severity": "critical"},
            {"severity": "critical"},
        ],
        "clients": [],
    }

    score = calculate_network_health(data)
    # 2 critical alerts = -20 from 100
    assert score == 80.0


def test_calculate_network_health_warning_alerts() -> None:
    """Test health score decreases with warning alerts."""
    data = {
        "devices": [],
        "alerts": [
            {"severity": "warning"},
            {"severity": "warning"},
        ],
        "clients": [],
    }

    score = calculate_network_health(data)
    # 2 warnings = -10 from 100
    assert score == 90.0


def test_calculate_network_health_unhealthy_clients() -> None:
    """Test health score decreases with unhealthy clients."""
    data = {
        "devices": [],
        "alerts": [],
        "clients": [
            {"status": "healthy"},
            {"status": "unhealthy"},
        ],
    }

    score = calculate_network_health(data)
    # 50% healthy clients
    assert score == 50.0


def test_calculate_network_health_combined_factors() -> None:
    """Test health score with multiple negative factors."""
    data = {
        "devices": [
            {"status": "online"},
            {"status": "offline"},
        ],
        "alerts": [
            {"severity": "critical"},  # -10
        ],
        "clients": [
            {"status": "healthy"},
            {"status": "unhealthy"},
        ],
    }

    # 50% devices online = 50
    # -10 for critical alert = 40
    # 50% healthy clients = 20
    score = calculate_network_health(data)
    assert score == 20.0


def test_calculate_network_health_minimum_zero() -> None:
    """Test health score cannot go below zero."""
    data = {
        "devices": [],
        "alerts": [{"severity": "critical"} for _ in range(15)],  # -150
        "clients": [],
    }

    score = calculate_network_health(data)
    assert score == 0.0


# ===== get_active_vlans Tests =====


def test_get_active_vlans_returns_enabled_vlans() -> None:
    """Test that only enabled VLANs are returned."""
    network_data = {
        "vlans": [
            {
                "id": 1,
                "name": "Default",
                "subnet": "192.168.1.0/24",
                "enabled": True,
                "applianceIp": "192.168.1.1",
            },
            {
                "id": 2,
                "name": "Guest",
                "subnet": "192.168.2.0/24",
                "enabled": False,
                "applianceIp": "192.168.2.1",
            },
            {
                "id": 3,
                "name": "IoT",
                "subnet": "192.168.3.0/24",
                "enabled": True,
                "applianceIp": "192.168.3.1",
            },
        ]
    }

    vlans = get_active_vlans(network_data)

    assert len(vlans) == 2
    assert vlans[0]["id"] == 1
    assert vlans[0]["name"] == "Default"
    assert vlans[1]["id"] == 3
    assert vlans[1]["name"] == "IoT"


def test_get_active_vlans_empty_list() -> None:
    """Test returns empty list when no VLANs."""
    network_data: dict[str, object] = {"vlans": []}
    vlans = get_active_vlans(network_data)
    assert vlans == []


def test_get_active_vlans_missing_vlans_key() -> None:
    """Test returns empty list when vlans key is missing."""
    network_data: dict[str, object] = {}
    vlans = get_active_vlans(network_data)
    assert vlans == []


def test_get_active_vlans_includes_all_fields() -> None:
    """Test that returned VLANs include all expected fields."""
    network_data = {
        "vlans": [
            {
                "id": 10,
                "name": "Management",
                "subnet": "10.0.10.0/24",
                "applianceIp": "10.0.10.1",
                "enabled": True,
            }
        ]
    }

    vlans = get_active_vlans(network_data)

    assert len(vlans) == 1
    assert vlans[0] == {
        "id": 10,
        "name": "Management",
        "subnet": "10.0.10.0/24",
        "applianceIp": "10.0.10.1",
    }


# ===== get_ssid_status Tests =====


def test_get_ssid_status_enabled() -> None:
    """Test returns 'enabled' for enabled SSID."""
    network_data = {
        "wireless": {
            "ssids": [
                {"number": 0, "name": "Corporate", "enabled": True},
                {"number": 1, "name": "Guest", "enabled": False},
            ]
        }
    }

    status = get_ssid_status(network_data, 0)
    assert status == "enabled"


def test_get_ssid_status_disabled() -> None:
    """Test returns 'disabled' for disabled SSID."""
    network_data = {
        "wireless": {
            "ssids": [
                {"number": 0, "name": "Corporate", "enabled": True},
                {"number": 1, "name": "Guest", "enabled": False},
            ]
        }
    }

    status = get_ssid_status(network_data, 1)
    assert status == "disabled"


def test_get_ssid_status_not_found() -> None:
    """Test returns None when SSID number not found."""
    network_data = {
        "wireless": {
            "ssids": [
                {"number": 0, "name": "Corporate", "enabled": True},
            ]
        }
    }

    status = get_ssid_status(network_data, 5)
    assert status is None


def test_get_ssid_status_empty_ssids() -> None:
    """Test returns None when no SSIDs."""
    network_data: dict[str, Any] = {"wireless": {"ssids": []}}

    status = get_ssid_status(network_data, 0)
    assert status is None


def test_get_ssid_status_missing_wireless_key() -> None:
    """Test returns None when wireless key is missing."""
    network_data: dict[str, Any] = {}

    status = get_ssid_status(network_data, 0)
    assert status is None


# ===== is_private_ip Tests =====


def test_is_private_ip_private_class_a() -> None:
    """Test detects private Class A IP."""
    assert is_private_ip("10.0.0.1") is True
    assert is_private_ip("10.255.255.255") is True


def test_is_private_ip_private_class_b() -> None:
    """Test detects private Class B IP."""
    assert is_private_ip("172.16.0.1") is True
    assert is_private_ip("172.31.255.255") is True


def test_is_private_ip_private_class_c() -> None:
    """Test detects private Class C IP."""
    assert is_private_ip("192.168.0.1") is True
    assert is_private_ip("192.168.255.255") is True


def test_is_private_ip_public() -> None:
    """Test detects public IP as not private."""
    assert is_private_ip("8.8.8.8") is False
    assert is_private_ip("1.1.1.1") is False


def test_is_private_ip_from_url() -> None:
    """Test extracts IP from URL and checks if private."""
    assert is_private_ip("rtsp://192.168.1.100:9000/live") is True
    assert is_private_ip("http://10.0.0.50/stream") is True
    assert is_private_ip("https://8.8.8.8/api") is False


def test_is_private_ip_none() -> None:
    """Test returns False for None input."""
    assert is_private_ip(None) is False


def test_is_private_ip_empty_string() -> None:
    """Test returns False for empty string."""
    assert is_private_ip("") is False


def test_is_private_ip_invalid_input() -> None:
    """Test returns False for invalid input."""
    assert is_private_ip("not-an-ip") is False
    assert is_private_ip("invalid.url.format") is False


def test_is_private_ip_localhost() -> None:
    """Test localhost is considered private."""
    assert is_private_ip("127.0.0.1") is True


# ===== construct_rtsp_url Tests =====


def test_construct_rtsp_url() -> None:
    """Test RTSP URL construction."""
    url = construct_rtsp_url("192.168.1.100")
    assert url == "rtsp://192.168.1.100:9000/live"


def test_construct_rtsp_url_different_ips() -> None:
    """Test RTSP URL construction with various IPs."""
    assert construct_rtsp_url("10.0.0.1") == "rtsp://10.0.0.1:9000/live"
    assert construct_rtsp_url("172.16.0.50") == "rtsp://172.16.0.50:9000/live"
