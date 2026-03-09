"""Services for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import voluptuous as vol

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

if TYPE_CHECKING:
    from .ipsk_manager import IPSKManager

_LOGGER = logging.getLogger(__name__)

SERVICE_CREATE_GUEST_KEY = "create_guest_key"
SERVICE_GENERATE_GUEST_ACCESS = "generate_guest_access"

# Schema for technical/automation use
SERVICE_CREATE_GUEST_KEY_SCHEMA = vol.Schema(
    {
        vol.Required("network_id"): cv.string,
        vol.Required("ssid_number"): vol.All(vol.Coerce(int), vol.Range(min=0, max=14)),
        vol.Required("duration_minutes"): cv.positive_int,
        vol.Optional("passphrase"): cv.string,
        vol.Optional("name", default="Guest Key"): cv.string,
        vol.Optional("group_policy_id"): cv.string,
    }
)

# Schema for frontend card use (matches JS property names)
GUEST_ACCESS_SCHEMA = vol.Schema(
    {
        vol.Required("network_id"): cv.string,
        vol.Required("ssid"): vol.All(vol.Coerce(int), vol.Range(min=0, max=14)),
        vol.Required("duration"): cv.positive_int,
        vol.Optional("guest_name", default="Guest"): cv.string,
        vol.Optional("passphrase"): cv.string,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the Meraki integration."""

    async def _async_create_guest_key(call: ServiceCall) -> None:
        """Create a guest IPSK using technical parameters."""
        network_id = call.data["network_id"]
        ssid_number = str(call.data["ssid_number"])
        duration_minutes = call.data["duration_minutes"]
        passphrase = call.data.get("passphrase")
        name = call.data["name"]
        group_policy_id = call.data.get("group_policy_id")

        ipsk_manager: IPSKManager | None = hass.data[DOMAIN].get("ipsk_manager")
        if not ipsk_manager:
            raise HomeAssistantError("IPSK Manager not initialized")

        config_entry_id = _find_config_entry_by_network(hass, network_id)
        if not config_entry_id:
            raise HomeAssistantError(f"Network ID {network_id} not found")

        await ipsk_manager.create_guest_key(
            config_entry_id=config_entry_id,
            network_id=network_id,
            ssid_number=ssid_number,
            duration_minutes=duration_minutes,
            name=name,
            passphrase=passphrase,
            group_policy_id=group_policy_id,
        )

    async def _async_generate_guest_access(call: ServiceCall) -> None:
        """Generate a guest IPSK using frontend-friendly parameters."""
        network_id = call.data["network_id"]
        ssid = str(call.data["ssid"])
        duration = call.data["duration"]
        guest_name = call.data["guest_name"]
        passphrase = call.data.get("passphrase")

        ipsk_manager: IPSKManager | None = hass.data[DOMAIN].get("ipsk_manager")
        if not ipsk_manager:
            raise HomeAssistantError("IPSK Manager not initialized")

        config_entry_id = _find_config_entry_by_network(hass, network_id)
        if not config_entry_id:
            raise HomeAssistantError(f"Network ID {network_id} not found")

        # Map frontend parameters to the underlying IPSK manager method
        await ipsk_manager.create_guest_key(
            config_entry_id=config_entry_id,
            network_id=network_id,
            ssid_number=ssid,
            duration_minutes=duration,
            name=guest_name,
            passphrase=passphrase,
        )

    # Register both service entry points
    hass.services.async_register(
        DOMAIN,
        SERVICE_CREATE_GUEST_KEY,
        _async_create_guest_key,
        schema=SERVICE_CREATE_GUEST_KEY_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_GUEST_ACCESS,
        _async_generate_guest_access,
        schema=GUEST_ACCESS_SCHEMA,
    )


def _find_config_entry_by_network(hass: HomeAssistant, network_id: str) -> str | None:
    """Helper to find which config entry manages a specific network."""
    for entry_id, entry_data in hass.data[DOMAIN].items():
        if not isinstance(entry_data, dict):
            continue
        main_coordinator = entry_data.get("main_coordinator")
        if (
            main_coordinator
            and hasattr(main_coordinator, "networks_by_id")
            and network_id in main_coordinator.networks_by_id
        ):
            return entry_id
    return None