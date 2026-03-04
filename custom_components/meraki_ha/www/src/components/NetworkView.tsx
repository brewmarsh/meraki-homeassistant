import React, { useState, useEffect } from 'react';
import NetworkCard from './network/NetworkCard';
import { groupNetworkDevices } from './network/NetworkHelpers';
import { NetworkData } from '../types/meraki';
import { HomeAssistant } from '../types/ha';

interface NetworkViewProps {
  hass: HomeAssistant;
  data: NetworkData;
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

  const networkGroups = React.useMemo(() => groupNetworkDevices(networks, devices), [networks, devices]);

  if (!networks || networks.length === 0) {
    return <p className="text-[var(--primary-text-color)]">No networks found.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      {networks.map((network) => {
        const isOpen = openNetworkIds.includes(network.id);
        const groups = networkGroups[network.id] || [];
        const networkVlans = vlans?.[network.id];

        return (
          <NetworkCard
            key={network.id}
            network={network}
            isOpen={isOpen}
            onToggleOpen={handleNetworkClick}
            onToggleTrack={onToggle}
            hass={hass}
            groups={groups}
            networkVlans={networkVlans}
            configEntryId={configEntryId}
            setActiveView={setActiveView}
          />
        );
      })}
    </div>
  );
};

export default NetworkView;