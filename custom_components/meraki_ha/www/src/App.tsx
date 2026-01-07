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
    <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
      {onSettingsClick && (
        <button
          onClick={onSettingsClick}
          className="settings-btn"
          title="Settings"
          style={{
            background: 'var(--bg-tertiary)',
            border: '1px solid var(--card-border)',
            borderRadius: 'var(--radius-sm)',
            padding: '8px 12px',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            transition: 'var(--transition)',
          }}
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
  }>({ view: 'dashboard' });
  const [showSettings, setShowSettings] = useState<boolean>(false);

  // Apply HA theme variables to the panel
  const { style: themeStyle } = useHaTheme(hass);

  // Use a ref for hass to avoid re-renders when hass object changes
  // The hass object changes on every HA state update, which would cause constant refetches
  const hassRef = useRef(hass);
  hassRef.current = hass;

  // Track if we've already loaded data to prevent duplicate fetches
  const hasLoadedRef = useRef(false);

  // Get the config entry ID from panel config
  const configEntryId = panel?.config?.config_entry_id;

  /**
   * Fetch data from the backend using Home Assistant's WebSocket API
   */
  const fetchData = useCallback(async () => {
    const currentHass = hassRef.current;
    if (!currentHass || !configEntryId) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Use hass.callWS to call our WebSocket command
      const result = await currentHass.callWS<MerakiData>({
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
      hasLoadedRef.current = true;
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
  }, [configEntryId]);

  // Fetch data only once when configEntryId becomes available and hass is connected
  useEffect(() => {
    if (hass && configEntryId && !hasLoadedRef.current) {
      fetchData();
    }
  }, [hass, configEntryId, fetchData]);

  // Show loading state while waiting for hass
  if (!hass) {
    return (
      <div className="meraki-panel" style={themeStyle}>
        <LoadingSpinner />
        <p
          style={{
            textAlign: 'center',
            color: 'var(--text-secondary)',
            marginTop: '16px',
          }}
        >
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
        <ErrorDisplay message={error} onRetry={fetchData} />
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
