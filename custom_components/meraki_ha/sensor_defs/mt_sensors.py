"""Sensor entity descriptions for Meraki MT sensors."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfSoundPressure,
    UnitOfTemperature,
)

from ..sensor.device.meraki_mt_base import MTSensorEntityDescription

# Descriptions for individual sensor metrics
MT_TEMPERATURE_DESCRIPTION = MTSensorEntityDescription(
    key="temperature",
    name="Temperature",
    device_class=SensorDeviceClass.TEMPERATURE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    value_key="celsius",
)

MT_HUMIDITY_DESCRIPTION = MTSensorEntityDescription(
    key="humidity",
    name="Humidity",
    device_class=SensorDeviceClass.HUMIDITY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=PERCENTAGE,
    value_key="relativePercentage",
)

MT_WATER_DESCRIPTION = MTSensorEntityDescription(
    key="water",
    name="Water Detection",
    device_class=SensorDeviceClass.MOISTURE,
    value_key="present",
)

MT_PM25_DESCRIPTION = MTSensorEntityDescription(
    key="pm25",
    name="PM2.5",
    device_class=SensorDeviceClass.PM25,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    value_key="concentration",
)

MT_TVOC_DESCRIPTION = MTSensorEntityDescription(
    key="tvoc",
    name="TVOC",
    device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    value_key="concentration",
)

MT_CO2_DESCRIPTION = MTSensorEntityDescription(
    key="co2",
    name="CO2",
    device_class=SensorDeviceClass.CO2,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    value_key="concentration",
)

MT_NOISE_DESCRIPTION = MTSensorEntityDescription(
    key="noise",
    name="Ambient Noise",
    device_class=SensorDeviceClass.SOUND_PRESSURE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfSoundPressure.WEIGHTED_DECIBEL_A,
    value_key="ambient",
)


MT_POWER_DESCRIPTION = MTSensorEntityDescription(
    key="power",
    name="Power",
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfPower.WATT,
    value_key="draw",
)

MT_VOLTAGE_DESCRIPTION = MTSensorEntityDescription(
    key="voltage",
    name="Voltage",
    device_class=SensorDeviceClass.VOLTAGE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    value_key="level",
)

MT_CURRENT_DESCRIPTION = MTSensorEntityDescription(
    key="current",
    name="Current",
    device_class=SensorDeviceClass.CURRENT,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    value_key="draw",
)


# Mapping of MT models to their supported sensor descriptions
MT_SENSOR_MODELS = {
    "MT10": [MT_TEMPERATURE_DESCRIPTION, MT_HUMIDITY_DESCRIPTION],
    "MT11": [MT_TEMPERATURE_DESCRIPTION],  # Assuming MT11 is a temperature sensor
    "MT12": [MT_WATER_DESCRIPTION],
    "MT14": [
        MT_PM25_DESCRIPTION,
        MT_TVOC_DESCRIPTION,
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
    ],
    "MT15": [
        MT_CO2_DESCRIPTION,
        MT_TVOC_DESCRIPTION,
        MT_PM25_DESCRIPTION,
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_NOISE_DESCRIPTION,
    ],
    "MT20": [],  # MT20 is a binary sensor, no standard sensors
    "MT30": [],  # Smart Automation Button, no standard sensors
    "MT40": [
        MT_POWER_DESCRIPTION,
        MT_VOLTAGE_DESCRIPTION,
        MT_CURRENT_DESCRIPTION,
    ],
}
