import React, { useState, memo } from 'react';

interface PortStatus {
  portId: string;
  status: string;
  enabled: boolean;
  isUplink?: boolean;
  speed?: string;
  duplex?: string;
  usageInKb?: { total?: number; sent?: number; recv?: number };
  trafficInKbps?: { total?: number; sent?: number; recv?: number };
  poe?: { isAllocated?: boolean; enabled?: boolean };
  powerUsageInWh?: number;
  clientName?: string;
  clientMac?: string;
  clientCount?: number;
  vlan?: number;
  errors?: string[];
  warnings?: string[];
  lldp?: {
    systemName?: string;
    systemDescription?: string;
    portId?: string;
    managementAddress?: string;
    portDescription?: string;
    systemCapabilities?: string;
    chassisId?: string;
  };
  cdp?: {
    deviceId?: string;
    systemName?: string;
    platform?: string;
    portId?: string;
    address?: string;
    nativeVlan?: number;
    managementAddress?: string;
    capabilities?: string;
  };
  securePort?: {
    enabled?: boolean;
    active?: boolean;
    authenticationStatus?: string;
  };
}

interface Client {
  id: string;
  mac: string;
  description?: string;
  ip?: string;
  manufacturer?: string;
  os?: string;
  status?: string;
  usage?: { sent: number; recv: number };
  vlan?: number;
  switchport?: string;
}

interface SwitchPortVisualizationProps {
  deviceName: string;
  model: string;
  ports: PortStatus[];
  clients?: Client[];
  onClientClick?: (clientId: string) => void;
}

const SwitchPortVisualizationComponent: React.FC<
  SwitchPortVisualizationProps
