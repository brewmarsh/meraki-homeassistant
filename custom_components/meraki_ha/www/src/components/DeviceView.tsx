import React from 'react';
import SwitchPortVisualization from './SwitchPortVisualization';
import SensorReading from './SensorReading';

interface PortStatus {
  portId: string;
  status: string;
  enabled: boolean;
  speed?: string;
  duplex?: string;
  usageInKb?: { total: number };
  poe?: { isAllocated?: boolean; enabled?: boolean };
  powerUsageInWh?: number;
  clientName?: string;
  clientMac?: string;
  vlan?: number;
}

interface Device {
  name: string;
  model: string;
  serial: string;
  firmware?: string;
  status: string;
  lanIp?: string;
  mac?: string;
  productType?: string;
  status_messages?: string[];
  entities?: Array<{ entity_id: string; name: string; state: string }>;
  ports_statuses?: PortStatus[];
  readings?: {
    temperature?: number;
    humidity?: number;
    battery?: number;
  };
  uptime?: number;
  lastReportedAt?: string;
}

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: {
    devices: Device[];
  };
}

const DeviceView: React.FC<DeviceViewProps> = ({
  activeView,
  setActiveView,
  data,
}) => {
  const device = data.devices.find((d) => d.serial === activeView.deviceId);

  if (!device) {
    return (
      <div>
        <button
          onClick={() => setActiveView({ view: 'dashboard' })}
          className="back-button"
        >
          ← Back to Dashboard
        </button>
        <div className="empty-state">
          <div className="icon">❓</div>
          <h3>Device Not Found</h3>
          <p>The requested device could not be found.</p>
        </div>
      </div>
    );
  }

  const {
    name,
    model = '',
    serial,
    firmware,
    status,
    lanIp,
    mac,
    productType,
    status_messages = [],
    entities = [],
    ports_statuses = [],
    readings,
    uptime,
    lastReportedAt,
  } = device;

  const getDeviceIcon = (): string => {
    const modelUpper = model.toUpperCase();
    const type = productType?.toLowerCase() || '';
    
    if (modelUpper.startsWith('MS') || type === 'switch') return '⚡';
    if (modelUpper.startsWith('MV') || type === 'camera') return '📹';
    if (modelUpper.startsWith('MR') || type === 'wireless') return '📶';
    if (modelUpper.startsWith('MT') || type === 'sensor') return '🌡️';
    if (modelUpper.startsWith('MX') || modelUpper.startsWith('Z') || type === 'appliance') return '🔒';
    return '📱';
  };

  const getDeviceTypeClass = (): string => {
    const modelUpper = model.toUpperCase();
    const type = productType?.toLowerCase() || '';
    
    if (modelUpper.startsWith('MS') || type === 'switch') return 'switch';
    if (modelUpper.startsWith('MV') || type === 'camera') return 'camera';
    if (modelUpper.startsWith('MR') || type === 'wireless') return 'wireless';
    if (modelUpper.startsWith('MT') || type === 'sensor') return 'sensor';
    if (modelUpper.startsWith('MX') || modelUpper.startsWith('Z') || type === 'appliance') return 'appliance';
    return '';
  };

  const isSwitch = model.toUpperCase().startsWith('MS') || productType === 'switch';
  const isSensor = model.toUpperCase().startsWith('MT') || productType === 'sensor';
  const isCamera = model.toUpperCase().startsWith('MV') || productType === 'camera';
  const isWireless = model.toUpperCase().startsWith('MR') || productType === 'wireless';

  const formatUptime = (seconds?: number): string => {
    if (!seconds) return '—';
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    return `${days} days, ${hours} hours`;
  };

  const formatLastSeen = (timestamp?: string): string => {
    if (!timestamp) return 'Just now';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours} hours ago`;
    return `${Math.floor(diffHours / 24)} days ago`;
  };

  const handleEntityClick = (entityId: string) => {
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    document.body.dispatchEvent(event);
  };

  // Calculate PoE stats for switches
  const poePorts = ports_statuses.filter((p) => p.poe?.isAllocated || p.poe?.enabled);
  const totalPoePower = ports_statuses.reduce((acc, p) => acc + (p.powerUsageInWh || 0), 0);

  return (
    <div>
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="back-button"
      >
        ← Back to Dashboard
      </button>

      {/* Device Header */}
      <div className="device-header">
        <div className={`device-icon ${getDeviceTypeClass()}`}>
          {getDeviceIcon()}
        </div>
        <div className="device-info">
          <h1>{name || serial}</h1>
          <div className="meta">
            <span><strong>Model:</strong> {model}</span>
            <span><strong>Serial:</strong> {serial}</span>
            {firmware && <span><strong>Firmware:</strong> {firmware}</span>}
          </div>
        </div>
        <div className={`status-pill ${status?.toLowerCase()}`}>
          <div className="dot"></div>
          {status || 'Unknown'}
        </div>
      </div>

      {/* Info Cards Grid */}
      <div className="cards-grid">
        <div className="info-card">
          <h3>ℹ️ Device Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <div className="label">LAN IP</div>
              <div className="value">{lanIp || '—'}</div>
            </div>
            <div className="info-item">
              <div className="label">MAC Address</div>
              <div className="value mono">{mac || '—'}</div>
            </div>
            <div className="info-item">
              <div className="label">Uptime</div>
              <div className="value">{formatUptime(uptime)}</div>
            </div>
            <div className="info-item">
              <div className="label">Last Seen</div>
              <div className="value">{formatLastSeen(lastReportedAt)}</div>
            </div>
          </div>
        </div>

        {/* Switch-specific Power Summary */}
        {isSwitch && ports_statuses.length > 0 && (
          <div className="info-card">
            <h3>⚡ Power Summary</h3>
            <div className="info-grid">
              <div className="info-item">
                <div className="label">Total PoE Power</div>
                <div className="value warning">{totalPoePower.toFixed(1)} W</div>
              </div>
              <div className="info-item">
                <div className="label">PoE Budget</div>
                <div className="value">370 W</div>
              </div>
              <div className="info-item">
                <div className="label">Active PoE Ports</div>
                <div className="value">{poePorts.length} of {ports_statuses.length}</div>
              </div>
              <div className="info-item">
                <div className="label">Utilization</div>
                <div className="value success">{((totalPoePower / 370) * 100).toFixed(1)}%</div>
              </div>
            </div>
          </div>
        )}

        {/* Sensor-specific Battery Info */}
        {isSensor && readings && (
          <div className="info-card">
            <h3>🔋 Sensor Status</h3>
            <div className="info-grid">
              <div className="info-item">
                <div className="label">Battery</div>
                <div className="value success">{readings.battery || 98}%</div>
              </div>
              <div className="info-item">
                <div className="label">Last Update</div>
                <div className="value">{formatLastSeen(lastReportedAt)}</div>
              </div>
              <div className="info-item">
                <div className="label">Network</div>
                <div className="value">Main Office</div>
              </div>
              <div className="info-item">
                <div className="label">Uptime</div>
                <div className="value">{formatUptime(uptime)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Switch Port Visualization */}
      {isSwitch && ports_statuses.length > 0 && (
        <SwitchPortVisualization
          deviceName={name || serial}
          model={model}
          ports={ports_statuses}
        />
      )}

      {/* Sensor Readings */}
      {isSensor && readings && (
        <div className="readings-grid">
          {readings.temperature != null && (
            <SensorReading
              type="temperature"
              value={readings.temperature}
              min={0}
              max={50}
              status="normal"
            />
          )}
          {readings.humidity != null && (
            <SensorReading
              type="humidity"
              value={readings.humidity}
              min={0}
              max={100}
              status="normal"
            />
          )}
        </div>
      )}

      {/* Status Messages */}
      {status_messages.length > 0 && (
        <div className="info-card" style={{ borderLeft: '4px solid var(--warning)' }}>
          <h3>⚠️ Status Messages</h3>
          <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--text-secondary)' }}>
            {status_messages.map((msg: string, index: number) => (
              <li key={index} style={{ marginBottom: '8px' }}>
                {msg}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Entities */}
      {entities.length > 0 && (
        <div className="info-card">
          <h3>🔗 Entities</h3>
          <table className="device-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Entity ID</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody>
              {entities.map((entity) => (
                <tr
                  key={entity.entity_id}
                  className="device-row"
                  onClick={() => handleEntityClick(entity.entity_id)}
                >
                  <td>{entity.name}</td>
                  <td style={{ fontFamily: 'monospace', fontSize: '13px', color: 'var(--text-muted)' }}>
                    {entity.entity_id}
                  </td>
                  <td>
                    <span className="detail-badge">{entity.state}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Camera-specific View */}
      {isCamera && (
        <div className="info-card">
          <h3>📹 Camera</h3>
          <div style={{ 
            background: 'var(--bg-primary)', 
            borderRadius: 'var(--radius-md)',
            padding: '40px',
            textAlign: 'center',
            color: 'var(--text-muted)'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>📹</div>
            <p>Camera stream available through Home Assistant's camera entity</p>
            <p style={{ fontSize: '13px', marginTop: '8px' }}>
              Click on the camera entity to view live stream
            </p>
          </div>
        </div>
      )}

      {/* Wireless AP-specific View */}
      {isWireless && (
        <div className="info-card">
          <h3>📶 Wireless Access Point</h3>
          <div className="info-grid">
            <div className="info-item">
              <div className="label">Connected Clients</div>
              <div className="value primary">—</div>
            </div>
            <div className="info-item">
              <div className="label">Radio Channels</div>
              <div className="value">2.4 GHz / 5 GHz</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DeviceView;
