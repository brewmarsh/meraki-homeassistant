import React from 'react';

interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
<<<<<<< HEAD
<<<<<<< HEAD
}

interface SSIDViewProps {
  ssids: SSID[];
}

const SSIDView: React.FC<SSIDViewProps> = ({ ssids }) => {
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
  entity_id?: string;
}

interface SSIDViewProps {
  hass: any;
  ssids: SSID[];
}

const SSIDView: React.FC<SSIDViewProps> = ({ hass, ssids }) => {
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
  if (!ssids || ssids.length === 0) {
    return null;
  }

  return (
<<<<<<< HEAD
<<<<<<< HEAD
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px', padding: '16px' }}>
      {ssids.map((ssid) => (
        <ha-card key={ssid.number}>
          <div className="card-content" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontWeight: 'bold' }}>{ssid.name}</span>
              <ha-icon icon={ssid.enabled ? 'mdi:wifi' : 'mdi:wifi-off'} style={{ color: ssid.enabled ? 'var(--primary-color)' : 'var(--disabled-text-color)' }}></ha-icon>
            </div>
            <span>{ssid.enabled ? 'Enabled' : 'Disabled'}</span>
          </div>
        </ha-card>
      ))}
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <ha-icon
                icon={isOn ? 'mdi:wifi' : 'mdi:wifi-off'}
                style={{
                  '--mdc-icon-size': '16px',
                  marginRight: '4px',
                  color: isOn
                    ? 'var(--primary-color)'
                    : 'var(--disabled-text-color)',
                } as React.CSSProperties}
              ></ha-icon>
              <span>{isOn ? 'Enabled' : 'Disabled'}</span>
            </div>
          </div>
        );
      })}
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    </div>
  );
};

export default SSIDView;
