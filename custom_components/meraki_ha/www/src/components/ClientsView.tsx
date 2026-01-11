import React, { useState, memo, useCallback } from 'react';
import ClientDetailView from './ClientDetailView';

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

interface ClientsViewProps {
  clients: Client[];
  onBack: () => void;
  initialClientId?: string;
}

/**
 * Memoized client row - only re-renders when this specific client changes
 */
interface ClientRowProps {
  client: Client;
  onClick: () => void;
  getClientIcon: (client: Client) => string;
  formatBytes: (bytes: number) => string;
}

const ClientRow = memo<ClientRowProps>(
  ({ client, onClick, getClientIcon, formatBytes }) => (
    <tr className="device-row" onClick={onClick}>
      <td>
        <div className="device-name-cell">
          <div className="device-icon text-xl">{getClientIcon(client)}</div>
          <div>
            <span className="name">{client.description || client.mac}</span>
            {client.os && (
              <div className="text-sm text-muted">{client.os}</div>
            )}
          </div>
        </div>
      </td>
      <td className="device-model">{client.ip || '—'}</td>
      <td className="device-model text-mono text-sm">{client.mac}</td>
      <td className="device-model">{client.manufacturer || '—'}</td>
      <td>
        <span className="detail-badge">
          {client.ssid || client.switchport || '—'}
        </span>
      </td>
      <td>
        {client.usage ? (
          <span className="text-sm">
            ↑{formatBytes(client.usage.sent)} ↓{formatBytes(client.usage.recv)}
          </span>
        ) : (
          '—'
        )}
      </td>
    </tr>
  ),
  (prevProps, nextProps) => {
    const prev = prevProps.client;
    const next = nextProps.client;

    // Only re-render if this client's data changed
    if (prev.id !== next.id) return false;
    if (prev.mac !== next.mac) return false;
    if (prev.ip !== next.ip) return false;
    if (prev.description !== next.description) return false;
    if (prev.status !== next.status) return false;
    if (prev.ssid !== next.ssid) return false;
    if (prev.switchport !== next.switchport) return false;
    if (prev.usage?.sent !== next.usage?.sent) return false;
    if (prev.usage?.recv !== next.usage?.recv) return false;

    return true; // No changes, skip re-render
  }
);

ClientRow.displayName = 'ClientRow';

const ClientsViewComponent: React.FC<ClientsViewProps> = ({
  clients,
  onBack,
  initialClientId,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClientId, setSelectedClientId] = useState<string | null>(
    initialClientId || null
  );

  // Find the selected client
  const selectedClient = selectedClientId
    ? clients.find(
        (c) => c.id === selectedClientId || c.mac === selectedClientId
      ) || null
    : null;

  // Show client detail view when clicked
  const handleClientClick = useCallback((client: Client) => {
    setSelectedClientId(client.id || client.mac);
  }, []);

  // Navigate to the HA device page for a client
  const handleNavigateToDevice = useCallback((client: Client) => {
    if (client.ha_device_id) {
      const path = `/config/devices/device/${client.ha_device_id}`;
      const event = new CustomEvent('hass-navigate', {
        detail: { path },
        bubbles: true,
        composed: true,
      });
      window.dispatchEvent(event);
    } else {
      console.warn('Cannot navigate: client is missing ha_device_id', client);
    }
  }, []);

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

  // Memoized helper functions to prevent ClientRow re-renders
  const formatBytes = useCallback((bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }, []);

  const formatDate = useCallback((dateString?: string): string => {
    if (!dateString) return '—';
    const date = new Date(dateString);
    return date.toLocaleString();
  }, []);

  const getClientIcon = useCallback((client: Client): string => {
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
  }, []);

  // Show client detail view if a client is selected
  if (selectedClient) {
    return (
      <ClientDetailView
        client={selectedClient}
        onBack={() => setSelectedClientId(null)}
        onNavigateToDevice={() => handleNavigateToDevice(selectedClient)}
      />
    );
  }

  return (
    <div>
      <button onClick={onBack} className="back-button">
        ← Back to Dashboard
      </button>

      <div className="device-header">
        <div className="device-icon device-icon-gradient">👥</div>
        <div className="device-info">
          <h1>Connected Clients</h1>
          <div className="meta">
            <span>{clients.length} total clients</span>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      <div className="mb-5">
        <input
          type="text"
          placeholder="Search clients by name, MAC, IP, manufacturer..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
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
              <ClientRow
                key={client.id || client.mac}
                client={client}
                onClick={() => handleClientClick(client)}
                getClientIcon={getClientIcon}
                formatBytes={formatBytes}
              />
            ))}
            {filteredClients.length === 0 && (
              <tr>
                <td colSpan={6} className="empty-state-message">
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

// Memoize ClientsView to prevent unnecessary re-renders
const ClientsView = memo(ClientsViewComponent, (prevProps, nextProps) => {
  // Only re-render if clients array changed
  if (prevProps.clients.length !== nextProps.clients.length) {
    return false;
  }
  // Compare client IDs
  const prevIds = prevProps.clients.map((c) => c.id).join('|');
  const nextIds = nextProps.clients.map((c) => c.id).join('|');
  return prevIds === nextIds;
});

export default ClientsView;
