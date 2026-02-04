"""Services setup helper for the Meraki integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from custom_components.meraki_ha.const import DOMAIN

if TYPE_CHECKING:
    from custom_components.meraki_ha.services.camera_service import CameraService
    from custom_components.meraki_ha.services.device_control_service import (
        DeviceControlService,
    )
    from custom_components.meraki_ha.services.switch_port_service import (
        SwitchPortService,
    )

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
    device_control_service: DeviceControlService,
    switch_port_service: SwitchPortService,
    camera_service: CameraService,
) -> None:
    """Set up the services for the Meraki integration."""

    async def _async_reboot_device(call: ServiceCall) -> None:
        """Reboot a device."""
        if device_control_service:
            await device_control_service.async_reboot(call.data["serial"])

    async def _async_cycle_port(call: ServiceCall) -> None:
        """Cycle a switch port."""
        if switch_port_service:
            await switch_port_service.async_cycle_ports(
                call.data["serial"], [call.data["port_id"]]
            )

    async def _async_generate_snapshot(call: ServiceCall) -> None:
        """Generate a camera snapshot."""
        if camera_service and (serial := call.data.get("serial")):
            await camera_service.generate_snapshot(serial)

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
