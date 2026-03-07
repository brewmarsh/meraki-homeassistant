"""
Services Manager.

This module defines the ServicesManager class, which is responsible for
registering services for the Meraki HA integration.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import voluptuous as vol

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

if TYPE_CHECKING:
    from .camera_service import CameraService
    from .device_control_service import DeviceControlService
    from .switch_port_service import SwitchPortService

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


class ServicesManager:
    """Manager for registering services."""

    def __init__(
        self,
        hass: HomeAssistant,
        device_control_service: DeviceControlService,
        switch_port_service: SwitchPortService,
        camera_service: CameraService,
    ) -> None:
        """Initialize the ServicesManager."""
        self.hass = hass
        self.device_control_service = device_control_service
        self.switch_port_service = switch_port_service
        self.camera_service = camera_service

    async def async_register_services(self) -> None:
        """Register services."""

        async def _async_reboot_device(call: ServiceCall) -> None:
            """Reboot a device."""
            if self.device_control_service:
                await self.device_control_service.async_reboot(call.data["serial"])

        async def _async_cycle_port(call: ServiceCall) -> None:
            """Cycle a switch port."""
            if self.switch_port_service:
                await self.switch_port_service.async_cycle_ports(
                    call.data["serial"], [call.data["port_id"]]
                )

        async def _async_generate_snapshot(call: ServiceCall) -> None:
            """Generate a camera snapshot."""
            if self.camera_service and (serial := call.data.get("serial")):
                await self.camera_service.generate_snapshot(serial)

        self.hass.services.async_register(
            DOMAIN,
            "reboot_device",
            _async_reboot_device,
            schema=SERVICE_REBOOT_DEVICE_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "cycle_port",
            _async_cycle_port,
            schema=SERVICE_CYCLE_PORT_SCHEMA,
        )

        self.hass.services.async_register(
            DOMAIN,
            "generate_snapshot",
            _async_generate_snapshot,
            schema=SERVICE_GENERATE_SNAPSHOT_SCHEMA,
        )
