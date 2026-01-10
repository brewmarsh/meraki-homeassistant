"""Helper functions for creating Home Assistant DeviceInfo objects."""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)

# Mapping of Meraki product types to display names and models
DEVICE_TYPE_DISPLAY_NAMES: dict[str, str] = {
    "wireless": "Access Points",
    "switch": "Switches",
    "camera": "Cameras",
    "appliance": "Security Appliances",
    "cellularGateway": "Cellular Gateways",
    "sensor": "Sensors",
    "clients": "Clients",  # Special grouping for network clients
    "vlans": "VLANs",  # Special grouping for network VLANs
    "ssids": "SSIDs",  # Special grouping for wireless SSIDs
}

DEVICE_TYPE_MODELS: dict[str, str] = {
    "wireless": "MR Series",
    "switch": "MS Series",
    "camera": "MV Series",
    "appliance": "MX Series",
    "cellularGateway": "MG Series",
    "sensor": "MT Series",
    "clients": "Network Clients",  # Special grouping for network clients
    "vlans": "Network VLANs",  # Special grouping for network VLANs
    "ssids": "Wireless SSIDs",  # Special grouping for wireless SSIDs
}


def create_organization_device_info(
    org_id: str,
    org_name: str,
) -> DeviceInfo:
    """
    Create DeviceInfo for the Meraki Organization (top-level hub).

    This is the root of the device hierarchy:
    Organization → Network → Devices/Clients
    """
    return DeviceInfo(
        identifiers={(DOMAIN, f"org_{org_id}")},
        name=org_name,
        manufacturer="Cisco Meraki",
        model="Organization",
    )


def create_device_type_group_info(
    network_id: str,
    network_name: str,
    product_type: str,
) -> DeviceInfo:
    """
    Create DeviceInfo for a device type grouping (linked to Network).

    Hierarchy: Organization → Network → Device Type Group → Devices

    Parameters
    ----------
    network_id : str
        The network ID this group belongs to.
    network_name : str
        The name of the network (used in the group name).
    product_type : str
        The Meraki product type (wireless, switch, camera, etc.).

    """
    display_name = DEVICE_TYPE_DISPLAY_NAMES.get(product_type, product_type.title())
    model_name = DEVICE_TYPE_MODELS.get(product_type, "Meraki Devices")

    return DeviceInfo(
        identifiers={(DOMAIN, f"devicetype_{network_id}_{product_type}")},
        name=f"{network_name} {display_name}",
        manufacturer="Cisco Meraki",
        model=model_name,
        via_device=(DOMAIN, f"network_{network_id}"),
    )


def create_network_device_info(
    network_data: Mapping[str, Any],
    config_entry: ConfigEntry,
) -> DeviceInfo:
    """
    Create DeviceInfo for a Meraki Network (linked to Organization).

    Hierarchy: Organization → Network → Device Type Groups → Devices
    """
    network_id = network_data.get("id")
    org_id = network_data.get("organizationId")
    device_data_for_naming = {**network_data, "productType": "network"}
    formatted_name = format_device_name(
        device=device_data_for_naming,
        config=config_entry.options,
    )

    device_info = DeviceInfo(
        identifiers={(DOMAIN, f"network_{network_id}")},
        name=formatted_name,
        manufacturer="Cisco Meraki",
        model="Network",
    )

    # Link network to its parent organization
    if org_id:
        device_info["via_device"] = (DOMAIN, f"org_{org_id}")

    return device_info


def resolve_device_info(
    entity_data: Mapping[str, Any],
    config_entry: ConfigEntry,
    ssid_data: Mapping[str, Any] | None = None,
) -> DeviceInfo | None:
    """
    Resolve the DeviceInfo for a Meraki entity.

    This function contains the logic to determine whether an entity should be
    linked to a physical device or a logical SSID "device" in the Home
    Assistant device registry.

    Device Hierarchy:
    - Organization (top-level hub)
      - Network (under organization)
        - Devices (APs, switches, cameras - under network)
        - SSIDs (under network)
        - Clients (under network, as siblings to devices)
    """
    # Determine the effective data to use for device resolution.
    # If ssid_data is explicitly passed, it takes precedence for SSID devices.
    # Otherwise, check if the entity_data itself represents an SSID.
    effective_data = entity_data
    is_ssid = "number" in effective_data and "networkId" in effective_data
    if ssid_data:
        is_ssid = True
        effective_data = ssid_data

    # Create device info for an SSID (linked to SSIDs group under network)
    # Hierarchy: Organization → Network → SSIDs Group → SSID
    if is_ssid:
        network_id = effective_data.get("networkId")
        ssid_number = effective_data.get("number")
        if network_id:
            # Use ssid_ prefix to prevent collisions with other entity types
            identifier = (DOMAIN, f"ssid_{network_id}_{ssid_number}")
            device_data_for_naming = {**effective_data, "productType": "ssid"}
            formatted_name = format_device_name(
                device=device_data_for_naming,
                config=config_entry.options,
            )
            # Link SSID to its SSIDs group (under network)
            return DeviceInfo(
                identifiers={identifier},
                name=formatted_name,
                model="Wireless SSID",
                manufacturer="Cisco Meraki",
                via_device=(DOMAIN, f"devicetype_{network_id}_ssids"),
            )

    # Handle client devices (linked to Clients group under network)
    # Hierarchy: Organization → Network → Clients Group → Client
    client_mac = entity_data.get("mac")
    client_network_id = entity_data.get("networkId")
    if client_mac:
        # Use client_ prefix to prevent collisions with other entity types
        client_name = str(entity_data.get("description") or client_mac)
        client_manufacturer = str(entity_data.get("manufacturer") or "Unknown")

        device_info = DeviceInfo(
            identifiers={(DOMAIN, f"client_{client_mac}")},
            name=client_name,
            manufacturer=client_manufacturer,
        )

        # Link client to its Clients group (under network)
        if client_network_id:
            device_info["via_device"] = (
                DOMAIN,
                f"devicetype_{client_network_id}_clients",
            )

        return device_info

    # Handle network devices (linked to organization)
    network_id = entity_data.get("id")
    is_network = "productTypes" in entity_data and not entity_data.get("serial")
    if is_network and network_id:
        return create_network_device_info(entity_data, config_entry)

    # Handle physical devices (linked to their device type group)
    # Hierarchy: Organization → Network → Device Type Group → Device
    device_serial = entity_data.get("serial")
    device_network_id = entity_data.get("networkId")
    product_type = entity_data.get("productType")
    if device_serial:
        formatted_name = format_device_name(
            device=entity_data,
            config=config_entry.options,
        )
        device_info = DeviceInfo(
            identifiers={(DOMAIN, device_serial)},
            name=str(formatted_name),
            manufacturer="Cisco Meraki",
            model=str(entity_data.get("model") or "Unknown"),
            sw_version=str(entity_data.get("firmware") or ""),
        )
        # Link device to its device type group (if product type known)
        # Otherwise fall back to linking directly to network
        if device_network_id and product_type:
            device_info["via_device"] = (
                DOMAIN,
                f"devicetype_{device_network_id}_{product_type}",
            )
        elif device_network_id:
            device_info["via_device"] = (DOMAIN, f"network_{device_network_id}")
        return device_info

    # This may happen temporarily during startup or if a device type is unknown
    _LOGGER.debug("Could not resolve device info for entity data: %s", entity_data)
    return None
