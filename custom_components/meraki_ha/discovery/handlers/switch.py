"""
Meraki Switch Handler.

This module defines the SwitchHandler class, which is responsible for discovering
entities for Meraki switch devices.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from ...const_conf import CONF_ENABLE_DEVICE_SENSORS
from ...sensor.device.device_status import MerakiDeviceStatusSensor
from ...sensor.device.network_settings import (
    MerakiDeviceDNSSensor,
    MerakiDeviceGatewaySensor,
    MerakiDeviceIPSensor,
)
from ...sensor.device.switch_client_count import MerakiSwitchClientCountSensor
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.helpers.entity import Entity



_LOGGER = logging.getLogger(__name__)


class SwitchHandler(BaseHandler):
    """Handler for Meraki switch devices."""

    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover entities for switch devices."""
        if not self._coordinator.data:
            return

        # Discover Switch Device entities
        if self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
            for device in self._coordinator.data.get("devices", []):
                if device.product_type == "switch":
                    # Client Count per Switch
                    yield MerakiSwitchClientCountSensor(
                        self._coordinator, device, self._config_entry
                    )

                    # Status
                    yield MerakiDeviceStatusSensor(
                        self._coordinator, device, self._config_entry
                    )

                    # Standard IPs
                    yield MerakiDeviceIPSensor(
                        self._coordinator,
                        device,
                        self._config_entry,
                        "lanIp",
                        "LAN IP",
                    )
                    yield MerakiDeviceIPSensor(
                        self._coordinator,
                        device,
                        self._config_entry,
                        "publicIp",
                        "Public IP",
                    )

                    # Diagnostics (IP/Gateway/DNS) from uplinks
                    if device.uplinks:
                        for uplink in device.uplinks:
                            interface = uplink.get("interface")
                            if interface:
                                yield MerakiDeviceIPSensor(
                                    self._coordinator,
                                    device,
                                    self._config_entry,
                                    interface,
                                )
                                yield MerakiDeviceGatewaySensor(
                                    self._coordinator,
                                    device,
                                    self._config_entry,
                                    interface,
                                )
                                yield MerakiDeviceDNSSensor(
                                    self._coordinator,
                                    device,
                                    self._config_entry,
                                    interface,
                                )
