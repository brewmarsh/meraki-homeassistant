"""Services for the Meraki integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from ..const import DOMAIN

if TYPE_CHECKING:
    from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

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


async def async_setup_services(
    hass: HomeAssistant,
    coordinator: MerakiDataUpdateCoordinator,
) -> None:
    """Set up the services for the Meraki integration."""
    device_control_service = coordinator.device_control_service
    switch_port_service = coordinator.switch_port_service
    camera_service = coordinator.camera_service

    async def _async_reboot_device(call) -> None:
        """Reboot a device."""
        if device_control_service:
            await device_control_service.async_reboot(call.data["serial"])

    async def _async_cycle_port(call) -> None:
        """Cycle a switch port."""
        if switch_port_service:
            await switch_port_service.async_cycle_ports(
                call.data["serial"], [call.data["port_id"]]
            )

    async def _async_generate_snapshot(call) -> None:
        """Generate a camera snapshot."""
        if camera_service:
            await camera_service.generate_snapshot(call.data["serial"])

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

    hass.services.async_register(
        DOMAIN,
        "generate_snapshot",
        _async_generate_snapshot,
        schema=SERVICE_GENERATE_SNAPSHOT_SCHEMA,
    )
