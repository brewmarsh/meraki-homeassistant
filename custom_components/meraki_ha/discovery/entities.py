"""Discovery entities for Meraki devices."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ..binary_sensor.device.meraki_mt_binary_base import MerakiMtBinarySensor
from ..descriptions import (
    MT_BATTERY_DESCRIPTION,
    MT_BUTTON_DESCRIPTION,
    MT_CO2_DESCRIPTION,
    MT_DOOR_DESCRIPTION,
    MT_HUMIDITY_DESCRIPTION,
    MT_NOISE_DESCRIPTION,
    MT_PM25_DESCRIPTION,
    MT_SIGNAL_STRENGTH_DESCRIPTION,
    MT_TEMPERATURE_DESCRIPTION,
    MT_TVOC_DESCRIPTION,
    MT_WATER_DESCRIPTION,
)
from ..sensor.device.meraki_mt_base import MerakiMtSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from ..coordinators import MerakiMainCoordinator
    from ..core.models.device import MerakiDevice


class MerakiTemperatureSensor(MerakiMtSensor):
    """Temperature sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_TEMPERATURE_DESCRIPTION)


class MerakiHumiditySensor(MerakiMtSensor):
    """Humidity sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_HUMIDITY_DESCRIPTION)


class MerakiBatterySensor(MerakiMtSensor):
    """Battery sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_BATTERY_DESCRIPTION)


class MerakiSignalStrengthSensor(MerakiMtSensor):
    """Signal strength sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_SIGNAL_STRENGTH_DESCRIPTION)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        model_str = (
            self._device.get("model", "")
            if isinstance(self._device, dict)
            else getattr(self._device, "model", "")
        ) or ""
        if model_str.startswith("MT"):
            return None
        return cast(float | None, self._attr_native_value)


class MerakiCO2Sensor(MerakiMtSensor):
    """CO2 sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_CO2_DESCRIPTION)


class MerakiButtonPressSensor(MerakiMtSensor):
    """Button press sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_BUTTON_DESCRIPTION)


class MerakiWaterSensor(MerakiMtBinarySensor):
    """Water leak sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_WATER_DESCRIPTION)


class MerakiDoorSensor(MerakiMtBinarySensor):
    """Door sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_DOOR_DESCRIPTION)


class MerakiTVOCSensor(MerakiMtSensor):
    """TVOC sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_TVOC_DESCRIPTION)


class MerakiPM25Sensor(MerakiMtSensor):
    """PM2.5 sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_PM25_DESCRIPTION)


class MerakiNoiseSensor(MerakiMtSensor):
    """Noise sensor."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_NOISE_DESCRIPTION)
