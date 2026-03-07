"""Helper functions for managing the Home Assistant device registry."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr

from custom_components.meraki_ha.const.integration import DOMAIN, _LOGGER= logging.getLogger(__name__)

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


