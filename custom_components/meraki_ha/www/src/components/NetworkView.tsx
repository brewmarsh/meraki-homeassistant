import React, { useState, useEffect } from 'react';
import DeviceTable from './DeviceTable';
import SSIDView from './SSIDView';
import EventLog from './EventLog';
import HaSwitch from './HaSwitch';
import VlanTable from './VlanTable';

// Define the types for our data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
  entity_id?: string;
}

interface Vlan {
  id: string;
  name: string;
  subnet?: string;
  applianceIp?: string;
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
    if (device.model?.toUpperCase().startsWith('MV')) {
      return device.status === 'online';
    }

    const haState = device.entity_id && hass?.states?.[device.entity_id];
    let status = device.status;
    if (haState && haState.state !== 'unavailable' && haState.state !== 'unknown') {
      status = haState.state;
    }
    return ['online', 'active', 'home', 'on'].includes(status?.toLowerCase());
  };

  const networkGroups = React.useMemo(() => {
    if (!networks || !devices) return {};
    const result: Record<string, any[]> = {};

    networks.forEach((network) => {
      const networkDevices = devices.filter((d) => d.networkId === network.id);
      
      const filterByPrefix = (prefixes: string[]) => 
        networkDevices.filter(d => prefixes.some(p => d.model?.toUpperCase().startsWith(p)));

      result[network.id] = [
        { label: 'Appliances', devices: filterByPrefix(['MX', 'Z', 'MG', 'GX']), icon: 'mdi:shield-check', type: 'appliance' },
        { label: 'Switches', devices: filterByPrefix(['MS', 'GS']), icon: 'mdi:lan', type: 'switch' },
        { label: 'Cameras', devices: filterByPrefix(['MV']), icon: 'mdi:cctv', type: 'camera' },
        { label: 'Sensors', devices: filterByPrefix(['MT']), icon: 'mdi:thermometer', type: 'sensor' },
        { label: 'Wireless APs', devices: filterByPrefix(['MR', 'GR']), icon: 'mdi:wifi', type: 'wireless' },
        { label: 'Other Devices', devices: networkDevices.filter(d => !['MR', 'GR', 'MS', 'GS', 'MV', 'MT', 'MX', 'Z', 'MG', 'GX'].some(p => d.model?.toUpperCase().startsWith(p))), icon: 'mdi:devices', type: 'other' },
      ];
    });
    return result;
  }, [networks, devices]);

  if (!networks || networks.length === 0) {
    return <p className="text-[var(--primary-text-color)]">No networks found.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      {networks.map((network) => {
        const isOpen = openNetworkIds.includes(network.id);
        const enabledSsids = network.ssids?.filter((s) => 
          (s.entity_id && hass?.states?.[s.entity_id]?.state === 'on') || (!s.entity_id && s.enabled)
        ).length || 0;
        
        const totalSsids = network.ssids?.length || 0;
        const groups = networkGroups[network.id] || [];
        const networkVlans = vlans?.[network.id];

        return (
          <ha-card key={network.id} className="overflow-hidden">
            <div
              className="flex items-center p-4 cursor-pointer hover:bg-[var(--secondary-background-color)] transition-colors text-[var(--primary-text-color)]"
              onClick={() => handleNetworkClick(network.id)}
            >
              <span className="font-bold text-lg">[Network] {network.name}</span>
              <ha-icon
                className="ml-2 text-[var(--secondary-text-color)]"
                icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}
              ></ha-icon>
              
              <div className="ml-auto flex items-center" onClick={(e) => e.stopPropagation()}>
                <span className="mr-2 text-sm text-[var(--secondary-text-color)] hidden sm:inline">Track in HA</span>
                <ha-icon icon="hass:home-assistant" className="mr-2" style={{ color: 'var(--primary-color)' }}></ha-icon>
                <HaSwitch
                  checked={network.is_enabled}
                  onChange={(checked) => onToggle(network.id, checked)}
                />
              </div>
            </div>

            {isOpen && network.is_enabled && (
              <div className="p-4 border-t border-[var(--divider-color)] bg-[var(--card-background-color)]">
                {groups.map((group) => {
                  if (group.devices.length === 0) return null;
                  const onlineCount = group.devices.filter(isDeviceOnline).length;

                  return (
                    <div key={group.label} className="mb-8 last:mb-0">
                      <div className="flex items-center pb-2 mb-4 border-b border-[var(--divider-color)]">
                        <ha-icon icon={group.icon} className="mr-3" style={{ color: 'var(--primary-color)' }}></ha-icon>
                        <div className="flex items-baseline gap-2">
                          <span className="text-lg font-semibold">
                            <span className="text-[var(--state-active-color)]">{onlineCount}</span> / {group.devices.length}
                          </span>
                          <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">
                            {group.label} Online
                          </span>
                        </div>
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
                  <div className="mt-8">
                    <div className="flex items-center pb-2 mb-4 border-b border-[var(--divider-color)]">
                      <ha-icon icon="mdi:server-network" className="mr-3" style={{ color: 'var(--primary-color)' }}></ha-icon>
                      <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">VLANs / Subnets</span>
                    </div>
                    <VlanTable vlans={networkVlans} />
                  </div>
                )}

                {network.ssids && network.ssids.length > 0 && (
                  <div className="mt-8">
                    <div className="flex items-center pb-2 mb-4 border-b border-[var(--divider-color)]">
                      <ha-icon icon="mdi:wifi" className="mr-3" style={{ color: 'var(--primary-color)' }}></ha-icon>
                      <div className="flex items-baseline gap-2">
                        <span className="text-lg font-semibold">
                          <span className="text-[var(--state-active-color)]">{enabledSsids}</span> / {totalSsids}
                        </span>
                        <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">SSIDs Enabled</span>
                      </div>
                    </div>
                    <SSIDView hass={hass} ssids={network.ssids} configEntryId={configEntryId} />
                  </div>
                )}

                <div className="mt-8 pt-4 border-t border-[var(--divider-color)]">
                  <div className="flex items-center mb-4">
                    <ha-icon icon="mdi:history" className="mr-3" style={{ color: 'var(--primary-color)' }}></ha-icon>
                    <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">Network Event Log</span>
                  </div>
                  <EventLog hass={hass} networkId={network.id} configEntryId={configEntryId} productTypes={network.productTypes} />
                </div>
              </div>
            )}

            {isOpen && !network.is_enabled && (
              <div className="p-12 text-center bg-[var(--secondary-background-color)] border-t border-[var(--divider-color)]">
                <ha-icon icon="mdi:eye-off-outline" className="mb-3 text-[var(--secondary-text-color)]" style={{'--mdc-icon-size': '48px'} as any}></ha-icon>
                <p className="text-[var(--secondary-text-color)]">This network is not being tracked in Home Assistant.</p>
                <button
                  className="mt-4 font-medium text-[var(--primary-color)] hover:underline"
                  onClick={() => onToggle(network.id, true)}
                >
                  Enable tracking to view devices
                </button>
              </div>
            )}
          </ha-card>
        );
      })}
    </div>
  );
};

export default NetworkView;