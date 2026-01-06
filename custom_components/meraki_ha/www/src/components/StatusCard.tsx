import React from 'react';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon?: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error';
  onClick?: () => void;
}

const StatusCard: React.FC<StatusCardProps> = ({
  title,
  value,
  icon,
  variant = 'default',
  onClick,
}) => {
  const valueClass = variant === 'default' ? '' : variant;
  
  return (
    <div
      className="stat-card"
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      <div className="label">{title}</div>
      <div className={`value ${valueClass}`}>
        {icon && <span style={{ marginRight: '8px' }}>{icon}</span>}
        {value}
      </div>
    </div>
  );
};

export default StatusCard;
