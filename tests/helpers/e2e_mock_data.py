"""Mock data helpers for E2E testing."""

import dataclasses
from typing import Any

from tests.const import MOCK_ALL_DATA


def build_mock_switch_device() -> dict[str, Any]:
    """Build mock data for a switch device."""
    return {
        "serial": "Q234-ABCD-SW1",
        "name": "Office Switch",
        "model": "MS220",
        "networkId": "N_12345",
        "productType": "switch",
        "status": "online",
        "ports_statuses": [
            {"portId": "1", "status": "Connected", "enabled": True},
            {"portId": "2", "status": "Disconnected", "enabled": False},
        ],
        "entity_id": "switch.office_switch",
    }


def build_mock_camera_device() -> dict[str, Any]:
    """Build mock data for a camera device."""
    return {
        "serial": "Q234-ABCD-CAM1",
        "name": "Front Door Camera",
        "model": "MV12",
        "networkId": "N_12345",
        "productType": "camera",
        "status": "online",
        "lanIp": "192.168.1.50",
        "entity_id": "camera.front_door_camera",
    }


def build_mock_ssid() -> dict[str, Any]:
    """Build mock data for an SSID."""
    return {
        "number": 0,
        "name": "Guest WiFi",
        "enabled": True,
        "networkId": "N_12345",
        "entity_id": "switch.guest_wifi",
    }


def ensure_network_enabled(mock_data: dict[str, Any]) -> None:
    """Ensure at least one network is enabled in the mock data."""
    if mock_data.get("networks"):
        mock_data["networks"][0]["is_enabled"] = True


def _process_dataclasses(items: list[Any]) -> list[Any]:
    """Convert a list of items (potentially dataclasses) to dicts."""
    return [
        dataclasses.asdict(item)
        if dataclasses.is_dataclass(item) and not isinstance(item, type)
        else item
        for item in items
    ]


def prepare_mock_data(settings: dict[str, Any]) -> dict[str, Any]:
    """Prepare the complete mock data dictionary."""
    mock_data: dict[str, Any] = MOCK_ALL_DATA.copy()

    # Convert dataclasses to dicts for frontend consumption
    mock_data["networks"] = _process_dataclasses(mock_data.get("networks", []))
    mock_data["devices"] = _process_dataclasses(mock_data.get("devices", []))

    ensure_network_enabled(mock_data)

    mock_data["devices"].extend(
        [build_mock_switch_device(), build_mock_camera_device()]
    )

    mock_data["ssids"] = mock_data.get("ssids", []) + [build_mock_ssid()]
    if mock_data["networks"]:
        mock_data["networks"][0]["ssids"] = mock_data["ssids"]

    mock_data["options"] = settings
    return mock_data
