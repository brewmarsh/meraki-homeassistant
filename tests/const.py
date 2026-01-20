"""Constants for Meraki tests."""

from __future__ import annotations

from dataclasses import asdict
from unittest.mock import MagicMock

from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork

MOCK_CONFIG_ENTRY_ID = "test_entry"
MOCK_CONFIG_ENTRY = MagicMock()
MOCK_CONFIG_ENTRY.entry_id = MOCK_CONFIG_ENTRY_ID


MOCK_NETWORK_INIT = {
    "id": "N_12345",
    "name": "Test Network",
    "productTypes": ["appliance", "switch", "wireless", "cellularGateway"],
    "tags": "e2e-test",
    "organizationId": "12345",
}
MOCK_NETWORK = MerakiNetwork.from_dict(MOCK_NETWORK_INIT)


MOCK_DEVICE_INIT = {
    "serial": "Q234-ABCD-5678",
    "name": "Test Device",
    "mac": "00:11:22:33:44:55",
    "model": "MR33",
    "networkId": "N_12345",
    "productType": "wireless",
    "lanIp": "1.2.3.4",
    "status": "online",
}
MOCK_DEVICE = MerakiDevice.from_dict(MOCK_DEVICE_INIT)


MOCK_MX_DEVICE_INIT = {
    "serial": "Q234-ABCD-MX",
    "name": "Test MX Device",
    "model": "MX67",
    "networkId": "N_12345",
    "productType": "appliance",
    "lanIp": "1.2.3.5",
    "status": "online",
    "mac": "00:11:22:33:44:56",
}
MOCK_MX_DEVICE = MerakiDevice.from_dict(MOCK_MX_DEVICE_INIT)

MOCK_GX_DEVICE_INIT = {
    "serial": "Q234-ABCD-GX",
    "name": "Test GX Device",
    "model": "GX20",
    "networkId": "N_12345",
    "productType": "cellularGateway",
    "lanIp": "1.2.3.6",
    "status": "online",
    "mac": "00:11:22:33:44:57",
}
MOCK_GX_DEVICE = MerakiDevice.from_dict(MOCK_GX_DEVICE_INIT)

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


MOCK_L7_FIREWALL_RULES = {
    "rules": [
        {
            "policy": "deny",
            "type": "ipRange",
            "value": "192.168.1.1",
            "comment": "Managed by Home Assistant Meraki Parental Controls",
        }
    ]
}

MOCK_ALL_DATA = {
    "networks": [MOCK_NETWORK],
    "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
    "ssids": [MOCK_SSID],
    "clients": [],
    "l7_firewall_rules": MOCK_L7_FIREWALL_RULES,
}

MOCK_CAMERA_DEVICE = MerakiDevice(
    serial="Q234-ABCD-5678",
    name="Test Device",
    mac="00:11:22:33:44:55",
    model="MV12",
    network_id="N_12345",
    product_type="camera",
    lan_ip="1.2.3.4",
    status="online",
    video_settings={
        "rtspServerEnabled": True,
        "rtspUrl": "rtsp://test.com/stream",
    },
)
