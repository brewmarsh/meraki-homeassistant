"""Parsers for Meraki sensor data."""

from __future__ import annotations

import logging
from typing import Any, Callable

from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


def _handle_noise(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.ambient_noise = reading.get("noise", {}).get("ambient", {}).get("level")


def _handle_pm25(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.pm25 = reading.get("pm25", {}).get("concentration")


def _handle_power(device: MerakiDevice, reading: dict[str, Any]) -> None:
    power_data = reading.get("power", {})
    device.real_power = power_data.get("realPower") or power_data.get("draw")


def _handle_power_factor(device: MerakiDevice, reading: dict[str, Any]) -> None:
    pf_data = reading.get("power_factor") or reading.get("powerFactor")
    if isinstance(pf_data, dict):
        device.power_factor = pf_data.get("factor") or pf_data.get("percentage")


def _handle_frequency(device: MerakiDevice, reading: dict[str, Any]) -> None:
    freq_data = reading.get("frequency")
    if isinstance(freq_data, dict):
        device.frequency = freq_data.get("level")
    elif isinstance(freq_data, (int, float)):
        device.frequency = freq_data


def _handle_energy(device: MerakiDevice, reading: dict[str, Any]) -> None:
    energy_data = reading.get("energy") or reading.get("energyUsage")
    if isinstance(energy_data, dict):
        device.energy = (
            energy_data.get("energyUsage")
            or energy_data.get("draw")
            or energy_data.get("apparentPower")
        )
    elif isinstance(energy_data, (int, float)):
        device.energy = energy_data


def _handle_current(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.current = reading.get("current", {}).get("draw")


def _handle_voltage(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.voltage = reading.get("voltage", {}).get("level")


def _handle_door(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.door_open = reading.get("door", {}).get("open")


def _handle_water(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.water_present = reading.get("water", {}).get("present")


def _handle_button(device: MerakiDevice, reading: dict[str, Any]) -> None:
    device.button_press = reading.get("button")


def _handle_downstream_power(device: MerakiDevice, reading: dict[str, Any]) -> None:
    if "downstreamPower" in reading:
        data = reading.get("downstreamPower")
        if isinstance(data, dict):
            device.outlet_status = data.get("enabled")
    elif "value" in reading:
        device.outlet_status = reading.get("value")


METRIC_HANDLERS: dict[str, Callable[[MerakiDevice, dict[str, Any]], None]] = {
    "noise": _handle_noise,
    "pm25": _handle_pm25,
    "power": _handle_power,
    "power_factor": _handle_power_factor,
    "powerFactor": _handle_power_factor,
    "frequency": _handle_frequency,
    "energy": _handle_energy,
    "energyUsage": _handle_energy,
    "current": _handle_current,
    "voltage": _handle_voltage,
    "door": _handle_door,
    "water": _handle_water,
    "button": _handle_button,
    "downstreamPower": _handle_downstream_power,
    "downstream_power": _handle_downstream_power,
}


def _organize_readings(
    readings: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Organize readings by device serial."""
    return {
        reading["serial"]: reading.get("readings", [])
        for reading in readings
        if isinstance(reading, dict) and "serial" in reading
    }


def _merge_readings(
    sensor_readings: list[dict[str, Any]],
    battery_readings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge sensor and battery readings."""
    if not battery_readings:
        return sensor_readings

    # Use a set for faster lookup of existing metrics
    existing_metrics = {r.get("metric") for r in sensor_readings}
    merged = list(sensor_readings)

    for reading in battery_readings:
        if reading.get("metric") not in existing_metrics:
            merged.append(reading)

    return merged


def _process_device_metrics(
    device: MerakiDevice,
    readings: list[dict[str, Any]],
) -> None:
    """Process metrics for a single device."""
    device.readings = readings
    for reading in readings:
        metric = reading.get("metric")
        if metric == "power":
            _LOGGER.debug("MT40 Power Reading Payload: %s", reading)

        if metric and metric in METRIC_HANDLERS:
            METRIC_HANDLERS[metric](device, reading)


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
    readings_map = _organize_readings(sensor_readings or [])
    battery_map = _organize_readings(battery_readings or [])

    for device in devices:
        if not device.serial:
            continue

        readings = _merge_readings(
            readings_map.get(device.serial, []),
            battery_map.get(device.serial, []),
        )

        if readings:
            _process_device_metrics(device, readings)
