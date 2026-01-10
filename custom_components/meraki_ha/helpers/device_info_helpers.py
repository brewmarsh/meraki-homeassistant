"""Helper functions for creating Home Assistant DeviceInfo objects."""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


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

    # Create device info for an SSID (linked to network)
    # Hierarchy: Organization → Network → SSID
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
            # Link SSID directly to network (no intermediate grouping devices)
            return DeviceInfo(
                identifiers={identifier},
                name=formatted_name,
                model="Wireless SSID",
                manufacturer="Cisco Meraki",
                via_device=(DOMAIN, f"network_{network_id}"),
            )

    # Note: Client devices are intentionally NOT created via resolve_device_info.
    # The device_tracker.py handles clients and creates entities without devices
    # to avoid polluting the device registry with hundreds of MAC addresses.
    # This code path is kept for backwards compatibility but returns None for clients.
    client_mac = entity_data.get("mac")
    if client_mac and not entity_data.get("serial"):
        # This is a client, not a device - return None
        return None

    # Handle network devices (linked to organization)
    network_id = entity_data.get("id")
    is_network = "productTypes" in entity_data and not entity_data.get("serial")
    if is_network and network_id:
        return create_network_device_info(entity_data, config_entry)

    # Handle physical devices (linked directly to network)
    # Hierarchy: Organization → Network → Device
    # Note: We don't use intermediate "device type group" devices since HA
    # doesn't support collapsible folder hierarchy in the device registry UI.
    device_serial = entity_data.get("serial")
    device_network_id = entity_data.get("networkId")
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
        # Link device directly to its network
        if device_network_id:
            device_info["via_device"] = (DOMAIN, f"network_{device_network_id}")
        return device_info

    # This may happen temporarily during startup or if a device type is unknown
    _LOGGER.debug("Could not resolve device info for entity data: %s", entity_data)
    return None
