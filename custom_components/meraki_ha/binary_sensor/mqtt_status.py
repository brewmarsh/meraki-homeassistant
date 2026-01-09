"""MQTT Status Binary Sensor for Meraki Integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator
    from ..services.mqtt_relay import MqttRelayManager
    from ..services.mqtt_service import MerakiMqttService

_LOGGER = logging.getLogger(__name__)


class MerakiMqttStatusSensor(CoordinatorEntity, BinarySensorEntity):  # type: ignore[type-arg]
    """Binary sensor indicating MQTT service connection status."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True
    _attr_name = "MQTT Status"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        mqtt_service: MerakiMqttService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the MQTT status sensor."""
        super().__init__(coordinator)
        self._mqtt_service = mqtt_service
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_mqtt_status"

    @property
    def is_on(self) -> bool:
        """Return True if MQTT service is running."""
        return self._mqtt_service.is_running

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this sensor."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._config_entry.entry_id}_mqtt")},
            name="Meraki MQTT Service",
            manufacturer="Cisco Meraki",
            model="MQTT Integration",
            via_device=(DOMAIN, self._config_entry.entry_id),
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        stats = self._mqtt_service.get_statistics()
        return {
            "messages_received": stats["messages_received"],
            "messages_processed": stats["messages_processed"],
            "last_message_time": stats["last_message_time"],
            "start_time": stats["start_time"],
            "sensors_mapped": stats["sensors_mapped"],
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


class MerakiMqttRelayStatusSensor(CoordinatorEntity, BinarySensorEntity):  # type: ignore[type-arg]
    """Binary sensor indicating MQTT relay destination connection status."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        relay_manager: MqttRelayManager,
        destination_name: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the MQTT relay status sensor."""
        super().__init__(coordinator)
        self._relay_manager = relay_manager
        self._destination_name = destination_name
        self._config_entry = config_entry
        self._attr_name = f"MQTT Relay: {destination_name}"
        # Sanitize name for unique_id
        safe_name = destination_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{config_entry.entry_id}_mqtt_relay_{safe_name}"

    @property
    def is_on(self) -> bool:
        """Return True if relay destination is connected."""
        for dest in self._relay_manager.destinations:
            if dest.name == self._destination_name:
                return dest.status.value == "connected"
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this sensor."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._config_entry.entry_id}_mqtt")},
            name="Meraki MQTT Service",
            manufacturer="Cisco Meraki",
            model="MQTT Integration",
            via_device=(DOMAIN, self._config_entry.entry_id),
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        for dest in self._relay_manager.destinations:
            if dest.name == self._destination_name:
                return {
                    "host": dest.config.host,
                    "port": dest.config.port,
                    "topic_filter": dest.config.topic_filter,
                    "status": dest.status.value,
                    "messages_relayed": dest.messages_relayed,
                    "last_relay_time": (
                        dest.last_relay_time.isoformat()
                        if dest.last_relay_time
                        else None
                    ),
                    "last_error": dest.last_error,
                    "last_error_time": (
                        dest.last_error_time.isoformat()
                        if dest.last_error_time
                        else None
                    ),
                }
        return {}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


async def async_setup_mqtt_sensors(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
) -> list[BinarySensorEntity]:
    """Set up MQTT status binary sensors."""
    entities: list[BinarySensorEntity] = []

    entry_data = hass.data.get(DOMAIN, {}).get(config_entry.entry_id, {})
    mqtt_service = entry_data.get("mqtt_service")
    relay_manager = entry_data.get("mqtt_relay_manager")

    if mqtt_service is None:
        _LOGGER.debug("MQTT service not configured, skipping MQTT status sensors")
        return entities

    # Add main MQTT status sensor
    entities.append(MerakiMqttStatusSensor(coordinator, mqtt_service, config_entry))

    # Add relay destination sensors
    if relay_manager is not None:
        for dest in relay_manager.destinations:
            entities.append(
                MerakiMqttRelayStatusSensor(
                    coordinator, relay_manager, dest.name, config_entry
                )
            )

    _LOGGER.info("Created %d MQTT status sensors", len(entities))
    return entities
