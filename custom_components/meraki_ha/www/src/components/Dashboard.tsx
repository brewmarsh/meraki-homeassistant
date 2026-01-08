import React, { useState, useEffect, useRef, memo, useCallback } from 'react';
import StatusCard from './StatusCard';
import MqttStatusCard from './MqttStatusCard';

interface Device {
  serial: string;
  name: string;
  model: string;
  status: string;
  lanIp?: string;
  productType?: string;
  networkId?: string;
  readings?: {
    temperature?: number;
    humidity?: number;
  };
  ports_statuses?: Array<{
    status: string;
  }>;
}

interface Network {
  id: string;
  name: string;
  productTypes?: string[];
}

interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId?: string;
  entity_id?: string;
}

interface Client {
  id: string;
  mac: string;
  description?: string;
  ip?: string;
  networkId?: string;
  recentDeviceSerial?: string;
  ssid?: string;
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

interface DashboardProps {
  setActiveView: (view: {
    view: string;
    deviceId?: string;
    ssidNetworkId?: string;
    ssidNumber?: number;
  }) => void;
  data: {
    devices?: Device[];
    networks?: Network[];
    ssids?: SSID[];
    clients?: Client[];
    scan_interval?: number;
    last_updated?: string;
    mqtt?: {
      enabled: boolean;
      stats?: MqttServiceStats;
      relay_destinations?: Record<string, RelayDestination>;
    };
  };
  hass?: {
    callService?: (
      domain: string,
      service: string,
      data?: Record<string, unknown>,
      target?: { entity_id?: string | string[] }
    ) => Promise<void>;
  };
  // Default settings from integration options
  defaultViewMode?: 'network' | 'type';
  defaultDeviceTypeFilter?: string;
  defaultStatusFilter?: string;
  temperatureUnit?: 'celsius' | 'fahrenheit';
}

type DeviceTypeFilter =
  | 'all'
  | 'switch'
  | 'camera'
  | 'wireless'
  | 'sensor'
  | 'appliance';
type StatusFilter = 'all' | 'online' | 'offline' | 'alerting' | 'dormant';
type ViewMode = 'network' | 'type';

const DEVICE_TYPES: {
  value: DeviceTypeFilter;
  label: string;
  icon: string;
}[] = [
  { value: 'all', label: 'All Types', icon: '📱' },
  { value: 'switch', label: 'Switches', icon: '🔀' },
  { value: 'camera', label: 'Cameras', icon: '📹' },
  { value: 'wireless', label: 'Wireless', icon: '📶' },
  { value: 'sensor', label: 'Sensors', icon: '📡' },
  { value: 'appliance', label: 'Firewalls', icon: '🛡️' },
];

const STATUS_OPTIONS: { value: StatusFilter; label: string }[] = [
  { value: 'all', label: 'All Status' },
  { value: 'online', label: 'Online' },
  { value: 'offline', label: 'Offline' },
  { value: 'alerting', label: 'Alerting' },
  { value: 'dormant', label: 'Dormant' },
];

/**
 * Memoized device row - only re-renders when this specific device changes
 */
interface DeviceRowProps {
  device: Device;
  onClick: () => void;
  getDeviceIcon: (device: Device) => string;
  getDeviceTypeClass: (device: Device) => string;
  getDeviceDetail: (device: Device) => string;
}

const DeviceRow = memo<DeviceRowProps>(
  ({
    device,
    onClick,
    getDeviceIcon,
    getDeviceTypeClass,
    getDeviceDetail,
  }) => (
    <tr className="device-row" onClick={onClick}>
      <td>
        <div className="device-name-cell">
          <div className={`device-icon ${getDeviceTypeClass(device)}`}>
            {getDeviceIcon(device)}
          </div>
          <span className="name">{device.name || device.serial}</span>
        </div>
      </td>
      <td className="device-model">{device.model || '—'}</td>
      <td className="device-model cell-mono">{device.serial}</td>
      <td>
        <div className={`status-badge ${device.status?.toLowerCase()}`}>
          <div className="status-dot"></div>
          <span>{device.status || 'Unknown'}</span>
        </div>
      </td>
      <td className="device-model">{device.lanIp || '—'}</td>
      <td>
        <span className="detail-badge">{getDeviceDetail(device) || '—'}</span>
      </td>
    </tr>
  ),
  (prevProps, nextProps) => {
    const prev = prevProps.device;
    const next = nextProps.device;

    // Only re-render if device-specific data changed
    if (prev.serial !== next.serial) return false;
    if (prev.status !== next.status) return false;
    if (prev.name !== next.name) return false;
    if (prev.lanIp !== next.lanIp) return false;
    if (prev.model !== next.model) return false;

    // Check readings for sensor devices
    if (prev.readings?.temperature !== next.readings?.temperature)
      return false;
    if (prev.readings?.humidity !== next.readings?.humidity) return false;

    // Check ports for switches
    const prevConnected = prev.ports_statuses?.filter(
      (p) => p.status === 'Connected'
    ).length;
    const nextConnected = next.ports_statuses?.filter(
      (p) => p.status === 'Connected'
    ).length;
    if (prevConnected !== nextConnected) return false;

    return true; // No changes, skip re-render
  }
);

DeviceRow.displayName = 'DeviceRow';

const DashboardComponent: React.FC<DashboardProps> = ({
  setActiveView,
  data,
  hass: _hass,
  defaultViewMode = 'network',
  defaultDeviceTypeFilter = 'all',
  defaultStatusFilter = 'all',
  temperatureUnit = 'celsius',
}) => {
  const [expandedNetworks, setExpandedNetworks] = useState<Set<string>>(
    new Set()
  );
  const [expandedTypes, setExpandedTypes] = useState<Set<string>>(
    new Set(['switch', 'camera', 'wireless', 'sensor', 'appliance'])
  );
  // expandedSSIDs removed - SSIDs now navigate to dedicated view
  const [deviceTypeFilter, setDeviceTypeFilter] = useState<DeviceTypeFilter>(
    (defaultDeviceTypeFilter as DeviceTypeFilter) || 'all'
  );
  const [statusFilter, setStatusFilter] = useState<StatusFilter>(
    (defaultStatusFilter as StatusFilter) || 'all'
  );
  const [viewMode, setViewMode] = useState<ViewMode>(
    defaultViewMode || 'network'
  );
  const hasAutoExpandedRef = useRef(false);

  // Auto-expand if there's only one network (or a few networks)
  useEffect(() => {
    if (!hasAutoExpandedRef.current && data?.networks) {
      const networkIds = data.networks.map((n) => n.id);
      // Auto-expand if 3 or fewer networks
      if (networkIds.length > 0 && networkIds.length <= 3) {
        setExpandedNetworks(new Set(networkIds));
        hasAutoExpandedRef.current = true;
      }
    }
  }, [data?.networks]);

  if (!data) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <div className="loading-text">Loading dashboard...</div>
      </div>
    );
  }

  const {
    devices = [],
    networks = [],
    ssids = [],
    clients = [],
    scan_interval = 90,
    last_updated,
    mqtt,
  } = data;

  // Countdown state for next refresh
  const [countdown, setCountdown] = useState<number | null>(null);
  const countdownRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Calculate and update countdown
  useEffect(() => {
    if (!last_updated || !scan_interval) {
      console.log('[Meraki] Countdown disabled - missing data:', {
        last_updated,
        scan_interval,
      });
      setCountdown(null);
      return;
    }

    console.log('[Meraki] Countdown reset - new data received:', {
      last_updated,
      scan_interval,
    });

    const updateCountdown = () => {
      const lastUpdate = new Date(last_updated).getTime();
      const nextUpdate = lastUpdate + scan_interval * 1000;
      const now = Date.now();
      const remaining = Math.max(0, Math.floor((nextUpdate - now) / 1000));
      setCountdown(remaining);
    };

    updateCountdown();
    countdownRef.current = setInterval(updateCountdown, 1000);

    return () => {
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
    };
  }, [last_updated, scan_interval]);

  // Format timestamp as actual time (not relative)
  const formatTimestamp = (isoString: string): string => {
    const date = new Date(isoString);
    const now = new Date();
    const isToday = date.toDateString() === now.toDateString();

    if (isToday) {
      return date.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
    }
    return date.toLocaleString([], {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Format countdown
  const formatCountdown = (seconds: number): string => {
    if (seconds <= 0) return 'refreshing...';
    if (seconds < 60) return `${seconds}s`;
    return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
  };

  // Get device type
  const getDeviceType = (device: Device): DeviceTypeFilter => {
    const model = device.model?.toUpperCase() || '';
    const productType = device.productType?.toLowerCase() || '';

    if (model.startsWith('MS') || productType === 'switch') return 'switch';
    if (model.startsWith('MV') || productType === 'camera') return 'camera';
    if (model.startsWith('MR') || productType === 'wireless')
      return 'wireless';
    if (model.startsWith('MT') || productType === 'sensor') return 'sensor';
    if (
      model.startsWith('MX') ||
      model.startsWith('Z') ||
      productType === 'appliance'
    )
      return 'appliance';
    return 'all';
  };

  // Filter devices based on current filters
  const filterDevices = (deviceList: Device[]): Device[] => {
    return deviceList.filter((device) => {
      // Type filter
      if (
        deviceTypeFilter !== 'all' &&
        getDeviceType(device) !== deviceTypeFilter
      ) {
        return false;
      }
      // Status filter
      if (
        statusFilter !== 'all' &&
        device.status?.toLowerCase() !== statusFilter
      ) {
        return false;
      }
      return true;
    });
  };

  const filteredDevices = filterDevices(devices);

  // Calculate metrics
  const onlineDevices = devices.filter(
    (d) => d.status?.toLowerCase() === 'online'
  ).length;
  const totalClients = clients.length || 0;
  const activeSSIDs = ssids.filter((s) => s.enabled).length;

  const toggleNetwork = (networkId: string) => {
    setExpandedNetworks((prev) => {
      const next = new Set(prev);
      if (next.has(networkId)) {
        next.delete(networkId);
      } else {
        next.add(networkId);
      }
      return next;
    });
  };

  const toggleType = (type: string) => {
    setExpandedTypes((prev) => {
      const next = new Set(prev);
      if (next.has(type)) {
        next.delete(type);
      } else {
        next.add(type);
      }
      return next;
    });
  };

  // Memoized helper functions to prevent DeviceRow re-renders
  const getDeviceIcon = useCallback((device: Device): string => {
    const type = getDeviceType(device);
    const model = device.model?.toUpperCase() || '';

    // Sensor-specific icons based on model
    if (type === 'sensor') {
      if (
        model.startsWith('MT10') ||
        model.startsWith('MT11') ||
        model.startsWith('MT15')
      ) {
        return '🌡️'; // Temperature sensor
      }
      if (model.startsWith('MT12')) {
        return '🚪'; // Door/open-close sensor
      }
      if (model.startsWith('MT14')) {
        return '💨'; // Air quality sensor
      }
      if (model.startsWith('MT20')) {
        return '🔘'; // Button sensor
      }
      if (model.startsWith('MT30')) {
        return '⚡'; // Power meter
      }
      return '📡'; // Default sensor
    }

    const icons: Record<DeviceTypeFilter, string> = {
      switch: '🔀', // Network switch
      camera: '📹', // Camera
      wireless: '📶', // Wireless AP
      sensor: '📡', // Default sensor (fallback)
      appliance: '🛡️', // Security appliance/firewall
      all: '📱',
    };
    return icons[type];
  }, []);

  const getDeviceTypeClass = useCallback((device: Device): string => {
    return getDeviceType(device);
  }, []);

  const getDeviceDetail = useCallback(
    (device: Device): string => {
      const type = getDeviceType(device);

      if (type === 'switch') {
        const activePorts =
          device.ports_statuses?.filter(
            (p) => p.status?.toLowerCase() === 'connected'
          ).length || 0;
        return `${activePorts} ports active`;
      }
      if (type === 'camera') {
        return device.status?.toLowerCase() === 'online'
          ? 'Recording'
          : 'Offline';
      }
      if (type === 'wireless') {
        // Get actual client count from clients connected to this device
        const clientCount = clients.filter(
          (c) => c.recentDeviceSerial === device.serial
        ).length;
        return `${clientCount} clients`;
      }
      if (type === 'sensor') {
        if (device.readings?.temperature != null) {
          const tempC = device.readings.temperature;
          const temp =
            temperatureUnit === 'fahrenheit'
              ? ((tempC * 9) / 5 + 32).toFixed(1)
              : tempC.toFixed(1);
          const unit = temperatureUnit === 'fahrenheit' ? '°F' : '°C';
          const humidity = device.readings.humidity ?? '--';
          return `${temp}${unit} / ${humidity}%`;
        }
        return 'Active';
      }
      return '';
    },
    [clients, temperatureUnit]
  );

  // Memoized click handler factory
  const handleDeviceClick = useCallback(
    (serial: string) => {
      setActiveView({ view: 'device', deviceId: serial });
    },
    [setActiveView]
  );

  const getDevicesForNetwork = (networkId: string): Device[] => {
    return filteredDevices.filter((d) => d.networkId === networkId);
  };

  const getDevicesByType = (type: DeviceTypeFilter): Device[] => {
    return filteredDevices.filter((d) => getDeviceType(d) === type);
  };

  // SSID toggle is now handled in SSIDView

  const renderDeviceTable = (deviceList: Device[]) => (
    <table className="device-table">
      <thead>
        <tr>
          <th>Device</th>
          <th>Model</th>
          <th>Serial</th>
          <th>Status</th>
          <th>IP Address</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {deviceList.map((device) => (
          <DeviceRow
            key={device.serial}
            device={device}
            onClick={() => handleDeviceClick(device.serial)}
            getDeviceIcon={getDeviceIcon}
            getDeviceTypeClass={getDeviceTypeClass}
            getDeviceDetail={getDeviceDetail}
          />
        ))}
        {deviceList.length === 0 && (
          <tr>
            <td colSpan={6} className="empty-table-message">
              No devices match your filters
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );

  return (
    <div>
      {/* Refresh Indicator */}
      {last_updated && (
        <div className="refresh-indicator">
          <span className="refresh-indicator-item">
            <span className="refresh-indicator-icon">🔄</span>
            Last: {formatTimestamp(last_updated)}
          </span>
          {countdown !== null && (
            <span className="refresh-indicator-item">
              <span className="refresh-indicator-icon">⏱️</span>
              Next: {formatCountdown(countdown)}
            </span>
          )}
        </div>
      )}

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatusCard title="Total Devices" value={devices.length} />
        <StatusCard title="Online" value={onlineDevices} variant="success" />
        <StatusCard
          title="Connected Clients"
          value={totalClients}
          onClick={() => setActiveView({ view: 'clients' })}
          clickable
        />
        <StatusCard
          title="Active SSIDs"
          value={activeSSIDs}
          onClick={() => setActiveView({ view: 'ssids' })}
          clickable
        />
      </div>

      {/* MQTT Status Card - Only shown when MQTT is enabled */}
      {mqtt?.enabled && (
        <MqttStatusCard
          mqttStats={mqtt.stats || null}
          relayDestinations={mqtt.relay_destinations || {}}
        />
      )}

      {/* Filters and View Toggle */}
      <div className="filter-controls">
        {/* View Mode Toggle */}
        <div className="view-mode-toggle">
          <button
            onClick={() => setViewMode('network')}
            className={`view-mode-btn ${
              viewMode === 'network' ? 'active' : ''
            }`}
          >
            🌐 By Network
          </button>
          <button
            onClick={() => setViewMode('type')}
            className={`view-mode-btn ${viewMode === 'type' ? 'active' : ''}`}
          >
            📦 By Type
          </button>
        </div>

        {/* Device Type Filter */}
        <select
          value={deviceTypeFilter}
          onChange={(e) =>
            setDeviceTypeFilter(e.target.value as DeviceTypeFilter)
          }
          className="filter-select"
        >
          {DEVICE_TYPES.map((type) => (
            <option key={type.value} value={type.value}>
              {type.icon} {type.label}
            </option>
          ))}
        </select>

        {/* Status Filter */}
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
          className="filter-select"
        >
          {STATUS_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        {/* Filter indicator */}
        {(deviceTypeFilter !== 'all' || statusFilter !== 'all') && (
          <button
            onClick={() => {
              setDeviceTypeFilter('all');
              setStatusFilter('all');
            }}
            className="clear-filters-btn"
          >
            ✕ Clear Filters ({filteredDevices.length}/{devices.length})
          </button>
        )}
      </div>

      {/* View by Network */}
      {viewMode === 'network' &&
        networks.map((network) => {
          const networkDevices = getDevicesForNetwork(network.id);
          const onlineCount = networkDevices.filter(
            (d) => d.status?.toLowerCase() === 'online'
          ).length;
          const isExpanded = expandedNetworks.has(network.id);

          return (
            <div key={network.id} className="network-card">
              <div
                className="network-header"
                onClick={() => toggleNetwork(network.id)}
              >
                <div className="title">
                  <span className="network-icon">🌐</span>
                  <h2>{network.name}</h2>
                  <span className="badge">
                    {onlineCount}/{networkDevices.length} online
                  </span>
                </div>
                <span
                  className={`expand-icon ${isExpanded ? 'expanded' : ''}`}
                >
                  ▼
                </span>
              </div>

              {isExpanded && renderDeviceTable(networkDevices)}
            </div>
          );
        })}

      {/* View by Type */}
      {viewMode === 'type' &&
        DEVICE_TYPES.filter((t) => t.value !== 'all').map((type) => {
          const typeDevices = getDevicesByType(type.value);
          if (typeDevices.length === 0 && deviceTypeFilter !== 'all')
            return null;

          const onlineCount = typeDevices.filter(
            (d) => d.status?.toLowerCase() === 'online'
          ).length;
          const isExpanded = expandedTypes.has(type.value);

          return (
            <div key={type.value} className="network-card">
              <div
                className="network-header"
                onClick={() => toggleType(type.value)}
              >
                <div className="title">
                  <span className="network-icon">{type.icon}</span>
                  <h2>{type.label}</h2>
                  <span className="badge">
                    {onlineCount}/{typeDevices.length} online
                  </span>
                </div>
                <span
                  className={`expand-icon ${isExpanded ? 'expanded' : ''}`}
                >
                  ▼
                </span>
              </div>

              {isExpanded && renderDeviceTable(typeDevices)}
            </div>
          );
        })}

      {/* Fallback: Show all devices if no networks and network view */}
      {viewMode === 'network' &&
        networks.length === 0 &&
        filteredDevices.length > 0 && (
          <div className="network-card">
            <div className="network-header">
              <div className="title">
                <span className="network-icon">🌐</span>
                <h2>All Devices</h2>
                <span className="badge">{onlineDevices} online</span>
              </div>
            </div>
            {renderDeviceTable(filteredDevices)}
          </div>
        )}

      {/* Empty State */}
      {filteredDevices.length === 0 && (
        <div className="empty-state">
          <div className="icon">📡</div>
          <h3>No Devices Found</h3>
          <p>
            {deviceTypeFilter !== 'all' || statusFilter !== 'all'
              ? 'No devices match your current filters.'
              : 'Your Meraki devices will appear here once discovered.'}
          </p>
        </div>
      )}
    </div>
  );
};

// Memoize the Dashboard to prevent unnecessary re-renders
// Only re-render when data meaningfully changes
const Dashboard = memo(DashboardComponent, (prevProps, nextProps) => {
  // Return true if props are equal (skip re-render)
  // Return false if props are different (trigger re-render)

  // Check if data reference changed
  if (prevProps.data === nextProps.data) {
    return true; // Same reference, skip re-render
  }

  // Compare key data elements
  const prevData = prevProps.data;
  const nextData = nextProps.data;

  // Compare counts
  if (
    prevData.devices?.length !== nextData.devices?.length ||
    prevData.networks?.length !== nextData.networks?.length ||
    prevData.clients?.length !== nextData.clients?.length
  ) {
    return false; // Different counts, re-render
  }

  // Compare device statuses
  const prevStatuses = prevData.devices
    ?.map((d) => `${d.serial}:${d.status}`)
    .join('|');
  const nextStatuses = nextData.devices
    ?.map((d) => `${d.serial}:${d.status}`)
    .join('|');
  if (prevStatuses !== nextStatuses) {
    return false; // Status changed, re-render
  }

  // Compare timestamps - allow re-render for countdown updates
  if (prevData.last_updated !== nextData.last_updated) {
    return false; // Timestamp changed, re-render for countdown
  }

  return true; // No meaningful changes, skip re-render
});

export default Dashboard;
