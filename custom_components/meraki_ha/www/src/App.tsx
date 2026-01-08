/**
 * Meraki Home Assistant Panel - Main Application Component
 *
 * This component is the root of the React application. It receives the
 * Home Assistant `hass` object from the Web Component wrapper and uses
 * it to communicate with the backend via WebSocket.
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import ClientsView from './components/ClientsView';
import SSIDsListView from './components/SSIDsListView';
import SSIDView from './components/SSIDView';
import Settings from './components/Settings';
import { useHaTheme } from './hooks/useHaTheme';
import type { HomeAssistant, PanelInfo, RouteInfo } from './types/hass';

// Data types
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
  entity_id?: string;
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
  productType?: string;
  firmware?: string;
  status_messages?: string[];
  entities?: Array<{ entity_id: string; name: string; state: string }>;
  ports_statuses?: Array<{
    portId: string;
    status: string;
    enabled: boolean;
    isUplink?: boolean;
    speed?: string;
    duplex?: string;
    poe?: { isAllocated?: boolean; enabled?: boolean };
    powerUsageInWh?: number;
    usageInKb?: { total?: number; sent?: number; recv?: number };
    trafficInKbps?: { total?: number; sent?: number; recv?: number };
    clientName?: string;
    clientMac?: string;
    clientCount?: number;
    vlan?: number;
    errors?: string[];
    warnings?: string[];
    lldp?: {
      systemName?: string;
      systemDescription?: string;
      portId?: string;
      managementAddress?: string;
      portDescription?: string;
      chassisId?: string;
    };
    cdp?: {
      deviceId?: string;
      platform?: string;
      portId?: string;
      address?: string;
      nativeVlan?: number;
      managementAddress?: string;
    };
    securePort?: {
      enabled?: boolean;
      active?: boolean;
      authenticationStatus?: string;
    };
  }>;
  readings?: {
    temperature?: number;
    humidity?: number;
    battery?: number;
  };
  basicServiceSets?: Array<{
    ssidName?: string;
    ssidNumber?: number;
    enabled?: boolean;
    band?: string;
    bssid?: string;
    channel?: number;
    channelWidth?: string;
    power?: string;
    visible?: boolean;
    broadcasting?: boolean;
  }>;
}

interface Client {
  id: string;
  mac: string;
  description?: string;
  ip?: string;
  ip6?: string;
  user?: string;
  firstSeen?: string;
  lastSeen?: string;
  manufacturer?: string;
  os?: string;
  recentDeviceSerial?: string;
  recentDeviceName?: string;
  ssid?: string;
  vlan?: number;
  switchport?: string;
  status?: string;
  usage?: { sent: number; recv: number };
  networkId?: string;
}

interface MerakiData {
  networks: Network[];
  devices: Device[];
  ssids: SSID[];
  clients: Client[];
  enabled_networks: string[];
  config_entry_id: string;
  version?: string;
  // Dashboard settings from integration options
  dashboard_view_mode?: 'network' | 'type';
  dashboard_device_type_filter?: string;
  dashboard_status_filter?: string;
  camera_link_integration?: string;
  temperature_unit?: 'celsius' | 'fahrenheit';
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
    <span className="error-icon">⚠️</span>
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
 * Header component with logo, version, and settings button
 */
const Header: React.FC<{
  version?: string;
  onSettingsClick?: () => void;
}> = ({ version, onSettingsClick }) => (
  <div className="meraki-header">
    <div className="logo">🌐</div>
    <h1>Meraki Dashboard</h1>
    {version && <span className="version">v{version}</span>}
    <div className="header-actions">
      {onSettingsClick && (
        <button
          onClick={onSettingsClick}
          className="settings-btn"
          title="Settings"
        >
          ⚙️ Settings
        </button>
      )}
    </div>
  </div>
);

/**
 * Main App Component
 */
