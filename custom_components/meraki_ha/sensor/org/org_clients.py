"""Sensor entities for Meraki organization-level client counts."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.coordinators.device import MerakiDeviceCoordinator
from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationSSIDClientsSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki Organization SSID Clients sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"
    _attr_icon = "mdi:wifi"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        org_id: str,
        org_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._org_id = org_id
        self._org_name = org_name

        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{org_name} SSID Clients", "sensor", name_format, apply_format=False
        )
        self._attr_unique_id = f"{org_id}_clients_ssid"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, org_id)})

        # Initialize value from coordinator data if available
        self._update_internal_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the sensor."""
        if self.coordinator.data:
            self._attr_native_value = self.coordinator.data.get("clients_on_ssids", 0)
        else:
            self._attr_native_value = 0
        # _LOGGER.debug(
        #   "Sensor '%s': Updated value to %s from coordinator key 'clients_on_ssids'. Coordinator data present: %s",
        #   self.name,
        #   self._attr_native_value,
        #   bool(self.coordinator.data)
        # ) # Removed


class MerakiOrganizationWirelessClientsSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki Organization Wireless Clients sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"
    _attr_icon = "mdi:access-point-network"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        org_id: str,
        org_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._org_id = org_id
        self._org_name = org_name

        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{org_name} Wireless Clients", "sensor", name_format, apply_format=False
        )
        self._attr_unique_id = f"{org_id}_clients_wireless"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, org_id)})

        self._update_internal_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the sensor."""
        if self.coordinator.data:
            self._attr_native_value = self.coordinator.data.get(
                "clients_on_wireless", 0
            )
        else:
            self._attr_native_value = 0
        # _LOGGER.debug(
        #   "Sensor '%s': Updated value to %s from coordinator key 'clients_on_wireless'. Coordinator data present: %s",
        #   self.name,
        #   self._attr_native_value,
        #   bool(self.coordinator.data)
        # ) # Removed


class MerakiOrganizationApplianceClientsSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki Organization Appliance Clients sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"
    _attr_icon = "mdi:server-network"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        org_id: str,
        org_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._org_id = org_id
        self._org_name = org_name

        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{org_name} Appliance Clients", "sensor", name_format, apply_format=False
        )
        self._attr_unique_id = f"{org_id}_clients_appliance"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, org_id)})

        self._update_internal_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the sensor."""
        if self.coordinator.data:
            self._attr_native_value = self.coordinator.data.get(
                "clients_on_appliances", 0
            )
        else:
            self._attr_native_value = 0
        # _LOGGER.debug(
        #   "Sensor '%s': Updated value to %s from coordinator key 'clients_on_appliances'. Coordinator data present: %s",
        #   self.name,
        #   self._attr_native_value,
        #   bool(self.coordinator.data)
        # ) # Removed
