import React, { useState } from 'react';

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

interface SwitchPortVisualizationProps {
  deviceName: string;
  model: string;
  ports: PortStatus[];
}

const SwitchPortVisualization: React.FC<SwitchPortVisualizationProps> = ({
  deviceName,
  model,
  ports,
}) => {
  const [selectedPort, setSelectedPort] = useState<PortStatus | null>(null);

  const formatBytes = (kb: number): string => {
    if (kb >= 1000000) return `${(kb / 1000000).toFixed(1)} GB`;
    if (kb >= 1000) return `${(kb / 1000).toFixed(1)} MB`;
    return `${kb} KB`;
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
          </h4>
          
          {isConnected(selectedPort) && selectedPort.clientName && (
            <div className="client-info">
              <div className="client-avatar">💻</div>
              <div className="client-details">
                <div className="name">{selectedPort.clientName}</div>
                <div className="mac">{selectedPort.clientMac || 'Unknown MAC'}</div>
              </div>
            </div>
          )}
          
          <div className="port-stats">
            <div className="port-stat">
              <div className="label">Speed</div>
              <div className="value">{selectedPort.speed || '—'}</div>
            </div>
            <div className="port-stat">
              <div className="label">Traffic</div>
              <div className="value">
                {selectedPort.usageInKb?.total 
                  ? formatBytes(selectedPort.usageInKb.total) 
                  : '—'}
              </div>
            </div>
            <div className="port-stat">
              <div className="label">PoE Power</div>
              <div className="value" style={{ color: 'var(--warning)' }}>
                {selectedPort.powerUsageInWh 
                  ? `${selectedPort.powerUsageInWh} W` 
                  : '—'}
              </div>
            </div>
            <div className="port-stat">
              <div className="label">VLAN</div>
              <div className="value">{selectedPort.vlan || '—'}</div>
            </div>
          </div>
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

