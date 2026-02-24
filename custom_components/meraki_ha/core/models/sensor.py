"""Sensor models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(kw_only=True)
class MerakiSensorMixin:
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
