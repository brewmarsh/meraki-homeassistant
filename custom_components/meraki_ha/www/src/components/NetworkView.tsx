import React, { useState } from 'react';
<<<<<<< HEAD
<<<<<<< HEAD
import DeviceView from './DeviceView';
=======
<<<<<<< HEAD
import DeviceView from './DeviceView';
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
import DeviceTable from './DeviceTable';
import SSIDView from './SSIDView';

// Define the types for our data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
}
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

interface Network {
  id: string;
  name: string;
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
  ssids: SSID[];
  is_enabled: boolean;
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
  ssids: SSID[];
  is_enabled: boolean;
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
  };
<<<<<<< HEAD
<<<<<<< HEAD
}

const NetworkView: React.FC<NetworkViewProps> = ({ data }) => {
=======
<<<<<<< HEAD
}

const NetworkView: React.FC<NetworkViewProps> = ({ data }) => {
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
  onToggle: (networkId: string, enabled: boolean) => void;
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const NetworkView: React.FC<NetworkViewProps> = ({ data, onToggle, setActiveView }) => {
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        const enabledSsids = network.ssids
          ? network.ssids.filter((s) => s.enabled).length
          : 0;
        const totalSsids = network.ssids ? network.ssids.length : 0;

<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        return (
          <ha-card key={network.id}>
            <div
              className="card-header"
              onClick={() => handleNetworkClick(network.id)}
<<<<<<< HEAD
<<<<<<< HEAD
              style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '16px' }}
=======
<<<<<<< HEAD
              style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '16px' }}
            >
              <span>[Network] {network.name}</span>
              <ha-icon style={{ marginLeft: '8px' }} icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}></ha-icon>
            </div>
            {isOpen && (
              <div className="card-content">
                <DeviceView
                  devices={devices.filter((d) => d.networkId === network.id)}
                />
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
              style={{
                display: 'flex',
                alignItems: 'center',
                cursor: 'pointer',
                padding: '16px',
              }}
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
            >
              <span>[Network] {network.name}</span>
              <ha-icon style={{ marginLeft: '8px' }} icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}></ha-icon>
            </div>
            {isOpen && (
              <div className="card-content">
                <DeviceView
                  devices={devices.filter((d) => d.networkId === network.id)}
                />
<<<<<<< HEAD
=======
                {network.ssids && network.ssids.length > 0 && (
                  <>
                    <div
                      className="hero-indicator"
                      style={{ padding: '0 16px 16px' }}
                    >
                      <ha-icon icon="mdi:wifi"></ha-icon>
                      {enabledSsids} / {totalSsids} SSIDs Enabled
                    </div>
                    <SSIDView ssids={network.ssids} />
                  </>
                )}
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
              </div>
            )}
          </ha-card>
        );
      })}
    </div>
  );
};

export default NetworkView;
