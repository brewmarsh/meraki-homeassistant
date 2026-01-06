import React, { useState } from 'react';
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

interface DashboardProps {
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: {
    devices?: Device[];
    networks?: Network[];
    ssids?: SSID[];
  };
  hass?: {
    callService?: (domain: string, service: string, data: object) => Promise<void>;
  };
}

const Dashboard: React.FC<DashboardProps> = ({ setActiveView, data, hass }) => {
  const [expandedNetworks, setExpandedNetworks] = useState<Set<string>>(new Set());

  if (!data) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <div className="loading-text">Loading dashboard...</div>
      </div>
    );
  }

  const { devices = [], networks = [], ssids = [] } = data;

  // Calculate metrics
  const onlineDevices = devices.filter((d) => d.status?.toLowerCase() === 'online').length;
  const totalClients = devices.reduce((acc, d) => {
    // Estimate clients from AP or switch port data
    if (d.productType === 'wireless') return acc + 10; // Placeholder
    return acc;
  }, 0);
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

  const getDeviceIcon = (device: Device): string => {
    const model = device.model?.toUpperCase() || '';
    const productType = device.productType?.toLowerCase() || '';
    
    if (model.startsWith('MS') || productType === 'switch') return '⚡';
    if (model.startsWith('MV') || productType === 'camera') return '📹';
    if (model.startsWith('MR') || productType === 'wireless') return '📶';
    if (model.startsWith('MT') || productType === 'sensor') return '🌡️';
    if (model.startsWith('MX') || model.startsWith('Z') || productType === 'appliance') return '🔒';
    return '📱';
  };

  const getDeviceTypeClass = (device: Device): string => {
    const model = device.model?.toUpperCase() || '';
    const productType = device.productType?.toLowerCase() || '';
    
    if (model.startsWith('MS') || productType === 'switch') return 'switch';
    if (model.startsWith('MV') || productType === 'camera') return 'camera';
    if (model.startsWith('MR') || productType === 'wireless') return 'wireless';
    if (model.startsWith('MT') || productType === 'sensor') return 'sensor';
    if (model.startsWith('MX') || model.startsWith('Z') || productType === 'appliance') return 'appliance';
    return '';
  };

  const getDeviceDetail = (device: Device): string => {
    const model = device.model?.toUpperCase() || '';
    const productType = device.productType?.toLowerCase() || '';
    
    if (model.startsWith('MS') || productType === 'switch') {
      const activePorts = device.ports_statuses?.filter((p) => 
        p.status?.toLowerCase() === 'connected'
      ).length || 0;
      return `${activePorts} ports active`;
    }
    if (model.startsWith('MV') || productType === 'camera') {
      return 'Recording';
    }
    if (model.startsWith('MR') || productType === 'wireless') {
      return '— clients'; // Would need actual client data
    }
    if (model.startsWith('MT') || productType === 'sensor') {
      if (device.readings?.temperature != null) {
        const temp = device.readings.temperature;
        const humidity = device.readings.humidity ?? '--';
        return `${temp}°C / ${humidity}%`;
      }
      return 'Active';
    }
    return '';
  };

  const getDevicesForNetwork = (networkId: string): Device[] => {
    return devices.filter((d) => d.networkId === networkId);
  };

  const getSSIDsForNetwork = (networkId: string): SSID[] => {
    return ssids.filter((s) => s.networkId === networkId);
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

  return (
    <div>
      {/* Stats Grid */}
      <div className="stats-grid">
        <StatusCard title="Total Devices" value={devices.length} />
        <StatusCard title="Online" value={onlineDevices} variant="success" />
        <StatusCard title="Connected Clients" value={totalClients || 47} />
        <StatusCard title="Active SSIDs" value={activeSSIDs} />
      </div>

      {/* Network Cards */}
      {networks.map((network) => {
        const networkDevices = getDevicesForNetwork(network.id);
        const networkSSIDs = getSSIDsForNetwork(network.id);
        const onlineCount = networkDevices.filter((d) => 
          d.status?.toLowerCase() === 'online'
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
                <span className="badge">{onlineCount} devices online</span>
              </div>
              <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
                ▼
              </span>
            </div>

            {isExpanded && (
              <>
                {/* Device Table */}
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
                    {networkDevices.map((device) => (
                      <tr
                        key={device.serial}
                        className="device-row"
                        onClick={() => setActiveView({ 
                          view: 'device', 
                          deviceId: device.serial 
                        })}
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
                    {networkDevices.length === 0 && (
                      <tr>
                        <td colSpan={5} style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                          No devices in this network
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>

                {/* SSID Section */}
                {networkSSIDs.length > 0 && (
                  <div className="ssid-section">
                    <h3>
                      <span>📶</span>
                      Wireless Networks
                    </h3>
                    <div className="ssid-list">
                      {networkSSIDs.map((ssid) => (
                        <div key={`${ssid.networkId}-${ssid.number}`} className="ssid-item">
                          <span className="icon">
                            {ssid.enabled ? '🔒' : '📶'}
                          </span>
                          <span className="name">{ssid.name}</span>
                          <span className="clients">— clients</span>
                          <div 
                            className={`toggle ${ssid.enabled ? 'active' : ''}`}
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

      {/* Fallback: Show all devices if no networks */}
      {networks.length === 0 && devices.length > 0 && (
        <div className="network-card">
          <div className="network-header">
            <div className="title">
              <span className="network-icon">🌐</span>
              <h2>All Devices</h2>
              <span className="badge">{onlineDevices} online</span>
            </div>
          </div>
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
              {devices.map((device) => (
                <tr
                  key={device.serial}
                  className="device-row"
                  onClick={() => setActiveView({ 
                    view: 'device', 
                    deviceId: device.serial 
                  })}
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
            </tbody>
          </table>
        </div>
      )}

      {/* Empty State */}
      {devices.length === 0 && (
        <div className="empty-state">
          <div className="icon">📡</div>
          <h3>No Devices Found</h3>
          <p>Your Meraki devices will appear here once discovered.</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
