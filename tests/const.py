"""Constants for Meraki tests."""
from unittest.mock import MagicMock
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork

MOCK_CONFIG_ENTRY_ID = "test_entry"
MOCK_CONFIG_ENTRY = MagicMock()
MOCK_CONFIG_ENTRY.entry_id = MOCK_CONFIG_ENTRY_ID


MOCK_NETWORK: MerakiNetwork = {
    "id": "N_12345",
    "organizationId": "test-org",
    "name": "Test Network",
    "productTypes": ["appliance", "switch", "wireless", "cellularGateway"],
    "tags": "e2e-test",
    "clientCount": 5,
}

MOCK_DEVICE: MerakiDevice = {
    "serial": "Q234-ABCD-5678",
    "name": "Test Device",
    "model": "MR33",
    "networkId": "N_12345",
    "productType": "wireless",
    "lanIp": "1.2.3.4",
    "status": "online",
}

MOCK_MX_DEVICE: MerakiDevice = {
    "serial": "Q234-ABCD-MX",
    "name": "Test MX Device",
    "model": "MX67",
    "networkId": "N_12345",
    "productType": "appliance",
    "lanIp": "1.2.3.5",
    "status": "online",
}

MOCK_GX_DEVICE: MerakiDevice = {
    "serial": "Q234-ABCD-GX",
    "name": "Test GX Device",
    "model": "GX20",
    "networkId": "N_12345",
    "productType": "cellularGateway",
    "lanIp": "1.2.3.6",
    "status": "online",
}

MOCK_SSID = {
    "number": 0,
    "name": "Test SSID",
    "enabled": True,
    "splashPage": "None",
    "ssidAdminAccessible": False,
    "authMode": "psk",
    "psk": "password",
    "encryptionMode": "wpa",
    "wpaEncryptionMode": "WPA2 only",
    "ipAssignmentMode": "NAT mode",
    "useVlanTagging": False,
    "walledGardenEnabled": False,
    "walledGardenRanges": [],
    "minBitrate": 11,
    "bandSelection": "Dual band with band steering",
    "perClientBandwidthLimitUp": 0,
    "perClientBandwidthLimitDown": 0,
    "perSsidBandwidthLimitUp": 0,
    "perSsidBandwidthLimitDown": 0,
    "mandatoryDhcpEnabled": False,
    "visible": True,
    "availableOnAllAps": True,
    "availabilityTags": [],
    "networkId": "N_12345",
    "clientCount": 3,
}


MOCK_ALL_DATA = {
    "networks": [MOCK_NETWORK],
    "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
    "ssids": [MOCK_SSID],
    "clients": [],
}
