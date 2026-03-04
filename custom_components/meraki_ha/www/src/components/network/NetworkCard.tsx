import React from 'react';
import DeviceTable from '../DeviceTable';
import SSIDView from '../SSIDView';
import EventLog from '../EventLog';
import HaSwitch from '../HaSwitch';
import VlanTable from '../VlanTable';
import { Network, DeviceGroup, Vlan } from '../../types/meraki';
import { HomeAssistant } from '../../types/ha';
import { isDeviceOnline } from './NetworkHelpers';

interface NetworkCardProps {
  network: Network;
  isOpen: boolean;
  onToggleOpen: (networkId: string) => void;
  onToggleTrack: (networkId: string, enabled: boolean) => void;
  hass: HomeAssistant;
  groups: DeviceGroup[];
  networkVlans?: Vlan[];
  configEntryId: string;
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const NetworkCard: React.FC<NetworkCardProps> = ({
  network,
  isOpen,
  onToggleOpen,
  onToggleTrack,
  hass,
  groups,
  networkVlans,
  configEntryId,
  setActiveView,
}) => {
  const enabledSsids =
    network.ssids?.filter(
      (s) =>
        (s.entity_id && hass?.states?.[s.entity_id]?.state === 'on') ||
        (!s.entity_id && s.enabled)
    ).length || 0;

  const totalSsids = network.ssids?.length || 0;

  return (
    <ha-card key={network.id} className="overflow-hidden">
      <div
        className="flex items-center p-4 cursor-pointer hover:bg-[var(--secondary-background-color)] transition-colors text-[var(--primary-text-color)]"
        onClick={() => onToggleOpen(network.id)}
      >
        <span className="font-bold text-lg">[Network] {network.name}</span>
        <ha-icon
          className="ml-2 text-[var(--secondary-text-color)]"
          icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}
        ></ha-icon>

        <div
          className="ml-auto flex items-center"
          onClick={(e) => e.stopPropagation()}
        >
          <span className="mr-2 text-sm text-[var(--secondary-text-color)] hidden sm:inline">
            Track in HA
          </span>
          <ha-icon
            icon="hass:home-assistant"
            className="mr-2"
            style={{ color: 'var(--primary-color)' }}
          ></ha-icon>
          <HaSwitch
            checked={network.is_enabled}
            onChange={(checked) => onToggleTrack(network.id, checked)}
          />
        </div>
      </div>

      {isOpen && network.is_enabled && (
        <div className="p-4 border-t border-[var(--divider-color)] bg-[var(--card-background-color)]">
          {groups.map((group) => {
            if (group.devices.length === 0) return null;
            const onlineCount = group.devices.filter((d) =>
              isDeviceOnline(d, hass)
            ).length;

            return (
              <div key={group.label} className="mb-8 last:mb-0">
                <div className="flex items-center pb-2 mb-4 border-b border-[var(--divider-color)]">
                  <ha-icon
                    icon={group.icon}
                    className="mr-3"
                    style={{ color: 'var(--primary-color)' }}
                  ></ha-icon>
                  <div className="flex items-baseline gap-2">
                    <span className="text-lg font-semibold">
                      <span className="text-[var(--state-active-color)]">
                        {onlineCount}
                      </span>{' '}
                      / {group.devices.length}
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
                <ha-icon
                  icon="mdi:server-network"
                  className="mr-3"
                  style={{ color: 'var(--primary-color)' }}
                ></ha-icon>
                <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">
                  VLANs / Subnets
                </span>
              </div>
              <VlanTable vlans={networkVlans} />
            </div>
          )}

          {network.ssids && network.ssids.length > 0 && (
            <div className="mt-8">
              <div className="flex items-center pb-2 mb-4 border-b border-[var(--divider-color)]">
                <ha-icon
                  icon="mdi:wifi"
                  className="mr-3"
                  style={{ color: 'var(--primary-color)' }}
                ></ha-icon>
                <div className="flex items-baseline gap-2">
                  <span className="text-lg font-semibold">
                    <span className="text-[var(--state-active-color)]">
                      {enabledSsids}
                    </span>{' '}
                    / {totalSsids}
                  </span>
                  <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">
                    SSIDs Enabled
                  </span>
                </div>
              </div>
              <SSIDView
                hass={hass}
                ssids={network.ssids}
                configEntryId={configEntryId}
              />
            </div>
          )}

          <div className="mt-8 pt-4 border-t border-[var(--divider-color)]">
            <div className="flex items-center mb-4">
              <ha-icon
                icon="mdi:history"
                className="mr-3"
                style={{ color: 'var(--primary-color)' }}
              ></ha-icon>
              <span className="text-[var(--secondary-text-color)] uppercase text-xs tracking-wider font-bold">
                Network Event Log
              </span>
            </div>
            <EventLog
              hass={hass}
              networkId={network.id}
              configEntryId={configEntryId}
              productTypes={network.productTypes}
            />
          </div>
        </div>
      )}

      {isOpen && !network.is_enabled && (
        <div className="p-12 text-center bg-[var(--secondary-background-color)] border-t border-[var(--divider-color)]">
          <ha-icon
            icon="mdi:eye-off-outline"
            className="mb-3 text-[var(--secondary-text-color)]"
            style={{ '--mdc-icon-size': '48px' } as any}
          ></ha-icon>
          <p className="text-[var(--secondary-text-color)]">
            This network is not being tracked in Home Assistant.
          </p>
          <button
            className="mt-4 font-medium text-[var(--primary-color)] hover:underline"
            onClick={() => onToggleTrack(network.id, true)}
          >
            Enable tracking to view devices
          </button>
        </div>
      )}
    </ha-card>
  );
};

export default NetworkCard;
