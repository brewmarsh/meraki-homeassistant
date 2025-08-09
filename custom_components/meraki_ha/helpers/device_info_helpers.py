"""Helper functions for creating Home Assistant DeviceInfo objects."""
import logging
from typing import Any, Dict, Optional

from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


def resolve_device_info(
    entity_data: Dict[str, Any],
    config_entry: Dict[str, Any],
    ssid_data: Optional[Dict[str, Any]] = None,
) -> Optional[DeviceInfo]:
    """
    Resolve the DeviceInfo for a Meraki entity.

    This function contains the logic to determine whether an entity should be
    linked to a physical device or a logical SSID "device" in the Home

    Assistant device registry.

    Args:
        entity_data: The primary data dictionary for the entity.
        config_entry: The config entry for the integration.
        ssid_data: Optional SSID data if the entity is SSID-specific.

    Returns:
        A DeviceInfo object or None if linking is not possible.
    """
    device_serial = entity_data.get("serial")
    device_model = entity_data.get("model")
    device_firmware = entity_data.get("firmware")

    if ssid_data and ssid_data.get("number") is not None:
        network_id = entity_data.get("networkId")
        ssid_number = ssid_data.get("number")
        if network_id:
            ssid_device_identifier = (DOMAIN, f"{network_id}_{ssid_number}")

            # Create a device dict for the SSID to pass to the formatter
            ssid_device_data = {**ssid_data, "productType": "ssid"}

            formatted_ssid_name = format_device_name(
                device=ssid_device_data,
                config=config_entry.options,
            )

            return DeviceInfo(
                identifiers={ssid_device_identifier},
                name=formatted_ssid_name,
                model="Wireless SSID",
                manufacturer="Cisco Meraki",
            )
        else:
            _LOGGER.warning(
                "SSID-specific entity for SSID number %s is missing 'networkId'. "
                "Falling back to physical device linking.",
                ssid_number,
            )

    if not device_serial:
        _LOGGER.warning(
            "Meraki entity cannot determine device_info: Missing 'serial' for physical device."
        )
        return None

    formatted_device_name = format_device_name(
        device=entity_data,
        config=config_entry.options,
    )

    return DeviceInfo(
        identifiers={(DOMAIN, device_serial)},
        name=str(formatted_device_name),
        manufacturer="Cisco Meraki",
        model=str(device_model or "Unknown"),
        sw_version=str(device_firmware or ""),
    )