> = ({
  deviceName: _deviceName,
  model,
  ports,
  clients = [],
  onClientClick,
}) => {
  const [selectedPort, setSelectedPort] = useState<PortStatus | null>(null);

  // Get clients connected to a specific port
  // Handles various switchport formats:
  // - Simple: "4", "24", "Port 4"
  // - Stacked: "1/0/1", "2/0/24", "1/1/1"
  // - Mixed: "Port 1/0/1"
  // - Cisco style: "TenGigabitEthernet1/1/1", "GigabitEthernet1/0/24", "Gi1/0/1"
  const normalizePortId = (port: string): string => {
    let cleaned = port.trim();

    // Remove common prefixes like "Port ", "port", etc.
    cleaned = cleaned.replace(/^port\s*/i, '');

    // Remove Cisco-style speed/interface prefixes
    // Matches: TenGigabitEthernet, GigabitEthernet, FastEthernet, Ethernet
    // Also short forms: Te, Gi, Fa, Eth, etc.
    cleaned = cleaned.replace(
      /^(TenGigabit|Gigabit|Fast|Hundred)?Ethernet/i,
      ''
    );
    // Handle abbreviated forms: Te1/1/1, Gi1/0/24, Fa0/1
    cleaned = cleaned.replace(/^(Te|Gi|Fa|Eth?)\s*/i, '');

    // Return the cleaned value (preserves formats like "1/0/1")
    return cleaned.toLowerCase();
  };

  const getPortClients = (portId: string): Client[] => {
    const normalizedPortId = normalizePortId(portId);

    return clients.filter((client) => {
      if (!client.switchport) return false;
      const normalizedClientPort = normalizePortId(client.switchport);

      // Direct match (handles "1/0/1" == "1/0/1")
      if (normalizedClientPort === normalizedPortId) return true;

      // For stacked switches, also try matching just the last segment
      // e.g., portId "24" should match client.switchport "1/0/24"
      const portIdParts = normalizedPortId.split('/');
      const clientPortParts = normalizedClientPort.split('/');

      // If portId is simple (no slashes) and client has stacked format,
      // match the last segment
      if (portIdParts.length === 1 && clientPortParts.length > 1) {
        return (
          clientPortParts[clientPortParts.length - 1] === normalizedPortId
        );
      }

      // If both have same number of segments, compare directly
      if (portIdParts.length === clientPortParts.length) {
        return normalizedClientPort === normalizedPortId;
      }

      return false;
    });
  };

  const formatBytes = (kb: number): string => {
    if (kb >= 1000000) return `${(kb / 1000000).toFixed(1)} GB`;
    if (kb >= 1000) return `${(kb / 1000).toFixed(1)} MB`;
    return `${kb} KB`;
  };

  const formatKbps = (kbps: number): string => {
    if (kbps >= 1000) return `${(kbps / 1000).toFixed(1)} Mbps`;
    return `${kbps.toFixed(1)} Kbps`;
  };

  const isConnected = (port: PortStatus): boolean => {
    return port.status?.toLowerCase() === 'connected';
  };

  const hasPoe = (port: PortStatus): boolean => {
    return port.poe?.isAllocated === true || port.poe?.enabled === true;
  };

  const connectedCount = ports.filter(isConnected).length;
  const poeCount = ports.filter(hasPoe).length;

  return (
    <div className="info-card">
      <h3>
        <span>⚡</span> Port Status
      </h3>

      <div className="port-visualization">
        <div className="switch-chassis">
          <div className="switch-label">
            <span>Cisco Meraki {model}</span>
            <span>
              {connectedCount} of {ports.length} connected
            </span>
          </div>
          <div className="ports-row">
            {ports.map((port) => (
              <div
                key={port.portId}
                className={`port ${isConnected(port) ? 'connected' : ''} ${
                  selectedPort?.portId === port.portId ? 'selected' : ''
                }`}
                onClick={() => setSelectedPort(port)}
                title={`Port ${port.portId}${
                  port.clientName ? ` - ${port.clientName}` : ''
                }`}
              >
                <span className="num">{port.portId}</span>
                {hasPoe(port) && <span className="poe">⚡</span>}
              </div>
            ))}
          </div>
        </div>

        <div className="port-legend">
          <span>
            <div className="dot connected"></div>
            Connected ({connectedCount})
          </span>
          <span>
            <div className="dot disconnected"></div>
            Disconnected ({ports.length - connectedCount})
          </span>
          <span>⚡ PoE Active ({poeCount})</span>
        </div>
      </div>

      {selectedPort && (
        <div className="port-details">
          <h4 className="port-details-header">
            <span
              className={`port-status-icon ${
                isConnected(selectedPort) ? 'connected' : 'disconnected'
              }`}
            >
              🔌
            </span>
            Port {selectedPort.portId} - {selectedPort.status || 'Unknown'}
            {selectedPort.isUplink && (
              <span className="port-uplink-badge">↑ Uplink</span>
            )}
          </h4>

          {/* Errors and Warnings */}
          {(selectedPort.errors?.length || selectedPort.warnings?.length) && (
            <div className="port-alerts">
              {selectedPort.errors?.map((err, i) => (
                <div key={`err-${i}`} className="port-alert error">
                  <span>🚨</span> {err}
                </div>
              ))}
              {selectedPort.warnings?.map((warn, i) => (
                <div key={`warn-${i}`} className="port-alert warning">
                  <span>⚠️</span> {warn}
                </div>
              ))}
            </div>
          )}

          {/* Connected Clients for this port */}
          {isConnected(selectedPort) &&
            (() => {
              const portClients = getPortClients(selectedPort.portId);
              if (portClients.length === 0) {
                // Fallback to legacy port-level client data if no clients found
                if (selectedPort.clientName || selectedPort.clientMac) {
                  return (
                    <div className="client-info">
                      <div className="client-avatar">💻</div>
                      <div className="client-details">
                        <div className="name">
                          {selectedPort.clientName || 'Connected Device'}
                        </div>
                        {selectedPort.clientMac && (
                          <div className="mac">{selectedPort.clientMac}</div>
                        )}
                      </div>
                    </div>
                  );
                }
                return null;
              }
              return (
                <div className="port-clients">
                  <h5 className="port-clients-header">
                    👥 Connected Clients ({portClients.length})
                  </h5>
                  <div className="port-clients-list">
                    {portClients.map((client) => (
                      <div
                        key={client.id || client.mac}
                        className={`port-client-item ${
                          onClientClick ? 'clickable' : ''
                        }`}
                        onClick={() => onClientClick?.(client.id)}
                      >
                        <div className="port-client-icon">
                          {client.os?.toLowerCase().includes('ios') ||
                          client.manufacturer?.toLowerCase().includes('apple')
                            ? '📱'
                            : client.os?.toLowerCase().includes('windows')
                            ? '💻'
                            : '🔌'}
                        </div>
                        <div className="port-client-info">
                          <div className="port-client-name">
                            {client.description || client.mac}
                          </div>
                          <div className="port-client-meta">
                            {client.ip && (
                              <span className="port-client-ip">
                                {client.ip}
                              </span>
                            )}
                            {client.manufacturer && (
                              <span className="port-client-manufacturer">
                                {client.manufacturer}
                              </span>
                            )}
                          </div>
                        </div>
                        {client.vlan != null && (
                          <div className="port-client-vlan">
                            VLAN {client.vlan}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })()}

          {/* Port Stats - only show fields with data */}
          <div className="port-stats">
            {selectedPort.vlan != null && (
              <div className="port-stat">
                <div className="label">VLAN</div>
                <div className="value">{selectedPort.vlan}</div>
              </div>
            )}
            {selectedPort.speed && (
              <div className="port-stat">
                <div className="label">Speed</div>
                <div className="value">{selectedPort.speed}</div>
              </div>
            )}
            {selectedPort.duplex && (
              <div className="port-stat">
                <div className="label">Duplex</div>
                <div className="value">{selectedPort.duplex}</div>
              </div>
            )}
            {selectedPort.clientCount != null &&
              selectedPort.clientCount > 0 && (
                <div className="port-stat">
                  <div className="label">Clients</div>
                  <div className="value">{selectedPort.clientCount}</div>
                </div>
              )}
            {selectedPort.trafficInKbps?.total != null && (
              <div className="port-stat">
                <div className="label">Live Traffic</div>
                <div className="value">
                  {formatKbps(selectedPort.trafficInKbps.total)}
                </div>
              </div>
            )}
            {selectedPort.usageInKb?.total != null && (
              <div className="port-stat">
                <div className="label">Total Usage</div>
                <div className="value">
                  {formatBytes(selectedPort.usageInKb.total)}
                </div>
              </div>
            )}
            {hasPoe(selectedPort) && (
              <div className="port-stat">
                <div className="label">PoE Energy</div>
                <div className="value value-poe">
                  {selectedPort.powerUsageInWh != null
                    ? `${selectedPort.powerUsageInWh.toFixed(1)} Wh`
                    : 'Active'}
                </div>
              </div>
            )}
          </div>

          {/* Message for disconnected ports */}
          {!isConnected(selectedPort) && (
            <div className="port-empty-state">
              {selectedPort.enabled === false
                ? '🔒 Port is disabled'
                : '📴 No device connected to this port'}
            </div>
          )}

          {/* LLDP/CDP Neighbor Info */}
          {(selectedPort.lldp?.systemName || selectedPort.cdp?.deviceId) && (
            <div className="neighbor-discovery">
              <h5 className="neighbor-discovery-header">
                🔗 Neighbor Discovery
              </h5>
              {selectedPort.lldp?.systemName && (
                <div className="neighbor-protocol">
                  <div className="neighbor-protocol-label">LLDP</div>
                  <div className="neighbor-protocol-name">
                    {selectedPort.lldp.systemName}
                  </div>
                  {selectedPort.lldp.portId && (
                    <div className="neighbor-protocol-detail">
                      Port: {selectedPort.lldp.portId}{' '}
                      {selectedPort.lldp.portDescription &&
                        `(${selectedPort.lldp.portDescription})`}
                    </div>
                  )}
                  {selectedPort.lldp.managementAddress && (
                    <div className="neighbor-protocol-address">
                      {selectedPort.lldp.managementAddress}
                    </div>
                  )}
                </div>
              )}
              {selectedPort.cdp?.deviceId && (
                <div className="neighbor-protocol">
                  <div className="neighbor-protocol-label">CDP</div>
                  <div className="neighbor-protocol-name">
                    {selectedPort.cdp.deviceId}
                  </div>
                  {selectedPort.cdp.platform && (
                    <div className="neighbor-protocol-detail">
                      {selectedPort.cdp.platform}
                    </div>
                  )}
                  {selectedPort.cdp.portId && (
                    <div className="neighbor-protocol-detail">
                      Port: {selectedPort.cdp.portId}
                    </div>
                  )}
                  {selectedPort.cdp.managementAddress && (
                    <div className="neighbor-protocol-address">
                      {selectedPort.cdp.managementAddress}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* SecurePort Status */}
          {selectedPort.securePort?.enabled && (
            <div
              className={`secure-port-status ${
                selectedPort.securePort.active ? 'active' : 'inactive'
              }`}
            >
              <span>🔒</span>
              <span>
                SecurePort:{' '}
                {selectedPort.securePort.authenticationStatus ||
                  (selectedPort.securePort.active ? 'Active' : 'Inactive')}
              </span>
            </div>
          )}
        </div>
      )}

      {!selectedPort && (
        <div className="port-select-prompt">Click a port to view details</div>
      )}
    </div>
  );
};

// Memoize SwitchPortVisualization to prevent unnecessary re-renders
const SwitchPortVisualization = memo(
  SwitchPortVisualizationComponent,
  (prevProps, nextProps) => {
    // Re-render if ports or clients change
    if (prevProps.ports.length !== nextProps.ports.length) return false;
    if (prevProps.clients?.length !== nextProps.clients?.length) return false;

    // Compare connected port count
    const prevConnected = prevProps.ports.filter(
      (p) => p.status?.toLowerCase() === 'connected'
    ).length;
    const nextConnected = nextProps.ports.filter(
      (p) => p.status?.toLowerCase() === 'connected'
    ).length;
    if (prevConnected !== nextConnected) return false;

    return true;
  }
);

export default SwitchPortVisualization;
