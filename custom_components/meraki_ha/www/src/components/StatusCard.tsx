import React from 'react';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon: string;
}

const StatusCard: React.FC<StatusCardProps> = ({ title, value, icon }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-center">
      <div className="text-3xl mr-4">{icon}</div>
      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
        <p className="text-2xl font-semibold text-gray-900 dark:text-white">{value}</p>
      </div>
    </div>
  );
};

export default StatusCard;
