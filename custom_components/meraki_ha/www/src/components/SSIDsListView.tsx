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
      <div
        className="view-header"
        style={{ display: 'flex', alignItems: 'center', marginBottom: '24px' }}
      >
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <div style={{ flex: 1, marginLeft: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '24px' }}>📶</span>
            <div>
              <h2 style={{ margin: 0, fontSize: '20px' }}>
                Wireless Networks
              </h2>
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
                <span>{ssids.length} SSIDs</span>
                <span>•</span>
                <span style={{ color: 'var(--success)' }}>
                  {enabledCount} active
                </span>
                <span>•</span>
                <span>{totalClients} connected clients</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SSIDs by Network */}
      {Object.entries(ssidsByNetwork).map(([networkId, networkSSIDs]) => (
        <div key={networkId} className="card" style={{ marginBottom: '16px' }}>
          <div className="card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🌐</span>
              {getNetworkName(networkId)}
              <span
                style={{
                  fontSize: '12px',
                  color: 'var(--text-muted)',
                  fontWeight: 400,
                }}
              >
                ({networkSSIDs.length} SSIDs)
              </span>
            </h3>
          </div>
          <div className="card-content" style={{ padding: 0 }}>
            <table className="device-table" style={{ width: '100%' }}>
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
                      style={{ cursor: 'pointer' }}
                    >
                      <td>
                        <div
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '10px',
                          }}
                        >
                          <span style={{ fontSize: '18px' }}>
                            {ssid.enabled ? '🔒' : '📶'}
                          </span>
                          <span style={{ fontWeight: 500 }}>{ssid.name}</span>
                        </div>
                      </td>
                      <td>
                        <span
                          style={{
                            background: 'var(--bg-tertiary)',
                            padding: '2px 8px',
                            borderRadius: 'var(--radius-sm)',
                            fontSize: '12px',
                          }}
                        >
                          #{ssid.number}
                        </span>
                      </td>
                      <td>
                        <span
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '6px',
                            padding: '4px 12px',
                            borderRadius: '20px',
                            fontSize: '12px',
                            fontWeight: 500,
                            background: ssid.enabled
                              ? 'var(--success-light)'
                              : 'var(--bg-tertiary)',
                            color: ssid.enabled
                              ? 'var(--success)'
                              : 'var(--text-muted)',
                          }}
                        >
                          <span
                            style={{
                              width: '6px',
                              height: '6px',
                              borderRadius: '50%',
                              background: ssid.enabled
                                ? 'var(--success)'
                                : 'var(--text-muted)',
                            }}
                          />
                          {ssid.enabled ? 'Broadcasting' : 'Disabled'}
                        </span>
                      </td>
                      <td>
                        {clientCount > 0 ? (
                          <span
                            style={{
                              color: 'var(--primary)',
                              fontWeight: 500,
                            }}
                          >
                            {clientCount}{' '}
                            {clientCount === 1 ? 'client' : 'clients'}
                          </span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>
                            No clients
                          </span>
                        )}
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        <span style={{ color: 'var(--text-muted)' }}>→</span>
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
        <div
          style={{
            textAlign: 'center',
            padding: '60px 20px',
            color: 'var(--text-muted)',
          }}
        >
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>📶</div>
          <h3 style={{ marginBottom: '8px' }}>No SSIDs Found</h3>
          <p>
            No wireless networks are configured in your Meraki organization.
          </p>
        </div>
      )}
    </div>
  );
};

export default SSIDsListView;
