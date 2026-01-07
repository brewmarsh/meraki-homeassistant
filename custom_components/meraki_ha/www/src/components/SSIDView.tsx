import React from 'react';

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

const SSIDView: React.FC<SSIDViewProps> = ({
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

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const formatLastSeen = (dateStr?: string): string => {
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
  };

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
      <div className="view-header">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <div style={{ flex: 1, marginLeft: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '24px' }}>📶</span>
            <div>
              <h2 style={{ margin: 0, fontSize: '20px' }}>{ssid.name}</h2>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  marginTop: '4px',
                  color: 'var(--text-muted)',
                  fontSize: '13px',
                }}
              >
                {network && <span>Network: {network.name}</span>}
                <span>SSID #{ssid.number}</span>
                <span>•</span>
                <span
                  style={{
                    color: ssid.enabled
                      ? 'var(--success)'
                      : 'var(--text-muted)',
                  }}
                >
                  {ssid.enabled ? '● Broadcasting' : '○ Disabled'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SSID Status & Control Card */}
      <div className="card" style={{ marginTop: '24px' }}>
        <div className="card-header">
          <h3>SSID Control</h3>
        </div>
        <div className="card-content">
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '16px 20px',
              background: ssid.enabled
                ? 'var(--success-light)'
                : 'var(--bg-secondary)',
              borderRadius: 'var(--radius-md)',
            }}
          >
            <div>
              <div
                style={{
                  fontSize: '16px',
                  fontWeight: 500,
                  color: ssid.enabled ? 'var(--success)' : 'var(--text-muted)',
                }}
              >
                {ssid.enabled ? '● SSID is Enabled' : '○ SSID is Disabled'}
              </div>
              <div
                style={{
                  fontSize: '13px',
                  color: 'var(--text-muted)',
                  marginTop: '4px',
                }}
              >
                {ssid.enabled
                  ? 'Clients can connect to this wireless network'
                  : 'This network is not broadcasting'}
              </div>
            </div>
            <div
              className={`toggle ${ssid.enabled ? 'active' : ''}`}
              onClick={handleSSIDToggle}
              title={
                ssid.enabled ? 'Click to disable SSID' : 'Click to enable SSID'
              }
              style={{ cursor: 'pointer' }}
            />
          </div>
        </div>
      </div>

      {/* SSID Statistics */}
      <div className="card" style={{ marginTop: '16px' }}>
        <div className="card-header">
          <h3>Statistics</h3>
        </div>
        <div className="card-content">
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '24px',
            }}
          >
            <div>
              <div
                style={{
                  fontSize: '11px',
                  color: 'var(--text-muted)',
                  textTransform: 'uppercase',
                  marginBottom: '4px',
                }}
              >
                Connected Clients
              </div>
              <div
                style={{
                  fontSize: '24px',
                  fontWeight: 600,
                  color: 'var(--primary)',
                }}
              >
                {ssidClients.length}
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: '11px',
                  color: 'var(--text-muted)',
                  textTransform: 'uppercase',
                  marginBottom: '4px',
                }}
              >
                Data Sent
              </div>
              <div style={{ fontSize: '24px', fontWeight: 600 }}>
                {formatBytes(totalUsage.sent)}
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: '11px',
                  color: 'var(--text-muted)',
                  textTransform: 'uppercase',
                  marginBottom: '4px',
                }}
              >
                Data Received
              </div>
              <div style={{ fontSize: '24px', fontWeight: 600 }}>
                {formatBytes(totalUsage.recv)}
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: '11px',
                  color: 'var(--text-muted)',
                  textTransform: 'uppercase',
                  marginBottom: '4px',
                }}
              >
                Total Traffic
              </div>
              <div style={{ fontSize: '24px', fontWeight: 600 }}>
                {formatBytes(totalUsage.sent + totalUsage.recv)}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Connected Clients Table */}
      <div className="card" style={{ marginTop: '16px' }}>
        <div className="card-header">
          <h3>Connected Clients ({ssidClients.length})</h3>
        </div>
        <div className="card-content">
          {ssidClients.length > 0 ? (
            <table className="device-table" style={{ width: '100%' }}>
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
                  <tr
                    key={client.id || client.mac}
                    onClick={() => onClientClick?.(client.id || client.mac)}
                    style={{ cursor: onClientClick ? 'pointer' : 'default' }}
                  >
                    <td>
                      <div
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px',
                        }}
                      >
                        <span style={{ fontSize: '18px' }}>
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
                          <div style={{ fontWeight: 500 }}>
                            {client.description || client.mac}
                          </div>
                          {client.description && (
                            <div
                              style={{
                                fontSize: '11px',
                                color: 'var(--text-muted)',
                                fontFamily: 'monospace',
                              }}
                            >
                              {client.mac}
                            </div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span
                        style={{ fontFamily: 'monospace', fontSize: '13px' }}
                      >
                        {client.ip || '—'}
                      </span>
                    </td>
                    <td>{client.manufacturer || '—'}</td>
                    <td>{formatLastSeen(client.lastSeen)}</td>
                    <td>
                      {client.usage ? (
                        <span>
                          ↓{formatBytes(client.usage.recv)} ↑
                          {formatBytes(client.usage.sent)}
                        </span>
                      ) : (
                        '—'
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div
              style={{
                textAlign: 'center',
                padding: '40px',
                color: 'var(--text-muted)',
              }}
            >
              <div style={{ fontSize: '32px', marginBottom: '8px' }}>📴</div>
              <div>No clients connected to this SSID</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SSIDView;
