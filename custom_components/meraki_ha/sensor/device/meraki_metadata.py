"""Sensor entities for displaying Meraki device metadata."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiMetadataSensor(CoordinatorEntity, SensorEntity):
    """Base class for Meraki metadata sensors."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
        key: str,
        icon: str | None = None,
    ) -> None:
        """Initialize the metadata sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._key = key
        self._attr_translation_key = f"meraki_{key}"
        self._attr_unique_id = f"{self._device_serial}_{key}"
        self._attr_icon = icon

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
            serial_number=self._device_serial,
            sw_version=device_data.get("firmware"),
        )
        self._update_state()

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        if (current_device_data := self._get_current_device_data()) is not None:
            self._attr_native_value = current_device_data.get(self._key)
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self._get_current_device_data() is not None


class MerakiSerialNumberSensor(MerakiMetadataSensor):
    """Sensor for Meraki device serial number."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_data,
            config_entry,
            "serial",
            "mdi:barcode",
        )


class MerakiPublicIpSensor(MerakiMetadataSensor):
    """Sensor for Meraki device public IP address."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_data,
            config_entry,
            "publicIp",
            "mdi:ip-network",
        )


class MerakiFirmwareVersionSensor(MerakiMetadataSensor):
    """Sensor for Meraki device firmware version."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_data,
            config_entry,
            "firmware",
            "mdi:package-variant",
        )


class MerakiNetworkIdSensor(MerakiMetadataSensor):
    """Sensor for Meraki device network ID."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_data,
            config_entry,
            "networkId",
            "mdi:identifier",
        )


class MerakiMacAddressSensor(MerakiMetadataSensor):
    """Sensor for Meraki device MAC address."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_data,
            config_entry,
            "mac",
            "mdi:network-outline",
        )


class MerakiLanIpSensor(MerakiMetadataSensor):
    """Sensor for Meraki device LAN IP address."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, device_data, config_entry, "lanIp", "mdi:ip"
        )


class MerakiWan1IpSensor(MerakiMetadataSensor):
    """Sensor for Meraki device WAN1 IP address."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, device_data, config_entry, "wan1Ip", "mdi:wan"
        )


class MerakiWan2IpSensor(MerakiMetadataSensor):
    """Sensor for Meraki device WAN2 IP address."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, device_data, config_entry, "wan2Ip", "mdi:wan"
        )


class MerakiProductTypeSensor(MerakiMetadataSensor):
    """Sensor for Meraki device product type."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_data,
            config_entry,
            "productType",
            "mdi:package-variant-closed",
        )


class MerakiModelSensor(MerakiMetadataSensor):
    """Sensor for Meraki device model."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, device_data, config_entry, "model", "mdi:information-outline"
        )


class MerakiTagsSensor(MerakiMetadataSensor):
    """Sensor for Meraki device tags."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, device_data, config_entry, "tags", "mdi:tag-multiple"
        )

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        if (current_device_data := self._get_current_device_data()) is not None:
            tags = current_device_data.get(self._key, [])
            self._attr_native_value = ", ".join(tags) if tags else None
        else:
            self._attr_native_value = None
