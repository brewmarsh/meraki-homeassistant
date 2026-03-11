"""
Meraki Switch Handler.

This module defines the SwitchHandler class, which is responsible for discovering
entities for Meraki switch devices.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from custom_components.meraki_ha.const.config import (
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_PORT_SENSORS,
)

from ...sensor.device.switch_client_count import MerakiSwitchClientCountSensor
from ..providers import SwitchPortProvider
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
            devices = self._coordinator.data.get("devices", [])
            if not isinstance(devices, list):
                return

            for device in devices:
                try:
                    if not hasattr(device, "product_type"):
                        continue

                    # Add Exclusion Logic
                    if device.product_type == "appliance" or (
                        device.model
                        and (
                            device.model.startswith("MX") or device.model.startswith("Z3")
                        )
                    ):
                        _LOGGER.debug(
                            "Skipping device %s in Switch Handler (Appliance Handler)",
                            device.serial,
                        )
                        continue

                    if device.product_type == "switch":
                        # Client Count per Switch
                        try:
                            yield MerakiSwitchClientCountSensor(
                                self._coordinator, device, self._config_entry
                            )
                        except Exception as err:
                            _LOGGER.error(
                                "Failed to instantiate MerakiSwitchClientCountSensor for device %s: %s",
                                device.serial,
                                err,
                            )

                        # Switch Ports
                        if self._config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
                            try:
                                for entity in SwitchPortProvider.get_entities(
                                    self._coordinator, device, self._config_entry
                                ):
                                    yield entity
                            except Exception as err:
                                _LOGGER.error(
                                    "Failed to discover SwitchPort entities for device %s: %s",
                                    device.serial,
                                    err,
                                )
                except Exception as err:
                    _LOGGER.error(
                        "Failed to discover switch device entities for %s: %s",
                        getattr(device, "serial", "Unknown"),
                        err,
                        exc_info=True,
                    )
