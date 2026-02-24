"""Sensors for detailed Meraki SSID properties."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory

from ...coordinator import MerakiDataUpdateCoordinator
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDDetailSensor(MerakiEntity, SensorEntity):
    """Base class for a Meraki SSID detail sensor."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

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
        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        self._rf_profile = rf_profile
        self._attr_device_info = resolve_device_info(
            entity_data={"networkId": self._network_id},
            config_entry=self._config_entry,
            ssid_data=self._ssid_data,
        )

        # Rule 1: Use explicit naming to include SSID name for unique identification
        self._attr_name = f"{ssid_data['name']} {self.entity_description.name}"

        # Rule 2: Robust unique_id format (serial_classname_key)
        # For SSID-bound entities, we use network_id and ssid_number as the
        # unique identifier
        self._attr_unique_id = (
            f"{self._network_id}_{self._ssid_number}_{self.entity_description.key}"
        )

        self._update_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self.coordinator.data:
            return

        network_id = self._network_id
        ssid_number = self._ssid_number

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

    entity_description = SensorEntityDescription(
        key="walled_garden",
        name="walled garden",
        icon="mdi:wall",
    )

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

    entity_description = SensorEntityDescription(
        key="total_upload_limit",
        name="total upload limit",
        icon="mdi:upload-network",
        native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
    )

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        self._attr_native_value = self._ssid_data.get("perSsidBandwidthLimitUp")


class MerakiSSIDTotalDownloadLimitSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Total Download Limit sensor."""

    entity_description = SensorEntityDescription(
        key="total_download_limit",
        name="total download limit",
        icon="mdi:download-network",
        native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
    )

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        self._attr_native_value = self._ssid_data.get("perSsidBandwidthLimitDown")


class MerakiSSIDMandatoryDhcpSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID Mandatory DHCP sensor."""

    entity_description = SensorEntityDescription(
        key="mandatory_dhcp",
        name="mandatory DHCP",
        icon="mdi:ip-network",
    )

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        self._attr_native_value = (
            "enabled" if self._ssid_data.get("mandatoryDhcpEnabled") else "disabled"
        )


class MerakiSSIDMinBitrate24GhzSensor(MerakiSSIDDetailSensor):
    """Representation of an SSID 2.4GHz Minimum Bitrate sensor."""

    entity_description = SensorEntityDescription(
        key="min_bitrate_24",
        name="minimum bitrate 2.4GHz",
        icon="mdi:speedometer-slow",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
    )

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

    entity_description = SensorEntityDescription(
        key="min_bitrate_5",
        name="minimum bitrate 5GHz",
        icon="mdi:speedometer",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
    )

    def _update_state(self) -> None:
        """Update the sensor state from current data."""
        if self._rf_profile and self._rf_profile.get("fiveGhzSettings"):
            self._attr_native_value = self._rf_profile["fiveGhzSettings"].get(
                "minBitrate"
            )
        else:
            self._attr_native_value = None
