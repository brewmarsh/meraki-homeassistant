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
}

const NetworkView: React.FC<NetworkViewProps> = ({ data }) => {
  const [openNetworkId, setOpenNetworkId] = useState<string | null>(null);

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkId(openNetworkId === networkId ? null : networkId);
  };

  const { networks, devices } = data;

  if (!networks || networks.length === 0) {
    return <p>No networks found.</p>;
  }

  return (
    <div className="card-content">
      {networks.map((network) => (
        <div key={network.id} className="network-item">
          <div className="network-header" onClick={() => handleNetworkClick(network.id)}>
            <span>{network.name}</span>
            <span style={{ float: 'right' }}>{openNetworkId === network.id ? '▲' : '▼'}</span>
          </div>
          {openNetworkId === network.id && (
            <div className="network-devices">
              <DeviceView devices={devices.filter((d) => d.networkId === network.id)} />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default NetworkView;
