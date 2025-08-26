"""Constants for Meraki tests."""
from unittest.mock import MagicMock
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork

MOCK_CONFIG_ENTRY = MagicMock()
MOCK_CONFIG_ENTRY.entry_id = "test_entry"


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


MOCK_ALL_DATA = {
    "networks": [MOCK_NETWORK],
    "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
    "clients": [],
}
