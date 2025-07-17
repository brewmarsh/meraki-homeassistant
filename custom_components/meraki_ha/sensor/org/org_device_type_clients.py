import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_hacoordinators import MerakiDataUpdateCoordinator # Correct coordinator
from custom_components.meraki_haconst import DOMAIN # CONF_MERAKI_ORG_ID removed as it's not used directly for device ID key, DOMAIN is sufficient with org_id value

_LOGGER = logging.getLogger(__name__)

class MerakiOrgDeviceTypeClientsSensor(CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity):
    """Representation of a Meraki Organization Device Type Clients sensor.

    This sensor displays client counts categorized by network device types
    (SSID, Appliance, Wireless) for the entire Meraki organization.
    """

    _attr_icon = "mdi:account-group"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "clients"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        organization_id: str,
        organization_name: str,
    ) -> None:
        """Initialize the Meraki Organization Device Type Clients sensor.

        Args:
            coordinator: The data update coordinator.
            organization_id: The ID of the Meraki organization.
            organization_name: The name of the Meraki organization.
        """
        super().__init__(coordinator)
        self._organization_id = organization_id
        self._organization_name = organization_name

        self._attr_name = f"{self._organization_name} Client Types"
        self._attr_unique_id = f"meraki_org_{self._organization_id}_client_types"

        self._clients_on_ssids: Optional[int] = None
        self._clients_on_appliances: Optional[int] = None
        self._clients_on_wireless: Optional[int] = None

        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data."""
        if self.coordinator.data:
            # Data comes directly from the coordinator's root
            self._clients_on_ssids = self.coordinator.data.get("clients_on_ssids", 0)
            self._clients_on_appliances = self.coordinator.data.get("clients_on_appliances", 0)
            self._clients_on_wireless = self.coordinator.data.get("clients_on_wireless", 0)

            # Main state is the sum of these counts
            self._attr_native_value = (self._clients_on_ssids or 0) + \
                                      (self._clients_on_appliances or 0) + \
                                      (self._clients_on_wireless or 0)

            # _LOGGER.debug(
            #     "Sensor %s: SSID Clients: %s, Appliance Clients: %s, Wireless Clients: %s, Total State: %s",
            #     self.unique_id,
            #     self._clients_on_ssids,
            #     self._clients_on_appliances,
            #     self._clients_on_wireless,
            #     self._attr_native_value
            # ) # Removed
        else:
            # _LOGGER.debug(
            #     "Coordinator data not available for sensor %s. Setting states to 0.",
            #     self.unique_id
            # ) # Removed
            self._clients_on_ssids = 0
            self._clients_on_appliances = 0
            self._clients_on_wireless = 0
            self._attr_native_value = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the Meraki Organization."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._organization_id)}
            # The name, manufacturer, and model attributes should be inherited from the
            # device entry created by MerakiDataUpdateCoordinator.
            # Providing them here again, especially if the 'name' differs from the
            # original registration, can lead to unexpected updates or conflicts.
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes for the sensor."""
        attrs: Dict[str, Any] = {
            "organization_id": self._organization_id,
            "clients_on_ssids": self._clients_on_ssids,
            "clients_on_appliances": self._clients_on_appliances,
            "clients_on_wireless": self._clients_on_wireless,
        }
        return {k: v for k, v in attrs.items() if v is not None}
