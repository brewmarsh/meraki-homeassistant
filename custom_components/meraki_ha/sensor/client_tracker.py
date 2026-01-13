"""Sensor entities for tracking Meraki clients."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.utils.naming_utils import format_device_name
=======
<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.utils.naming_utils import format_device_name
=======
from ..core.utils.naming_utils import format_device_name
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)

_LOGGER = logging.getLogger(__name__)

CLIENT_TRACKER_DEVICE_ID = "client_tracker"


class ClientTrackerDeviceSensor(CoordinatorEntity, SensorEntity):
    """A sensor representing the Client Tracker device itself."""

    _attr_has_entity_name = True
    entity_description = SensorEntityDescription(
        key="client_tracker_total",
        name="Tracked Clients",
        icon="mdi:account-group",
    )

    def __init__(
<<<<<<< HEAD
        self, coordinator: MerakiDataUpdateCoordinator, config_entry: ConfigEntry
=======
<<<<<<< HEAD
        self, coordinator: MerakiDataUpdateCoordinator, config_entry: ConfigEntry
=======
        self, coordinator: MerakiDataCoordinator, config_entry: ConfigEntry
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{CLIENT_TRACKER_DEVICE_ID}"

        tracker_device_data = {
            "name": "Client Tracker",
            "productType": "tracker",
        }
        formatted_name = format_device_name(
            device=tracker_device_data,
            config=self._config_entry.options,
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, CLIENT_TRACKER_DEVICE_ID)},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Client Tracker",
        )
        self._update_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the state of the sensor."""
        if self.coordinator.data and self.coordinator.data.get("clients"):
            self._attr_native_value = len(self.coordinator.data["clients"])
        else:
            self._attr_native_value = 0


class MerakiClientSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki client as a sensor."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:lan-connect"

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._client_mac = client_data["mac"]
        self._attr_unique_id = f"client-{self._client_mac}"

        # The entity's name is the client's description or IP
        self._attr_name = client_data.get("description") or client_data.get("ip")

        # All client sensors are part of the single "Client Tracker" device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, CLIENT_TRACKER_DEVICE_ID)},
        )
        self._update_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the state of the sensor."""
        is_online = False
        client_info = {}
        if self.coordinator.data and self.coordinator.data.get("clients"):
            for client in self.coordinator.data["clients"]:
                if client.get("mac") == self._client_mac:
                    is_online = True
                    client_info = client
                    break

        self._attr_native_value = "online" if is_online else "offline"
        self._attr_extra_state_attributes = client_info
        self._attr_icon = "mdi:lan-connect" if is_online else "mdi:lan-disconnect"
