import React, { useState, useEffect } from 'react';
import HaSwitch from './HaSwitch';

// Define the types for SSID data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
  entity_id?: string;
}

interface SSIDViewProps {
  hass: any;
  ssids: SSID[];
  configEntryId: string;
}

const SSIDView: React.FC<SSIDViewProps> = ({
  hass,
  ssids,
  configEntryId,
}) => {
  const [localSSIDs, setLocalSSIDs] = useState(ssids);
  const [togglingStates, setTogglingStates] = useState<Record<number, boolean>>({});

  useEffect(() => {
    setLocalSSIDs(ssids);
  }, [ssids]);

  const handleToggle = async (ssidNumber: number, enabled: boolean) => {
    if (!hass || !configEntryId) return;

    setTogglingStates((prev) => ({ ...prev, [ssidNumber]: true }));

    const updatedSSIDs = localSSIDs.map((ssid) =>
      ssid.number === ssidNumber ? { ...ssid, enabled: enabled } : ssid
    );
    setLocalSSIDs(updatedSSIDs);

    try {
      await hass.callWS({
        type: 'meraki_ha/update_ssid',
        config_entry_id: configEntryId,
        ssid_number: ssidNumber,
        enabled: enabled,
      });
    } catch (err: any) {
      console.error('Error toggling SSID:', err);
      alert(`Failed to toggle SSID: ${err.message || 'Unknown error'}`);
      setLocalSSIDs(ssids);
    } finally {
      setTogglingStates((prev) => ({ ...prev, [ssidNumber]: false }));
    }
  };

  const displayedSSIDs = localSSIDs.filter(ssid => ssid.enabled || (ssid.entity_id && hass?.states?.[ssid.entity_id]));

  if (!ssids || displayedSSIDs.length === 0) {
    return <p className="text-[var(--secondary-text-color)]">No SSIDs found or enabled for this network.</p>;
  }

  return (
    <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {displayedSSIDs.map((ssid) => {
        const isEnabled = ssid.enabled || (ssid.entity_id && hass?.states?.[ssid.entity_id]?.state === 'on');
        const isCurrentlyToggling = togglingStates[ssid.number];

        return (
          <ha-card
            key={ssid.number}
            className="p-4 flex flex-col justify-between transition-shadow duration-200"
          >
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium text-lg text-[var(--primary-text-color)]">{ssid.name}</span>
              <HaSwitch
                checked={isEnabled}
                disabled={isCurrentlyToggling}
                onChange={(checked) => handleToggle(ssid.number, checked)}
              />
            </div>
            <div className="text-sm text-[var(--secondary-text-color)]">
              SSID #{ssid.number}
            </div>
            <div className="text-sm mt-2">
              <span style={{ color: isEnabled ? 'var(--success-color)' : 'var(--error-color)' }}>
                {isEnabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
          </ha-card>
        );
      })}
    </div>
  );
};

export default SSIDView;
