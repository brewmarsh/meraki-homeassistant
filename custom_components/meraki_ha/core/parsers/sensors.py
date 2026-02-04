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
                    power_data = reading.get("power", {})
                    device.real_power = power_data.get("realPower") or power_data.get(
                        "draw"
                    )
                elif metric in ("power_factor", "powerFactor"):
                    pf_data = reading.get("power_factor") or reading.get("powerFactor")
                    if isinstance(pf_data, dict):
                        device.power_factor = pf_data.get("factor") or pf_data.get(
                            "percentage"
                        )
                elif metric == "frequency":
                    freq_data = reading.get("frequency")
                    if isinstance(freq_data, dict):
                        device.frequency = freq_data.get("level")
                    elif isinstance(freq_data, (int, float)):
                        device.frequency = freq_data
                elif metric in ("energy", "energyUsage"):
                    energy_data = reading.get("energy") or reading.get("energyUsage")
                    if isinstance(energy_data, dict):
                        device.energy = (
                            energy_data.get("energyUsage")
                            or energy_data.get("draw")
                            or energy_data.get("apparentPower")
                        )
                    elif isinstance(energy_data, (int, float)):
                        device.energy = energy_data
                elif metric == "current":
                    device.current = reading.get("current", {}).get("draw")
                elif metric == "voltage":
                    device.voltage = reading.get("voltage", {}).get("level")
                elif metric == "door":
                    device.door_open = reading.get("door", {}).get("open")
                elif metric == "water":
                    device.water_present = reading.get("water", {}).get("present")
                elif metric == "button":
                    device.button_press = reading.get("button")
                elif metric in ("downstreamPower", "downstream_power"):
                    if "downstreamPower" in reading:
                        data = reading.get("downstreamPower")
                        if isinstance(data, dict):
                            device.outlet_status = data.get("enabled")
                    elif "value" in reading:
                        device.outlet_status = reading.get("value")
