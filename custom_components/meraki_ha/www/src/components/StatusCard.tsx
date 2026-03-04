import React from 'react';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon?: string;
  onClick?: () => void;
}

const StatusCard: React.FC<StatusCardProps> = ({
  title,
  value,
  icon,
  onClick,
}) => {
  return (
    <ha-card
      className="p-4 flex items-center transition-shadow duration-200"
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      {icon && (
        <div className="mr-4 text-[var(--primary-color)] flex items-center justify-center">
          <ha-icon icon={icon} style={{ fontSize: '24px' }}></ha-icon>
        </div>
      )}
      <div>
        <p className="text-sm text-[var(--secondary-text-color)]">{title}</p>
        <p className="text-2xl font-bold text-[var(--primary-text-color)]">
          {value}
        </p>
      </div>
    </ha-card>
  );
};

export default StatusCard;
