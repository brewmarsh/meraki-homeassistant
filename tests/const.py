"""Constants for Meraki tests."""

from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork

MOCK_NETWORK: MerakiNetwork = {
    "id": "N_12345",
    "name": "Test Network",
    "productTypes": ["appliance", "switch", "wireless"],
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

MOCK_ALL_DATA = {
    "networks": [MOCK_NETWORK],
    "devices": [MOCK_DEVICE],
    "clients": [],
}
