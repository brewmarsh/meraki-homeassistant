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

from ...core.errors import MerakiHAException, MerakiInformationalError
from ...const_conf import (
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
        """Discover entities for wireless devices and SSIDs."""
        if not self._coordinator.data or "ssids" not in self._coordinator.data:
            return

        # Discover AP Device entities
        try:
            async for entity in self._discover_device_entities():
                yield entity
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Error during wireless device entity discovery: %s", e)

        # Discover SSID entities
        try:
            async for entity in self._discover_ssid_entities():
                yield entity
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Error during SSID entity discovery: %s", e)

    async def _discover_device_entities(self) -> AsyncIterator[Entity]:
        """Discover entities for wireless devices."""
        if not self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
            return

        devices = self._coordinator.data.get("devices", [])
        if not isinstance(devices, list):
            return

        for device in devices:
            try:
                if not hasattr(device, "product_type"):
                    continue
                if device.product_type == "wireless":
                    # Client Count per AP
                    yield MerakiAPClientCountSensor(
                        self._coordinator, device, self._config_entry
                    )
                    # LED Control
                    if device.management_interface:
                        yield MerakiDeviceLEDSwitch(
                            self._coordinator, device, self._config_entry
                        )
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error(
                    "Error discovering entities for wireless device %s: %s",
                    getattr(device, "serial", "unknown"),
                    e,
                )
                continue

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
                if (
                    not isinstance(ssid, dict)
                    or "networkId" not in ssid
                    or "number" not in ssid
                ):
                    continue

                rf_profile = self._get_rf_profile(ssid)

                yield MerakiSSIDEnabledSwitch(
                    self._coordinator,
                    self._meraki_client,
                    self._config_entry,
                    ssid,
                    rf_profile,
                )
                yield MerakiSSIDBroadcastSwitch(
                    self._coordinator,
                    self._meraki_client,
                    self._config_entry,
                    ssid,
                    rf_profile,
                )
                yield MerakiSSIDNameText(
                    self._coordinator,
                    self._meraki_client,
                    self._config_entry,
                    ssid,
                )
                yield MerakiSSIDClientCountSensor(
                    self._coordinator, self._config_entry, ssid
                )

                if ssid.get("ipAssignmentMode") == "NAT mode":
                    yield MerakiAdultContentFilteringSwitch(
                        self._coordinator,
                        self._config_entry,
                        ssid,
                    )

                # RF Profile Select
                yield MerakiRFProfileSelect(
                    self._coordinator,
                    self._meraki_client,
                    self._config_entry,
                    ssid,
                )
            except MerakiInformationalError as e:
                _LOGGER.info(
                    "Optional feature for SSID %s (network %s) is disabled: %s",
                    ssid.get("name", "unknown"),
                    ssid.get("networkId", "unknown"),
                    e,
                )
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error(
                    "Error discovering entities for SSID %s (network %s): %s",
                    ssid.get("name", "unknown"),
                    ssid.get("networkId", "unknown"),
                    e,
                )
                continue

    def _get_rf_profile(self, ssid: dict[str, Any]) -> dict[str, Any] | None:
        """Find the RF profile for this SSID's network."""
        rf_profiles = (
            self._coordinator.data.get("rf_profiles")
            if self._coordinator.data
            else None
        )
        if isinstance(rf_profiles, dict):
            network_rf_profiles = rf_profiles.get(ssid["networkId"])
            if network_rf_profiles:
                return next(iter(network_rf_profiles), None)
        return None
