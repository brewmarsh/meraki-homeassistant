import React from 'react';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon?: React.ReactNode;
  onClick?: () => void;
}

<<<<<<< HEAD
<<<<<<< HEAD
const StatusCard: React.FC<StatusCardProps> = ({ title, value, icon, onClick }) => {
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
const StatusCard: React.FC<StatusCardProps> = ({
  title,
  value,
  icon,
  onClick,
}) => {
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
  return (
    <div
      className="bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md flex items-center transition-shadow duration-200"
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      {icon && <div className="mr-4 text-cisco-blue">{icon}</div>}
      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
<<<<<<< HEAD
<<<<<<< HEAD
        <p className="text-2xl font-bold text-dark-text dark:text-light-text">{value}</p>
=======
        <p className="text-2xl font-bold text-dark-text dark:text-light-text">
          {value}
        </p>
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
        <p className="text-2xl font-bold text-dark-text dark:text-light-text">
          {value}
        </p>
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
      </div>
    </div>
  );
};

export default StatusCard;
