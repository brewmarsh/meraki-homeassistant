import React, { memo, useCallback } from 'react';

// === Memoized Sub-components for granular updates ===

// SSID Client row props
interface SSIDClientRowProps {
  client: {
    id: string;
    mac: string;
    description?: string;
    ip?: string;
    manufacturer?: string;
    os?: string;
    lastSeen?: string;
    usage?: { sent: number; recv: number };
  };
  onClick?: () => void;
  formatLastSeen: (dateStr?: string) => string;
  formatBytes: (bytes: number) => string;
}

// Memoized client row for SSID view - only re-renders when this client changes
const SSIDClientRow = memo<SSIDClientRowProps>(
  ({ client, onClick, formatLastSeen, formatBytes }) => (
    <tr
      className={onClick ? 'device-row clickable' : 'device-row'}
      onClick={onClick}
    >
      <td>
        <div className="device-name-cell">
          <span className="text-xl">
            {client.os?.toLowerCase().includes('android')
              ? '📱'
              : client.os?.toLowerCase().includes('ios') ||
                client.os?.toLowerCase().includes('apple')
              ? '🍎'
              : client.os?.toLowerCase().includes('windows')
              ? '💻'
              : '📱'}
          </span>
          <div>
            <div className="name">{client.description || client.mac}</div>
            {client.description && (
              <div className="text-xs text-muted text-mono">{client.mac}</div>
            )}
          </div>
        </div>
      </td>
      <td className="text-mono text-sm">{client.ip || '—'}</td>
      <td>{client.manufacturer || '—'}</td>
      <td>{formatLastSeen(client.lastSeen)}</td>
      <td>
        {client.usage ? (
          <span className="text-sm">
            ↓{formatBytes(client.usage.recv)} ↑{formatBytes(client.usage.sent)}
          </span>
        ) : (
          '—'
        )}
      </td>
    </tr>
  ),
  (prev, next) =>
    prev.client.id === next.client.id &&
    prev.client.mac === next.client.mac &&
    prev.client.description === next.client.description &&
    prev.client.ip === next.client.ip &&
    prev.client.manufacturer === next.client.manufacturer &&
    prev.client.os === next.client.os &&
    prev.client.lastSeen === next.client.lastSeen &&
    prev.client.usage?.sent === next.client.usage?.sent &&
    prev.client.usage?.recv === next.client.usage?.recv
);

interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
  entity_id?: string;
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

interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
}

interface SSIDViewProps {
  ssid: SSID;
  clients: Client[];
  network?: Network;
  hass: any;
  onBack: () => void;
  onClientClick?: (clientId: string) => void;
}

const SSIDViewComponent: React.FC<SSIDViewProps> = ({
  ssid,
  clients,
  network,
  hass,
  onBack,
  onClientClick,
}) => {
  // Filter clients connected to this SSID
  const ssidClients = clients.filter((c) => c.ssid === ssid.name);

  const handleSSIDToggle = async () => {
    if (!ssid.entity_id || !hass) {
      console.error('Cannot toggle SSID: missing entity_id or hass');
      return;
    }

    try {
      const service = ssid.enabled ? 'turn_off' : 'turn_on';
      await hass.callService('switch', service, {
        entity_id: ssid.entity_id,
      });
      // Reload after a short delay to let HA update
      setTimeout(() => window.location.reload(), 1500);
    } catch (e) {
      console.error('Failed to toggle SSID:', e);
    }
  };

  const formatBytes = useCallback((bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }, []);

  const formatLastSeen = useCallback((dateStr?: string): string => {
    if (!dateStr) return 'Unknown';
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  }, []);

  // Calculate total usage for this SSID
  const totalUsage = ssidClients.reduce(
    (acc, client) => ({
      sent: acc.sent + (client.usage?.sent || 0),
      recv: acc.recv + (client.usage?.recv || 0),
    }),
    { sent: 0, recv: 0 }
  );

  return (
    <div className="ssid-view">
      {/* Header */}
      <div className="device-header">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <div className="device-icon wireless">📶</div>
        <div className="device-info">
          <h1>{ssid.name}</h1>
          <div className="meta">
            {network && <span>Network: {network.name}</span>}
            <span>SSID #{ssid.number}</span>
            <span className={ssid.enabled ? 'text-success' : 'text-muted'}>
              {ssid.enabled ? '● Broadcasting' : '○ Disabled'}
            </span>
          </div>
        </div>
      </div>

      {/* SSID Status & Control Card */}
      <div className="info-card">
        <h3>🎛️ SSID Control</h3>
        <div className={`ssid-control-panel ${ssid.enabled ? 'enabled' : ''}`}>
          <div className="ssid-control-info">
            <div
              className={`ssid-control-status ${
                ssid.enabled ? 'text-success' : 'text-muted'
              }`}
            >
              {ssid.enabled ? '● SSID is Enabled' : '○ SSID is Disabled'}
            </div>
            <div className="ssid-control-desc text-muted text-sm">
              {ssid.enabled
                ? 'Clients can connect to this wireless network'
                : 'This network is not broadcasting'}
            </div>
          </div>
          <div
            className={`toggle ${ssid.enabled ? 'active' : ''} clickable`}
            onClick={handleSSIDToggle}
            title={
              ssid.enabled ? 'Click to disable SSID' : 'Click to enable SSID'
            }
          />
        </div>
      </div>

      {/* SSID Statistics */}
      <div className="info-card">
        <h3>📊 Statistics</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="label">Connected Clients</div>
            <div className="value">{ssidClients.length}</div>
          </div>
          <div className="stat-card">
            <div className="label">Data Sent</div>
            <div className="value success">{formatBytes(totalUsage.sent)}</div>
          </div>
          <div className="stat-card">
            <div className="label">Data Received</div>
            <div className="value">{formatBytes(totalUsage.recv)}</div>
          </div>
          <div className="stat-card">
            <div className="label">Total Traffic</div>
            <div className="value">
              {formatBytes(totalUsage.sent + totalUsage.recv)}
            </div>
          </div>
        </div>
      </div>

      {/* Connected Clients Table */}
      <div className="info-card">
        <h3>👥 Connected Clients ({ssidClients.length})</h3>
        {ssidClients.length > 0 ? (
          <table className="device-table">
            <thead>
              <tr>
                <th>Client</th>
                <th>IP Address</th>
                <th>Manufacturer</th>
                <th>Last Seen</th>
                <th>Usage</th>
              </tr>
            </thead>
            <tbody>
              {ssidClients.map((client) => (
                <SSIDClientRow
                  key={client.id || client.mac}
                  client={client}
                  onClick={
                    onClientClick
                      ? () => onClientClick(client.id || client.mac)
                      : undefined
                  }
                  formatLastSeen={formatLastSeen}
                  formatBytes={formatBytes}
                />
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">📴</div>
            <p>No clients connected to this SSID</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Memoize SSIDView to prevent unnecessary re-renders
const SSIDView = memo(SSIDViewComponent, (prevProps, nextProps) => {
  // Re-render if SSID or client count changes
  if (prevProps.ssid.number !== nextProps.ssid.number) return false;
  if (prevProps.ssid.networkId !== nextProps.ssid.networkId) return false;
  if (prevProps.ssid.enabled !== nextProps.ssid.enabled) return false;

  // Compare client count for this SSID
  const prevClients = prevProps.clients.filter(
    (c) => c.ssid === prevProps.ssid.name
  ).length;
  const nextClients = nextProps.clients.filter(
    (c) => c.ssid === nextProps.ssid.name
  ).length;
  if (prevClients !== nextClients) return false;

  return true;
});

export default SSIDView;
