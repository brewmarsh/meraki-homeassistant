from enum import Enum


class SensorStateClass(Enum):
    MEASUREMENT = "measurement"


class SensorEntity:
    def __init__(self):
        self._attr_unique_id = None
        self._attr_native_value = None
        self.extra_state_attributes = {}

    @property
    def unique_id(self):
        return getattr(self, "_attr_unique_id", None)

    @property
    def native_value(self):
        return getattr(self, "_attr_native_value", None)

    @property
    def name(self):
        return getattr(self, "_attr_name", None)
