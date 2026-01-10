import React, { memo } from 'react';

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
  recentDeviceMac?: string;
  ssid?: string;
  vlan?: number;
  switchport?: string;
  status?: string;
  usage?: { sent: number; recv: number };
  networkId?: string;
  ha_device_id?: string;
  is_blocked?: boolean;
}

interface ClientDetailViewProps {
  client: Client;
  onBack: () => void;
  onNavigateToDevice?: () => void;
}

const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return '—';
  const date = new Date(dateString);
  return date.toLocaleString();
};

const getClientIcon = (client: Client): string => {
  const os = client.os?.toLowerCase() || '';
  const manufacturer = client.manufacturer?.toLowerCase() || '';

  if (os.includes('ios') || manufacturer.includes('apple')) return '📱';
  if (os.includes('android')) return '📱';
  if (os.includes('windows')) return '💻';
  if (os.includes('mac')) return '🖥️';
  if (os.includes('linux')) return '🐧';
  if (manufacturer.includes('amazon')) return '📺';
  if (manufacturer.includes('roku')) return '📺';
  if (manufacturer.includes('samsung')) return '📺';
  if (manufacturer.includes('sonos')) return '🔊';
  return '🔌';
};

const ClientDetailViewComponent: React.FC<ClientDetailViewProps> = ({
  client,
  onBack,
  onNavigateToDevice,
}) => {
  const connectionType = client.ssid
    ? 'wireless'
    : client.switchport
    ? 'wired'
    : 'unknown';

  return (
    <div>
      <button onClick={onBack} className="back-button">
        ← Back to Clients
      </button>

      {/* Client Header */}
      <div className="device-header">
        <div className="device-icon device-icon-gradient text-4xl">
          {getClientIcon(client)}
        </div>
        <div className="device-info">
          <h1>{client.description || client.mac}</h1>
          <div className="meta">
            <span
              className={`status-badge ${
                client.status === 'Online' ? 'status-online' : 'status-offline'
              }`}
            >
              {client.status || 'Unknown'}
            </span>
            {client.is_blocked && (
              <span className="status-badge status-alerting">Blocked</span>
            )}
            <span className="detail-badge">
              {connectionType === 'wireless' ? '📶 Wireless' : '🔌 Wired'}
            </span>
          </div>
        </div>
        {onNavigateToDevice && client.ha_device_id && (
          <button
            onClick={onNavigateToDevice}
            className="btn btn-primary"
            style={{ marginLeft: 'auto' }}
          >
            View in Home Assistant →
          </button>
        )}
      </div>

      {/* Client Details Grid */}
      <div
        className="detail-grid"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1rem',
          marginTop: '1.5rem',
        }}
      >
        {/* Network Information */}
        <div className="network-card">
          <h3 className="section-title">📡 Network Information</h3>
          <div className="detail-list">
            <div className="detail-item">
              <span className="detail-label">IP Address</span>
              <span className="detail-value text-mono">
                {client.ip || '—'}
              </span>
            </div>
            {client.ip6 && (
              <div className="detail-item">
                <span className="detail-label">IPv6 Address</span>
                <span className="detail-value text-mono text-sm">
                  {client.ip6}
                </span>
              </div>
            )}
            <div className="detail-item">
              <span className="detail-label">MAC Address</span>
              <span className="detail-value text-mono">{client.mac}</span>
            </div>
            {client.vlan !== undefined && (
              <div className="detail-item">
                <span className="detail-label">VLAN</span>
                <span className="detail-value">{client.vlan}</span>
              </div>
            )}
            {client.networkId && (
              <div className="detail-item">
                <span className="detail-label">Network ID</span>
                <span className="detail-value text-mono text-sm">
                  {client.networkId}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Connection Information */}
        <div className="network-card">
          <h3 className="section-title">🔗 Connection</h3>
          <div className="detail-list">
            <div className="detail-item">
              <span className="detail-label">Connection Type</span>
              <span className="detail-value">
                {connectionType === 'wireless'
                  ? '📶 Wireless'
                  : connectionType === 'wired'
                  ? '🔌 Wired'
                  : '—'}
              </span>
            </div>
            {client.ssid && (
              <div className="detail-item">
                <span className="detail-label">SSID</span>
                <span className="detail-value">{client.ssid}</span>
              </div>
            )}
            {client.switchport && (
              <div className="detail-item">
                <span className="detail-label">Switchport</span>
                <span className="detail-value">Port {client.switchport}</span>
              </div>
            )}
            {client.recentDeviceName && (
              <div className="detail-item">
                <span className="detail-label">Connected To</span>
                <span className="detail-value">{client.recentDeviceName}</span>
              </div>
            )}
            {client.recentDeviceSerial && (
              <div className="detail-item">
                <span className="detail-label">Device Serial</span>
                <span className="detail-value text-mono">
                  {client.recentDeviceSerial}
                </span>
              </div>
            )}
            {client.recentDeviceMac && (
              <div className="detail-item">
                <span className="detail-label">Device MAC</span>
                <span className="detail-value text-mono">
                  {client.recentDeviceMac}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Device Information */}
        <div className="network-card">
          <h3 className="section-title">📋 Device Information</h3>
          <div className="detail-list">
            {client.manufacturer && (
              <div className="detail-item">
                <span className="detail-label">Manufacturer</span>
                <span className="detail-value">{client.manufacturer}</span>
              </div>
            )}
            {client.os && (
              <div className="detail-item">
                <span className="detail-label">Operating System</span>
                <span className="detail-value">{client.os}</span>
              </div>
            )}
            {client.user && (
              <div className="detail-item">
                <span className="detail-label">User</span>
                <span className="detail-value">{client.user}</span>
              </div>
            )}
            {client.description && client.description !== client.mac && (
              <div className="detail-item">
                <span className="detail-label">Hostname</span>
                <span className="detail-value">{client.description}</span>
              </div>
            )}
          </div>
        </div>

        {/* Usage Statistics */}
        <div className="network-card">
          <h3 className="section-title">📊 Usage Statistics</h3>
          <div className="detail-list">
            {client.usage && (
              <>
                <div className="detail-item">
                  <span className="detail-label">Data Sent</span>
                  <span className="detail-value">
                    <span className="text-success">↑</span>{' '}
                    {formatBytes(client.usage.sent)}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Data Received</span>
                  <span className="detail-value">
                    <span className="text-info">↓</span>{' '}
                    {formatBytes(client.usage.recv)}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Total Usage</span>
                  <span className="detail-value">
                    {formatBytes(client.usage.sent + client.usage.recv)}
                  </span>
                </div>
              </>
            )}
            {!client.usage && (
              <div className="detail-item">
                <span className="detail-label">Usage</span>
                <span className="detail-value text-muted">
                  No data available
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Timeline */}
        <div className="network-card">
          <h3 className="section-title">🕐 Timeline</h3>
          <div className="detail-list">
            <div className="detail-item">
              <span className="detail-label">First Seen</span>
              <span className="detail-value">
                {formatDate(client.firstSeen)}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Last Seen</span>
              <span className="detail-value">
                {formatDate(client.lastSeen)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ClientDetailView = memo(ClientDetailViewComponent);

export default ClientDetailView;
