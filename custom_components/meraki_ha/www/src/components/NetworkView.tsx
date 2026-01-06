<<<<<<< HEAD
<<<<<<< HEAD
import React, { useState } from 'react';
import DeviceTable from './DeviceTable';
import SSIDView from './SSIDView';
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
import React, { useState, useEffect } from 'react';
import DeviceTable from './DeviceTable';
import SSIDView from './SSIDView';
import EventLog from './EventLog';
import HaSwitch from './HaSwitch';
import VlanTable from './VlanTable';
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

// Define the types for our data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
  entity_id?: string;
}

interface Vlan {
  id: string;
  name: string;
  subnet?: string;
  applianceIp?: string;
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
}

interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
<<<<<<< HEAD
<<<<<<< HEAD
=======
  productTypes?: string[];
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
  productTypes?: string[];
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
<<<<<<< HEAD
<<<<<<< HEAD
}

interface NetworkViewProps {
  data: {
    networks: Network[];
    devices: Device[];
  };
  onToggle: (networkId: string, enabled: boolean) => void;
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const NetworkView: React.FC<NetworkViewProps> = ({ data, onToggle, setActiveView }) => {
  const [openNetworkId, setOpenNetworkId] = useState<string | null>(null);

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkId(openNetworkId === networkId ? null : networkId);
  };

  const { networks, devices } = data;
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
  ports_statuses?: any[];
  wan1Ip?: string;
  wan2Ip?: string;
}

interface NetworkViewProps {
  hass: any;
  data: {
    networks: Network[];
    devices: Device[];
    vlans?: { [key: string]: Vlan[] };
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

  const { networks, devices, vlans } = data;

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
    // For cameras, prioritize device status from API
    if (device.model?.toUpperCase().startsWith('MV')) {
       return device.status === 'online';
    }

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

  const networkGroups = React.useMemo(() => {
    if (!networks || !devices) return {};

    const result: Record<string, any[]> = {};

    networks.forEach((network) => {
      // Group devices
      const networkDevices = devices.filter(
        (d) => d.networkId === network.id
      );
      const wirelessDevices = networkDevices.filter(
        (d) =>
          d.model?.toUpperCase().startsWith('MR') ||
          d.model?.toUpperCase().startsWith('GR')
      );
      const switchDevices = networkDevices.filter(
        (d) =>
          d.model?.toUpperCase().startsWith('MS') ||
          d.model?.toUpperCase().startsWith('GS')
      );
      const cameraDevices = networkDevices.filter((d) =>
        d.model?.toUpperCase().startsWith('MV')
      );
      const sensorDevices = networkDevices.filter((d) =>
        d.model?.toUpperCase().startsWith('MT')
      );
      const applianceDevices = networkDevices.filter(
        (d) =>
          d.model?.toUpperCase().startsWith('MX') ||
          d.model?.toUpperCase().startsWith('Z') ||
          d.model?.toUpperCase().startsWith('MG') ||
          d.model?.toUpperCase().startsWith('GX')
      );
      const otherDevices = networkDevices.filter(
        (d) =>
          !d.model?.toUpperCase().startsWith('MR') &&
          !d.model?.toUpperCase().startsWith('GR') &&
          !d.model?.toUpperCase().startsWith('MS') &&
          !d.model?.toUpperCase().startsWith('GS') &&
          !d.model?.toUpperCase().startsWith('MV') &&
          !d.model?.toUpperCase().startsWith('MT') &&
          !d.model?.toUpperCase().startsWith('MX') &&
          !d.model?.toUpperCase().startsWith('Z') &&
          !d.model?.toUpperCase().startsWith('MG') &&
          !d.model?.toUpperCase().startsWith('GX')
      );

      result[network.id] = [
        {
          label: 'Appliances',
          devices: applianceDevices,
          icon: 'mdi:shield-check',
          type: 'appliance',
        },
        {
          label: 'Switches',
          devices: switchDevices,
          icon: 'mdi:lan',
          type: 'switch',
        },
        {
          label: 'Cameras',
          devices: cameraDevices,
          icon: 'mdi:cctv',
          type: 'camera',
        },
        {
          label: 'Sensors',
          devices: sensorDevices,
          icon: 'mdi:thermometer',
          type: 'sensor',
        },
        {
          label: 'Wireless APs',
          devices: wirelessDevices,
          icon: 'mdi:wifi',
          type: 'wireless',
        },
        {
          label: 'Other Devices',
          devices: otherDevices,
          icon: 'mdi:devices',
          type: 'other',
        },
      ];
    });

    return result;
  }, [networks, devices]);
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

  if (!networks || networks.length === 0) {
    return <p>No networks found.</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {networks.map((network) => {
<<<<<<< HEAD
<<<<<<< HEAD
        const isOpen = openNetworkId === network.id;
        const enabledSsids = network.ssids
          ? network.ssids.filter((s) => s.enabled).length
          : 0;
        const totalSsids = network.ssids ? network.ssids.length : 0;

=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        const isOpen = openNetworkIds.includes(network.id);
        const enabledSsids = network.ssids
          ? network.ssids.filter((s) => {
              // Check entity state if available, else fallback to s.enabled
              if (s.entity_id && hass?.states?.[s.entity_id]) {
                return hass.states[s.entity_id].state === 'on';
              }
              return s.enabled;
            }).length
          : 0;
        const totalSsids = network.ssids ? network.ssids.length : 0;

        const groups = networkGroups[network.id] || [];
        const networkVlans = vlans ? vlans[network.id] : undefined;

<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
<<<<<<< HEAD
<<<<<<< HEAD
                <ha-switch
                  checked={network.is_enabled}
                  onchange={(e: any) => onToggle(network.id, e.target.checked)}
                ></ha-switch>
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
                <HaSwitch
                  checked={network.is_enabled}
                  onChange={(checked) => onToggle(network.id, checked)}
                />
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
              </div>
            </div>
            {isOpen && network.is_enabled && (
              <div className="card-content">
<<<<<<< HEAD
<<<<<<< HEAD
                <DeviceTable
                  devices={devices.filter((d) => d.networkId === network.id)}
                  setActiveView={setActiveView}
                />
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
                        deviceType={group.type}
                      />
                    </div>
                  );
                })}

                {networkVlans && networkVlans.length > 0 && (
                    <div style={{ marginBottom: '16px' }}>
                        <VlanTable vlans={networkVlans} />
                    </div>
                )}

<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
                {network.ssids && network.ssids.length > 0 && (
                  <>
                    <div
                      className="hero-indicator"
<<<<<<< HEAD
<<<<<<< HEAD
                      style={{ padding: '0 16px 16px' }}
=======
                      style={{ padding: '16px' }}
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
                      style={{ padding: '16px' }}
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
                    >
                      <ha-icon icon="mdi:wifi"></ha-icon>
                      {enabledSsids} / {totalSsids} SSIDs Enabled
                    </div>
<<<<<<< HEAD
<<<<<<< HEAD
                    <SSIDView ssids={network.ssids} />
                  </>
                )}
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
                    <SSIDView hass={hass} ssids={network.ssids} />
                  </>
                )}
                <EventLog
                  hass={hass}
                  networkId={network.id}
                  configEntryId={configEntryId}
                  productTypes={network.productTypes}
                />
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
              </div>
            )}
          </ha-card>
        );
      })}
    </div>
  );
};

export default NetworkView;
