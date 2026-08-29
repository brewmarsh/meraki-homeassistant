"""Helper functions for creating Home Assistant DeviceInfo objects."""

import logging
from dataclasses import asdict, is_dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from custom_components.meraki_ha.const.integration import DOMAIN

from ..core.models.device import MerakiDevice
from ..core.models.network import MerakiNetwork
from ..core.utils.naming_utils import format_device_name, standardize_device_name

_LOGGER = logging.getLogger(__name__)

DEVICE_TYPE_MAPPING = {
    "sensor": "Sensor",
    "camera": "Camera",
    "switch": "Switch",
    "wireless": "Wireless",
    "appliance": "Appliance",
    "security": "Appliance",
    "cellularGateway": "Gateway",
}


def _resolve_ssid_info(data: dict[str, Any]) -> DeviceInfo | None:
    """Resolve DeviceInfo for an SSID (Virtual Controller)."""
    network_id = data.get("networkId")
    if network_id:
        # Refactor: SSID entities are now attached to the Virtual Controller
        # (Network Device). We return only the identifier, letting the
        # MerakiNetworkEntity populate details.
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{network_id}")},
        )
    return None


def _resolve_client_info(data: dict[str, Any]) -> DeviceInfo | None:
    """Resolve DeviceInfo for a client device."""
    client_mac = data.get("mac")
    parent_serial = data.get("recentDeviceSerial")
    if client_mac and parent_serial:
        return DeviceInfo(
            identifiers={(DOMAIN, client_mac)},
            name=standardize_device_name(str(data.get("description") or client_mac)),
            manufacturer="Cisco Meraki",
            via_device=(DOMAIN, parent_serial),
        )
    return None


def _resolve_network_info(data: dict[str, Any]) -> DeviceInfo | None:
    """Resolve DeviceInfo for a network device (Virtual Controller)."""
    network_id = data.get("id")
    is_network = ("productTypes" in data or "product_types" in data) and not data.get(
        "serial"
    )
    if is_network and network_id:
        # Special case: if model is already "Network", return it (tests rely on this)
        model = data.get("model") or "Network Controller Service"

        # Refactor: Virtual Controller Pattern
        raw_net_name = data.get("name") or "Unknown Network"

        # Design Doc: Name format "Site: {name}"
        # Check if already prefixed to avoid double prefix
        if str(raw_net_name).startswith("Site: "):
            name = raw_net_name
        else:
            name = f"Site: {raw_net_name}"

        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{network_id}")},
            name=standardize_device_name(name),
            manufacturer="Cisco Meraki",
            model=model,
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=f"https://dashboard.meraki.com/gen/n/{network_id}/manage/nodes",
        )
    return None


def _resolve_physical_device_info(
    data: dict[str, Any], config_entry: ConfigEntry
) -> DeviceInfo | None:
    """Resolve DeviceInfo for a physical device."""
    device_serial = data.get("serial")
    network_id = data.get("networkId")
    if device_serial:
        model = str(data.get("model") or "Unknown")

        # Optimization: Use the centralized format_device_name.
        name = format_device_name(data, config_entry.options)

        device_info = DeviceInfo(
            identifiers={(DOMAIN, device_serial)},
            name=name,
            manufacturer="Cisco Meraki",
            model=model,
            sw_version=str(data.get("firmware") or ""),
        )
        if network_id:
            device_info["via_device"] = (DOMAIN, f"network_{network_id}")
        return device_info
    return None


def resolve_device_info(
    entity_data: MerakiDevice | MerakiNetwork | dict[str, Any],
    config_entry: ConfigEntry,
    ssid_data: dict[str, Any] | None = None,
) -> DeviceInfo | None:
    """
    Resolve the DeviceInfo for a Meraki entity.

    This function contains the logic to determine whether an entity should be
    linked to a physical device or a logical SSID "device" in the Home
    Assistant device registry.
    """
    # Determine the effective data to use for device resolution.
    effective_data = entity_data
    is_ssid = False

    if is_dataclass(effective_data):
        is_ssid = hasattr(effective_data, "number") and hasattr(
            effective_data, "networkId"
        )
    else:
        is_ssid = "number" in effective_data and "networkId" in effective_data

    if ssid_data:
        is_ssid = True
        effective_data = ssid_data

    # Convert dataclasses to dicts for consistent access below
    entity_data_dict: dict[str, Any]
    if is_dataclass(entity_data) and not isinstance(entity_data, type):
        entity_data_dict = asdict(entity_data)
    elif isinstance(entity_data, dict):
        entity_data_dict = entity_data
    else:
        entity_data_dict = {}

    effective_data_dict: dict[str, Any]
    if is_dataclass(effective_data) and not isinstance(effective_data, type):
        effective_data_dict = asdict(effective_data)
    elif isinstance(effective_data, dict):
        effective_data_dict = effective_data
    else:
        effective_data_dict = {}

    # Resolve using specialized helpers
    if is_ssid:
        return _resolve_ssid_info(effective_data_dict)

    if info := _resolve_client_info(entity_data_dict):
        return info

    if info := _resolve_network_info(entity_data_dict):
        return info

    if info := _resolve_physical_device_info(entity_data_dict, config_entry):
        return info

    # This may happen temporarily during startup or if a device type is unknown
    _LOGGER.debug("Could not resolve device info for entity data: %s", entity_data)
    return None
