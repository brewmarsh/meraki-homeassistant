"""Sensor models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import MerakiBaseDevice


@dataclass(kw_only=True)
class SensorMixin:
    """Mixin for Meraki Sensor specific fields."""

    sensor_relationships: list[dict[str, Any]] = field(default_factory=list)
    readings: list[dict[str, Any]] = field(default_factory=list)
    ambient_noise: float | None = None
    pm25: float | None = None
    real_power: float | None = None
    power_factor: float | None = None
    current: float | None = None
    voltage: float | None = None
    door_open: bool | None = None
    water_present: bool | None = None
    button_press: dict[str, Any] | None = None
    frequency: float | None = None
    energy: float | None = None
    outlet_status: bool | None = None

    def sensor_to_dict(self) -> dict[str, Any]:
        """Convert sensor fields to dictionary."""
        return {
            "sensorRelationships": self.sensor_relationships,
            "readings": self.readings,
            "outletStatus": self.outlet_status,
            "ambientNoise": self.ambient_noise,
            "pm25": self.pm25,
            "realPower": self.real_power,
            "powerFactor": self.power_factor,
            "current": self.current,
            "voltage": self.voltage,
            "door_open": self.door_open,
            "water_present": self.water_present,
            "button_press": self.button_press,
            "frequency": self.frequency,
            "energy": self.energy,
        }

    @staticmethod
    def sensor_from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Parse sensor fields from dictionary."""
        return {
            "sensor_relationships": data.get("sensorRelationships", []),
            "readings": data.get("readings", []),
            "outlet_status": data.get("outletStatus"),
            "ambient_noise": data.get("ambientNoise"),
            "pm25": data.get("pm25"),
            "real_power": data.get("realPower"),
            "power_factor": data.get("powerFactor"),
            "current": data.get("current"),
            "voltage": data.get("voltage"),
            "door_open": data.get("doorOpen"),
            "water_present": data.get("waterPresent"),
            "button_press": data.get("buttonPress"),
            "frequency": data.get("frequency"),
            "energy": data.get("energy"),
        }


@dataclass(kw_only=True)
class MerakiSensorDevice(MerakiBaseDevice, SensorMixin):
    """Dataclass for a Meraki Sensor."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = self.base_to_dict()
        data.update(self.sensor_to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiSensorDevice:
        """Create a MerakiSensorDevice from a dictionary."""
        kwargs = cls.base_from_dict(data)
        kwargs.update(cls.sensor_from_dict(data))
        return cls(**kwargs)
