"""Parsers for Meraki sensor data."""

from __future__ import annotations

import logging
from typing import Any

from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


def parse_sensor_data(
    devices: list[MerakiDevice],
    sensor_readings: list[dict[str, Any]] | None,
    battery_readings: list[dict[str, Any]] | None,
) -> None:
    """
    Parse and merge sensor and battery readings into the device list.

    Args:
        devices: A list of Meraki devices.
        sensor_readings: A list of sensor readings from the API.
        battery_readings: A list of battery readings from the API.
    """
    if not sensor_readings:
        sensor_readings = []
    if not battery_readings:
        battery_readings = []

    readings_by_serial = {
        reading["serial"]: reading.get("readings", [])
        for reading in sensor_readings
        if isinstance(reading, dict) and "serial" in reading
    }

    battery_readings_by_serial = {
        reading["serial"]: reading.get("readings", [])
        for reading in battery_readings
        if isinstance(reading, dict) and "serial" in reading
    }

    for device in devices:
        device_serial = device.serial
        device_readings = readings_by_serial.get(device_serial, [])

        if battery_readings_for_device := battery_readings_by_serial.get(device_serial):
            existing_metrics = {r["metric"] for r in device_readings}
            for reading in battery_readings_for_device:
                if reading.get("metric") not in existing_metrics:
                    device_readings.append(reading)

        if device_readings:
            device.readings = device_readings

            for reading in device_readings:
                metric = reading.get("metric")
                if metric == "noise":
                    device.ambient_noise = (
                        reading.get("noise", {}).get("ambient", {}).get("level")
                    )
                elif metric == "pm25":
                    device.pm25 = reading.get("pm25", {}).get("concentration")
                elif metric == "power":
                    device.real_power = reading.get("power", {}).get("draw")
                elif metric == "power_factor":
                    device.power_factor = reading.get("power_factor", {}).get("factor")
                elif metric == "current":
                    device.current = reading.get("current", {}).get("draw")
                elif metric == "voltage":
                    device.voltage = reading.get("voltage", {}).get("level")
                elif metric == "door":
                    device.door_open = reading.get("door", {}).get("open")
