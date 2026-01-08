import React from 'react';

interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
}

interface SSIDViewProps {
  ssids: SSID[];
}

const SSIDView: React.FC<SSIDViewProps> = ({ ssids }) => {
  if (!ssids || ssids.length === 0) {
    return null;
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px', padding: '16px' }}>
      {ssids.map((ssid) => (
        <ha-card key={ssid.number}>
          <div className="card-content" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontWeight: 'bold' }}>{ssid.name}</span>
              <ha-icon icon={ssid.enabled ? 'mdi:wifi' : 'mdi:wifi-off'} style={{ color: ssid.enabled ? 'var(--primary-color)' : 'var(--disabled-text-color)' }}></ha-icon>
            </div>
            <span>{ssid.enabled ? 'Enabled' : 'Disabled'}</span>
          </div>
        </ha-card>
      ))}
    </div>
  );
};

export default SSIDView;
