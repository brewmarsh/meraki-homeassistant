/**
 * Meraki Home Assistant Panel - Main Application Component
 *
 * This component is the root of the React application. It receives the
 * Home Assistant `hass` object from the Web Component wrapper and uses
 * it to communicate with the backend via WebSocket.
 */

import React, { useState, useEffect, useCallback } from 'react';
import NetworkView from './components/NetworkView';
import DeviceView from './components/DeviceView';
import type { HomeAssistant, PanelInfo, RouteInfo } from './types/hass';

// Data types
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
}

interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
}

interface Device {
  entity_id: string;
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
  networkId?: string;
  firmware?: string;
  status_messages?: string[];
  entities?: Array<{ entity_id: string; name: string; state: string }>;
}

interface MerakiData {
  networks: Network[];
  devices: Device[];
  ssids: SSID[];
  enabled_networks: string[];
  config_entry_id: string;
  version?: string;
  [key: string]: unknown;
}

interface AppProps {
  hass: HomeAssistant | null;
  panel: PanelInfo | null;
  narrow: boolean;
  route: RouteInfo | null;
}

/**
 * Loading spinner component
 */
const LoadingSpinner: React.FC = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
    <span className="loading-text">Loading Meraki data...</span>
  </div>
);

/**
 * Error display component
 */
const ErrorDisplay: React.FC<{ message: string; onRetry?: () => void }> = ({
  message,
  onRetry,
}) => (
  <div className="error-container">
    <ha-icon icon="mdi:alert-circle"></ha-icon>
    <div className="error-content">
      <h3>Error Loading Data</h3>
      <p>{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="retry-button">
          Retry
        </button>
      )}
    </div>
  </div>
);

/**
 * Header component with version display
 */
const Header: React.FC<{ version?: string }> = ({ version }) => (
  <div className="meraki-header">
    <h1>Meraki Dashboard</h1>
    {version && <span className="version">v{version}</span>}
  </div>
);

/**
 * Main App Component
 */
const App: React.FC<AppProps> = ({ hass, panel, narrow }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<{
    view: string;
    deviceId?: string;
  }>({ view: 'dashboard' });

  // Get the config entry ID from panel config
  const configEntryId = panel?.config?.config_entry_id;

  /**
   * Fetch data from the backend using Home Assistant's WebSocket API
   */
  const fetchData = useCallback(async () => {
    if (!hass || !configEntryId) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Use hass.callWS to call our WebSocket command
      const result = await hass.callWS<MerakiData>({
        type: 'meraki_ha/get_config',
        config_entry_id: configEntryId,
      });

      // Process networks to add is_enabled flag
      if (result.networks && result.enabled_networks) {
        const processedNetworks = result.networks.map((network) => ({
          ...network,
          is_enabled: result.enabled_networks.includes(network.id),
        }));
        result.networks = processedNetworks;
      }

      setData(result);
    } catch (err) {
      console.error('Failed to fetch Meraki data:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to fetch data from Meraki integration'
      );
    } finally {
      setLoading(false);
    }
  }, [hass, configEntryId]);

  // Fetch data when hass or configEntryId becomes available
  useEffect(() => {
    if (hass && configEntryId) {
      fetchData();
    }
  }, [hass, configEntryId, fetchData]);

  // Show loading state while waiting for hass
  if (!hass) {
    return (
      <div className="meraki-panel">
        <LoadingSpinner />
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
          Waiting for Home Assistant connection...
        </p>
      </div>
    );
  }

  // Show loading state while fetching data
  if (loading) {
    return (
      <div className="meraki-panel">
        <Header />
        <LoadingSpinner />
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="meraki-panel">
        <Header />
        <ErrorDisplay message={error} onRetry={fetchData} />
      </div>
    );
  }

  // Show empty state
  if (!data) {
    return (
      <div className="meraki-panel">
        <Header />
        <div className="empty-state">
          <ha-icon icon="mdi:database-off"></ha-icon>
          <p>No data available.</p>
        </div>
      </div>
    );
  }

  // Render the appropriate view
  return (
    <div className="meraki-panel" style={{ maxWidth: narrow ? '100%' : '1200px', margin: '0 auto' }}>
      <Header version={data.version} />

      {activeView.view === 'dashboard' ? (
        <NetworkView
          data={data}
          setActiveView={setActiveView}
        />
      ) : (
        <DeviceView
          activeView={activeView}
          setActiveView={setActiveView}
          data={data}
        />
      )}
    </div>
  );
};

export default App;
