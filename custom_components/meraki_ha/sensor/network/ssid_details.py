"""Sensors for detailed Meraki SSID properties."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDDetailSensor(CoordinatorEntity, SensorEntity):
    """Base class for a Meraki SSID detail sensor."""

    _attr_has_entity_name = True
    entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid_data = ssid_data
        self._rf_profile = rf_profile
        self._attr_device_info = resolve_device_info(
            entity_data={"networkId": self._ssid_data["networkId"]},
            config_entry=self._config_entry,
            ssid_data=self._ssid_data,
        )
        self._update_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self.coordinator.data:
            return

        network_id = self._ssid_data.get("networkId")
        ssid_number = self._ssid_data.get("number")

        # Update SSID data
        if "wireless_settings" in self.coordinator.data:
            network_ssids = self.coordinator.data["wireless_settings"].get(network_id)
            if network_ssids:
                for ssid in network_ssids:
                    if str(ssid.get("number")) == str(ssid_number):
                        self._ssid_data = ssid
                        break

        # Update RF profile data
        if "rf_profiles" in self.coordinator.data:
            network_rf_profiles = self.coordinator.data["rf_profiles"].get(network_id)
            if network_rf_profiles:
                # Match same logic as discovery: take the first available profile
                self._rf_profile = next(iter(network_rf_profiles), None)

        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the sensor state from current data."""


class MerakiSSIDWalledGardenSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Walled Garden sensor."""

    _attr_icon = "mdi:wall"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = (
            f"{ssid_data['networkId']}_{ssid_data['number']}_walled_garden"
        )
        self._attr_name = "Walled garden"
        super().__init__(coordinator, config_entry, ssid_data, rf_profile)

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
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

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = (
            f"{ssid_data['networkId']}_{ssid_data['number']}_upload_limit"
        )
        self._attr_name = "Total upload limit"
        super().__init__(coordinator, config_entry, ssid_data, rf_profile)

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        self._attr_native_value = self._ssid_data.get("perSsidBandwidthLimitUp")


class MerakiSSIDTotalDownloadLimitSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Total Download Limit sensor."""

    _attr_icon = "mdi:download-network"
    _attr_native_unit_of_measurement = UnitOfDataRate.KILOBITS_PER_SECOND

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = (
            f"{ssid_data['networkId']}_{ssid_data['number']}_download_limit"
        )
        self._attr_name = "Total download limit"
        super().__init__(coordinator, config_entry, ssid_data, rf_profile)

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        self._attr_native_value = self._ssid_data.get("perSsidBandwidthLimitDown")


class MerakiSSIDMandatoryDhcpSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Mandatory DHCP sensor."""

    _attr_icon = "mdi:ip-network"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = (
            f"{ssid_data['networkId']}_{ssid_data['number']}_mandatory_dhcp"
        )
        self._attr_name = "Mandatory DHCP"
        super().__init__(coordinator, config_entry, ssid_data, rf_profile)

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        self._attr_native_value = (
            "enabled" if self._ssid_data.get("mandatoryDhcpEnabled") else "disabled"
        )


class MerakiSSIDMinBitrate24GhzSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID 2.4GHz Minimum Bitrate sensor."""

    _attr_icon = "mdi:speedometer-slow"
    _attr_native_unit_of_measurement = UnitOfDataRate.MEGABITS_PER_SECOND

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = (
            f"{ssid_data['networkId']}_{ssid_data['number']}_min_bitrate_24"
        )
        self._attr_name = "Minimum bitrate 2.4GHz"
        super().__init__(coordinator, config_entry, ssid_data, rf_profile)

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
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

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        rf_profile: dict[str, Any] | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = (
            f"{ssid_data['networkId']}_{ssid_data['number']}_min_bitrate_5"
        )
        self._attr_name = "Minimum bitrate 5GHz"
        super().__init__(coordinator, config_entry, ssid_data, rf_profile)

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        if self._rf_profile and self._rf_profile.get("fiveGhzSettings"):
            self._attr_native_value = self._rf_profile["fiveGhzSettings"].get(
                "minBitrate"
            )
        else:
            self._attr_native_value = None
