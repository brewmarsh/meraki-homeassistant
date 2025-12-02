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
  productTypes?: string[];
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
  configEntryId: string;
}

const NetworkView: React.FC<NetworkViewProps> = ({
  hass,
  data,
  onToggle,
  setActiveView,
  configEntryId,
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

  const isDeviceOnline = (device: Device) => {
    const haState = device.entity_id && hass?.states?.[device.entity_id];
    let status = device.status;
    if (
      haState &&
      haState.state !== 'unavailable' &&
      haState.state !== 'unknown'
    ) {
      status = haState.state;
    }
    return ['online', 'alerting', 'active', 'home', 'on'].includes(
      status?.toLowerCase()
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

        // Group devices
        const networkDevices = devices.filter(
          (d) => d.networkId === network.id
        );
        const wirelessDevices = networkDevices.filter((d) =>
          d.model?.toUpperCase().startsWith('MR')
        );
        const switchDevices = networkDevices.filter((d) =>
          d.model?.toUpperCase().startsWith('MS')
        );
        const cameraDevices = networkDevices.filter((d) =>
          d.model?.toUpperCase().startsWith('MV')
        );
        const otherDevices = networkDevices.filter(
          (d) =>
            !d.model?.toUpperCase().startsWith('MR') &&
            !d.model?.toUpperCase().startsWith('MS') &&
            !d.model?.toUpperCase().startsWith('MV')
        );

        const groups = [
          {
            label: 'Wireless APs',
            devices: wirelessDevices,
            icon: 'mdi:wifi',
          },
          {
            label: 'Switches',
            devices: switchDevices,
            icon: 'mdi:lan',
          },
          {
            label: 'Cameras',
            devices: cameraDevices,
            icon: 'mdi:cctv',
          },
          {
            label: 'Other Devices',
            devices: otherDevices,
            icon: 'mdi:devices',
          },
        ];

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
                {groups.map((group) => {
                  if (group.devices.length === 0) return null;
                  const onlineCount = group.devices.filter(isDeviceOnline).length;
                  const totalCount = group.devices.length;

                  return (
                    <div key={group.label} style={{ marginBottom: '16px' }}>
                      <div
                        className="hero-indicator"
                        style={{ padding: '0 16px 16px' }}
                      >
                        <ha-icon icon={group.icon}></ha-icon>
                        {onlineCount} / {totalCount} {group.label} Online
                      </div>
                      <DeviceTable
                        hass={hass}
                        devices={group.devices}
                        setActiveView={setActiveView}
                      />
                    </div>
                  );
                })}

                {network.ssids && network.ssids.length > 0 && (
                  <>
                    <div
                      className="hero-indicator"
                      style={{ padding: '16px' }}
                    >
                      <ha-icon icon="mdi:wifi"></ha-icon>
                      {enabledSsids} / {totalSsids} SSIDs Enabled
                    </div>
                    <SSIDView hass={hass} ssids={network.ssids} />
                  </>
                )}
                <EventLog
                  hass={hass}
                  networkId={network.id}
                  configEntryId={configEntryId}
                  productTypes={network.productTypes}
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
