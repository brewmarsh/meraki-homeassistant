"""Factory for creating SSID-related sensor entities."""

import logging
from typing import Any, Dict, List
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator

# Import the specific sensor classes
from .ssid_availability import MerakiSSIDAvailabilitySensor
from .ssid_channel import MerakiSSIDChannelSensor
from .ssid_client_count import MerakiSSIDClientCountSensor
from .ssid_splash_page import MerakiSSIDSplashPageSensor
from .ssid_auth_mode import MerakiSSIDAuthModeSensor
from .ssid_encryption_mode import MerakiSSIDEncryptionModeSensor
from .ssid_wpa_encryption_mode import MerakiSSIDWPAEncryptionModeSensor
from .ssid_ip_assignment_mode import MerakiSSIDIPAssignmentModeSensor
from .ssid_band_selection import MerakiSSIDBandSelectionSensor
from .ssid_per_client_bandwidth_limit import MerakiSSIDPerClientBandwidthLimitSensor
from .ssid_per_ssid_bandwidth_limit import MerakiSSIDPerSsidBandwidthLimitSensor
from .ssid_visible import MerakiSSIDVisibleSensor
from .ssid_details import (
    MerakiSSIDWalledGardenSensor,
    MerakiSSIDTotalUploadLimitSensor,
    MerakiSSIDTotalDownloadLimitSensor,
    MerakiSSIDMandatoryDhcpSensor,
    MerakiSSIDMinBitrate24GhzSensor,
    MerakiSSIDMinBitrate5GhzSensor,
)

_LOGGER = logging.getLogger(__name__)


def create_ssid_sensors(
    coordinator: MerakiDataCoordinator,
    config_entry: ConfigEntry,
    ssid_data: Dict[str, Any],
) -> List[SensorEntity]:
    """Create and return a list of sensor entities for a given SSID."""
    _LOGGER.debug("Creating SSID sensors for SSID: %s", ssid_data.get("name"))
    # Find the RF profile for this SSID's network
    rf_profile = None
    if coordinator.data and coordinator.data.get("rf_profiles"):
        network_rf_profiles = coordinator.data["rf_profiles"].get(
            ssid_data["networkId"]
        )
        if network_rf_profiles:
            # This logic assumes the first profile is the one applied.
            # A more robust implementation might need to match the profile name
            # if that information becomes available on the SSID object.
            rf_profile = next(iter(network_rf_profiles), None)

    sensors: List[SensorEntity] = [
        MerakiSSIDAvailabilitySensor(coordinator, config_entry, ssid_data),
        MerakiSSIDChannelSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDClientCountSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDSplashPageSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDAuthModeSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDEncryptionModeSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDWPAEncryptionModeSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDIPAssignmentModeSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDBandSelectionSensor(coordinator, config_entry, ssid_data),
        MerakiSSIDPerClientBandwidthLimitSensor(
            coordinator, config_entry, ssid_data, "up"
        ),
        MerakiSSIDPerClientBandwidthLimitSensor(
            coordinator, config_entry, ssid_data, "down"
        ),
        MerakiSSIDPerSsidBandwidthLimitSensor(
            coordinator, config_entry, ssid_data, "up"
        ),
        MerakiSSIDPerSsidBandwidthLimitSensor(
            coordinator, config_entry, ssid_data, "down"
        ),
        MerakiSSIDVisibleSensor(coordinator, config_entry, ssid_data),
        # Add the new detail sensors
        MerakiSSIDWalledGardenSensor(coordinator, config_entry, ssid_data, rf_profile),
        MerakiSSIDTotalUploadLimitSensor(
            coordinator, config_entry, ssid_data, rf_profile
        ),
        MerakiSSIDTotalDownloadLimitSensor(
            coordinator, config_entry, ssid_data, rf_profile
        ),
        MerakiSSIDMandatoryDhcpSensor(coordinator, config_entry, ssid_data, rf_profile),
        MerakiSSIDMinBitrate24GhzSensor(
            coordinator, config_entry, ssid_data, rf_profile
        ),
        MerakiSSIDMinBitrate5GhzSensor(
            coordinator, config_entry, ssid_data, rf_profile
        ),
    ]
    return sensors
