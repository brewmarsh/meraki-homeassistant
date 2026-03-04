import React from 'react';

const ConfigNotFoundState: React.FC = () => {
  return (
    <div className="flex flex-col justify-center items-center h-screen bg-[var(--primary-background-color)] text-[var(--primary-text-color)] p-4 text-center">
      <ha-icon icon="mdi:alert-circle-outline" style={{ '--mdc-icon-size': '64px', color: 'var(--error-color)' } as any} className="mb-4"></ha-icon>
      <h2 className="text-xl font-bold mb-2">Integration Not Configured</h2>
      <p className="mb-6 max-w-md text-[var(--secondary-text-color)]">
        The Meraki integration has not been configured yet. Please ensure the integration is added in Home Assistant.
      </p>
      <a
        href="/config/integrations"
        className="bg-[var(--primary-color)] text-[var(--text-primary-color, white)] px-6 py-2 rounded-lg hover:opacity-90 transition-colors"
      >
        Go to Integrations
      </a>
    </div>
  );
};

export default ConfigNotFoundState;
