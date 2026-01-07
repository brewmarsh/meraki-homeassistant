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
  ssid?: string;
}

interface Network {
  id: string;
  name: string;
}

interface SSIDsListViewProps {
  ssids: SSID[];
  clients: Client[];
  networks: Network[];
  onBack: () => void;
  onSSIDClick: (ssid: SSID) => void;
}

const SSIDsListView: React.FC<SSIDsListViewProps> = ({
  ssids,
  clients,
  networks,
  onBack,
  onSSIDClick,
}) => {
  // Group SSIDs by network
  const ssidsByNetwork = ssids.reduce(
    (acc, ssid) => {
      const networkId = ssid.networkId || 'unknown';
      if (!acc[networkId]) {
        acc[networkId] = [];
      }
      acc[networkId].push(ssid);
      return acc;
    },
    {} as Record<string, SSID[]>
  );

  const getNetworkName = (networkId: string): string => {
    const network = networks.find((n) => n.id === networkId);
    return network?.name || networkId;
  };

  const getClientCount = (ssidName: string): number => {
    return clients.filter((c) => c.ssid === ssidName).length;
  };

  const enabledCount = ssids.filter((s) => s.enabled).length;
  const totalClients = ssids.reduce(
    (sum, ssid) => sum + getClientCount(ssid.name),
    0
  );

  return (
    <div className="ssids-list-view">
      {/* Header */}
      <div className="view-header">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <div className="view-header-content">
          <div className="view-header-title">
            <span className="view-header-icon">📶</span>
            <div>
              <h2>Wireless Networks</h2>
              <div className="meta-info view-header-stats">
                <span>{ssids.length} SSIDs</span>
                <span className="separator">•</span>
                <span className="text-success">{enabledCount} active</span>
                <span className="separator">•</span>
                <span>{totalClients} connected clients</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SSIDs by Network */}
      {Object.entries(ssidsByNetwork).map(([networkId, networkSSIDs]) => (
        <div key={networkId} className="card ssid-network-card">
          <div className="card-header">
            <h3>
              <span>🌐</span>
              {getNetworkName(networkId)}
              <span className="text-muted ssid-count">
                ({networkSSIDs.length} SSIDs)
              </span>
            </h3>
          </div>
          <div className="card-content">
            <table className="device-table">
              <thead>
                <tr>
                  <th>SSID</th>
                  <th>Number</th>
                  <th>Status</th>
                  <th>Connected Clients</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {networkSSIDs.map((ssid) => {
                  const clientCount = getClientCount(ssid.name);
                  return (
                    <tr
                      key={`${ssid.networkId}-${ssid.number}`}
                      onClick={() => onSSIDClick(ssid)}
                      className="device-row"
                    >
                      <td>
                        <div className="ssid-name-cell">
                          <span className="ssid-icon">
                            {ssid.enabled ? '🔒' : '📶'}
                          </span>
                          <span className="ssid-name">{ssid.name}</span>
                        </div>
                      </td>
                      <td>
                        <span className="number-badge">#{ssid.number}</span>
                      </td>
                      <td>
                        <span
                          className={`status-badge ${
                            ssid.enabled ? 'enabled' : 'disabled'
                          }`}
                        >
                          <span className="dot" />
                          {ssid.enabled ? 'Broadcasting' : 'Disabled'}
                        </span>
                      </td>
                      <td>
                        {clientCount > 0 ? (
                          <span className="client-count text-primary">
                            {clientCount}{' '}
                            {clientCount === 1 ? 'client' : 'clients'}
                          </span>
                        ) : (
                          <span className="text-muted">No clients</span>
                        )}
                      </td>
                      <td className="arrow-cell">
                        <span className="arrow-indicator">→</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ))}

      {ssids.length === 0 && (
        <div className="empty-state-message">
          <div className="empty-icon">📶</div>
          <h3>No SSIDs Found</h3>
          <p>
            No wireless networks are configured in your Meraki organization.
          </p>
        </div>
      )}
    </div>
  );
};

export default SSIDsListView;
