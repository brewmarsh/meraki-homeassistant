import React, { useState } from 'react';

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
}

interface ClientsViewProps {
  clients: Client[];
  setActiveView: (view: {
    view: string;
    deviceId?: string;
    clientId?: string;
  }) => void;
  onBack: () => void;
}

const ClientsView: React.FC<ClientsViewProps> = ({
  clients,
  setActiveView,
  onBack,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);

  // Filter clients based on search
  const filteredClients = clients.filter((client) => {
    const search = searchTerm.toLowerCase();
    return (
      client.description?.toLowerCase().includes(search) ||
      client.mac?.toLowerCase().includes(search) ||
      client.ip?.toLowerCase().includes(search) ||
      client.manufacturer?.toLowerCase().includes(search) ||
      client.user?.toLowerCase().includes(search) ||
      client.os?.toLowerCase().includes(search)
    );
  });

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
    return '🔌';
  };

  if (selectedClient) {
    return (
      <div>
        <button
          onClick={() => setSelectedClient(null)}
          className="back-button"
        >
          ← Back to Clients
        </button>

        <div className="device-header">
          <div className="device-icon">{getClientIcon(selectedClient)}</div>
          <div className="device-info">
            <h1>{selectedClient.description || selectedClient.mac}</h1>
            <div className="meta">
              <span>
                <strong>MAC:</strong>{' '}
                <span style={{ fontFamily: 'monospace' }}>
                  {selectedClient.mac}
                </span>
              </span>
              {selectedClient.ip && (
                <span>
                  <strong>IP:</strong> {selectedClient.ip}
                </span>
              )}
              {selectedClient.manufacturer && (
                <span>
                  <strong>Manufacturer:</strong> {selectedClient.manufacturer}
                </span>
              )}
              {selectedClient.os && (
                <span>
                  <strong>OS:</strong> {selectedClient.os}
                </span>
              )}
              {selectedClient.vlan && (
                <span>
                  <strong>VLAN:</strong> {selectedClient.vlan}
                </span>
              )}
              {selectedClient.ssid && (
                <span>
                  <strong>SSID:</strong> {selectedClient.ssid}
                </span>
              )}
            </div>
            {selectedClient.lastSeen && (
              <div
                className="meta"
                style={{ marginTop: '4px', fontSize: '12px' }}
              >
                <span style={{ color: 'var(--text-muted)' }}>
                  Last seen: {formatDate(selectedClient.lastSeen)}
                </span>
              </div>
            )}
          </div>
          <div
            className={`status-pill ${
              selectedClient.status?.toLowerCase() || 'online'
            }`}
          >
            <div className="dot"></div>
            {selectedClient.status || 'Online'}
          </div>
        </div>

        {/* Single comprehensive session card */}
        <div className="info-card" style={{ marginBottom: '20px' }}>
          <h3>📊 Session Details</h3>

          {/* Usage Stats Row */}
          {selectedClient.usage && (
            <div
              style={{
                display: 'flex',
                gap: '32px',
                marginBottom: '20px',
                padding: '16px',
                background: 'var(--bg-primary)',
                borderRadius: 'var(--radius-md)',
              }}
            >
              <div style={{ flex: 1, textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '12px',
                    color: 'var(--text-muted)',
                    marginBottom: '4px',
                  }}
                >
                  UPLOADED
                </div>
                <div
                  style={{
                    fontSize: '24px',
                    fontWeight: 600,
                    color: 'var(--success)',
                  }}
                >
                  ↑ {formatBytes(selectedClient.usage.sent)}
                </div>
              </div>
              <div
                style={{
                  width: '1px',
                  background: 'var(--card-border)',
                }}
              />
              <div style={{ flex: 1, textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '12px',
                    color: 'var(--text-muted)',
                    marginBottom: '4px',
                  }}
                >
                  DOWNLOADED
                </div>
                <div
                  style={{
                    fontSize: '24px',
                    fontWeight: 600,
                    color: 'var(--primary)',
                  }}
                >
                  ↓ {formatBytes(selectedClient.usage.recv)}
                </div>
              </div>
              <div
                style={{
                  width: '1px',
                  background: 'var(--card-border)',
                }}
              />
              <div style={{ flex: 1, textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '12px',
                    color: 'var(--text-muted)',
                    marginBottom: '4px',
                  }}
                >
                  TOTAL
                </div>
                <div
                  style={{
                    fontSize: '24px',
                    fontWeight: 600,
                    color: 'var(--text-primary)',
                  }}
                >
                  {formatBytes(
                    selectedClient.usage.sent + selectedClient.usage.recv
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Details Grid */}
          <div className="info-grid">
            {/* Connection Type */}
            <div className="info-item">
              <div className="label">Connection Type</div>
              <div className="value">
                {selectedClient.ssid ? '📶 Wireless' : '🔌 Wired'}
              </div>
            </div>

            {/* Connected Device */}
            {(selectedClient.recentDeviceName ||
              selectedClient.recentDeviceSerial) && (
              <div className="info-item">
                <div className="label">Connected To</div>
                <div className="value">
                  {selectedClient.recentDeviceName ||
                    selectedClient.recentDeviceSerial}
                  {selectedClient.switchport &&
                    ` (Port ${selectedClient.switchport})`}
                </div>
              </div>
            )}

            {/* SSID for wireless */}
            {selectedClient.ssid && (
              <div className="info-item">
                <div className="label">SSID</div>
                <div className="value">{selectedClient.ssid}</div>
              </div>
            )}

            {/* VLAN */}
            {selectedClient.vlan && (
              <div className="info-item">
                <div className="label">VLAN</div>
                <div className="value">{selectedClient.vlan}</div>
              </div>
            )}

            {/* IPv6 if available */}
            {selectedClient.ip6 && (
              <div className="info-item">
                <div className="label">IPv6 Address</div>
                <div className="value mono" style={{ fontSize: '11px' }}>
                  {selectedClient.ip6}
                </div>
              </div>
            )}

            {/* User (802.1x) */}
            {selectedClient.user && (
              <div className="info-item">
                <div className="label">User (802.1x)</div>
                <div className="value">{selectedClient.user}</div>
              </div>
            )}

            {/* First Seen */}
            {selectedClient.firstSeen && (
              <div className="info-item">
                <div className="label">First Connected</div>
                <div className="value">
                  {formatDate(selectedClient.firstSeen)}
                </div>
              </div>
            )}

            {/* Session Duration - calculated if we have both dates */}
            {selectedClient.firstSeen && selectedClient.lastSeen && (
              <div className="info-item">
                <div className="label">Known For</div>
                <div className="value">
                  {(() => {
                    const first = new Date(selectedClient.firstSeen);
                    const last = new Date(selectedClient.lastSeen);
                    const days = Math.floor(
                      (last.getTime() - first.getTime()) /
                        (1000 * 60 * 60 * 24)
                    );
                    if (days > 30) return `${Math.floor(days / 30)} months`;
                    if (days > 0) return `${days} days`;
                    return 'Today';
                  })()}
                </div>
              </div>
            )}
          </div>

          {/* View Device Button */}
          {selectedClient.recentDeviceSerial && (
            <button
              onClick={() =>
                setActiveView({
                  view: 'device',
                  deviceId: selectedClient.recentDeviceSerial,
                })
              }
              style={{
                marginTop: '16px',
                padding: '10px 20px',
                borderRadius: 'var(--radius-md)',
                border: 'none',
                background: 'var(--primary)',
                color: 'white',
                cursor: 'pointer',
                fontWeight: 500,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              🔗 View Connected Device
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div>
      <button onClick={onBack} className="back-button">
        ← Back to Dashboard
      </button>

      <div className="device-header">
        <div
          className="device-icon"
          style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}
        >
          👥
        </div>
        <div className="device-info">
          <h1>Connected Clients</h1>
          <div className="meta">
            <span>{clients.length} total clients</span>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Search clients by name, MAC, IP, manufacturer..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border)',
            background: 'var(--bg-secondary)',
            color: 'var(--text-primary)',
            fontSize: '14px',
          }}
        />
      </div>

      {/* Clients Table */}
      <div className="network-card">
        <table className="device-table">
          <thead>
            <tr>
              <th>Client</th>
              <th>IP Address</th>
              <th>MAC Address</th>
              <th>Manufacturer</th>
              <th>SSID / Port</th>
              <th>Usage</th>
            </tr>
          </thead>
          <tbody>
            {filteredClients.map((client) => (
              <tr
                key={client.id || client.mac}
                className="device-row"
                onClick={() => setSelectedClient(client)}
              >
                <td>
                  <div className="device-name-cell">
                    <div className="device-icon" style={{ fontSize: '20px' }}>
                      {getClientIcon(client)}
                    </div>
                    <div>
                      <span className="name">
                        {client.description || client.mac}
                      </span>
                      {client.os && (
                        <div
                          style={{
                            fontSize: '12px',
                            color: 'var(--text-muted)',
                          }}
                        >
                          {client.os}
                        </div>
                      )}
                    </div>
                  </div>
                </td>
                <td className="device-model">{client.ip || '—'}</td>
                <td
                  className="device-model"
                  style={{ fontFamily: 'monospace', fontSize: '12px' }}
                >
                  {client.mac}
                </td>
                <td className="device-model">{client.manufacturer || '—'}</td>
                <td>
                  <span className="detail-badge">
                    {client.ssid || client.switchport || '—'}
                  </span>
                </td>
                <td>
                  {client.usage ? (
                    <span style={{ fontSize: '12px' }}>
                      ↑{formatBytes(client.usage.sent)} ↓
                      {formatBytes(client.usage.recv)}
                    </span>
                  ) : (
                    '—'
                  )}
                </td>
              </tr>
            ))}
            {filteredClients.length === 0 && (
              <tr>
                <td
                  colSpan={6}
                  style={{
                    textAlign: 'center',
                    color: 'var(--text-muted)',
                    padding: '40px',
                  }}
                >
                  {searchTerm
                    ? 'No clients match your search'
                    : 'No clients found'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ClientsView;
