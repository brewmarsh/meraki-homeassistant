"""
Meraki SSID Handler

This module defines the SSIDHandler class, which is responsible for discovering
virtual devices and entities for each Meraki SSID.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from ....switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)
from ....text.meraki_ssid_name import MerakiSSIDNameText
from .base import BaseDeviceHandler

# Import the specific sensor classes
from ....sensor.network.ssid_availability import MerakiSSIDAvailabilitySensor
from ....sensor.network.ssid_channel import MerakiSSIDChannelSensor
from ....sensor.network.ssid_client_count import MerakiSSIDClientCountSensor
from ....sensor.network.ssid_splash_page import MerakiSSIDSplashPageSensor
from ....sensor.network.ssid_auth_mode import MerakiSSIDAuthModeSensor
from ....sensor.network.ssid_encryption_mode import MerakiSSIDEncryptionModeSensor
from ....sensor.network.ssid_wpa_encryption_mode import MerakiSSIDWPAEncryptionModeSensor
from ....sensor.network.ssid_ip_assignment_mode import MerakiSSIDIPAssignmentModeSensor
from ....sensor.network.ssid_band_selection import MerakiSSIDBandSelectionSensor
from ....sensor.network.ssid_per_client_bandwidth_limit import (
    MerakiSSIDPerClientBandwidthLimitSensor,
)
from ....sensor.network.ssid_per_ssid_bandwidth_limit import (
    MerakiSSIDPerSsidBandwidthLimitSensor,
)
from ....sensor.network.ssid_visible import MerakiSSIDVisibleSensor
from ....sensor.network.ssid_details import (
    MerakiSSIDWalledGardenSensor,
    MerakiSSIDTotalUploadLimitSensor,
    MerakiSSIDTotalDownloadLimitSensor,
    MerakiSSIDMandatoryDhcpSensor,
    MerakiSSIDMinBitrate24GhzSensor,
    MerakiSSIDMinBitrate5GhzSensor,
)


if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....core.api.client import MerakiAPIClient
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator


_LOGGER = logging.getLogger(__name__)


class SSIDHandler(BaseDeviceHandler):
    """Handler for Meraki SSIDs."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        config_entry: "ConfigEntry",
        meraki_client: "MerakiAPIClient",
    ) -> None:
        """Initialize the SSIDHandler."""
        super().__init__(coordinator, None, config_entry, None)
        self._meraki_client = meraki_client

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for all SSIDs."""
        entities: List[Entity] = []
        if not self.coordinator.data or "ssids" not in self.coordinator.data:
            return entities

        for ssid in self.coordinator.data["ssids"]:
            if "networkId" not in ssid or "number" not in ssid:
                continue

            # Find the RF profile for this SSID's network
            rf_profile = None
            if self.coordinator.data and self.coordinator.data.get("rf_profiles"):
                network_rf_profiles = self.coordinator.data["rf_profiles"].get(
                    ssid["networkId"]
                )
                if network_rf_profiles:
                    rf_profile = next(iter(network_rf_profiles), None)

            entities.extend(
                [
                    MerakiSSIDEnabledSwitch(
                        self.coordinator,
                        self._meraki_client,
                        self.config_entry,
                        ssid,
                    ),
                    MerakiSSIDBroadcastSwitch(
                        self.coordinator,
                        self._meraki_client,
                        self.config_entry,
                        ssid,
                    ),
                    MerakiSSIDNameText(
                        self.coordinator,
                        self._meraki_client,
                        self.config_entry,
                        ssid,
                    ),
                    MerakiSSIDAvailabilitySensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDChannelSensor(self.coordinator, self.config_entry, ssid),
                    MerakiSSIDClientCountSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDSplashPageSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDAuthModeSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDEncryptionModeSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDWPAEncryptionModeSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDIPAssignmentModeSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDBandSelectionSensor(
                        self.coordinator, self.config_entry, ssid
                    ),
                    MerakiSSIDPerClientBandwidthLimitSensor(
                        self.coordinator, self.config_entry, ssid, "up"
                    ),
                    MerakiSSIDPerClientBandwidthLimitSensor(
                        self.coordinator, self.config_entry, ssid, "down"
                    ),
                    MerakiSSIDPerSsidBandwidthLimitSensor(
                        self.coordinator, self.config_entry, ssid, "up"
                    ),
                    MerakiSSIDPerSsidBandwidthLimitSensor(
                        self.coordinator, self.config_entry, ssid, "down"
                    ),
                    MerakiSSIDVisibleSensor(self.coordinator, self.config_entry, ssid),
                    MerakiSSIDWalledGardenSensor(
                        self.coordinator, self.config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDTotalUploadLimitSensor(
                        self.coordinator, self.config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDTotalDownloadLimitSensor(
                        self.coordinator, self.config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDMandatoryDhcpSensor(
                        self.coordinator, self.config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDMinBitrate24GhzSensor(
                        self.coordinator, self.config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDMinBitrate5GhzSensor(
                        self.coordinator, self.config_entry, ssid, rf_profile
                    ),
                ]
            )
        return entities
