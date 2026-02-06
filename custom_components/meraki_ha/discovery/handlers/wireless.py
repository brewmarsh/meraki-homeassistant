"""
Meraki Wireless Handler.

This module defines the WirelessHandler class, which is responsible for discovering
entities for Meraki wireless networks and devices.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from ...const_conf import (
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
)
from ...sensor.device.ap_client_count import MerakiAPClientCountSensor
from ...sensor.network.ssid_auth_mode import MerakiSSIDAuthModeSensor

# Import the specific sensor classes
from ...sensor.network.ssid_availability import MerakiSSIDAvailabilitySensor
from ...sensor.network.ssid_band_selection import MerakiSSIDBandSelectionSensor
from ...sensor.network.ssid_client_count import MerakiSSIDClientCountSensor
from ...sensor.network.ssid_details import (
    MerakiSSIDMandatoryDhcpSensor,
    MerakiSSIDMinBitrate5GhzSensor,
    MerakiSSIDMinBitrate24GhzSensor,
    MerakiSSIDTotalDownloadLimitSensor,
    MerakiSSIDTotalUploadLimitSensor,
    MerakiSSIDWalledGardenSensor,
)
from ...sensor.network.ssid_encryption_mode import MerakiSSIDEncryptionModeSensor
from ...sensor.network.ssid_ip_assignment_mode import MerakiSSIDIPAssignmentModeSensor
from ...sensor.network.ssid_per_client_bandwidth_limit import (
    MerakiSSIDPerClientBandwidthLimitSensor,
)
from ...sensor.network.ssid_per_ssid_bandwidth_limit import (
    MerakiSSIDPerSsidBandwidthLimitSensor,
)
from ...sensor.network.ssid_psk import MerakiSSIDPSKSensor
from ...sensor.network.ssid_splash_page import MerakiSSIDSplashPageSensor
from ...sensor.network.ssid_visible import MerakiSSIDVisibleSensor
from ...sensor.network.ssid_wpa_encryption_mode import MerakiSSIDWPAEncryptionModeSensor
from ...switch.adult_content_filtering import MerakiAdultContentFilteringSwitch
from ...switch.meraki_device_led_switch import MerakiDeviceLEDSwitch
from ...text.meraki_ssid_name import MerakiSSIDNameText
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...coordinator import MerakiDataUpdateCoordinator
    from ...core.api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class WirelessHandler(BaseHandler):
    """Handler for Meraki wireless devices and SSIDs."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the WirelessHandler."""
        super().__init__(coordinator, config_entry)
        self._meraki_client = meraki_client

    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover entities for wireless devices and SSIDs."""
        from ...meraki_select.rf_profile import MerakiRFProfileSelect
        from ...switch.meraki_ssid_device_switch import (
            MerakiSSIDBroadcastSwitch,
            MerakiSSIDEnabledSwitch,
        )

        if not self._coordinator.data or "ssids" not in self._coordinator.data:
            return

        # Discover AP Device entities
        if self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
            for device in self._coordinator.data.get("devices", []):
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

        # Check if SSID sensors/entities are enabled
        if not self._config_entry.options.get(CONF_ENABLE_SSID_SENSORS, True):
            return

        for ssid in self._coordinator.data.get("ssids", []):
            if "networkId" not in ssid or "number" not in ssid:
                continue

            # Find the RF profile for this SSID's network
            rf_profile = None
            if self._coordinator.data and self._coordinator.data.get("rf_profiles"):
                network_rf_profiles = self._coordinator.data["rf_profiles"].get(
                    ssid["networkId"]
                )
                if network_rf_profiles:
                    rf_profile = next(iter(network_rf_profiles), None)

            yield MerakiSSIDEnabledSwitch(
                self._coordinator,
                self._meraki_client,
                self._config_entry,
                ssid,
            )
            yield MerakiSSIDBroadcastSwitch(
                self._coordinator,
                self._meraki_client,
                self._config_entry,
                ssid,
            )
            yield MerakiSSIDNameText(
                self._coordinator,
                self._meraki_client,
                self._config_entry,
                ssid,
            )
            yield MerakiSSIDAvailabilitySensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDClientCountSensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDSplashPageSensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDAuthModeSensor(self._coordinator, self._config_entry, ssid)
            yield MerakiSSIDPSKSensor(self._coordinator, self._config_entry, ssid)
            yield MerakiSSIDEncryptionModeSensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDWPAEncryptionModeSensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDIPAssignmentModeSensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDBandSelectionSensor(
                self._coordinator, self._config_entry, ssid
            )
            yield MerakiSSIDPerClientBandwidthLimitSensor(
                self._coordinator, self._config_entry, ssid, "up"
            )
            yield MerakiSSIDPerClientBandwidthLimitSensor(
                self._coordinator, self._config_entry, ssid, "down"
            )
            yield MerakiSSIDPerSsidBandwidthLimitSensor(
                self._coordinator, self._config_entry, ssid, "up"
            )
            yield MerakiSSIDPerSsidBandwidthLimitSensor(
                self._coordinator, self._config_entry, ssid, "down"
            )
            yield MerakiSSIDVisibleSensor(self._coordinator, self._config_entry, ssid)
            yield MerakiSSIDWalledGardenSensor(
                self._coordinator, self._config_entry, ssid, rf_profile
            )
            yield MerakiSSIDTotalUploadLimitSensor(
                self._coordinator, self._config_entry, ssid, rf_profile
            )
            yield MerakiSSIDTotalDownloadLimitSensor(
                self._coordinator, self._config_entry, ssid, rf_profile
            )
            yield MerakiSSIDMandatoryDhcpSensor(
                self._coordinator, self._config_entry, ssid, rf_profile
            )
            yield MerakiSSIDMinBitrate24GhzSensor(
                self._coordinator, self._config_entry, ssid, rf_profile
            )
            yield MerakiSSIDMinBitrate5GhzSensor(
                self._coordinator, self._config_entry, ssid, rf_profile
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
