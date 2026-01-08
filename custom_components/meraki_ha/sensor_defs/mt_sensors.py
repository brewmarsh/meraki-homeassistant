"""Sensor entity descriptions for Meraki MT sensors."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
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
    name="Temperature",
    device_class=SensorDeviceClass.TEMPERATURE,
    state_class=SensorStateClass.MEASUREMENT,
    # Unit is set dynamically based on user preference - defaults to Celsius
    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
)

MT_INDOOR_AIR_QUALITY_DESCRIPTION = SensorEntityDescription(
    key="indoorAirQuality",
    name="Indoor Air Quality",
    device_class=SensorDeviceClass.AQI,
    state_class=SensorStateClass.MEASUREMENT,
    icon="mdi:air-filter",
)

MT_HUMIDITY_DESCRIPTION = SensorEntityDescription(
    key="humidity",
    name="Humidity",
    device_class=SensorDeviceClass.HUMIDITY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=PERCENTAGE,
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
    key="realPower",  # API uses realPower, not power
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

MT_BATTERY_DESCRIPTION = SensorEntityDescription(
    key="battery",
    name="Battery",
    device_class=SensorDeviceClass.BATTERY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=PERCENTAGE,
)

MT_BUTTON_DESCRIPTION = SensorEntityDescription(
    key="button",
    name="Last Button Press",
    icon="mdi:gesture-tap-button",
    # No device class for enum/string
)

# Binary Sensors
MT_WATER_DESCRIPTION = BinarySensorEntityDescription(
    key="water",
    name="Water Leak",
    device_class=BinarySensorDeviceClass.MOISTURE,
)

MT_DOOR_DESCRIPTION = BinarySensorEntityDescription(
    key="door",
    name="Door",
    device_class=BinarySensorDeviceClass.DOOR,
)

# Mapping of MT models to their supported sensor descriptions
MT_SENSOR_MODELS: dict[str, list[SensorEntityDescription]] = {
    "MT10": [
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_BATTERY_DESCRIPTION,
    ],
    "MT11": [MT_TEMPERATURE_DESCRIPTION, MT_BATTERY_DESCRIPTION],
    "MT12": [MT_TEMPERATURE_DESCRIPTION, MT_BATTERY_DESCRIPTION],
    "MT14": [
        MT_PM25_DESCRIPTION,
        MT_TVOC_DESCRIPTION,
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_NOISE_DESCRIPTION,
        MT_BATTERY_DESCRIPTION,
    ],
    "MT15": [
        MT_INDOOR_AIR_QUALITY_DESCRIPTION,
        MT_CO2_DESCRIPTION,
        MT_TVOC_DESCRIPTION,
        MT_PM25_DESCRIPTION,
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_NOISE_DESCRIPTION,
    ],
    "MT20": [
        MT_TEMPERATURE_DESCRIPTION,
        MT_HUMIDITY_DESCRIPTION,
        MT_BATTERY_DESCRIPTION,
    ],
    "MT30": [MT_BATTERY_DESCRIPTION, MT_BUTTON_DESCRIPTION],
    "MT40": [
        MT_POWER_DESCRIPTION,
        MT_VOLTAGE_DESCRIPTION,
        MT_CURRENT_DESCRIPTION,
    ],
}

# Mapping of MT models to their supported binary sensor descriptions
MT_BINARY_SENSOR_MODELS: dict[str, list[BinarySensorEntityDescription]] = {
    "MT10": [],
    "MT11": [],
    "MT12": [MT_WATER_DESCRIPTION],
    "MT14": [],
    "MT15": [],
    "MT20": [MT_DOOR_DESCRIPTION],
    "MT30": [],
    "MT40": [],
}
