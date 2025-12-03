import React from 'react';
import HaSwitch from './HaSwitch';

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

  const handleToggle = (checked: boolean, ssid: SSID) => {
    if (ssid.entity_id) {
      hass.callService('switch', checked ? 'turn_on' : 'turn_off', {
        entity_id: ssid.entity_id,
      });
    }
  };

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
              <HaSwitch
                checked={isOn}
                onChange={(checked) => handleToggle(checked, ssid)}
                disabled={!ssid.entity_id}
              />
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
