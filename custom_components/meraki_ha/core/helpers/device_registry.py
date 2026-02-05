"""Helper functions for managing the Home Assistant device registry."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr

from ...const import DOMAIN
from ...core.const import get_ssid_identifier

_LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from ..models.network import MerakiNetwork


def async_ensure_network_devices_exist(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    networks: list[MerakiNetwork | dict[str, Any]],
) -> None:
    """Pre-register network devices in the device registry.

    This ensures that entities linking to these networks via via_device
    don't trigger warnings about non-existing devices.

    Args:
    ----
        hass: The Home Assistant instance.
        config_entry: The config entry.
        networks: The list of networks (as objects or dicts) to ensure exist.

    """
    device_registry = dr.async_get(hass)

    for network in networks:
        if isinstance(network, dict):
            network_id = network.get("id")
            network_name = network.get("name")
        else:
            network_id = network.id
            network_name = network.name

        if not network_id:
            continue

        # Canonical Name Policy: [Network] Prefix
        if network_name and not network_name.startswith("[Network] "):
            network_name = f"[Network] {network_name}"

        device_registry.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={(DOMAIN, f"network_{network_id}")},
            name=network_name,
            manufacturer="Cisco Meraki",
            model="Meraki Network",
        )


def async_ensure_ssid_devices_exist(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    ssids: list[dict[str, Any]],
) -> None:
    """Pre-register SSID devices in the device registry.

    Args:
    ----
        hass: The Home Assistant instance.
        config_entry: The config entry.
        ssids: The list of SSIDs to ensure exist.

    """
    device_registry = dr.async_get(hass)

    for ssid in ssids:
        network_id = ssid.get("networkId")
        ssid_number = ssid.get("number")
        ssid_name = ssid.get("name")

        if not network_id or ssid_number is None:
            continue

        # Canonical Identifier
        identifier_str = get_ssid_identifier(network_id, ssid_number)
        identifier = (DOMAIN, identifier_str)

        # Legacy ID Check (Cleanup Warning)
        # Check if any device has the old ":ssid:" format for this SSID
        legacy_identifier = f"{network_id}:ssid:{ssid_number}"
        legacy_found = False
        for device in dr.async_entries_for_config_entry(
            device_registry, config_entry.entry_id
        ):
            if (DOMAIN, legacy_identifier) in device.identifiers:
                _LOGGER.warning(
                    "Legacy SSID device detected for SSID %s (ID: %s). "
                    "Please consider removing it to avoid duplicates.",
                    ssid_name,
                    legacy_identifier,
                )
                legacy_found = True
                break

        # Canonical Name Policy: [SSID] Prefix
        if ssid_name and not ssid_name.startswith("[SSID] "):
            ssid_name = f"[SSID] {ssid_name}"

        device_registry.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={identifier},
            name=ssid_name,
            manufacturer="Cisco Meraki",
            model="Wireless SSID",
            via_device=(DOMAIN, f"network_{network_id}"),
        )
