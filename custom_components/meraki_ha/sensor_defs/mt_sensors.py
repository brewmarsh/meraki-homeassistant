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
    UnitOfTemperature,
    UnitOfSoundPressure,
)

# Descriptions for individual sensor metrics
MT_TEMPERATURE_DESCRIPTION = SensorEntityDescription(
    key="temperature",
    name="Temperature",
    device_class=SensorDeviceClass.TEMPERATURE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
)

MT_HUMIDITY_DESCRIPTION = SensorEntityDescription(
    key="humidity",
    name="Humidity",
    device_class=SensorDeviceClass.HUMIDITY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=PERCENTAGE,
)

MT_WATER_DESCRIPTION = SensorEntityDescription(
    key="water",
    name="Water Detection",
    device_class=SensorDeviceClass.MOISTURE,
)

MT_PM25_DESCRIPTION = SensorEntityDescription(
    key="pm25",
    name="PM2.5",
    device_class=SensorDeviceClass.PM25,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

MT_TVOC_DESCRIPTION = SensorEntityDescription(
    key="tvoc",
    name="TVOC",
    device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

MT_CO2_DESCRIPTION = SensorEntityDescription(
    key="co2",
    name="CO2",
    device_class=SensorDeviceClass.CO2,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
)

MT_NOISE_DESCRIPTION = SensorEntityDescription(
    key="noise",
    name="Ambient Noise",
    device_class=SensorDeviceClass.SOUND_PRESSURE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfSoundPressure.WEIGHTED_DECIBEL_A,
)


MT_POWER_DESCRIPTION = SensorEntityDescription(
    key="power",
    name="Power",
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfPower.WATT,
)

MT_VOLTAGE_DESCRIPTION = SensorEntityDescription(
    key="voltage",
    name="Voltage",
    device_class=SensorDeviceClass.VOLTAGE,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfElectricPotential.VOLT,
)

MT_CURRENT_DESCRIPTION = SensorEntityDescription(
    key="current",
    name="Current",
    device_class=SensorDeviceClass.CURRENT,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
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
    "MT40": [
        MT_POWER_DESCRIPTION,
        MT_VOLTAGE_DESCRIPTION,
        MT_CURRENT_DESCRIPTION,
    ],
}
