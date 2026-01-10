/**
 * Meraki Home Assistant Panel - Main Application Component
 *
 * This component is the root of the React application. It receives the
 * Home Assistant `hass` object from the Web Component wrapper and uses
 * it to communicate with the backend via WebSocket.
 */

import React, {
  useState,
  useEffect,
  useCallback,
  useRef,
  useMemo,
} from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import ClientsView from './components/ClientsView';
import SSIDsListView from './components/SSIDsListView';
import SSIDView from './components/SSIDView';
import { useHaTheme } from './hooks/useHaTheme';
import type {
  HomeAssistant,
  PanelInfo,
  RouteInfo,
  HassEntity,
} from './types/hass';

// Data types from device/entity registry
interface HaDevice {
  id: string;
  config_entries: string[];
  identifiers: Array<[string, string]>;
  manufacturer: string | null;
  model: string | null;
  name: string | null;
  via_device_id: string | null;
  area_id: string | null;
  disabled_by: string | null;
  entry_type: 'service' | null;
}

interface HaEntity {
  id: string;
  entity_id: string;
  device_id: string | null;
  area_id: string | null;
  platform: string;
  config_entry_id: string | null;
  disabled_by: string | null;
  hidden_by: string | null;
  entity_category: string | null;
  has_entity_name: boolean;
  name: string | null;
  icon: string | null;
  original_name?: string;
  unique_id: string;
}

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
  ha_device_id?: string;
  via_device_id?: string | null;
  is_blocked?: boolean;
}

interface MqttServiceStats {
  is_running: boolean;
  messages_received: number;
  messages_processed: number;
  last_message_time: string | null;
  start_time: string | null;
  sensors_mapped: number;
}

