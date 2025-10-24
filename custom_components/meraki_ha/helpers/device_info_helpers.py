"""Helper functions for creating Home Assistant DeviceInfo objects."""

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


def resolve_device_info(
    entity_data: dict[str, Any],
    config_entry: ConfigEntry,
    ssid_data: dict[str, Any] | None = None,
) -> DeviceInfo | None:
    """Resolve the DeviceInfo for a Meraki entity.

    This function contains the logic to determine whether an entity should be
    linked to a physical device or a logical SSID "device" in the Home
    Assistant device registry.
    """
    # Determine the effective data to use for device resolution.
    # If ssid_data is explicitly passed, it takes precedence for SSID devices.
    # Otherwise, check if the entity_data itself represents an SSID.
    effective_data = entity_data
    is_ssid = "number" in effective_data and "networkId" in effective_data
    if ssid_data:
        is_ssid = True
        effective_data = ssid_data

    # Create device info for an SSID
    if is_ssid:
        network_id = effective_data.get("networkId")
        ssid_number = effective_data.get("number")
        if network_id:
            identifier = (DOMAIN, f"{network_id}_{ssid_number}")
            device_data_for_naming = {**effective_data, "productType": "ssid"}
            formatted_name = format_device_name(
                device=device_data_for_naming,
                config=config_entry.options,
            )
            return DeviceInfo(
                identifiers={identifier},
                name=formatted_name,
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
        device_data_for_naming = {**entity_data, "productType": "network"}
        formatted_name = format_device_name(
            device=device_data_for_naming,
            config=config_entry.options,
        )
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{network_id}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )

    if is_network and network_id:
        device_data_for_naming = {**entity_data, "productType": "network"}
        formatted_name = format_device_name(
            device=device_data_for_naming,
            config=config_entry.options,
        )
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{network_id}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )

    # Fallback to creating device info for a physical device
    device_serial = entity_data.get("serial")
    if device_serial:
        formatted_name = format_device_name(
            device=entity_data,
            config=config_entry.options,
        )
        return DeviceInfo(
            identifiers={(DOMAIN, device_serial)},
            name=str(formatted_name),
            manufacturer="Cisco Meraki",
            model=str(entity_data.get("model") or "Unknown"),
            sw_version=str(entity_data.get("firmware") or ""),
        )

    # This may happen temporarily during startup or if a device type is unknown
    _LOGGER.debug("Could not resolve device info for entity data: %s", entity_data)
    return None
