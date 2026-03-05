import React from 'react';
// Frontend version: 2.3.0-beta.120
import TimedAccess from './components/TimedAccess';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';
import ConfigNotFoundState from './components/ConfigNotFoundState';
import { useMerakiData } from './hooks/useMerakiData';
import { AppProps } from './types/data';

const App: React.FC<AppProps> = ({ hass, panel, config_entry_id }) => {
  const configEntryId = config_entry_id || panel?.config?.config_entry_id;

  const {
    data,
    loading,
    error,
    configNotFound,
    fetchData,
  } = useMerakiData(hass, configEntryId);

  if (loading) {
    return <LoadingState />;
  }

  if (configNotFound) {
    return <ConfigNotFoundState />;
  }

  if (error && !data) {
    return <ErrorState error={error} onRetry={fetchData} />;
  }

  if (!data) {
    return (
      <div className="flex justify-center items-center h-screen bg-[var(--primary-background-color)] text-[var(--primary-text-color)]">
        No data found.
      </div>
    );
  }

  return (
    <div className="p-4 relative bg-[var(--primary-background-color)] text-[var(--primary-text-color)] min-h-screen">
      <div className="flex justify-between items-center mb-4 border-b border-[var(--divider-color)] pb-4">
        <h1 className="text-2xl font-bold">Cisco Meraki Integration</h1>
        <div className="flex gap-2">
          <button
            onClick={fetchData}
            className="p-2 rounded-full hover:bg-[var(--secondary-background-color)] text-[var(--secondary-text-color)] transition-colors"
            title="Refresh Data"
          >
            <ha-icon icon="mdi:refresh"></ha-icon>
          </button>
        </div>
      </div>

      <TimedAccess
        hass={hass}
        configEntryId={configEntryId!}
        data={data}
      />

      <div className="absolute bottom-0 right-0 p-2 text-xs text-[var(--secondary-text-color)]">
        Version: {data.version || '2.3.0-beta.120'}
      </div>
    </div>
  );
};

export default App;
