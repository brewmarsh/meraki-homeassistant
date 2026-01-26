"""Sensor entity descriptions for Meraki MT sensors."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
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

# Descriptions for individual sensor metrics
MT_TEMPERATURE_DESCRIPTION = SensorEntityDescription(
    key="temperature",
    translation_key="mt_temperature",
    device_class=SensorDeviceClass.TEMPERATURE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
)

MT_HUMIDITY_DESCRIPTION = SensorEntityDescription(
    key="humidity",
    translation_key="mt_humidity",
    device_class=SensorDeviceClass.HUMIDITY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=PERCENTAGE,
)

MT_WATER_DESCRIPTION = SensorEntityDescription(
    key="water",
    translation_key="mt_water_detection",
    device_class=SensorDeviceClass.MOISTURE,
)

MT_PM25_DESCRIPTION = SensorEntityDescription(
    key="pm25",
    translation_key="mt_pm25",
    device_class=SensorDeviceClass.PM25,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

MT_TVOC_DESCRIPTION = SensorEntityDescription(
    key="tvoc",
    translation_key="mt_tvoc",
    device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

MT_CO2_DESCRIPTION = SensorEntityDescription(
    key="co2",
    translation_key="mt_co2",
    device_class=SensorDeviceClass.CO2,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
)

MT_NOISE_DESCRIPTION = SensorEntityDescription(
    key="noise",
    translation_key="mt_noise",
    device_class=SensorDeviceClass.SOUND_PRESSURE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfSoundPressure.WEIGHTED_DECIBEL_A,
)


MT_POWER_DESCRIPTION = SensorEntityDescription(
    key="power",
    translation_key="mt_power",
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfPower.WATT,
)

MT_VOLTAGE_DESCRIPTION = SensorEntityDescription(
    key="voltage",
    translation_key="mt_voltage",
    device_class=SensorDeviceClass.VOLTAGE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfElectricPotential.VOLT,
)

MT_CURRENT_DESCRIPTION = SensorEntityDescription(
    key="current",
    translation_key="mt_current",
    device_class=SensorDeviceClass.CURRENT,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
)

MT_BATTERY_DESCRIPTION = SensorEntityDescription(
    key="battery",
    translation_key="mt_battery",
    device_class=SensorDeviceClass.BATTERY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=PERCENTAGE,
)


# Mapping of MT models to their supported sensor descriptions
MT_SENSOR_MODELS = {
    "MT10": [
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_BATTERY_DESCRIPTION,
    ],
    "MT11": [MT_TEMPERATURE_DESCRIPTION, MT_BATTERY_DESCRIPTION],
    "MT12": [MT_WATER_DESCRIPTION, MT_BATTERY_DESCRIPTION],
    "MT14": [
        MT_PM25_DESCRIPTION,
        MT_TVOC_DESCRIPTION,
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_BATTERY_DESCRIPTION,
    ],
    "MT15": [
        MT_CO2_DESCRIPTION,
        MT_TVOC_DESCRIPTION,
        MT_PM25_DESCRIPTION,
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_NOISE_DESCRIPTION,
        MT_BATTERY_DESCRIPTION,
    ],
    "MT20": [MT_BATTERY_DESCRIPTION],
    "MT30": [MT_BATTERY_DESCRIPTION],
    "MT40": [
        MT_POWER_DESCRIPTION,
        MT_VOLTAGE_DESCRIPTION,
        MT_CURRENT_DESCRIPTION,
    ],
}