interface RelayDestination {
  name: string;
  status: 'connected' | 'connecting' | 'disconnected' | 'error';
  host: string;
  port: number;
  topic_filter: string;
  messages_relayed: number;
  last_relay_time: string | null;
  last_error: string | null;
  last_error_time: string | null;
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
  dashboard_device_type_filter?: string[] | string;
  dashboard_status_filter?: string;
  camera_link_integration?: string;
  temperature_unit?: 'celsius' | 'fahrenheit';
  // MQTT status data
  mqtt?: {
    enabled: boolean;
    stats?: MqttServiceStats;
    relay_destinations?: Record<string, RelayDestination>;
  };
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
    clientId?: string;
    ssidNetworkId?: string;
    ssidNumber?: number;
  }>({ view: 'dashboard' });
  const [retryCount, setRetryCount] = useState<number>(0);

  // === State for HA device and entity registries ===
  const [haDevices, setHaDevices] = useState<HaDevice[]>([]);
  const [haEntities, setHaEntities] = useState<HaEntity[]>([]);
  const [haEntityStates, setHaEntityStates] = useState<
    Record<string, HassEntity>
  >({});

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

  // Fetch device/entity registry data
  useEffect(() => {
    const currentHass = hassRef.current;
    if (!currentHass) return;

    const fetchHaData = async () => {
      try {
        const [devices, entities, entityStates] = await Promise.all([
          currentHass.callWS<HaDevice[]>({
            type: 'config/device_registry/list',
          }),
          currentHass.callWS<HaEntity[]>({
            type: 'config/entity_registry/list',
          }),
          currentHass.callWS<HassEntity[]>({ type: 'get_states' }),
        ]);

        setHaDevices(devices);
        setHaEntities(entities);

        const statesMap = entityStates.reduce(
          (acc, state) => {
            acc[state.entity_id] = state;
            return acc;
          },
          {} as Record<string, HassEntity>
        );
        setHaEntityStates(statesMap);

        console.log('[Meraki] Fetched HA registries:', {
          devices: devices.length,
          entities: entities.length,
          states: entityStates.length,
        });
      } catch (err) {
        console.error('Failed to fetch HA device/entity registries:', err);
        setError('Could not load device and entity data from Home Assistant.');
      }
    };

    fetchHaData();

    // Subscribe to all state changes to keep entity states fresh
    const subscribeEvents = async () => {
      try {
        return await currentHass.connection.subscribeMessage(
          (event: any) => {
            if (event.event_type === 'state_changed') {
              const { entity_id, new_state } = event.data;
              if (new_state) {
                setHaEntityStates((prevStates) => ({
                  ...prevStates,
                  [entity_id]: new_state,
                }));
              } else {
                // Entity was removed
                setHaEntityStates((prevStates) => {
                  const newStates = { ...prevStates };
                  delete newStates[entity_id];
                  return newStates;
                });
              }
            }
          },
          { type: 'subscribe_events', event_type: 'state_changed' }
        );
      } catch (err) {
        console.error('Failed to subscribe to state changes:', err);
        return () => {};
      }
    };

    const unsubscribe = subscribeEvents();

    return () => {
      unsubscribe.then((unsub) => unsub());
    };
  }, [hassRef, retryCount]);

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
   * Compare two data objects to check if they are meaningfully different
   * Only triggers re-render if actual data changed, not just timestamps
   */
  const hasDataChanged = useCallback(
    (oldData: MerakiData | null, newData: MerakiData): boolean => {
      if (!oldData) return true;

      // Compare key data counts (excluding clients, which are now from HA registry)
      if (
        oldData.devices?.length !== newData.devices?.length ||
        oldData.networks?.length !== newData.networks?.length ||
        oldData.ssids?.length !== newData.ssids?.length
      ) {
        return true;
      }

      // Compare device statuses (quick check for status changes)
      const oldDeviceStates = oldData.devices
        ?.map((d) => `${d.serial}:${d.status}`)
        .sort()
        .join('|');
      const newDeviceStates = newData.devices
        ?.map((d) => `${d.serial}:${d.status}`)
        .sort()
        .join('|');
      if (oldDeviceStates !== newDeviceStates) {
        return true;
      }

      // Compare client count per device (for port visualizations)
      const oldClientDevices = oldData.clients
        ?.map((c) => c.recentDeviceSerial)
        .sort()
        .join('|');
      const newClientDevices = newData.clients
        ?.map((c) => c.recentDeviceSerial)
        .sort()
        .join('|');
      if (oldClientDevices !== newClientDevices) {
        return true;
      }

      // Always accept if last_updated changed (for timestamp display)
      // but don't force full re-render - handled by memoized components
      return false;
    },
    []
  );

  // Store the last update timestamp separately to avoid re-renders
  const lastUpdatedRef = useRef<string | null>(null);

  // Memoize processed client data from HA registries
  // Uses both device_tracker entities and client sensor entities for complete data
  const processedClients = useMemo((): Client[] => {
    // First, try to use clients from the backend data (API)
    // This is the most complete source as it comes directly from Meraki
    if (data?.clients && data.clients.length > 0) {
      return data.clients.map((client) => {
        // Find the corresponding device_tracker entity for status
        const macPart = client.mac.replace(/:/g, '_').toLowerCase();
        const trackerEntityId = `device_tracker.meraki_client_${macPart}`;
        const trackerState = haEntityStates[trackerEntityId];
        const trackerEntity = haEntities.find(
          (e) => e.entity_id === trackerEntityId
        );
        const device = trackerEntity?.device_id
          ? haDevices.find((d) => d.id === trackerEntity.device_id)
          : null;

        // Find the block switch entity for this client
        const switchEntityId = `switch.meraki_client_${macPart}_block`;
        const switchState = haEntityStates[switchEntityId];

        return {
          ...client,
          id: client.id || trackerEntity?.device_id || client.mac,
          ha_device_id: trackerEntity?.device_id || '',
          status:
            trackerState?.state === 'home'
              ? 'Online'
              : trackerState?.state === 'not_home'
              ? 'Offline'
              : client.status || 'Unknown',
          via_device_id: device?.via_device_id,
          is_blocked: switchState?.state === 'on',
        };
      });
    }

    // Fallback: Build client list from HA entity registry
    if (!haEntities.length || !Object.keys(haEntityStates).length) {
      return [];
    }

    // Find all Meraki client tracker entities (device_tracker.meraki_client_*)
    // This approach works for both:
    // 1. Dedicated Meraki client devices (identifiers contain client_MAC)
    // 2. Existing devices like Sonos/Apple TV where Meraki entity is linked
    const clientTrackerEntities = haEntities.filter((e) =>
      e.entity_id.startsWith('device_tracker.meraki_client_')
    );

    return clientTrackerEntities.map((trackerEntity) => {
      const trackerState = haEntityStates[trackerEntity.entity_id];
      const device = haDevices.find((d) => d.id === trackerEntity.device_id);

      // Extract MAC from entity_id (device_tracker.meraki_client_XX_XX_XX_XX_XX_XX)
      const macPart = trackerEntity.entity_id.replace(
        'device_tracker.meraki_client_',
        ''
      );
      const mac = macPart.replace(/_/g, ':');

      // Find the block switch entity for this client
      const switchEntityId = `switch.meraki_client_${macPart}_block`;
      const switchState = haEntityStates[switchEntityId];

      // Also check for client sensor entities for additional data
      const vlanSensorId = `sensor.meraki_client_${macPart}_vlan`;
      const ssidSensorId = `sensor.meraki_client_${macPart}_ssid`;
      const connDeviceSensorId = `sensor.meraki_client_${macPart}_connected_device`;
      const switchportSensorId = `sensor.meraki_client_${macPart}_switchport`;

      const vlanState = haEntityStates[vlanSensorId];
      const ssidState = haEntityStates[ssidSensorId];
      const connDeviceState = haEntityStates[connDeviceSensorId];
      const switchportState = haEntityStates[switchportSensorId];

      return {
        id: trackerEntity.device_id || trackerEntity.entity_id,
        mac: mac,
        ha_device_id: trackerEntity.device_id || '',
        description:
          device?.name || trackerState?.attributes?.friendly_name || mac,
        ip: trackerState?.attributes?.ip_address || '',
        manufacturer:
          device?.manufacturer ||
          trackerState?.attributes?.manufacturer ||
          'Unknown',
        os: trackerState?.attributes?.os || '',
        status: trackerState?.state === 'home' ? 'Online' : 'Offline',
        // Use sensor entities if available, fall back to device_tracker attributes
        ssid: ssidState?.state || trackerState?.attributes?.ssid || '',
        switchport:
          switchportState?.state || trackerState?.attributes?.switchport,
        vlan:
          (vlanState?.state ? parseInt(vlanState.state, 10) : undefined) ||
          trackerState?.attributes?.vlan,
        recentDeviceSerial:
          connDeviceState?.attributes?.device_serial ||
          trackerState?.attributes?.connected_to_serial ||
          '',
        recentDeviceName:
          connDeviceState?.state ||
          trackerState?.attributes?.connected_to_device,
        via_device_id: device?.via_device_id,
        is_blocked: switchState?.state === 'on',
      };
    });
  }, [data?.clients, haDevices, haEntities, haEntityStates]);

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

                // Update timestamp ref (doesn't trigger re-render)
                lastUpdatedRef.current =
                  (message.last_updated as string) || null;

                // Only update state if data actually changed
                setData((prevData) => {
                  if (hasDataChanged(prevData, processed)) {
                    console.log(
                      '[Meraki] Data changed, updating state',
                      processed.last_updated
                    );
                    return processed;
                  }
                  // Data hasn't meaningfully changed, but update timestamps
                  if (
                    prevData &&
                    prevData.last_updated !== processed.last_updated
                  ) {
                    console.log(
                      '[Meraki] Only timestamp changed, light update'
                    );
                    return { ...prevData, ...processed };
                  }
                  console.log('[Meraki] No changes detected, skipping update');
                  return prevData;
                });

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

  // Memoize filtered networks to prevent recalculation on every render
  // NOTE: These hooks must be before any early returns to comply with Rules of Hooks
  const enabledNetworks = useMemo(
    () => data?.networks?.filter((network) => network.is_enabled) || [],
    [data?.networks]
  );

  // Memoize processed data with only enabled networks
  const processedData = useMemo(
    () =>
      data
        ? {
            ...data,
            networks: enabledNetworks,
          }
        : null,
    [data, enabledNetworks]
  );

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
  if (!data || !processedData) {
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

  // Render the appropriate view
  const renderView = () => {
    switch (activeView.view) {
      case 'clients':
        return (
          <ClientsView
            clients={processedClients}
            onBack={() => setActiveView({ view: 'dashboard' })}
            initialClientId={activeView.clientId}
          />
        );
      case 'device':
        return (
          <DeviceView
            activeView={activeView}
            setActiveView={setActiveView}
            data={data}
            clients={processedClients}
            haDevices={haDevices}
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
            clients={processedClients}
            network={ssidNetwork}
            hass={hass}
            onBack={() => setActiveView({ view: 'ssids' })}
            onClientClick={(haDeviceId) => {
              if (haDeviceId) {
                const path = `/config/devices/device/${haDeviceId}`;
                const event = new CustomEvent('hass-navigate', {
                  detail: { path },
                  bubbles: true,
                  composed: true,
                });
                window.dispatchEvent(event);
              }
            }}
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
        onSettingsClick={() =>
          hass?.showOptionsFlow(configEntryId || '', null, {
            step_id: 'init',
          })
        }
      />
      {renderView()}
    </div>
  );
};

export default App;
