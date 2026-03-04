import React from 'react';

const LoadingState: React.FC = () => {
  return (
    <div className="flex justify-center items-center h-screen bg-[var(--primary-background-color)] text-[var(--primary-text-color)]">
      <ha-circular-progress active alt="Loading Meraki data..."></ha-circular-progress>
    </div>
  );
};

export default LoadingState;
