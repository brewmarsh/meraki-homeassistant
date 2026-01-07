import React, { useState, useEffect, useRef } from 'react';
import StatusCard from './StatusCard';

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
}

interface DashboardProps {
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: {
    devices?: Device[];
    networks?: Network[];
    ssids?: SSID[];
    clients?: Client[];
    scan_interval?: number;
    last_updated?: string;
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
  { value: 'switch', label: 'Switches', icon: '⚡' },
  { value: 'camera', label: 'Cameras', icon: '📹' },
  { value: 'wireless', label: 'Wireless', icon: '📶' },
  { value: 'sensor', label: 'Sensors', icon: '🌡️' },
  { value: 'appliance', label: 'Appliances', icon: '🔒' },
];

const STATUS_OPTIONS: { value: StatusFilter; label: string }[] = [
  { value: 'all', label: 'All Status' },
  { value: 'online', label: 'Online' },
  { value: 'offline', label: 'Offline' },
  { value: 'alerting', label: 'Alerting' },
  { value: 'dormant', label: 'Dormant' },
];

const Dashboard: React.FC<DashboardProps> = ({
  setActiveView,
  data,
  hass,
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
    scan_interval = 60,
    last_updated,
  } = data;

  // Countdown state for next refresh
  const [countdown, setCountdown] = useState<number | null>(null);
  const countdownRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Calculate and update countdown
  useEffect(() => {
    if (!last_updated || !scan_interval) {
      setCountdown(null);
      return;
    }

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

  const getDeviceIcon = (device: Device): string => {
    const type = getDeviceType(device);
    const icons: Record<DeviceTypeFilter, string> = {
      switch: '⚡',
      camera: '📹',
      wireless: '📶',
      sensor: '🌡️',
      appliance: '🔒',
      all: '📱',
    };
    return icons[type];
  };

  const getDeviceTypeClass = (device: Device): string => {
    return getDeviceType(device);
  };

  const getDeviceDetail = (device: Device): string => {
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
      return '— clients';
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
  };

  const getDevicesForNetwork = (networkId: string): Device[] => {
    return filteredDevices.filter((d) => d.networkId === networkId);
  };

  const getSSIDsForNetwork = (networkId: string): SSID[] => {
    return ssids.filter((s) => s.networkId === networkId);
  };

  const getDevicesByType = (type: DeviceTypeFilter): Device[] => {
    return filteredDevices.filter((d) => getDeviceType(d) === type);
  };

  const handleSSIDToggle = async (ssid: SSID) => {
    if (!hass?.callService || !ssid.entity_id) return;

    try {
      await hass.callService('switch', ssid.enabled ? 'turn_off' : 'turn_on', {
        entity_id: ssid.entity_id,
      });
    } catch (error) {
      console.error('Failed to toggle SSID:', error);
    }
  };

  const renderDeviceTable = (deviceList: Device[]) => (
    <table className="device-table">
      <thead>
        <tr>
          <th>Device</th>
          <th>Model</th>
          <th>Status</th>
          <th>IP Address</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {deviceList.map((device) => (
          <tr
            key={device.serial}
            className="device-row"
            onClick={() =>
              setActiveView({
                view: 'device',
                deviceId: device.serial,
              })
            }
          >
            <td>
              <div className="device-name-cell">
                <div className={`device-icon ${getDeviceTypeClass(device)}`}>
                  {getDeviceIcon(device)}
                </div>
                <span className="name">{device.name || device.serial}</span>
              </div>
            </td>
            <td className="device-model">{device.model || '—'}</td>
            <td>
              <div className={`status-badge ${device.status?.toLowerCase()}`}>
                <div className="status-dot"></div>
                <span>{device.status || 'Unknown'}</span>
              </div>
            </td>
            <td className="device-model">{device.lanIp || '—'}</td>
            <td>
              <span className="detail-badge">
                {getDeviceDetail(device) || '—'}
              </span>
            </td>
          </tr>
        ))}
        {deviceList.length === 0 && (
          <tr>
            <td
              colSpan={5}
              style={{ textAlign: 'center', color: 'var(--text-muted)' }}
            >
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
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            alignItems: 'center',
            gap: '16px',
            marginBottom: '12px',
            fontSize: '12px',
            color: 'var(--text-muted)',
            opacity: 0.8,
          }}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ fontSize: '10px' }}>🔄</span>
            Last: {formatTimestamp(last_updated)}
          </span>
          {countdown !== null && (
            <span
              style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              <span style={{ fontSize: '10px' }}>⏱️</span>
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
        <StatusCard title="Active SSIDs" value={activeSSIDs} />
      </div>

      {/* Filters and View Toggle */}
      <div
        style={{
          display: 'flex',
          gap: '12px',
          marginBottom: '20px',
          flexWrap: 'wrap',
          alignItems: 'center',
        }}
      >
        {/* View Mode Toggle */}
        <div
          style={{
            display: 'flex',
            gap: '4px',
            background: 'var(--bg-secondary)',
            borderRadius: 'var(--radius-md)',
            padding: '4px',
          }}
        >
          <button
            onClick={() => setViewMode('network')}
            style={{
              padding: '8px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background:
                viewMode === 'network' ? 'var(--primary)' : 'transparent',
              color:
                viewMode === 'network' ? 'white' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 500,
              fontSize: '13px',
            }}
          >
            🌐 By Network
          </button>
          <button
            onClick={() => setViewMode('type')}
            style={{
              padding: '8px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background:
                viewMode === 'type' ? 'var(--primary)' : 'transparent',
              color: viewMode === 'type' ? 'white' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 500,
              fontSize: '13px',
            }}
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
          style={{
            padding: '8px 12px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border)',
            background: 'var(--bg-secondary)',
            color: 'var(--text-primary)',
            fontSize: '13px',
            cursor: 'pointer',
          }}
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
          style={{
            padding: '8px 12px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border)',
            background: 'var(--bg-secondary)',
            color: 'var(--text-primary)',
            fontSize: '13px',
            cursor: 'pointer',
          }}
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
            style={{
              padding: '8px 12px',
              borderRadius: 'var(--radius-md)',
              border: 'none',
              background: 'var(--warning)',
              color: 'white',
              fontSize: '12px',
              cursor: 'pointer',
              fontWeight: 500,
            }}
          >
            ✕ Clear Filters ({filteredDevices.length}/{devices.length})
          </button>
        )}
      </div>

      {/* View by Network */}
      {viewMode === 'network' &&
        networks.map((network) => {
          const networkDevices = getDevicesForNetwork(network.id);
          const networkSSIDs = getSSIDsForNetwork(network.id);
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

              {isExpanded && (
                <>
                  {renderDeviceTable(networkDevices)}

                  {/* SSID Section */}
                  {networkSSIDs.length > 0 && (
                    <div className="ssid-section">
                      <h3>
                        <span>📶</span>
                        Wireless Networks
                      </h3>
                      <div className="ssid-list">
                        {networkSSIDs.map((ssid) => (
                          <div
                            key={`${ssid.networkId}-${ssid.number}`}
                            className="ssid-item"
                          >
                            <span className="icon">
                              {ssid.enabled ? '🔒' : '📶'}
                            </span>
                            <span className="name">{ssid.name}</span>
                            <span className="clients">— clients</span>
                            <div
                              className={`toggle ${
                                ssid.enabled ? 'active' : ''
                              }`}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleSSIDToggle(ssid);
                              }}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
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

export default Dashboard;
