"""
Meraki Wireless Handler.

This module defines the WirelessHandler class, which is responsible for discovering
entities for Meraki wireless networks and devices.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import HomeAssistantError

# Specialized Exception Handling
from ...core.errors import MerakiHAException, MerakiInformationalError

# Decomposed Constants
from custom_components.meraki_ha.const.config import (
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
)
from ...sensor.device.ap_client_count import MerakiAPClientCountSensor
from ...sensor.network.ssid_client_count import MerakiSSIDClientCountSensor
from ...switch.adult_content_filtering import MerakiAdultContentFilteringSwitch
from ...switch.meraki_device_led_switch import MerakiDeviceLEDSwitch
from ...text.meraki_ssid_name import MerakiSSIDNameText
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...core.api import MerakiApiClientProtocol
    from ..coordinators import MerakiSwitchCoordinator


_LOGGER = logging.getLogger(__name__)


class WirelessHandler(BaseHandler):
    """Handler for Meraki wireless devices and SSIDs."""

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        config_entry: ConfigEntry,
        meraki_client: MerakiApiClientProtocol,
    ) -> None:
        """Initialize the WirelessHandler."""
        super().__init__(coordinator, config_entry)
        self._meraki_client = meraki_client

    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover entities for wireless devices and SSIDs with resilience."""
        if not self._coordinator.data or "ssids" not in self._coordinator.data:
            return

        # 1. Discover AP Device entities (Client Count, LED Control)
        try:
            async for entity in self._discover_device_entities():
                yield entity
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Fatal error during wireless device discovery: %s", e)

        # 2. Discover SSID entities (Broadcast, Enable, Name, Client Count)
        try:
            async for entity in self._discover_ssid_entities():
                yield entity
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Fatal error during SSID entity discovery: %s", e)

    async def _discover_device_entities(self) -> AsyncIterator[Entity]:
        """Discover entities for wireless Access Points."""
        if not self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
            return

        devices = self._coordinator.data.get("devices", [])
        if not isinstance(devices, list):
            return

        for device in devices:
            try:
                if getattr(device, "product_type", None) == "wireless":
                    # Client Count per AP
                    yield MerakiAPClientCountSensor(
                        self._coordinator, device, self._config_entry
                    )
                    # LED Control (Requires management interface)
                    if getattr(device, "management_interface", None):
                        yield MerakiDeviceLEDSwitch(
                            self._coordinator, device, self._config_entry
                        )
            except MerakiInformationalError as e:
                _LOGGER.info("Bypassing optional feature for AP %s: %s", 
                             getattr(device, "serial", "unknown"), e)
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error("Error discovering wireless device %s: %s", 
                              getattr(device, "serial", "unknown"), e)

    async def _discover_ssid_entities(self) -> AsyncIterator[Entity]:
        """Discover entities for wireless SSIDs."""
        from ...meraki_select.rf_profile import MerakiRFProfileSelect
        from ...switch.meraki_ssid_device_switch import (
            MerakiSSIDBroadcastSwitch,
            MerakiSSIDEnabledSwitch,
        )

        if not self._config_entry.options.get(CONF_ENABLE_SSID_SENSORS, True):
            return

        ssids = self._coordinator.data.get("ssids", [])
        if not isinstance(ssids, list):
            return

        for ssid in ssids:
            try:
                if not isinstance(ssid, dict) or "networkId" not in ssid or "number" not in ssid:
                    continue

                rf_profile = self._get_rf_profile(ssid)

                # Core SSID Controls
                yield MerakiSSIDEnabledSwitch(self._coordinator, self._meraki_client, 
                                             self._config_entry, ssid, rf_profile)
                yield MerakiSSIDBroadcastSwitch(self._coordinator, self._meraki_client, 
                                               self._config_entry, ssid, rf_profile)
                yield MerakiSSIDNameText(self._coordinator, self._meraki_client, 
                                        self._config_entry, ssid)
                yield MerakiSSIDClientCountSensor(self._coordinator, self._config_entry, ssid)

                # NAT-specific features
                if ssid.get("ipAssignmentMode") == "NAT mode":
                    yield MerakiAdultContentFilteringSwitch(self._coordinator, self._config_entry, ssid)

                # RF Profile Selection
                yield MerakiRFProfileSelect(self._coordinator, self._meraki_client, 
                                           self._config_entry, ssid)

            except MerakiInformationalError as e:
                _LOGGER.info("Bypassing optional feature for SSID %s: %s", 
                             ssid.get("name", "unknown"), e)
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error("Error discovering SSID %s: %s", 
                              ssid.get("name", "unknown"), e)

    def _get_rf_profile(self, ssid: dict[str, Any]) -> dict[str, Any] | None:
        """Find the RF profile for this SSID's network."""
        rf_profiles = self._coordinator.data.get("rf_profiles") if self._coordinator.data else None
        if isinstance(rf_profiles, dict):
            network_rf_profiles = rf_profiles.get(ssid["networkId"])
            if network_rf_profiles:
                return next(iter(network_rf_profiles), None)
        return None