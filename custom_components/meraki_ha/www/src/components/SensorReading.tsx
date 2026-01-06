import React from 'react';

interface SensorReadingProps {
  type: 'temperature' | 'humidity' | 'water' | 'door' | 'tvoc' | 'pm25' | 'noise' | 'battery';
  value: number;
  unit?: string;
  min?: number;
  max?: number;
  status?: 'normal' | 'warning' | 'critical';
}

const SensorReading: React.FC<SensorReadingProps> = ({
  type,
  value,
  unit,
  min = 0,
  max = 100,
  status = 'normal',
}) => {
  const getIcon = (): string => {
    switch (type) {
      case 'temperature': return '🌡️';
      case 'humidity': return '💧';
      case 'water': return '🌊';
      case 'door': return '🚪';
      case 'tvoc': return '🌬️';
      case 'pm25': return '🌫️';
      case 'noise': return '🔊';
      case 'battery': return '🔋';
      default: return '📊';
    }
  };

  const getLabel = (): string => {
    switch (type) {
      case 'temperature': return 'Temperature';
      case 'humidity': return 'Humidity';
      case 'water': return 'Water Detection';
      case 'door': return 'Door Status';
      case 'tvoc': return 'TVOC';
      case 'pm25': return 'PM2.5';
      case 'noise': return 'Noise Level';
      case 'battery': return 'Battery';
      default: return type;
    }
  };

  const getDefaultUnit = (): string => {
    switch (type) {
      case 'temperature': return '°C';
      case 'humidity': return '%';
      case 'tvoc': return 'ppb';
      case 'pm25': return 'µg/m³';
      case 'noise': return 'dB';
      case 'battery': return '%';
      default: return '';
    }
  };

  const getStatusMessage = (): string => {
    switch (status) {
      case 'normal': 
        return type === 'humidity' ? 'Optimal humidity' : 'Within normal range';
      case 'warning': 
        return 'Above threshold';
      case 'critical': 
        return 'Critical level!';
      default: 
        return '';
    }
  };

  const getGaugePercent = (): number => {
    if (max === min) return 0;
    return Math.min(100, Math.max(0, ((value - min) / (max - min)) * 100));
  };

  const displayUnit = unit || getDefaultUnit();
  const gaugePercent = getGaugePercent();

  return (
    <div className={`reading-card ${type}`}>
      <div className="icon-wrapper">
        <span style={{ fontSize: '36px' }}>{getIcon()}</span>
      </div>
      <div className="reading-label">{getLabel()}</div>
      <div className="reading-value">
        {typeof value === 'number' ? value.toFixed(1) : value}
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
          className={`gauge-fill ${type === 'temperature' ? 'temp' : 'humidity'}`}
          style={{ width: `${gaugePercent}%` }}
        />
      </div>
      <div className="gauge-labels">
        <span>{min}{displayUnit}</span>
        <span>{((max + min) / 2).toFixed(0)}{displayUnit}</span>
        <span>{max}{displayUnit}</span>
      </div>
    </div>
  );
};

export default SensorReading;

