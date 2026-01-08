import React, { memo } from 'react';

export type MetricType =
  // Switch metrics
  | 'poeEnergy'
  | 'connectedClients'
  | 'uptime'
  | 'connectedPorts'
  | 'activePoe'
  // Wireless metrics
  | 'activeSSIDs'
  | 'channelUtilization'
  // Appliance metrics
  | 'wanStatus'
  // Camera metrics
  | 'recordingStatus'
  | 'motionDetection'
  // Generic
  | 'count'
  | 'percentage'
  | 'status';

export type MetricStatus = 'normal' | 'warning' | 'critical' | 'inactive';

export type GaugeColor =
  | 'primary'
  | 'success'
  | 'warning'
  | 'error'
  | 'info'
  | 'purple';

interface GaugeConfig {
  min: number;
  max: number;
  color?: GaugeColor;
  showLabels?: boolean;
}

interface MetricCardProps {
  icon: string;
  label: string;
  value: number | string;
  unit?: string;
  secondaryValue?: string;
  gauge?: GaugeConfig;
  status?: MetricStatus;
  statusMessage?: string;
  onClick?: () => void;
}

const MetricCardComponent: React.FC<MetricCardProps> = ({
  icon,
  label,
  value,
  unit = '',
  secondaryValue,
  gauge,
  status = 'normal',
  statusMessage,
  onClick,
}) => {
  const getStatusIcon = (): string => {
    switch (status) {
      case 'normal':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'critical':
        return '🚨';
      case 'inactive':
        return '⏸️';
      default:
        return '';
    }
  };

  const getGaugePercent = (): number => {
    if (!gauge || typeof value !== 'number') return 0;
    const { min, max } = gauge;
    if (max === min) return 0;
    return Math.min(100, Math.max(0, ((value - min) / (max - min)) * 100));
  };

  const getGaugeColorClass = (): string => {
    if (!gauge?.color) {
      // Auto-determine color based on status
      switch (status) {
        case 'normal':
          return 'success';
        case 'warning':
          return 'warning';
        case 'critical':
          return 'error';
        default:
          return 'primary';
      }
    }
    return gauge.color;
  };

  const getIconWrapperClass = (): string => {
    const colorClass = getGaugeColorClass();
    return `metric-icon-wrapper metric-icon-${colorClass}`;
  };

  const formatValue = (): string => {
    if (typeof value === 'number') {
      // Format based on value size
      if (Number.isInteger(value)) {
        return value.toString();
      }
      return value.toFixed(1);
    }
    return value;
  };

  const gaugePercent = getGaugePercent();
  const showGaugeLabels = gauge?.showLabels !== false && gauge;

  return (
    <div
      className={`metric-card ${onClick ? 'clickable' : ''}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      <div className={getIconWrapperClass()}>
        <span className="metric-icon">{icon}</span>
      </div>

      <div className="metric-label">{label}</div>

      <div className="metric-value">
        {formatValue()}
        {unit && <span className="metric-unit">{unit}</span>}
      </div>

      {secondaryValue && (
        <div className="metric-secondary">{secondaryValue}</div>
      )}

      {statusMessage && (
        <div className={`metric-status metric-status-${status}`}>
          <span>{getStatusIcon()}</span>
          {statusMessage}
        </div>
      )}

      {gauge && (
        <>
          <div className="metric-gauge-wrapper">
            <div
              className={`metric-gauge-fill metric-gauge-${getGaugeColorClass()}`}
              style={{ width: `${gaugePercent}%` }}
            />
          </div>
          {showGaugeLabels && (
            <div className="metric-gauge-labels">
              <span>
                {gauge.min}
                {unit}
              </span>
              <span>
                {gauge.max}
                {unit}
              </span>
            </div>
          )}
        </>
      )}
    </div>
  );
};

// Memoize MetricCard - re-render only when value or status changes
const MetricCard = memo(MetricCardComponent);

export default MetricCard;
