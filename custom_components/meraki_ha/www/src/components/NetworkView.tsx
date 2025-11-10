import React, { useState } from 'react';
import DeviceView from './DeviceView';

interface Network {
  id: string;
  name: string;
}

interface Device {
  entity_id: string;
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
    enabled_networks: string[];
    config_entry_id: string;
  };
  hass: any;
}

const NetworkView: React.FC<NetworkViewProps> = ({ data, hass }) => {
  const [openNetworkId, setOpenNetworkId] = useState<string | null>(null);

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkId(openNetworkId === networkId ? null : networkId);
  };

  const { networks, devices, enabled_networks, config_entry_id } = data;

  if (!networks || networks.length === 0) {
    return <p>No networks found.</p>;
  }

  const handleToggle = async (networkId: string, enabled: boolean) => {
    const newEnabledNetworks = enabled
      ? [...enabled_networks, networkId]
      : enabled_networks.filter((id) => id !== networkId);

    try {
      await hass.connection.sendMessagePromise({
        type: 'meraki_ha/update_enabled_networks',
        config_entry_id,
        enabled_networks: newEnabledNetworks,
      });
    } catch (err) {
      console.error('Error updating enabled networks:', err);
    }
  };

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
              <span>[Network] {network.name}</span>
              <ha-icon style={{ marginLeft: '8px' }} icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}></ha-icon>
              <div style={{ marginLeft: 'auto' }}>
                <ha-switch
                  checked={enabled_networks === null || enabled_networks === undefined || enabled_networks.includes(network.id)}
                  onchange={(e: any) => handleToggle(network.id, e.target.checked)}
                ></ha-switch>
              </div>
            </div>
            {isOpen && (
              <div className="card-content">
                <DeviceView
                  devices={devices.filter((d) => d.networkId === network.id)}
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
