import React from 'react';

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
}

const SSIDView: React.FC<SSIDViewProps> = ({ hass, ssids }) => {
  if (!ssids || ssids.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: '16px',
        padding: '16px',
      }}
    >
      {ssids.map((ssid) => {
        let isOn = ssid.enabled;
        if (ssid.entity_id && hass?.states?.[ssid.entity_id]) {
          isOn = hass.states[ssid.entity_id].state === 'on';
        }

        return (
          <div
            key={ssid.number}
            className="bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-sm border border-light-border dark:border-dark-border flex flex-col gap-2"
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <span style={{ fontWeight: 'bold' }}>{ssid.name}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <ha-icon
                icon={isOn ? 'mdi:wifi' : 'mdi:wifi-off'}
                style={{
                  width: '16px',
                  height: '16px',
                  color: isOn
                    ? 'var(--primary-color)'
                    : 'var(--disabled-text-color)',
                }}
              ></ha-icon>
              <span>{isOn ? 'Enabled' : 'Disabled'}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SSIDView;
