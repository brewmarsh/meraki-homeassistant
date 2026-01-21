"""Sensors for detailed Meraki SSID properties."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate
from homeassistant.helpers.entity import EntityCategory

<<<<<<< HEAD
from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDDetailSensor(SensorEntity):
    """Base class for a Meraki SSID detail sensor."""

    _attr_has_entity_name = True
    entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._config_entry = config_entry
        self._ssid_data = ssid_data
        self._rf_profile = rf_profile
        self._attr_device_info = resolve_device_info(
            entity_data={"networkId": self._ssid_data["networkId"]},
            config_entry=self._config_entry,
            ssid_data=self._ssid_data,
        )


class MerakiSSIDWalledGardenSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Walled Garden sensor."""

    _attr_icon = "mdi:wall"

    def __init__(self, *args, **kwargs):
        """Initialize the sensor."""
        super().__init__(*args, **kwargs)
        self._attr_unique_id = (
            f"{self._ssid_data['networkId']}_{self._ssid_data['number']}_walled_garden"
        )
        self._attr_name = "Walled Garden"
        self._attr_native_value = (
            "enabled" if self._ssid_data.get("walledGardenEnabled") else "disabled"
        )
        self._attr_extra_state_attributes = {
            "ranges": self._ssid_data.get("walledGardenRanges", [])
        }


class MerakiSSIDTotalUploadLimitSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Total Upload Limit sensor."""

    _attr_icon = "mdi:upload-network"
    _attr_native_unit_of_measurement = UnitOfDataRate.KILOBITS_PER_SECOND

    def __init__(self, *args, **kwargs):
        """Initialize the sensor."""
        super().__init__(*args, **kwargs)
        self._attr_unique_id = (
            f"{self._ssid_data['networkId']}_{self._ssid_data['number']}_upload_limit"
        )
        self._attr_name = "Total Upload Limit"
        self._attr_native_value = self._ssid_data.get("perSsidBandwidthLimitUp")


class MerakiSSIDTotalDownloadLimitSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Total Download Limit sensor."""

    _attr_icon = "mdi:download-network"
    _attr_native_unit_of_measurement = UnitOfDataRate.KILOBITS_PER_SECOND

    def __init__(self, *args, **kwargs):
        """Initialize the sensor."""
        super().__init__(*args, **kwargs)
        self._attr_unique_id = (
            f"{self._ssid_data['networkId']}_{self._ssid_data['number']}_download_limit"
        )
        self._attr_name = "Total Download Limit"
        self._attr_native_value = self._ssid_data.get("perSsidBandwidthLimitDown")


class MerakiSSIDMandatoryDhcpSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Mandatory DHCP sensor."""

    _attr_icon = "mdi:ip-network"

    def __init__(self, *args, **kwargs):
        """Initialize the sensor."""
        super().__init__(*args, **kwargs)
        self._attr_unique_id = (
            f"{self._ssid_data['networkId']}_{self._ssid_data['number']}_mandatory_dhcp"
        )
        self._attr_name = "Mandatory DHCP"
        self._attr_native_value = (
            "enabled" if self._ssid_data.get("mandatoryDhcpEnabled") else "disabled"
        )


class MerakiSSIDMinBitrate24GhzSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID 2.4GHz Minimum Bitrate sensor."""

    _attr_icon = "mdi:speedometer-slow"
    _attr_native_unit_of_measurement = UnitOfDataRate.MEGABITS_PER_SECOND

    def __init__(self, *args, **kwargs):
        """Initialize the sensor."""
        super().__init__(*args, **kwargs)
        self._attr_unique_id = (
            f"{self._ssid_data['networkId']}_{self._ssid_data['number']}_min_bitrate_24"
        )
        self._attr_name = "Minimum Bitrate 2.4GHz"
        if self._rf_profile and self._rf_profile.get("twoFourGhzSettings"):
            self._attr_native_value = self._rf_profile["twoFourGhzSettings"].get(
                "minBitrate"
            )
        else:
            self._attr_native_value = None


class MerakiSSIDMinBitrate5GhzSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID 5GHz Minimum Bitrate sensor."""

    _attr_icon = "mdi:speedometer"
    _attr_native_unit_of_measurement = UnitOfDataRate.MEGABITS_PER_SECOND

    def __init__(self, *args, **kwargs):
        """Initialize the sensor."""
        super().__init__(*args, **kwargs)
        self._attr_unique_id = (
            f"{self._ssid_data['networkId']}_{self._ssid_data['number']}_min_bitrate_5"
        )
        self._attr_name = "Minimum Bitrate 5GHz"
        if self._rf_profile and self._rf_profile.get("fiveGhzSettings"):
            self._attr_native_value = self._rf_profile["fiveGhzSettings"].get(
                "minBitrate"
            )
        else:
            self._attr_native_value = None
