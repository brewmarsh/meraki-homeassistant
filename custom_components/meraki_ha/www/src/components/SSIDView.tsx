import React, { useState, useEffect } from 'react';

// Define the types for SSID data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string; // Keep networkId for context if needed, though not directly used in rendering
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
  const [isToggling, setIsToggling] = useState<Record<number, boolean>>({});

  useEffect(() => {
    // Update local state if ssids prop changes
    setLocalSSIDs(ssids);
  }, [ssids]);

  const handleToggle = async (ssidNumber: number, enabled: boolean) => {
    if (!hass || !configEntryId) return;

    setIsToggling((prev) => ({ ...prev, [ssidNumber]: true }));

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
      // Revert UI state on error
      setLocalSSIDs(ssids); // Revert to original state from props
    } finally {
      setIsToggling((prev) => ({ ...prev, [ssidNumber]: false }));
    }
  };

  // Filter SSIDs to only show those that are enabled or have an entity
  const displayedSSIDs = localSSIDs.filter(ssid => ssid.enabled || (ssid.entity_id && hass?.states?.[ssid.entity_id]));


  if (!ssids || displayedSSIDs.length === 0) {
    return <p>No SSIDs found or enabled for this network.</p>;
  }

  return (
    <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {displayedSSIDs.map((ssid) => {
        const isEnabled = ssid.enabled || (ssid.entity_id && hass?.states?.[ssid.entity_id]?.state === 'on');
        const isToggling = isToggling[ssid.number];

        return (
          <div
            key={ssid.number}
            className="bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-sm border border-light-border dark:border-dark-border flex flex-col justify-between transition-shadow duration-200 hover:shadow-md"
          >
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium text-lg">{ssid.name}</span>
              <ha-switch
                checked={isEnabled}
                disabled={isToggling}
                onClick={(e: any) => {
                  e.stopPropagation(); // Prevent triggering parent onClick if any
                  handleToggle(ssid.number, !isEnabled);
                }}
              ></ha-switch>
            </div>
            <div className="text-sm text-gray-500 dark:text-gray-400">
              SSID #{ssid.number}
            </div>
            <div className="text-sm mt-2">
              {/* Display entity state if available, otherwise fallback to enabled status */}
              {ssid.entity_id && hass?.states?.[ssid.entity_id] ? (
                <span className={`text-${isEnabled ? 'green' : 'red'}-500`}>
                  {hass.states[ssid.entity_id].state === 'on' ? 'Online' : 'Offline'}
                </span>
              ) : (
                <span className={`text-${isEnabled ? 'green' : 'red'}-500`}>
                  {isEnabled ? 'Enabled' : 'Disabled'}
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SSIDView;
