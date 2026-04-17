"""Services for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import voluptuous as vol

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv

if TYPE_CHECKING:
    from .ipsk_manager import IPSKManager

_LOGGER = logging.getLogger(__name__)

SERVICE_CREATE_GUEST_KEY = "create_guest_key"
SERVICE_GENERATE_GUEST_ACCESS = "generate_guest_access"

# Service schemas
SERVICE_REBOOT_DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required("serial"): cv.string,
    }
)

SERVICE_CYCLE_PORT_SCHEMA = vol.Schema(
    {
        vol.Required("serial"): cv.string,
        vol.Required("port_id"): cv.string,
    }
)

SERVICE_GENERATE_SNAPSHOT_SCHEMA = vol.Schema(
    {
        vol.Required("serial"): cv.string,
    }
)

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

GUEST_ACCESS_SCHEMA = vol.Schema(
    {
        vol.Required("network_id"): cv.string,
        vol.Required("ssid"): vol.All(vol.Coerce(int), vol.Range(min=0, max=14)),
        vol.Required("duration"): cv.positive_int,
        vol.Optional("guest_name", default="Guest"): cv.string,
        vol.Optional("passphrase"): cv.string,
        vol.Optional("group_policy"): cv.string,
        vol.Optional("group_policy_id"): cv.string,
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
            raise ServiceValidationError("IPSK Manager not initialized")

        config_entry_id = _find_config_entry_by_network(hass, network_id)
        if not config_entry_id:
            raise ServiceValidationError(f"Network ID {network_id} not found")

        # Handle policy logic
        policy_id_to_use = group_policy_id
        if policy_id_to_use == "NONE":
            policy_id_to_use = "NONE"
        elif not policy_id_to_use or policy_id_to_use == "CREATE":
            policy_id_to_use = await ipsk_manager.get_or_create_guest_policy(
                config_entry_id, network_id
            )
            if not policy_id_to_use:
                raise ServiceValidationError(
                    "A Group Policy ID is required but could not be "
                    "determined or created."
                )

        await ipsk_manager.create_guest_key(
            config_entry_id=config_entry_id,
            network_id=network_id,
            ssid_number=ssid_number,
            duration_minutes=duration_minutes,
            name=name,
            passphrase=passphrase,
            group_policy_id=policy_id_to_use,
        )

    async def _async_generate_guest_access(call: ServiceCall) -> None:
        """Generate a guest IPSK using frontend-friendly parameters."""
        network_id = call.data["network_id"]
        ssid = str(call.data["ssid"])
        duration = call.data["duration"]
        guest_name = call.data["guest_name"]
        passphrase = call.data.get("passphrase")
        group_policy = call.data.get("group_policy") or call.data.get("group_policy_id")

        ipsk_manager: IPSKManager | None = hass.data[DOMAIN].get("ipsk_manager")
        if not ipsk_manager:
            raise ServiceValidationError("IPSK Manager not initialized")

        config_entry_id = _find_config_entry_by_network(hass, network_id)
        if not config_entry_id:
            raise ServiceValidationError(f"Network ID {network_id} not found")

        # Handle policy logic
        policy_id_to_use = group_policy
        if policy_id_to_use == "NONE":
            policy_id_to_use = "NONE"
        elif not policy_id_to_use or policy_id_to_use == "CREATE":
            policy_id_to_use = await ipsk_manager.get_or_create_guest_policy(
                config_entry_id, network_id
            )
            if not policy_id_to_use:
                raise ServiceValidationError(
                    "A Group Policy ID is required but could not be "
                    "determined or created."
                )

        await ipsk_manager.create_guest_key(
            config_entry_id=config_entry_id,
            network_id=network_id,
            ssid_number=ssid,
            duration_minutes=duration,
            name=guest_name,
            passphrase=passphrase,
            group_policy_id=policy_id_to_use,
        )

    async def _async_reboot_device(call: ServiceCall) -> None:
        """Reboot a Meraki device."""
        serial = call.data["serial"]
        # Find config entry that manages this device
        for _entry_id, entry_data in hass.data[DOMAIN].items():
            if not isinstance(entry_data, dict):
                continue
            api_client = entry_data.get("api_client")
            main_coordinator = entry_data.get("main_coordinator")
            if main_coordinator and api_client:
                # Check if device is in this coordinator
                devices = main_coordinator.data.get("devices", [])
                if any(d.serial == serial for d in devices):
                    await api_client.async_reboot_device(serial)
                    return

        raise ServiceValidationError(f"Device with serial {serial} not found")

    async def _async_cycle_port(call: ServiceCall) -> None:
        """Cycle a Meraki switch port."""
        serial = call.data["serial"]
        port_id = call.data["port_id"]
        # Find config entry that manages this device
        for _entry_id, entry_data in hass.data[DOMAIN].items():
            if not isinstance(entry_data, dict):
                continue
            api_client = entry_data.get("api_client")
            main_coordinator = entry_data.get("main_coordinator")
            if main_coordinator and api_client:
                # Check if device is in this coordinator
                devices = main_coordinator.data.get("devices", [])
                if any(d.serial == serial for d in devices):
                    await api_client.switch.cycle_device_switch_ports(serial, [port_id])
                    return

        raise ServiceValidationError(f"Device with serial {serial} not found")

    # Register services
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

    hass.services.async_register(
        DOMAIN,
        "reboot_device",
        _async_reboot_device,
        schema=SERVICE_REBOOT_DEVICE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        "cycle_port",
        _async_cycle_port,
        schema=SERVICE_CYCLE_PORT_SCHEMA,
    )


def _find_config_entry_by_network(hass: HomeAssistant, network_id: str) -> str | None:
    """Find which config entry manages a specific network."""
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
