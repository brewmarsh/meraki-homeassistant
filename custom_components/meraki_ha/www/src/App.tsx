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
  <div className="flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    <span className="ml-3 text-gray-600 dark:text-gray-300">Loading Meraki data...</span>
  </div>
);

/**
 * Error display component
 */
const ErrorDisplay: React.FC<{ message: string; onRetry?: () => void }> = ({
  message,
  onRetry,
}) => (
  <div className="p-6 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 rounded-lg">
    <div className="flex items-center">
      <svg
        className="w-6 h-6 text-red-500 dark:text-red-400 mr-3"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <div>
        <h3 className="text-lg font-semibold text-red-700 dark:text-red-300">
          Error Loading Data
        </h3>
        <p className="text-red-600 dark:text-red-400">{message}</p>
      </div>
    </div>
    {onRetry && (
      <button
        onClick={onRetry}
        className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
      >
        Retry
      </button>
    )}
  </div>
);

/**
 * Header component with version display
 */
const Header: React.FC<{ version?: string }> = ({ version }) => (
  <div className="flex items-center justify-between mb-6">
    <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
      Meraki Dashboard
    </h1>
    {version && (
      <span className="text-sm text-gray-500 dark:text-gray-400">
        v{version}
      </span>
    )}
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

  /**
   * Handle network toggle (enable/disable tracking)
   */
  const handleNetworkToggle = useCallback(
    async (networkId: string, enabled: boolean) => {
      if (!hass || !data || !configEntryId) {
        return;
      }

      // Optimistically update the UI
      const updatedNetworks = data.networks.map((network) =>
        network.id === networkId ? { ...network, is_enabled: enabled } : network
      );
      setData({ ...data, networks: updatedNetworks });

      // Get the new list of enabled network IDs
      const enabledNetworkIds = updatedNetworks
        .filter((network) => network.is_enabled)
        .map((network) => network.id);

      try {
        // Send the update to the backend
        await hass.callWS({
          type: 'meraki_ha/update_enabled_networks',
          config_entry_id: configEntryId,
          enabled_networks: enabledNetworkIds,
        });
      } catch (err) {
        console.error('Failed to update enabled networks:', err);
        // Revert on error
        setData(data);
        setError('Failed to update network settings');
      }
    },
    [hass, data, configEntryId]
  );

  // Show loading state while waiting for hass
  if (!hass) {
    return (
      <div className="p-4">
        <LoadingSpinner />
        <p className="text-center text-gray-500 mt-4">
          Waiting for Home Assistant connection...
        </p>
      </div>
    );
  }

  // Show loading state while fetching data
  if (loading) {
    return (
      <div className="p-4">
        <Header />
        <LoadingSpinner />
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="p-4">
        <Header />
        <ErrorDisplay message={error} onRetry={fetchData} />
      </div>
    );
  }

  // Show empty state
  if (!data) {
    return (
      <div className="p-4">
        <Header />
        <p className="text-gray-500 dark:text-gray-400">No data available.</p>
      </div>
    );
  }

  // Render the appropriate view
  return (
    <div className={`p-4 ${narrow ? 'max-w-full' : 'max-w-7xl mx-auto'}`}>
      <Header version={data.version} />

      {activeView.view === 'dashboard' ? (
        <NetworkView
          data={data}
          onToggle={handleNetworkToggle}
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
