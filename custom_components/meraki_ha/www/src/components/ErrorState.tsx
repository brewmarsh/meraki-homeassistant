import React from 'react';

interface ErrorStateProps {
  error: string;
  onRetry: () => void;
}

const ErrorState: React.FC<ErrorStateProps> = ({ error, onRetry }) => {
  return (
    <div className="flex flex-col justify-center items-center h-screen bg-[var(--primary-background-color)] text-[var(--primary-text-color)] p-4 text-center">
      <ha-icon icon="mdi:error-outline" style={{ '--mdc-icon-size': '64px', color: 'var(--error-color)' } as any} className="mb-4"></ha-icon>
      <h2 className="text-xl font-bold mb-2">Error</h2>
      <p className="mb-6 text-[var(--secondary-text-color)]">{error}</p>
      <button
        onClick={onRetry}
        className="bg-[var(--primary-color)] text-[var(--text-primary-color, white)] px-6 py-2 rounded-lg hover:opacity-90 transition-colors"
      >
        Retry
      </button>
    </div>
  );
};

export default ErrorState;
