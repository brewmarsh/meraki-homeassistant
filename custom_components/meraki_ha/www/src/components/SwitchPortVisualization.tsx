import React, { useState } from 'react';

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

interface SwitchPortVisualizationProps {
  deviceName: string;
  model: string;
  ports: PortStatus[];
}

const SwitchPortVisualization: React.FC<SwitchPortVisualizationProps> = ({
  deviceName: _deviceName,
  model,
  ports,
}) => {
  const [selectedPort, setSelectedPort] = useState<PortStatus | null>(null);

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
            <span>{connectedCount} of {ports.length} connected</span>
          </div>
          <div className="ports-row">
            {ports.map((port) => (
              <div
                key={port.portId}
                className={`port ${isConnected(port) ? 'connected' : ''} ${
                  selectedPort?.portId === port.portId ? 'selected' : ''
                }`}
                onClick={() => setSelectedPort(port)}
                title={`Port ${port.portId}${port.clientName ? ` - ${port.clientName}` : ''}`}
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
          <h4>
            <span style={{ color: isConnected(selectedPort) ? 'var(--success)' : 'var(--text-muted)' }}>
              🔌
            </span>
            Port {selectedPort.portId} - {selectedPort.status || 'Unknown'}
            {selectedPort.isUplink && <span style={{ marginLeft: '8px', fontSize: '12px', color: 'var(--primary)' }}>↑ Uplink</span>}
          </h4>
          
          {/* Errors and Warnings */}
          {(selectedPort.errors?.length || selectedPort.warnings?.length) && (
            <div style={{ marginBottom: '12px' }}>
              {selectedPort.errors?.map((err, i) => (
                <div key={`err-${i}`} style={{ color: 'var(--error)', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span>🚨</span> {err}
                </div>
              ))}
              {selectedPort.warnings?.map((warn, i) => (
                <div key={`warn-${i}`} style={{ color: 'var(--warning)', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span>⚠️</span> {warn}
                </div>
              ))}
            </div>
          )}
          
          {/* Client Info */}
          {isConnected(selectedPort) && selectedPort.clientName && (
            <div className="client-info">
              <div className="client-avatar">💻</div>
              <div className="client-details">
                <div className="name">{selectedPort.clientName}</div>
                <div className="mac">{selectedPort.clientMac || 'Unknown MAC'}</div>
              </div>
            </div>
          )}
          
          {/* Port Stats */}
          <div className="port-stats">
            <div className="port-stat">
              <div className="label">Speed</div>
              <div className="value">{selectedPort.speed || '—'}</div>
            </div>
            <div className="port-stat">
              <div className="label">Duplex</div>
              <div className="value">{selectedPort.duplex || '—'}</div>
            </div>
            <div className="port-stat">
              <div className="label">Live Traffic</div>
              <div className="value">
                {selectedPort.trafficInKbps?.total != null
                  ? formatKbps(selectedPort.trafficInKbps.total)
                  : '—'}
              </div>
            </div>
            <div className="port-stat">
              <div className="label">Total Usage</div>
              <div className="value">
                {selectedPort.usageInKb?.total != null
                  ? formatBytes(selectedPort.usageInKb.total)
                  : '—'}
              </div>
            </div>
            <div className="port-stat">
              <div className="label">PoE Energy</div>
              <div className="value" style={{ color: 'var(--warning)' }}>
                {selectedPort.powerUsageInWh != null
                  ? `${selectedPort.powerUsageInWh.toFixed(1)} Wh`
                  : '—'}
              </div>
            </div>
            <div className="port-stat">
              <div className="label">VLAN</div>
              <div className="value">{selectedPort.vlan || '—'}</div>
            </div>
            <div className="port-stat">
              <div className="label">Clients</div>
              <div className="value">{selectedPort.clientCount ?? '—'}</div>
            </div>
          </div>

          {/* LLDP/CDP Neighbor Info */}
          {(selectedPort.lldp?.systemName || selectedPort.cdp?.deviceId) && (
            <div style={{ marginTop: '16px', padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)' }}>
              <h5 style={{ margin: '0 0 8px 0', fontSize: '13px', color: 'var(--text-muted)' }}>
                🔗 Neighbor Discovery
              </h5>
              {selectedPort.lldp?.systemName && (
                <div style={{ marginBottom: '8px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>LLDP</div>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>{selectedPort.lldp.systemName}</div>
                  {selectedPort.lldp.portId && (
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                      Port: {selectedPort.lldp.portId} {selectedPort.lldp.portDescription && `(${selectedPort.lldp.portDescription})`}
                    </div>
                  )}
                  {selectedPort.lldp.managementAddress && (
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)', fontFamily: 'monospace' }}>
                      {selectedPort.lldp.managementAddress}
                    </div>
                  )}
                </div>
              )}
              {selectedPort.cdp?.deviceId && (
                <div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>CDP</div>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>{selectedPort.cdp.deviceId}</div>
                  {selectedPort.cdp.platform && (
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                      {selectedPort.cdp.platform}
                    </div>
                  )}
                  {selectedPort.cdp.portId && (
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                      Port: {selectedPort.cdp.portId}
                    </div>
                  )}
                  {selectedPort.cdp.managementAddress && (
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)', fontFamily: 'monospace' }}>
                      {selectedPort.cdp.managementAddress}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* SecurePort Status */}
          {selectedPort.securePort?.enabled && (
            <div style={{ marginTop: '12px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>🔒</span>
              <span style={{ color: selectedPort.securePort.active ? 'var(--success)' : 'var(--text-muted)' }}>
                SecurePort: {selectedPort.securePort.authenticationStatus || (selectedPort.securePort.active ? 'Active' : 'Inactive')}
              </span>
            </div>
          )}
        </div>
      )}

      {!selectedPort && (
        <div style={{ 
          textAlign: 'center', 
          padding: '20px', 
          color: 'var(--text-muted)',
          fontSize: '14px' 
        }}>
          Click a port to view details
        </div>
      )}
    </div>
  );
};

export default SwitchPortVisualization;

