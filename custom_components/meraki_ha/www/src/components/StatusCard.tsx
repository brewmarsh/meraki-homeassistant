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
      style={{ 
        cursor: isClickable ? 'pointer' : 'default',
        transition: 'transform 0.2s, box-shadow 0.2s',
      }}
      onMouseEnter={(e) => {
        if (isClickable) {
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        }
      }}
      onMouseLeave={(e) => {
        if (isClickable) {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '';
        }
      }}
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
