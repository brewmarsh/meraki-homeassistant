"""
Meraki Switch Handler.

This module defines the SwitchHandler class, which is responsible for discovering
entities for Meraki switch devices.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from homeassistant.exceptions import HomeAssistantError

# Specialized Exception Handling
from ...core.errors import MerakiHAException, MerakiInformationalError

# Decomposed Constants
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
        """
        Discover entities for switch devices with resilience.
        
        This handler differentiates between dedicated switches and appliances 
        with switch ports (MX/Z3), delegating the latter to the ApplianceHandler.
        """
        if not self._coordinator.data:
            return

        if not self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
            _LOGGER.debug("Switch device sensors are disabled in options.")
            return

        devices = self._coordinator.data.get("devices", [])
        if not isinstance(devices, list):
            return

        for device in devices:
            try:
                if not hasattr(device, "product_type"):
                    continue

                # Filter out Appliances (delegated to ApplianceHandler)
                if device.product_type == "appliance" or (
                    device.model
                    and (
                        device.model.startswith("MX") or device.model.startswith("Z3")
                    )
                ):
                    _LOGGER.debug(
                        "Skipping appliance-class device %s in Switch Handler",
                        device.serial,
                    )
                    continue

                if device.product_type == "switch":
                    # Client Count per Switch
                    yield MerakiSwitchClientCountSensor(
                        self._coordinator, device, self._config_entry
                    )

                    # Switch Port Discovery
                    if self._config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
                        for entity in SwitchPortProvider.get_entities(
                            self._coordinator, device, self._config_entry
                        ):
                            yield entity

            except MerakiInformationalError as e:
                # Gracefully bypass features disabled in the Meraki Dashboard
                _LOGGER.info(
                    "Bypassing optional switch feature for %s: %s",
                    getattr(device, "serial", "unknown"),
                    e,
                )
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error(
                    "Critical discovery error for switch %s: %s",
                    getattr(device, "serial", "unknown"),
                    e,
                )
                continue