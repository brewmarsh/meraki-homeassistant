"""
Meraki SSID Handler

This module defines the SSIDHandler class, which is responsible for discovering
virtual devices and entities for each Meraki SSID.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from ...text.meraki_ssid_name import MerakiSSIDNameText
from .base import BaseHandler

# Import the specific sensor classes
from ...sensor.network.ssid_availability import MerakiSSIDAvailabilitySensor
from ...sensor.network.ssid_channel import MerakiSSIDChannelSensor
from ...sensor.network.ssid_client_count import MerakiSSIDClientCountSensor
from ...sensor.network.ssid_splash_page import MerakiSSIDSplashPageSensor
from ...sensor.network.ssid_auth_mode import MerakiSSIDAuthModeSensor
from ...sensor.network.ssid_encryption_mode import MerakiSSIDEncryptionModeSensor
from ...sensor.network.ssid_wpa_encryption_mode import MerakiSSIDWPAEncryptionModeSensor
from ...sensor.network.ssid_ip_assignment_mode import MerakiSSIDIPAssignmentModeSensor
from ...sensor.network.ssid_band_selection import MerakiSSIDBandSelectionSensor
from ...sensor.network.ssid_per_client_bandwidth_limit import (
    MerakiSSIDPerClientBandwidthLimitSensor,
)
from ...sensor.network.ssid_per_ssid_bandwidth_limit import (
    MerakiSSIDPerSsidBandwidthLimitSensor,
)
from ...sensor.network.ssid_visible import MerakiSSIDVisibleSensor
from ...sensor.network.ssid_details import (
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

    from ...core.api.client import MerakiAPIClient
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator


_LOGGER = logging.getLogger(__name__)


class SSIDHandler(BaseHandler):
    """Handler for Meraki SSIDs."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        config_entry: "ConfigEntry",
        meraki_client: "MerakiAPIClient",
    ) -> None:
        """Initialize the SSIDHandler."""
        super().__init__(coordinator, config_entry)
        self._meraki_client = meraki_client

    @classmethod
    def create(
        cls,
        coordinator: "MerakiDataCoordinator",
        config_entry: "ConfigEntry",
        meraki_client: "MerakiAPIClient",
    ) -> "SSIDHandler":
        """Create an instance of the handler."""
        return cls(
            coordinator,
            config_entry,
            meraki_client,
        )

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for all SSIDs."""
        from ...switch.meraki_ssid_device_switch import (
            MerakiSSIDEnabledSwitch,
            MerakiSSIDBroadcastSwitch,
        )

        entities: List[Entity] = []
        if not self._coordinator.data or "ssids" not in self._coordinator.data:
            return entities

        for ssid in self._coordinator.data["ssids"]:
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

            entities.extend(
                [
                    MerakiSSIDEnabledSwitch(
                        self._coordinator,
                        self._meraki_client,
                        self._config_entry,
                        ssid,
                    ),
                    MerakiSSIDBroadcastSwitch(
                        self._coordinator,
                        self._meraki_client,
                        self._config_entry,
                        ssid,
                    ),
                    MerakiSSIDNameText(
                        self._coordinator,
                        self._meraki_client,
                        self._config_entry,
                        ssid,
                    ),
                    MerakiSSIDAvailabilitySensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDChannelSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDClientCountSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDSplashPageSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDAuthModeSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDEncryptionModeSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDWPAEncryptionModeSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDIPAssignmentModeSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDBandSelectionSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDPerClientBandwidthLimitSensor(
                        self._coordinator, self._config_entry, ssid, "up"
                    ),
                    MerakiSSIDPerClientBandwidthLimitSensor(
                        self._coordinator, self._config_entry, ssid, "down"
                    ),
                    MerakiSSIDPerSsidBandwidthLimitSensor(
                        self._coordinator, self._config_entry, ssid, "up"
                    ),
                    MerakiSSIDPerSsidBandwidthLimitSensor(
                        self._coordinator, self._config_entry, ssid, "down"
                    ),
                    MerakiSSIDVisibleSensor(
                        self._coordinator, self._config_entry, ssid
                    ),
                    MerakiSSIDWalledGardenSensor(
                        self._coordinator, self._config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDTotalUploadLimitSensor(
                        self._coordinator, self._config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDTotalDownloadLimitSensor(
                        self._coordinator, self._config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDMandatoryDhcpSensor(
                        self._coordinator, self._config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDMinBitrate24GhzSensor(
                        self._coordinator, self._config_entry, ssid, rf_profile
                    ),
                    MerakiSSIDMinBitrate5GhzSensor(
                        self._coordinator, self._config_entry, ssid, rf_profile
                    ),
                ]
            )
        return entities
