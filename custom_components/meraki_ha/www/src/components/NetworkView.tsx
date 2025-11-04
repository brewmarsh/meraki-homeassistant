import React, { useState } from 'react';
import DeviceView from './DeviceView';

interface Network {
  id: string;
  name: string;
}

interface Device {
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
  networkId?: string;
}

interface NetworkViewProps {
  data: {
    networks: Network[];
    devices: Device[];
  };
  hass: any;
  config_entry_id: string;
}

const NetworkView: React.FC<NetworkViewProps> = ({ data, hass, config_entry_id }) => {
  const [openNetworkId, setOpenNetworkId] = useState<string | null>(null);

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkId(openNetworkId === networkId ? null : networkId);
  };

  const { networks, devices } = data;

  if (!networks || networks.length === 0) {
    return <p>No networks found.</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {networks.map((network) => {
        const isOpen = openNetworkId === network.id;
        return (
          <ha-card key={network.id}>
            <div
              className="card-header"
              onClick={() => handleNetworkClick(network.id)}
              style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '16px' }}
            >
              <span>{network.name}</span>
              <ha-icon style={{ marginLeft: '8px' }} icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}></ha-icon>
            </div>
            {isOpen && (
              <div className="card-content">
                <DeviceView
                  devices={devices.filter((d) => d.networkId === network.id)}
                  hass={hass}
                  config_entry_id={config_entry_id}
                />
              </div>
            )}
          </ha-card>
        );
      })}
    </div>
  );
};

export default NetworkView;
