"""Sensor entities for Meraki organization-level client counts."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name, format_entity_name
=======
from ...core.utils.naming_utils import format_device_name
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationSSIDClientsSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Representation of a Meraki Organization SSID Clients sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"
    _attr_icon = "mdi:wifi"

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        org_id: str,
        org_name: str,
    ) -> None:
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            org_id: The organization ID.
            org_name: The organization name.

        """
        super().__init__(coordinator)
        self._org_id = org_id
        self._org_name = org_name

        self._attr_name = format_entity_name(org_name, "SSID Clients")
        self._attr_unique_id = f"{org_id}_clients_ssid"

        org_device_data = {"name": org_name, "productType": "organization"}
        formatted_name = format_device_name(
            device=org_device_data,
            config=self.coordinator.config_entry.options,
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, org_id)},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Organization",
        )

        # Initialize value from coordinator data if available
        self._update_internal_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the sensor."""
        self._attr_native_value = (
            self.coordinator.data.get("clients_on_ssids", 0)
            if self.coordinator.data
            else 0
        )


class MerakiOrganizationWirelessClientsSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Representation of a Meraki Organization Wireless Clients sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"
    _attr_icon = "mdi:access-point-network"

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        org_id: str,
        org_name: str,
    ) -> None:
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            org_id: The organization ID.
            org_name: The organization name.

        """
        super().__init__(coordinator)
        self._org_id = org_id
        self._org_name = org_name

        self._attr_name = format_entity_name(org_name, "Wireless Clients")
        self._attr_unique_id = f"{org_id}_clients_wireless"

        org_device_data = {"name": org_name, "productType": "organization"}
        formatted_name = format_device_name(
            device=org_device_data,
            config=self.coordinator.config_entry.options,
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, org_id)},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Organization",
        )

        self._update_internal_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the sensor."""
        self._attr_native_value = (
            self.coordinator.data.get("clients_on_wireless", 0)
            if self.coordinator.data
            else 0
        )


class MerakiOrganizationApplianceClientsSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Representation of a Meraki Organization Appliance Clients sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"
    _attr_icon = "mdi:server-network"

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        org_id: str,
        org_name: str,
    ) -> None:
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            org_id: The organization ID.
            org_name: The organization name.

        """
        super().__init__(coordinator)
        self._org_id = org_id
        self._org_name = org_name

        self._attr_name = format_entity_name(org_name, "Appliance Clients")
        self._attr_unique_id = f"{org_id}_clients_appliance"

        org_device_data = {"name": org_name, "productType": "organization"}
        formatted_name = format_device_name(
            device=org_device_data,
            config=self.coordinator.config_entry.options,
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, org_id)},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Organization",
        )

        self._update_internal_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the sensor."""
        self._attr_native_value = (
            self.coordinator.data.get("clients_on_appliances", 0)
            if self.coordinator.data
            else 0
        )
