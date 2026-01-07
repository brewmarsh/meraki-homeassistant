import React from 'react';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon?: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error';
  onClick?: () => void;
  clickable?: boolean;
}

const StatusCard: React.FC<StatusCardProps> = ({
  title,
  value,
  icon,
  variant = 'default',
  onClick,
  clickable = false,
}) => {
  const valueClass = variant === 'default' ? '' : variant;
  const isClickable = onClick || clickable;

  return (
    <div
      className={`stat-card ${isClickable ? 'clickable' : ''}`}
      onClick={onClick}
    >
      <div className="label">{title}</div>
      <div className={`value ${valueClass}`}>
        {icon && <span className="stat-icon">{icon}</span>}
        {value}
      </div>
    </div>
  );
};

export default StatusCard;
