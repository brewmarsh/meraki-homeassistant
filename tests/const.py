"""Constants for Meraki tests."""

from unittest.mock import MagicMock
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork

MOCK_CONFIG_ENTRY_ID = "test_entry"
MOCK_CONFIG_ENTRY = MagicMock()
MOCK_CONFIG_ENTRY.entry_id = MOCK_CONFIG_ENTRY_ID


MOCK_NETWORK: MerakiNetwork = {
    "id": "N_12345",
    "organization_id": "test-org",
    "name": "Test Network",
    "product_types": ["appliance", "switch", "wireless", "cellularGateway"],
    "tags": "e2e-test",
    "client_count": 5,
}

MOCK_DEVICE: MerakiDevice = {
    "serial": "Q234-ABCD-5678",
    "name": "Test Device",
    "model": "MR33",
    "network_id": "N_12345",
    "product_type": "wireless",
    "lan_ip": "1.2.3.4",
    "status": "online",
}

MOCK_MX_DEVICE: MerakiDevice = {
    "serial": "Q234-ABCD-MX",
    "name": "Test MX Device",
    "model": "MX67",
    "network_id": "N_12345",
    "product_type": "appliance",
    "lan_ip": "1.2.3.5",
    "status": "online",
}

MOCK_GX_DEVICE: MerakiDevice = {
    "serial": "Q234-ABCD-GX",
    "name": "Test GX Device",
    "model": "GX20",
    "network_id": "N_12345",
    "product_type": "cellularGateway",
    "lan_ip": "1.2.3.6",
    "status": "online",
}

MOCK_SSID = {
    "number": 0,
    "name": "Test SSID",
    "enabled": True,
    "splash_page": "None",
    "ssid_admin_accessible": False,
    "auth_mode": "psk",
    "psk": "password",
    "encryption_mode": "wpa",
    "wpa_encryption_mode": "WPA2 only",
    "ip_assignment_mode": "NAT mode",
    "use_vlan_tagging": False,
    "walled_garden_enabled": False,
    "walled_garden_ranges": [],
    "min_bitrate": 11,
    "band_selection": "Dual band with band steering",
    "per_client_bandwidth_limit_up": 0,
    "per_client_bandwidth_limit_down": 0,
    "per_ssid_bandwidth_limit_up": 0,
    "per_ssid_bandwidth_limit_down": 0,
    "mandatory_dhcp_enabled": False,
    "visible": True,
    "available_on_all_aps": True,
    "availability_tags": [],
    "network_id": "N_12345",
    "client_count": 3,
}


MOCK_ALL_DATA = {
    "networks": [MOCK_NETWORK],
    "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
    "ssids": [MOCK_SSID],
    "clients": [],
}
