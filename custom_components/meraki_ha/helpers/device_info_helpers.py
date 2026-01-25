"""Helper functions for creating Home Assistant DeviceInfo objects."""

import logging
from dataclasses import asdict, is_dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..types import MerakiDevice, MerakiNetwork

_LOGGER = logging.getLogger(__name__)

DEVICE_TYPE_MAPPING = {
    "camera": "Camera",
    "switch": "Switch",
    "wireless": "Wireless",
    "appliance": "Appliance",
    "security": "Appliance",
    "cellularGateway": "Gateway",
}


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
    if is_dataclass(entity_data):
        entity_data = asdict(entity_data)
    if is_dataclass(effective_data):
        effective_data = asdict(effective_data)

    # Create device info for an SSID
    if is_ssid:
        network_id = effective_data.get("networkId")
        ssid_number = effective_data.get("number")
        if network_id:
            identifier = (DOMAIN, f"{network_id}_{ssid_number}")
            name = effective_data.get("name")
            return DeviceInfo(
                identifiers={identifier},
                name=f"[SSID] {name}",
                model="Wireless SSID",
                manufacturer="Cisco Meraki",
            )

    # Handle client devices, which are linked to a physical device
    client_mac = entity_data.get("mac")
    parent_serial = entity_data.get("recentDeviceSerial")
    if client_mac and parent_serial:
        return DeviceInfo(
            identifiers={(DOMAIN, client_mac)},
            name=str(entity_data.get("description") or client_mac),
            manufacturer=str(entity_data.get("manufacturer") or "Unknown"),
            via_device=(DOMAIN, parent_serial),
        )

    # Handle network devices
    network_id = entity_data.get("id")
    is_network = "productTypes" in entity_data and not entity_data.get("serial")
    if is_network and network_id:
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{network_id}")},
            name=entity_data.get("name"),
            manufacturer="Cisco Meraki",
            model="Network",
        )

    # Fallback to creating device info for a physical device
    device_serial = entity_data.get("serial")
    if device_serial:
        product_type = entity_data.get("productType")
        prefix = DEVICE_TYPE_MAPPING.get(product_type, "Device")
        name = entity_data.get("name")
        return DeviceInfo(
            identifiers={(DOMAIN, device_serial)},
            name=f"[{prefix}] {name}",
            manufacturer="Cisco Meraki",
            model=str(entity_data.get("model") or "Unknown"),
            sw_version=str(entity_data.get("firmware") or ""),
        )

    # This may happen temporarily during startup or if a device type is unknown
    _LOGGER.debug("Could not resolve device info for entity data: %s", entity_data)
    return None
