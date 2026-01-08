import React, { memo } from 'react';

interface SensorReadingProps {
  type:
    | 'temperature'
    | 'humidity'
    | 'water'
    | 'door'
    | 'tvoc'
    | 'pm25'
    | 'noise'
    | 'battery'
    | 'co2'
    | 'indoorAirQuality';
  value: number;
  unit?: string;
  min?: number;
  max?: number;
  status?: 'normal' | 'warning' | 'critical';
  temperatureUnit?: 'celsius' | 'fahrenheit';
}

const SensorReadingComponent: React.FC<SensorReadingProps> = ({
  type,
  value,
  unit,
  min,
  max,
  status = 'normal',
  temperatureUnit = 'celsius',
}) => {
  const getIcon = (): string => {
    switch (type) {
      case 'temperature':
        return '🌡️';
      case 'humidity':
        return '💧';
      case 'water':
        return '🌊';
      case 'door':
        return '🚪';
      case 'tvoc':
        return '🌬️';
      case 'pm25':
        return '🌫️';
      case 'noise':
        return '🔊';
      case 'battery':
        return '🔋';
      case 'co2':
        return '💨';
      case 'indoorAirQuality':
        return '🍃';
      default:
        return '📊';
    }
  };

  const getLabel = (): string => {
    switch (type) {
      case 'temperature':
        return 'Temperature';
      case 'humidity':
        return 'Humidity';
      case 'water':
        return 'Water Detection';
      case 'door':
        return 'Door Status';
      case 'tvoc':
        return 'TVOC';
      case 'pm25':
        return 'PM2.5';
      case 'noise':
        return 'Noise Level';
      case 'battery':
        return 'Battery';
      case 'co2':
        return 'CO₂';
      case 'indoorAirQuality':
        return 'Air Quality';
      default:
        return type;
    }
  };

  const getDefaultUnit = (): string => {
    switch (type) {
      case 'temperature':
        return temperatureUnit === 'fahrenheit' ? '°F' : '°C';
      case 'humidity':
        return '%';
      case 'tvoc':
        return 'ppb';
      case 'pm25':
        return 'µg/m³';
      case 'noise':
        return 'dB';
      case 'battery':
        return '%';
      case 'co2':
        return 'ppm';
      case 'indoorAirQuality':
        return '';
      default:
        return '';
    }
  };

  // Convert temperature from Celsius to Fahrenheit if needed
  const getDisplayValue = (): number => {
    if (type === 'temperature' && temperatureUnit === 'fahrenheit') {
      return (value * 9) / 5 + 32;
    }
    return value;
  };

  // Get appropriate min/max for gauge based on type and unit
  const getGaugeRange = (): { min: number; max: number } => {
    if (min !== undefined && max !== undefined) {
      // If custom min/max provided, convert for temperature
      if (type === 'temperature' && temperatureUnit === 'fahrenheit') {
        return { min: (min * 9) / 5 + 32, max: (max * 9) / 5 + 32 };
      }
      return { min, max };
    }
    // Default ranges by type
    switch (type) {
      case 'temperature':
        return temperatureUnit === 'fahrenheit'
          ? { min: 32, max: 122 } // 0-50°C in °F
          : { min: 0, max: 50 };
      case 'humidity':
      case 'battery':
        return { min: 0, max: 100 };
      case 'tvoc':
        return { min: 0, max: 1000 };
      case 'pm25':
        return { min: 0, max: 150 };
      case 'noise':
        return { min: 20, max: 100 };
      case 'co2':
        return { min: 400, max: 2000 };
      case 'indoorAirQuality':
        return { min: 0, max: 100 };
      default:
        return { min: 0, max: 100 };
    }
  };

  const getStatusMessage = (): string => {
    switch (status) {
      case 'normal':
        if (type === 'humidity') return 'Optimal humidity';
        if (type === 'indoorAirQuality') return 'Good air quality';
        if (type === 'co2') return 'Normal CO₂';
        return 'Within normal range';
      case 'warning':
        return 'Above threshold';
      case 'critical':
        return 'Critical level!';
      default:
        return '';
    }
  };

  const getGaugePercent = (): number => {
    const range = getGaugeRange();
    const displayVal = getDisplayValue();
    if (range.max === range.min) return 0;
    return Math.min(
      100,
      Math.max(0, ((displayVal - range.min) / (range.max - range.min)) * 100)
    );
  };

  // Get gauge color class based on type
  const getGaugeClass = (): string => {
    switch (type) {
      case 'temperature':
        return 'temp';
      case 'humidity':
        return 'humidity';
      case 'tvoc':
      case 'pm25':
      case 'co2':
      case 'indoorAirQuality':
        return 'air-quality';
      case 'noise':
        return 'noise';
      case 'battery':
        return 'battery';
      default:
        return 'default';
    }
  };

  const displayUnit = unit || getDefaultUnit();
  const gaugePercent = getGaugePercent();
  const displayValue = getDisplayValue();
  const range = getGaugeRange();

  return (
    <div className={`reading-card ${type}`}>
      <div className="icon-wrapper">
        <span className="reading-icon">{getIcon()}</span>
      </div>
      <div className="reading-label">{getLabel()}</div>
      <div className="reading-value">
        {typeof displayValue === 'number'
          ? displayValue.toFixed(1)
          : displayValue}
        <span className="reading-unit">{displayUnit}</span>
      </div>
      <div className="reading-status">
        {status === 'normal' && <span>✅</span>}
        {status === 'warning' && <span>⚠️</span>}
        {status === 'critical' && <span>🚨</span>}
        {getStatusMessage()}
      </div>
      <div className="gauge-wrapper">
        <div
          className={`gauge-fill ${getGaugeClass()}`}
          style={{ width: `${gaugePercent}%` }}
        />
      </div>
      <div className="gauge-labels">
        <span>
          {range.min.toFixed(0)}
          {displayUnit}
        </span>
        <span>
          {((range.max + range.min) / 2).toFixed(0)}
          {displayUnit}
        </span>
        <span>
          {range.max.toFixed(0)}
          {displayUnit}
        </span>
      </div>
    </div>
  );
};

// Memoize SensorReading - re-render only when value or status changes
const SensorReading = memo(SensorReadingComponent);

export default SensorReading;