const App: React.FC<AppProps> = ({ hass, panel, narrow: _narrow }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<{
    view: string;
    deviceId?: string;
    ssidNetworkId?: string;
    ssidNumber?: number;
  }>({ view: 'dashboard' });
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const [retryCount, setRetryCount] = useState<number>(0);

  // Apply HA theme variables to the panel
  const { style: themeStyle } = useHaTheme(hass);

  // Retry connection by incrementing retry count to trigger re-subscription
  const retryConnection = useCallback(() => {
    hasLoadedRef.current = false;
    setRetryCount((c) => c + 1);
  }, []);

  // Use a ref for hass to avoid re-renders when hass object changes
  // The hass object changes on every HA state update, which would cause constant refetches
  const hassRef = useRef(hass);
  hassRef.current = hass;

  // Track if we've already loaded data to prevent duplicate fetches
  const hasLoadedRef = useRef(false);

  // Get the config entry ID from panel config
  const configEntryId = panel?.config?.config_entry_id;

  /**
   * Process incoming data to add is_enabled flag to networks
   */
  const processData = useCallback((result: MerakiData): MerakiData => {
    if (result.networks && result.enabled_networks) {
      const processedNetworks = result.networks.map((network) => ({
        ...network,
        is_enabled: result.enabled_networks.includes(network.id),
      }));
      return { ...result, networks: processedNetworks };
    }
    return result;
  }, []);

  /**
   * Subscribe to real-time Meraki data updates via WebSocket
   * Uses refs to avoid re-subscribing when hass object updates
   */
  useEffect(() => {
    const currentHass = hassRef.current;
    if (!currentHass || !configEntryId) {
      return;
    }

    let unsubscribe: (() => void) | null = null;
    let isSubscribed = true;

    const setupSubscription = async () => {
      try {
        // Only show loading on initial load, not on data updates
        if (!hasLoadedRef.current) {
          setLoading(true);
        }
        setError(null);

        // Subscribe to meraki data updates - this sends initial data and pushes updates
        unsubscribe =
          await currentHass.connection.subscribeMessage<MerakiData>(
            (message: MerakiData) => {
              if (isSubscribed && message) {
                console.log('[Meraki] Received data update:', {
                  last_updated: message.last_updated,
                  scan_interval: message.scan_interval,
                  networks: message.networks?.length,
                  devices: message.devices?.length,
                });
                const processed = processData(message);
                setData(processed);
                setLoading(false);
                hasLoadedRef.current = true;
              }
            },
            {
              type: 'meraki_ha/subscribe_meraki_data',
              config_entry_id: configEntryId,
            }
          );
      } catch (err) {
        console.error('Failed to subscribe to Meraki data:', err);
        if (isSubscribed) {
          setError(
            err instanceof Error
              ? err.message
              : 'Failed to connect to Meraki integration'
          );
          setLoading(false);
        }
      }
    };

    setupSubscription();

    // Cleanup subscription on unmount or when config entry changes
    return () => {
      isSubscribed = false;
      if (unsubscribe) {
        unsubscribe();
      }
    };
    // Only re-subscribe when configEntryId changes or retry is requested
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [configEntryId, retryCount]);

  // Show loading state while waiting for hass
  if (!hass) {
    return (
      <div className="meraki-panel" style={themeStyle}>
        <LoadingSpinner />
        <p className="loading-message">
          Waiting for Home Assistant connection...
        </p>
      </div>
    );
  }

  // Show loading state while fetching data
  if (loading) {
    return (
      <div className="meraki-panel" style={themeStyle}>
        <Header />
        <LoadingSpinner />
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="meraki-panel" style={themeStyle}>
        <Header />
        <ErrorDisplay message={error} onRetry={retryConnection} />
      </div>
    );
  }

  // Show empty state
  if (!data) {
    return (
      <div className="meraki-panel" style={themeStyle}>
        <Header />
        <div className="empty-state">
          <div className="icon">📡</div>
          <h3>No Data Available</h3>
          <p>Could not load Meraki data. Please try again.</p>
        </div>
      </div>
    );
  }

  // Filter to only show enabled networks
  const enabledNetworks =
    data.networks?.filter((network) => network.is_enabled) || [];

  // Create processed data with only enabled networks
  const processedData = {
    ...data,
    networks: enabledNetworks,
  };

  // Render the appropriate view
  const renderView = () => {
    switch (activeView.view) {
      case 'clients':
        return (
          <ClientsView
            clients={data.clients || []}
            setActiveView={setActiveView}
            onBack={() => setActiveView({ view: 'dashboard' })}
          />
        );
      case 'device':
        return (
          <DeviceView
            activeView={activeView}
            setActiveView={setActiveView}
            data={data}
            hass={hass}
            configEntryId={configEntryId}
            cameraLinkIntegration={data.camera_link_integration}
            configEntryOptions={{
              temperature_unit: data.temperature_unit,
            }}
          />
        );
      case 'ssids':
        return (
          <SSIDsListView
            ssids={data.ssids || []}
            clients={data.clients || []}
            networks={data.networks || []}
            onBack={() => setActiveView({ view: 'dashboard' })}
            onSSIDClick={(ssid) =>
              setActiveView({
                view: 'ssid',
                ssidNetworkId: ssid.networkId,
                ssidNumber: ssid.number,
              })
            }
          />
        );
      case 'ssid': {
        // Find the SSID from data
        const selectedSSID = data.ssids?.find(
          (s) =>
            s.networkId === activeView.ssidNetworkId &&
            s.number === activeView.ssidNumber
        );
        if (!selectedSSID) {
          return (
            <div className="error-container">
              <span className="error-icon">⚠️</span>
              <p>SSID not found</p>
              <button
                onClick={() => setActiveView({ view: 'ssids' })}
                className="retry-button"
              >
                Back to SSIDs
              </button>
            </div>
          );
        }
        const ssidNetwork = data.networks?.find(
          (n) => n.id === selectedSSID.networkId
        );
        return (
          <SSIDView
            ssid={selectedSSID}
            clients={data.clients || []}
            network={ssidNetwork}
            hass={hass}
            onBack={() => setActiveView({ view: 'ssids' })}
            onClientClick={(clientId) =>
              setActiveView({ view: 'clients', deviceId: clientId })
            }
          />
        );
      }
      default:
        return (
          <Dashboard
            data={processedData}
            setActiveView={setActiveView}
            hass={hass}
            defaultViewMode={data.dashboard_view_mode}
            defaultDeviceTypeFilter={data.dashboard_device_type_filter}
            defaultStatusFilter={data.dashboard_status_filter}
            temperatureUnit={data.temperature_unit}
          />
        );
    }
  };

  return (
    <div className="meraki-panel" style={themeStyle}>
      <Header
        version={data.version}
        onSettingsClick={() => setShowSettings(true)}
      />
      {renderView()}

      {/* Settings Modal */}
      {showSettings && configEntryId && (
        <Settings
          hass={hass}
          options={data}
          configEntryId={configEntryId}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
};

export default App;
