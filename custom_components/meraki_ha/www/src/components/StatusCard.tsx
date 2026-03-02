import React from 'react';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon?: React.ReactNode;
  onClick?: () => void;
}

const StatusCard: React.FC<StatusCardProps> = ({
  title,
  value,
  icon,
  onClick,
}) => {
  return (
    <div
      className="bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md flex items-center transition-shadow duration-200 border border-light-border dark:border-dark-border"
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      {icon && (
        <div className="mr-4 text-[var(--primary-color)] flex items-center justify-center">
          {typeof icon === 'string' ? (
            <span style={{ fontSize: '24px' }}>{icon}</span>
          ) : (
            icon
          )}
        </div>
      )}
      <div>
        <p className="text-sm text-[var(--secondary-text-color)]">{title}</p>
        <p className="text-2xl font-bold text-[var(--primary-text-color)]">
          {value}
        </p>
      </div>
    </div>
  );
};

export default StatusCard;
