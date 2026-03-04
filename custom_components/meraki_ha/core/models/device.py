"""Device models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .appliance import ApplianceMixin
from .base import MerakiBaseDevice
from .camera import CameraMixin
from .sensor import SensorMixin
from .switch import SwitchMixin
from .wireless import WirelessMixin


@dataclass(kw_only=True)
class MerakiDevice(
    MerakiBaseDevice,
    ApplianceMixin,
    CameraMixin,
    SensorMixin,
    SwitchMixin,
    WirelessMixin,
):
    """Dataclass for a Meraki device (aggregate)."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = self.base_to_dict()
        data.update(self.appliance_to_dict())
        data.update(self.camera_to_dict())
        data.update(self.switch_to_dict())
        data.update(self.wireless_to_dict())
        data.update(self.sensor_to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiDevice:
        """Create a MerakiDevice instance from a dictionary."""
        kwargs = cls.base_from_dict(data)
        kwargs.update(ApplianceMixin.appliance_from_dict(data))
        kwargs.update(CameraMixin.camera_from_dict(data))
        kwargs.update(SwitchMixin.switch_from_dict(data))
        kwargs.update(WirelessMixin.wireless_from_dict(data))
        kwargs.update(SensorMixin.sensor_from_dict(data))
        return cls(**kwargs)
