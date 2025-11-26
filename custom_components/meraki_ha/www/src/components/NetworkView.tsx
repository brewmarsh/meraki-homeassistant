import React, { useState, useEffect } from 'react';
import DeviceTable from './DeviceTable';
import SSIDView from './SSIDView';
import EventLog from './EventLog';

// Define the types for our data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
}

interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
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
  hass: any;
  data: {
    networks: Network[];
    devices: Device[];
  };
  onToggle: (networkId: string, enabled: boolean) => void;
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const NetworkView: React.FC<NetworkViewProps> = ({
  hass,
  data,
  onToggle,
  setActiveView,
}) => {
  const [openNetworkIds, setOpenNetworkIds] = useState<string[]>(() => {
    const saved = sessionStorage.getItem('openNetworkIds');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    sessionStorage.setItem('openNetworkIds', JSON.stringify(openNetworkIds));
  }, [openNetworkIds]);

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkIds((prev) =>
      prev.includes(networkId)
        ? prev.filter((id) => id !== networkId)
        : [...prev, networkId]
    );
  };

  const { networks, devices } = data;

  if (!networks || networks.length === 0) {
    return <p>No networks found.</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {networks.map((network) => {
        const isOpen = openNetworkIds.includes(network.id);
        const enabledSsids = network.ssids
          ? network.ssids.filter((s) => s.enabled).length
          : 0;
        const totalSsids = network.ssids ? network.ssids.length : 0;

        return (
          <ha-card key={network.id}>
            <div
              className="card-header"
              onClick={() => handleNetworkClick(network.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                cursor: 'pointer',
                padding: '16px',
              }}
            >
              <span>[Network] {network.name}</span>
              <ha-icon
                style={{ marginLeft: '8px' }}
                icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}
              ></ha-icon>
              <div
                style={{
                  marginLeft: 'auto',
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                <span style={{ marginRight: '8px' }}>Track in</span>
                <ha-icon
                  icon="hass:home-assistant"
                  style={{ color: 'var(--primary-color)', marginRight: '8px' }}
                ></ha-icon>
                <ha-switch
                  checked={network.is_enabled}
                  onchange={(e: any) => onToggle(network.id, e.target.checked)}
                ></ha-switch>
              </div>
            </div>
            {isOpen && network.is_enabled && (
              <div className="card-content">
                <DeviceTable
                  devices={devices.filter((d) => d.networkId === network.id)}
                  setActiveView={setActiveView}
                />
                {network.ssids && network.ssids.length > 0 && (
                  <>
                    <div
                      className="hero-indicator"
                      style={{ padding: '0 16px 16px' }}
                    >
                      <ha-icon icon="mdi:wifi"></ha-icon>
                      {enabledSsids} / {totalSsids} SSIDs Enabled
                    </div>
                    <SSIDView hass={hass} ssids={network.ssids} />
                  </>
                )}
                <EventLog hass={hass} networkId={network.id} />
              </div>
            )}
          </ha-card>
        );
      })}
    </div>
  );
};

export default NetworkView;
